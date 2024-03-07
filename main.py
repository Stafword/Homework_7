from classes import AddressBook, Record


def input_error(func):
    # Декоратор, який обробляє помилки введення для функцій.
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено."
        except ValueError as e:
            return e
        except IndexError:
            return "Недійсна кількість аргументів для цієї команди."

    return inner


def parse_input(user_input):
    # Розбирає введену користувачем команду на команду та аргументи.
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    # Змінює номер телефону контакту.
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Контакт оновлено."
    else:
        raise KeyError


@input_error
def show_phone(args, book):
    (name,) = args
    record = book.find(name)
    if record:
        return "; ".join([str(phone) for phone in record.phones])
    else:
        raise KeyError


@input_error
def show_all(book):
    return "\n".join([str(record) for record in book.data.values()])


@input_error
def add_birthday(args, book):
    # Додає день народження для контакту.
    name = args[0]
    birthday = args[1]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "День народження додано."
    else:
        raise KeyError


@input_error
def show_birthday(args, book):
    # Показує день народження за ім'ям контакту.
    (name,) = args
    record = book.find(name)
    return str(record.birthday)


def main():
    """Основна функція програми."""
    book = AddressBook()
    print("Ласкаво просимо до помічника!")
    print(
        "Доступні команди: add, change, phone, all, add-birthday, show-birthday, birthdays, hello, close або exit"
    )
    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу допомогти?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            birthdays = book.get_upcoming_birthdays()
            if not len(birthdays):
                print("Немає майбутніх днів народження.")
                continue
            for day in birthdays:
                print(f"{day}")
        else:
            print("Невірна команда.")


if __name__ == "__main__":
    main()
