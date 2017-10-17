from copy import copy
from django.core.exceptions import ImproperlyConfigured

from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ValidationError

from django_fsm import can_proceed, has_transition_perm, FSMFieldMixin


def add_transition_actions(Klass):
    Model = Klass.queryset.model
    fsm_fields = [f.name for f in Model._meta.fields
                  if isinstance(f, FSMFieldMixin)]
    if len(fsm_fields) == 0:
        raise ImproperlyConfigured(
            "There is no FSM field at {0}".format(Model))

    if len(fsm_fields) > 1:
        raise ImproperlyConfigured(
            "There is more than one FSM field at {0}".format(Model))

    method_name = "get_all_{0}_transitions".format(fsm_fields[0])

    for f in getattr(Model, method_name)(Model()):
        def get_fn(name_):
            name = copy(name_)

            def fn(self, request, **kwargs):
                args = self.get_serializer(data=request.data)
                args.is_valid(raise_exception=True)
                obj = self.get_object()
                transition = getattr(obj, name)
                if can_proceed(transition) and\
                   has_transition_perm(transition, request.user):
                    transition(**args.validated_data)
                    obj.save()
                    return Response()
                else:
                    raise ValidationError(
                        "You cant perform '{}' transition".format(name))
            return fn

        serializer_class = f.custom.get('args_serializer') or Serializer

        setattr(Klass, f.name, detail_route(
            methods=['post'],
            serializer_class=serializer_class)(get_fn(f.name)))
    return Klass
