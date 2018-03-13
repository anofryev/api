from django.db import models


class StudyInvitationStatus:
    NEW = 1
    ACCEPTED = 2
    DECLINED = 3

    CHOICES = (
        (NEW, 'New'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    )


class StudyInvitation(models.Model):
    email = models.EmailField(
        max_length=255,
        verbose_name='Email address',
    )
    study = models.ForeignKey(
        'Study',
        on_delete=models.CASCADE,
        verbose_name='Study'
    )
    doctor = models.ForeignKey(
        'accounts.Doctor',
        on_delete=models.CASCADE,
        verbose_name='Doctor'
    )
    status = models.PositiveSmallIntegerField(
        choices=StudyInvitationStatus.CHOICES,
        default=StudyInvitationStatus.NEW,
        verbose_name='Status'
    )

    class Meta:
        verbose_name = 'Study invitation'
        verbose_name_plural = 'Study invitations'
