from django.db import models

from .doctor import Doctor


# Participant is a patient, who can log in into system (so, can be a doctor)
class Participant(models.Model):
    doctor_ptr = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='participant_role'
    )

    def __str__(self):
        return self.doctor_ptr.__str__()

    class Meta:
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'


def is_participant(user):
    return Participant.objects.filter(doctor_ptr=user).exists()
