from django.contrib import admin

from apps.moles.models import MoleImage


class MoleImageInline(admin.StackedInline):
    model = MoleImage


class MoleAdmin(admin.ModelAdmin):
    inlines = (MoleImageInline,)
