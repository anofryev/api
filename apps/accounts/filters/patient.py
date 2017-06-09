from django.db.models import Count, Case, When, F
from django_filters import FilterSet, ChoiceFilter, BooleanFilter

from ..models import Patient
from ..models import SexEnum, RaceEnum


class PatientFilter(FilterSet):
    race = ChoiceFilter(choices=RaceEnum.CHOICES)
    sex = ChoiceFilter(choices=SexEnum.CHOICES)
    path_pending = BooleanFilter(method='filter_path_pending')

    class Meta:
        model = Patient
        fields = ('race', 'sex', )

    def filter_path_pending(self, qs, name, value):
        """
        Filters list of patient which have `biopsy` and empty `path_diagnosis`
        """
        return qs.annotate(
            mole_images_with_path_pending=Count(
                Case(
                    When(
                        moles__images__biopsy=True,
                        moles__images__path_diagnosis__exact='',
                        then=F('moles__images__pk')
                    ),
                    default=None
                ),
                distinct=True
            )
        ).filter(mole_images_with_path_pending__gt=0)
