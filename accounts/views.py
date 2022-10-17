from allauth.account.models import EmailAddress
from customerio import SendEmailRequest, CustomerIOException
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from accounts import models
from accounts import serializers
from accounts.serializers import InviteMemberSerializer
from hospital.models import Hospital, Department, Employee
from src.settings import emails_api


class WaitingListViewSet(viewsets.ModelViewSet):
    queryset = models.WaitingList.objects.all()
    serializer_class = serializers.WaitingListSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'waiting-list'


class InviteMemberViewSet(viewsets.ViewSet):

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
    def get_or_create_employee(invited_user: models.User, department: Department, phone=None) -> None:
        Employee.objects.get_or_create(
            user=invited_user, department=department,
            defaults={'status': Employee.PENDING, 'phone': phone, 'attribution': Employee.Patients}
        )

    @staticmethod
    def send_invite_email(
            invitee: models.User, created: bool, sender: models.User,
            hospital: Hospital, department: Department
    ) -> None:

        button_text = 'Log In'
        invite_link = settings.DOMAIN_NAME + 'sign-in'
        if created:
            invite = models.MemberInvite.objects.create(
                invitee=invitee,
                sender=sender,
                status=models.MemberInvite.INVITED
            )
            button_text = 'Create an account'
            invite_link = invite.get_invite_url()

        email_request = SendEmailRequest(
            to=invitee.email,
            transactional_message_id=12,
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
        department = get_object_or_404(Department, slug=self.kwargs['department_slug'])

        serializer = InviteMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invited_user, created = self.get_or_create_user(
            serializer.validated_data['email'],
            serializer.validated_data['first_name'],
            serializer.validated_data['last_name'],
        )
        phone = serializer.validated_data.get('phone', None)
        self.get_or_create_employee(invited_user, department, phone)
        self.send_invite_email(invited_user, created, request.user, hospital, department)

        return Response(status=200)

    def accept_invite(self, request, *args, **kwargs):
        invitation = models.MemberInvite.get_invite_object_from_hash(request.data['hash'])
        invitation.status = models.MemberInvite.ACCEPTED
        invitation.save()

        EmailAddress.objects.filter(user=invitation.invitee).update(verified=True)
        invitation.invitee.set_password(request.data['password'])

        return Response(status=status.HTTP_200_OK)
