from django.db import models


class Site(models.Model):
    title = models.CharField(
        max_length=120)

    site_coordinator = models.OneToOneField(
        'accounts.Coordinator',
        on_delete=models.CASCADE,
        related_name='site'
    )

    def __str__(self):
        return self.title
