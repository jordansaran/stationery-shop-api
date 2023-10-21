from enum import Enum


class Weekday(Enum):
    MONDAY: int = 1
    TUESDAY: int = 2
    WEDNESDAY: int = 3
    THURSDAY: int = 4
    FRIDAY: int = 5
    SATURDAY: int = 6
    SUNDAY: int = 7

    @classmethod
    def days_week(cls):
        return (
            (cls.MONDAY.value, 'Segunda-feira'),
            (cls.TUESDAY.value, 'Terça-feira'),
            (cls.WEDNESDAY.value, 'Quarta-feira'),
            (cls.THURSDAY.value, 'Quinta-feira'),
            (cls.FRIDAY.value, 'Sexta-feira'),
            (cls.SATURDAY.value, 'Sábado'),
            (cls.SUNDAY.value, 'Domingo'),
        )
