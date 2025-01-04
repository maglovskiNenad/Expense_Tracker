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
    print("\nYou are logged in successfuly!\n")
else:
    print("\nError,Try Again\n")


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

        category_braekdown = data[0]["summary"]["categories_breakdown"]

        if new_expense["category"] in category_braekdown:
            category_braekdown[new_expense["category"]
                               ] += new_expense["amount"]
        else:
            category_braekdown[new_expense["category"]] = new_expense["amount"]

        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)

        update_expenses()
        print("\nNew expense added successfully!\n")
    except FileNotFoundError:
        print("File not found, make sure the JSON file exists.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Make sure the file contains valid JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")


def update_expenses():
    data = load_data()
    try:
        sum_expenses = 0
        sum_incom = 0
        for user in data:
            user_amount = user['expenses']
            total_expenses = user["summary"]
            incom = user["income"]

            for amount in user_amount:
                sum_expenses += amount["amount"]

            for total_incom in incom:
                sum_incom += total_incom["amount"]

        total_expenses["total_expenses"] = sum_expenses
        total_expenses["remaining_budget"] = total_expenses["total_income"] - sum_expenses
        total_expenses["total_income"] = sum_incom

        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)

        print("\nAll expenses updated!\n")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding.")
    except Exception as e:
        print(f"An error occurred: {e}")


def summary_expense():
    data = load_data()
    table = PrettyTable()

    table.field_names = ["Total Income", "Total Expenses",
                         "Remaining Budget"]

    table.add_row([data[0]["summary"]["total_income"],
                   data[0]["summary"]["total_expenses"], data[0]["summary"]["remaining_budget"]])
    print(table)


def check_id(id, username):
    data = load_data()
    if data[0]["name"].lower() == username.lower():
        for user_id in data:
            for expenses_id in user_id["expenses"]:
                if int(expenses_id["expense_id"]) == int(id):
                    return True
                
    return False

def delete_expense(username):
    question_delete = input("Are you sure you want to delete your expense? Y/n: ")
    show_all_expenses()
    question_id = input("Select the Id of the expense you would like to delete: ")
    if question_delete.lower() == "y" and check_id(id=question_id,username=username):
        data = load_data()
        expenses = data[0]["expenses"]
        data[0]["expenses"] = [expens for expens in expenses if int(expens["expense_id"])!= int(question_id)]
        try:
            with open("users.json","w") as file:
                json.dump(data,file,indent=4)

            print(f"\nThe expense with ID:{question_id} was successfully deleted!\n")
        except FileNotFoundError:
            print("Fajl is not found.")
        except json.JSONDecodeError:
            print("Error reading JSON file.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("\nOooops!An error occurred!\n")

def shows_by_month():
    data = load_data()
    expenses = data[0]["expenses"]
    
    expenses_by_month = {}
    for expens in expenses:
        month = datetime.strptime(expens["date"],"%Y-%m-%d").strftime("%B")
        category = expens["category"]
        amount = expens["amount"]

        if month not in expenses_by_month:
            expenses_by_month[month] = {}
        if category not in expenses_by_month[month]:
            expenses_by_month[month][category] = 0
        expenses_by_month[month][category] += amount

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
    
    categories = sorted({expens["category"] for expens in expenses})
    table = PrettyTable()
    table.field_names = ["Category"] + month_order

    for category in categories:
        row = [category]
        for mont in month_order:
            row.append(expenses_by_month.get(mont,{}).get(category,0))
        table.add_row(row)
    print(table)

while logged_in and user_login:
        print("\n1.Show all expense by months\n2.Delete expense\n3.Show summary of expenses\n4.Show all expenses\n5.Add expense\n6.Update expense\n7.Exit")
        choice = int(input("Please choose: "))
        match choice:
            case 1:
                shows_by_month()
            case 2:
                delete_expense(username_input)
            case 3:
                summary_expense()
            case 4:
                show_all_expenses()
            case 5:
                add_expenses()
            case 6:
                update_expenses()
            case 7:
                break