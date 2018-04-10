from django.db.models import Func
from django.contrib.postgres.aggregates import ArrayAgg as ArrayAggBase


# NOTE: remove after update to django 2.0.4 and upper
class ArrayAgg(ArrayAggBase):
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super().__init__(expression, distinct='DISTINCT ' if distinct else '',
                         **extra)


class ArrayRemove(Func):
    function = 'ARRAY_REMOVE'
