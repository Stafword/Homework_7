from collections import UserDict
from datetime import datetime, timedelta, date


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
        # Перевірка правильності формату номеру телефону
        if not self._validate_phone(value):
            raise ValueError("Номер повинен складатися з 10 цифер.")
        super().__init__(value)

    def _validate_phone(self, value):
        return isinstance(value, str) and len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        # Перевірка правильності формату дати народження
        if not self._validate_date(value):
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")
        super().__init__(value)

    def _validate_date(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def get_date_object(self):
        # Повертає об'єкт date
        return datetime.strptime(self.value, "%d.%m.%Y").date()


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
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # Редагування телефонного номера
        if not self.find_phone(old_phone):
            raise ValueError("Номер телефону для редагування не існує")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        # Пошук телефонного номера
        for p in self.phones:
            if p.value == phone:
                return p
        return None

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

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_bdays = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.get_date_object()

                # Визначення дати наступного для народження
                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday = bday.replace(year=today.year + 1)
                else:
                    bday = bday_this_year

                days_until_bday = (bday - today).days

                # Перевірка чи наступний день відбудеться протягом наступного тижня
                if 0 <= days_until_bday <= 7:
                    if bday.weekday() >= 5:
                        days_until_monday = 7 - bday.weekday()
                        bday += timedelta(days_until_monday)

                    upcoming_bdays.append(
                        {
                            "name": record.name.value,
                            "congratulation_date": bday.strftime("%Y.%m.%d"),
                        }
                    )

        return upcoming_bdays

    def __str__(self):
        # Представлення телефонної книги у зрозумілому формуті
        return "\n".join(str(record) for record in self.data.values())


# # Створення нової адресної книги
# book = AddressBook()

# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
# book.delete("Jane")
