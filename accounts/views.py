from allauth.account.models import EmailAddress
from customerio import SendEmailRequest, CustomerIOException
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
            defaults={'status': Employee.PENDING, 'phone': phone, 'attribution': Employee.Patients}
        )

    @staticmethod
    def send_invite_email(
            request, invitee: models.User, created: bool,
            sender: models.User, hospital: Hospital, department: Department
    ) -> None:
        print(created)
        button_text = _('Log In')
        uri = request.build_absolute_uri('/')
        invite_link = f'{uri}sign-in'
        if created:
            invite = models.MemberInvite.objects.create(
                invitee=invitee,
                sender=sender,
                department=department,
                status=models.MemberInvite.INVITED
            )
            button_text = _('Create an account')
            invite_link = invite.get_invite_url(uri)

        email_request = SendEmailRequest(
            to=invitee.email,
            transactional_message_id=CustomerIOEmail.InviteUserEmail,
            message_data={
                'inviteeFirstName': invitee.first_name,
                'hospitalName': hospital.name,
                'departmentName': department.name,
                'buttonText': button_text,
                'inviteLink': invite_link,
            },
            identifiers={
                'email': invitee.email,
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

        invited_user, user_created = self.get_or_create_user(
            serializer.validated_data['email'],
            serializer.validated_data['first_name'],
            serializer.validated_data['last_name'],
        )
        phone = serializer.validated_data.get('phone', None)
        employee, employee_created = self.get_or_create_employee(invited_user, department, phone)

        if employee_created:
            self.send_invite_email(request, invited_user, user_created, request.user, hospital, department)
            return Response(status=200)
        return Response(_('Invitee is already an employee of this department'), status=status.HTTP_400_BAD_REQUEST)


class AcceptInviteViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def accept_invite(self, request, *args, **kwargs):
        try:
            invitation = models.MemberInvite.get_invite_object_from_hash(request.data['hash'])
        except IndexError:
            return Response(_('Hash was not found'), status=status.HTTP_400_BAD_REQUEST)

        invitation.status = models.MemberInvite.ACCEPTED
        invitation.save()

        EmailAddress.objects.filter(user=invitation.invitee).update(verified=True)
        invitation.invitee.set_password(request.data['password'])
        invitation.invitee.save()

        return Response(status=status.HTTP_200_OK)
