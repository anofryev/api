from ...models import Patient


class PatientInfoMixin(object):
    """
    Provides helper for getting patient info.
    """

    def get_patient_pk(self):
        return self.kwargs['patient_pk']

    def get_patient(self):
        return Patient.objects.get(pk=self.get_patient_pk())
