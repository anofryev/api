from rest_framework import viewsets, mixins
from templated_mail.mail import BaseEmailMessage

from ..serializers import DoctorRegistrationRequestSerializer
from ..permissions import IsCoordinator
from ..models import Doctor


class CoordinatorApprovedEmail(BaseEmailMessage):
    template_name = 'email/you_was_approved.html'


class CoordinatorRejectedEmail(BaseEmailMessage):
    template_name = 'email/you_was_rejected.html'


class DoctorRegistrationRequestViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin):
    serializer_class = DoctorRegistrationRequestSerializer
    permission_classes = (IsCoordinator, )
    queryset = Doctor.objects.none()

    def get_queryset(self):
        return Doctor.objects.filter(
            approved_by_coordinator=False,
            my_coordinator_id=self.request.user.id)

    def update(self, request, pk, partial=False):
        result = super(DoctorRegistrationRequestViewSet, self).update(
            request, pk, partial=partial)
        if self.request.data['approved_by_coordinator']:
            doctor = Doctor.objects.get(pk=pk)
            site_title = doctor.my_coordinator.site.title
            CoordinatorApprovedEmail(
                self.request,
                {'site_title': site_title, 'doctor': doctor}
            ).send([doctor.email])

        return result

    def destroy(self, request, pk):
        doctor = Doctor.objects.get(pk=pk)
        site_title = doctor.my_coordinator.site.title
        email = doctor.email
        result = super(DoctorRegistrationRequestViewSet, self).destroy(
            request, pk)
        CoordinatorRejectedEmail(
            self.request,
            {'site_title': site_title}
        ).send([email])
        return result
