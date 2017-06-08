from factory import DjangoModelFactory, PostGenerationMethodCall, Faker

from ..models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('user_name')
    password = PostGenerationMethodCall('set_password', 'password')
