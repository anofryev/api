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
    patient = models.ForeignKey(
        'accounts.Patient',
        on_delete=models.CASCADE,
        verbose_name='Patient',
        blank=True, null=True
    )

    def __str__(self):
        return '{0} invites {1} to {2} : {3}'.format(
            self.doctor,
            self.email,
            self.study,
            self.get_status_display())

    class Meta:
        verbose_name = 'Study invitation'
        verbose_name_plural = 'Study invitations'
