import json
from datetime import datetime
from prettytable import PrettyTable
import random

username_input = input("Username:")
password_input = input("Password:")
logged_in = True


def load_data():
    try:
        with open("users.json", "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as error:
        print(f"JSON Decode Errror:{error}")


def user_login(username, password):
    user_data = load_data()
    for user in user_data:
        if user["name"].lower() == username.lower():
            return user["user_id"] == password


logged_successfully = user_login(username_input, password_input)
is_logged = True

if logged_successfully:
    print("You are logged in successfuly!")
else:
    print("Error,Try Again")


def show_all_expenses():
    user_data = load_data()
    table = PrettyTable()
    table.field_names = ["Id", "Date",
                         "Description", "Category", "Amount"]
    for user_expenses in user_data:
        expenses = user_expenses["expenses"]
        for expens in expenses:
            table.add_row([expens["expense_id"], expens["date"],
                          expens["description"], expens["category"], expens["amount"]])
    print(table)


def add_expenses():
    description = input("Description:")
    amount = input("Amount:")
    category = input("Category:")

    now = datetime.now()
    current_data = now.date()
    id = random.randint(100, 999)

    new_expense = {
        "expense_id": str(id),
        "date": str(current_data),
        "category": category,
        "description": description,
        "amount": int(amount)
    }
    try:
        data = load_data()

        if "expenses" in data[0]:
            data[0]["expenses"].append(new_expense)
        else:
            data[0]["expenses"] = [new_expense]

        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)
        print("New expense added successfully!")
    except FileNotFoundError:
        print("File not found, make sure the JSON file exists.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Make sure the file contains valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")
# whiel loop


# TODO Users can update an expense.

# TODO Users can delete an expense.

# TODO Users can view a summary of all expenses.

# TODO Users can view a summary of expenses for a specific month(of current year)

# Add expense categories and allow users to filter expenses by category.
# Allow users to set a budget for each month and show a warning when the user exceeds the budget.
# Allow users to export expenses to a CSV file.

# Use a simple text file to store the expenses data. You can use JSON, CSV, or any other format to store the data.
# Add error handling to handle invalid inputs and edge cases (e.g. negative amounts, non-existent expense IDs, etc).
# Use functions to modularize the code and make it easier to test and maintain.
