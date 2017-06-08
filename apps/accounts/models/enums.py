class UnitsOfLengthEnum(object):
    CENTIMETER = 'cm'
    INCH = 'in'

    CHOICES = (
        (CENTIMETER, 'Centimeter'),
        (INCH, 'Inch')
    )


class SexEnum(object):
    MALE = 'm'
    FEMALE = 'f'

    CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )


class RaceEnum(object):
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = 1
    ASIAN = 2
    BLACK_OR_AFRICAN_AMERICAN = 3
    HISPANIC_OR_LATINO = 4
    NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER = 5
    WHITE = 6

    CHOICES = (
        (
            AMERICAN_INDIAN_OR_ALASKA_NATIVE,
            'American Indian/Alaska Native'
        ),
        (
            ASIAN,
            'Asian'
        ),
        (
            BLACK_OR_AFRICAN_AMERICAN,
            'Black/African American'
        ),
        (
            HISPANIC_OR_LATINO, 'Hispanic/Latino'
        ),
        (
            NATIVE_HAWAIIAN_OR_PACIFIC_ISLANDER,
            'Native Hawaiian/Pacific Islander'
        ),
        (
            WHITE,
            'White'
        ),
    )
