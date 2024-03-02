from collections import UserDict
import re
from datetime import datetime, timedelta


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command."
        except KeyError:
            return "Enter the argument for the command"
        except IndexError:
            return "Enter the argument for the command"

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not re.match(r"\d{10}", value):
            raise (Exception("Invalid phone number."))


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    @input_error
    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except Exception as e:
            print(e)

    @input_error
    def find_in_list(self, phone) -> int:
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                return i
            return None

    @input_error
    def remove_phone(self, phone):
        i = self.find_in_list(phone)
        if i != None:
            del self.phones[i]
            print(f"Phone number {phone} was delated from {self.name.value} contact.")
        else:
            return f"Phone {phone} not found in {self.name} contact"

    @input_error
    def edit_phone(self, old_phone, new_phone):
        i = self.find_in_list(old_phone)
        if i != None:
            self.phones[i].value = new_phone
            return f"Phone number {old_phone} was changed to {new_phone}."
        else:
            return f"Phone {old_phone} not found in {self.name} contact."

    @input_error
    def find_phone(self, phone):
        if phone in map(str, self.phones):
            return phone
        else:
            return f"Phone {phone} not found in {self.name} contact."

    @input_error
    def contact_phone(self, name):
        phones = ""
        phones = f"{self.name.value} : "
        for phone in self.phones:
            phones += f"{phone.value} "
        return phones

    @input_error
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return f"Birthday for contact {self.name.value} added"

    @input_error
    def show_birthday(self):
        return (
            f"{self.name.value} birthday at {self.birthday.value.strftime('%d.%m.%Y')}"
        )

    def __str__(self) -> str:
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):

    @input_error
    def add_record(self, record):
        self.data[record.name.value] = record
        return f"Contact added"

    @input_error
    def find(self, name):
        if name in self.data:
            return self.data[name]

    @input_error
    def del_record(self, name):
        del self.data[name.name.value]
        return f"The entry {name.name.value} was deleted."

    @input_error
    def birthdays(self) -> list:
        self.book = self
        congratulation_list = []
        current_date = datetime.today().date()
        birthday_list = ""

        for v in self.book.book:
            birthday = self.book[v].birthday
            if birthday is not None:
                birthday = birthday.value
                birthday = birthday.replace(year=current_date.year)
                if birthday.toordinal() < current_date.toordinal():
                    birthday = birthday.replace(year=current_date.year + 1)
                if birthday.toordinal() - current_date.toordinal() <= 7:
                    if birthday.weekday() == 5:
                        birthday = birthday + timedelta(days=2)
                    elif birthday.weekday() == 6:
                        birthday = birthday + timedelta(days=1)
                    congratulation_list.append(
                        {
                            "name": self.book[v].name.value,
                            "congratulation_day": birthday.strftime("%d.%m.%Y"),
                        }
                    )
        for rec in congratulation_list:
            birthday_list += f"{rec['name']} : {rec['congratulation_day']}\n"
        if birthday_list:
            return birthday_list
        else:
            return "No birthdays the next seven days."


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) != 2:
                print("Enter the argument for the command")
            else:
                name, phone = args
                record = Record(name)
                record.add_phone(phone)
                print(book.add_record(record))

        elif command == "change":
            if len(args) != 3:
                print("Enter the argument for the command")
            else:
                name, old_phone, new_phone = args
                record = book.find(name)
                print(record.edit_phone(old_phone, new_phone))

        elif command == "phone":
            if len(args) != 1:
                print("Enter the argument for the command")
            else:
                name = args[0]
                record = book.find(name)
                print(record.contact_phone(name))

        elif command == "all":
            for name, record in book.data.items():
                print(record.contact_phone(name))

        elif command == "add-birthday":
            if len(args) != 2:
                print("Enter the argument for the command")
            else:
                name, birthday = args
                record = book.find(name)
                print(record.add_birthday(birthday))

        elif command == "show-birthday":
            if len(args) != 1:
                print("Enter the argument for the command")
            else:
                name = args[0]
                record = book.find(name)
                print(record.show_birthday())

        elif command == "birthdays":
            print(book.birthdays())

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
