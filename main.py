import csv
import sys
from datetime import datetime

expense_categories = [
    "Rent", "Insurance", "Utilities", "Misc", "Entertainment", "Health",
    "Groceries", "Salary", "Other"
]

income_categories = ["Salary", "Other"]

TRANSACTIONS_FILENAME = "transactions.csv"
SPEC_FILENAME = "spec.csv"


def exit_program():
  print("Terminating program.")
  sys.exit()


def list_expense_categories():
  print("CATEGORIES: ")
  for i, category in enumerate(expense_categories):
    print(f"{i + 1}. {category}")


def list_income_categories():
  print("CATEGORIES: ")
  for i, category in enumerate(income_categories):
    print(f"{i + 1}. {category}")


def write_transactions(transactions):
  try:
    with open(TRANSACTIONS_FILENAME, "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerows(transactions)
  except Exception as e:
    print(type(e), e)
    exit_program()


def list_transactions(transactions):
  for i, transaction in enumerate(transactions, start=1):
    print(
        f"{i}. Transaction ID: {transaction[0]} (Date: {transaction[1]}) (Category: {transaction[2]}) (Amount: {transaction[3]})"
    )
  print()


def get_expense_category_input():
  category = "Other"
  list_expense_categories()
  while True:
    category = input("Enter category: ")
    if category in expense_categories:
      return category
    else:
      print("Invalid category. Please try again.")
      continue


def get_income_category_input():
  category = "Other"
  list_income_categories()
  while True:
    category = input("Enter category: ")
    if category in income_categories:
      return category
    else:
      print("Invalid category. Please try again.")
      continue


def get_expense_amount_input():

  while True:
    amount = int(input("Enter expense amount: "))
    if amount > 0:
      return amount
    else:
      print("Invalid amount, must be greater than 0. Please try again")
      continue


def add_expense(transactions):
  last_id = 0
  if (len(transactions) == 0):
    last_id = int(transactions[-1][0])
  new_id = last_id + 1
  date = input("Enter date (MM/DD/YYYY) or Enter for today: ") or datetime.now(
  ).date().strftime("%m/%d/%Y")
  category = get_expense_category_input()
  amount = int(input("Enter amount: "))
  amount = 0 - amount
  new_transaction = [new_id, date, category, amount]
  transactions.append(new_transaction)
  write_transactions(transactions)
  print(f"Transaction {new_id}: was added.\n")


def add_income(transactions):
  last_id = 0
  if (len(transactions) == 0):
    last_id = int(transactions[-1][0])
  new_id = last_id + 1
  date = input("Enter date (MM/DD/YYYY) or Enter for today: ") or datetime.now(
  ).date().strftime("%m/%d/%Y")
  category = get_income_category_input()
  amount = int(input("Enter amount: "))
  new_transaction = [new_id, date, category, amount]
  transactions.append(new_transaction)
  write_transactions(transactions)
  print(f"Transaction {new_id}: was added.\n")


def read_transactions():
  try:
    transactions = []
    with open(TRANSACTIONS_FILENAME, newline='') as file:
      reader = csv.reader(file)
      transactions = list(reader)
    return transactions
  except Exception as e:
    print(type(e), e)
    exit_program()


def display_menu():
  print("The Employee Salary List program")
  print()
  print("LIST OF COMMANDS")
  print("list - List all transactions")
  print("income -  Add income")
  print("expense -  Add expense")
  print("del -  Delete an employee")
  print("updid -  Update id of employee")
  print("exit - Exit program")
  print()


display_menu()
transactions = read_transactions()
# print(transactions)
while True:
  command = input("Command: ")
  if command.lower() == "list":
    list_transactions(transactions)
    print("list command entered")
    # list_employees(employees)
  elif command.lower() == "income":
    add_income(transactions)
    # print("income command entered")
  elif command.lower() == "expense":
    add_expense(transactions)
    # print("add command entered")
    # add_employee(employees)
  elif command.lower() == "del":
    print("del command entered")
    # delete_employee(employees)
  elif command.lower() == "updid":
    print("upid command entered")
    # upd_id(employees)
  elif command.lower() == "exit":
    print("Goodbye!")
    break
  else:
    print("Not a valid command. Please try again.\n")
