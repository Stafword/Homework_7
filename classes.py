from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError(
                "Невірний формат номера. Номер телефону має складатися з 10 цифр."
            )


class Birthday(Field):
    def __init__(self, value):
        # Перевірка правильності формату дати народження
        date_format = "%d.%m.%Y"
        try:
            self.date = datetime.strptime(value, date_format).date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")


class Record:
    def __init__(self, name):
        # Ім'я контакту
        self.name = Name(name)
        # Список телефонів
        self.phones = []
        # Дата народження
        self.birthday = None

    def add_phone(self, phone):
        # Додавання нового телефонного номера
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видалення телефонного номера
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        # Редагування телефонного номера
        if not self.find_phone(old_phone):
            raise ValueError("Номер телефону для редагування не існує")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        # Пошук телефонного номера
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday):
        # Додавання дати народження
        if self.birthday:
            raise ValueError("Дата народження вже існує для цього контакту")
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Представлення запису у зрозумілому форматі
        return f"Ім'я контакту: {str(self.name)}, Телефони: {'; '.join(str(p) for p in self.phones)}, Дата народження: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        # Додавання нового запису в телефонну книгу
        self.data[record.name.value] = record

    def find(self, name):
        # Пошук запису за ім'ям
        return self.data.get(name)

    def delete(self, name):
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    @staticmethod
    def find_next_weekday(d, weekday):
        """
        Функція для знаходження наступного заданого дня тижня після заданої дати.
        d: datetime.date - початкова дата.
        weekday: int - день тижня від 0 (понеділок) до 6 (неділя).
        """
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Якщо день народження вже минув у цьому тижні.
            days_ahead += 7
        return d + timedelta(days_ahead)

    def get_upcoming_birthdays(self, days=7) -> list:
        today = datetime.today().date()
        upcoming_birthdays = []

        for user in self.data.values():
            if user.birthday is None:
                continue
            birthday_this_year = user.birthday.date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                if birthday_this_year.weekday() >= 5:  # субота або неділя
                    birthday_this_year = self.find_next_weekday(
                        birthday_this_year, 0
                    )  # Понеділок

                congratulation_date_str = birthday_this_year.strftime("%Y.%m.%d")
                upcoming_birthdays.append(
                    {
                        "name": user.name.value,
                        "congratulation_date": congratulation_date_str,
                    }
                )

        return upcoming_birthdays
