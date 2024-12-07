import factory
from user.models import CustomUser


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    birth_date = factory.Faker('date_of_birth', minimum_age=10, maximum_age=75)