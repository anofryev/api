from django_filters import FilterSet, ChoiceFilter, BooleanFilter

from ..models import Patient
from ..models import SexEnum, RaceEnum


class PatientFilter(FilterSet):
    race = ChoiceFilter(choices=RaceEnum.CHOICES)
    sex = ChoiceFilter(choices=SexEnum.CHOICES)
    path_pending = BooleanFilter(method='filter_path_pending')

    class Meta:
        model = Patient
        fields = ('race', 'sex',)

    def filter_path_pending(self, qs, name, value):
        return qs.filter()
