from funcy import walk_keys

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_fsm import (
    FSMIntegerField, transition,
    TransitionNotAllowed, RETURN_VALUE, )
from rest_framework import serializers

from templated_mail.mail import BaseEmailMessage

from .coordinator import is_coordinator
from .patient import DoctorToPatient
from .doctor import Doctor


class CoordinatorRegistrationNotification(BaseEmailMessage):
    template_name = 'email/coordnator_notification.html'

    def get_context_data(self):
        context = super(CoordinatorRegistrationNotification,
                        self).get_context_data()
        context['url'] = "{}#/doctor-registration-requests".format(
            settings.DJOSER['DOMAIN'])
        return context


class CoordinatorApprovedEmail(BaseEmailMessage):
    template_name = 'email/you_was_approved.html'


class CoordinatorRejectedEmail(BaseEmailMessage):
    template_name = 'email/you_was_rejected.html'


class DoctorSharedPatientsEmail(BaseEmailMessage):
    template_name = 'email/doctor_shared_patients.html'


class ConfirmArgsSerializer(serializers.Serializer):
    encrypted_keys = serializers.DictField(child=serializers.CharField())

    def validate(self, data):
        data['encrypted_keys'] = walk_keys(int, data['encrypted_keys'])
        return data


class JoinStateEnum(object):
    NEW = 0
    REJECTED = 1
    APPROVED = 2
    CONFIRMED = 4


def is_site_coordinator(instance, user):
    coordinator = is_coordinator(user)
    if coordinator is None:
        return False

    return coordinator.site == instance.site


class SiteJoinRequest(models.Model):
    """
    Join request statuses

    new -> just created
    rejected -> site coordinator rejected joinig
    approved -> site coordinator approved joining
    confirmed -> doctor confirmed joining and shared all patients
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    state = FSMIntegerField(default=JoinStateEnum.NEW)
    doctor = models.ForeignKey('accounts.Doctor')
    site = models.ForeignKey('accounts.Site')

    class Meta:
        unique_together = (
            'doctor',
            'site', )

    @transition(
        field=state,
        source=JoinStateEnum.NEW,
        target=JoinStateEnum.REJECTED,
        permission=is_site_coordinator)
    def reject(self):
        """
        There is no side effects for the decline action
        """
        CoordinatorRejectedEmail(
            context={'site_title': self.site.title,
                     'doctor': self.doctor}).send([self.doctor.email])

    @transition(
        field=state,
        source=JoinStateEnum.NEW,
        target=RETURN_VALUE(JoinStateEnum.APPROVED, JoinStateEnum.CONFIRMED),
        permission=is_site_coordinator)
    def approve(self):
        has_patients = self.doctor.patients.exists()
        CoordinatorApprovedEmail(
            context={'site_title': self.site.title,
                     'has_patients': has_patients,
                     'doctor': self.doctor}).send([self.doctor.email])
        if not has_patients:
            self.doctor.my_coordinator_id = self.site.site_coordinator_id
            self.doctor.save()
            return JoinStateEnum.CONFIRMED

        return JoinStateEnum.APPROVED

    @transition(
        field=state,
        source=JoinStateEnum.APPROVED,
        target=JoinStateEnum.CONFIRMED,
        permission=lambda instance, user: instance.doctor_id == user.id,
        custom={'args_serializer': ConfirmArgsSerializer})
    def confirm(self, encrypted_keys=None):
        encrypted_keys = encrypted_keys or {}
        patients_ids = list(
            self.doctor.doctortopatient_set.values_list(
                'patient_id', flat=True))

        doctor_id = self.site.site_coordinator_id

        if set(patients_ids) != set(encrypted_keys.keys()):
            raise TransitionNotAllowed(
                "Not enough encrypted keys", object=self, method=self.confirm)

        DoctorToPatient.objects.bulk_create([
            DoctorToPatient(
                doctor_id=doctor_id,
                patient_id=patient_id,
                encrypted_key=encrypted_key)
            for patient_id, encrypted_key in encrypted_keys.items()
        ])

        self.doctor.my_coordinator_id = self.site.site_coordinator_id
        self.doctor.save()

        DoctorSharedPatientsEmail(context={
            'site_title': self.site.title,
            'doctor': self.doctor
        }).send([Doctor.objects.get(id=self.site.site_coordinator_id).email])


@receiver(post_save, sender=SiteJoinRequest)
def notify_coordinator(sender, instance, created, **kwargs):
    if created and instance.state == JoinStateEnum.NEW:
        doctor = instance.doctor
        to = [Doctor.objects.get(id=instance.site.site_coordinator_id).email]

        CoordinatorRegistrationNotification(
            context={'doctor': "{0} {1}".format(
                     doctor.first_name,
                     doctor.last_name)}).send(to)
