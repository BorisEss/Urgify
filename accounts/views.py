from allauth.account.models import EmailAddress
from customerio import SendEmailRequest, CustomerIOException
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from django.db import DatabaseError, transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging

from accounts import models
from accounts import serializers
from accounts.serializers import InviteMemberSerializer
from hospital.permissions import MembershipPermission
from hospital.models import Hospital, Department, Employee
from src.settings import emails_api
from src.email import CustomerIOEmail


class WaitingListViewSet(viewsets.ModelViewSet):
    queryset = models.WaitingList.objects.all()
    serializer_class = serializers.WaitingListSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'waiting-list'


class InviteMemberViewSet(viewsets.GenericViewSet):
    permission_classes = (MembershipPermission,)

    @staticmethod
    def get_or_create_user(email: str, first_name: str, last_name: str) -> tuple[models.User, bool]:
        user, created = models.User.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'last_name': last_name}
        )
        if created:
            user.set_unusable_password()
            user.save()
            EmailAddress.objects.create(user=user, email=email, primary=True)

        return user, created

    @staticmethod
    def get_or_create_employee(invited_user: models.User, department: Department, phone=None) -> Employee:
        return Employee.objects.get_or_create(
            user=invited_user, department=department,
            defaults={'phone': phone, 'attribution': Employee.PATIENTS}
        )

    @staticmethod
    def send_invite_email(request, invite: models.MemberInvite, hospital: Hospital, created: bool) -> None:

        uri = request.build_absolute_uri('/')
        button_text = _('Accept invite')
        url = f'{uri}accept-invite-existing-user/'
        if created:
            button_text = _('Create an account')
            url = f'{uri}accept-invite-new-user/'

        invite_hash = invite.get_invite_hash()
        url += f'{invite_hash}?hospital={hospital.slug}&department={invite.department.slug}'

        email_request = SendEmailRequest(
            to=invite.invitee.email,
            transactional_message_id=CustomerIOEmail.InviteUserEmail,
            message_data={
                'inviteeFirstName': invite.invitee.first_name,
                'hospitalName': hospital.name,
                'departmentName': invite.department.name,
                'buttonText': button_text,
                'inviteLink': url,
            },
            identifiers={
                'email': invite.invitee.email,
            },
        )

        try:
            emails_api.send_email(email_request)
        except CustomerIOException as e:
            print('Send email error: ', e)

    @swagger_auto_schema(manual_parameters=[])
    def create(self, request, *args, **kwargs):
        hospital = get_object_or_404(Hospital, slug=self.kwargs['hospital_slug'])
        department = get_object_or_404(Department, slug=self.kwargs['department_slug'], hospital=hospital)

        serializer = InviteMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone', None)

        invited_user, user_created = self.get_or_create_user(
            serializer.validated_data['email'],
            serializer.validated_data['first_name'],
            serializer.validated_data['last_name'],
        )

        employee, _ = Employee.objects.get_or_create(
            user=invited_user, department=department,
            defaults={'phone': phone, 'attribution': Employee.PATIENTS}
        )
        invite, invitation_created = models.MemberInvite.objects.get_or_create(
            invitee=invited_user,
            department=department,
            defaults={'sender': request.user}
        )

        if invitation_created:
            self.send_invite_email(request, invite, hospital, user_created)
            return Response(status=200)

        message = 'Invitation for this user in this department is already sent'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class AcceptInviteViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @staticmethod
    def validate_invitation_hash(request) -> models.MemberInvite | Response:
        try:
            invitation = models.MemberInvite.get_invite_object_from_hash(request.data['hash'])
        except IndexError:
            return Response(_('Invitation was not found'), status=status.HTTP_400_BAD_REQUEST)

        if invitation.status == models.MemberInvite.ACCEPTED:
            return Response(_('User already accepted this invite'), status=status.HTTP_400_BAD_REQUEST)

        return invitation

    @staticmethod
    def accept_invite(invitation: models.MemberInvite):
        try:
            with transaction.atomic():
                invitation.status = models.MemberInvite.ACCEPTED
                invitation.save()

                employee = invitation.invitee.employee.get(department=invitation.department)
                employee.status = Employee.ACTIVE
                employee.save()

                EmailAddress.objects.filter(user=invitation.invitee).update(verified=True)
        except DatabaseError as e:
            logging.error(e, exc_info=True)
            return Response(
                _('Error when trying to save invitation status'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def accept_invite_new_user(self, request, *args, **kwargs):
        invitation = self.validate_invitation_hash(request)
        self.accept_invite(invitation)

        invitation.invitee.set_password(request.data['password'])
        invitation.invitee.save()

        return Response(status=status.HTTP_200_OK)

    def accept_invite_existing_user(self, request):
        invitation = self.validate_invitation_hash(request)
        self.accept_invite(invitation)
        return Response(status=status.HTTP_200_OK)
