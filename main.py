import csv
import sys
from datetime import datetime

expense_categories = [
    "Rent", "Insurance", "Utilities", "Misc", "Entertainment", "Health",
    "Groceries", "Other"
]

income_categories = ["Salary", "Other"]

TRANSACTIONS_FILENAME = "transactions.csv"
SPEC_FILENAME = "spec.csv"


def exit_program():
  print("Terminating program.")
  sys.exit()


def get_total_income(transactions):
  total_income = 0
  for i, transaction in enumerate(transactions):
    transaction_type = transaction[2]
    if (transaction_type == "income"):
      total_income += float(transaction[4])
  return total_income


def display_total_income(transactions):
  total_income = get_total_income(transactions)
  print(f"Total Income: ${total_income:.2f}")


def list_categories(type):
  print("CATEGORIES: ")
  if type == "expense":
    for i, category in enumerate(expense_categories):
      print(f"{i + 1}. {category}")
  else:
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
  for i, transaction in enumerate(transactions):
    print(
        f"Transaction ID: {transaction[0]} (Date: {transaction[1]}) (Type: {transaction[2]}) (Category: {transaction[3]}) (Amount: {transaction[4]})"
    )
  print()


def category_input(type):
  temp_categories = expense_categories if type == "expense" else income_categories
  category = "Other"
  list_categories(type)
  while True:
    category = input("Enter category: ")
    if category in temp_categories:
      return category
    else:
      print("Invalid category. Please try again.")
      continue


def get_expense_amount_input():
  while True:
    amount = float(input("Enter expense amount: "))
    if amount > 0:
      return amount
    else:
      print("Invalid amount, must be greater than 0. Please try again")
      continue


# Differences
def add_expense(transactions):
  last_id = 0
  if (len(transactions) != 0):
    last_id = int(transactions[-1][0])
  print("lastid: " + str(last_id))
  print(transactions[-1])
  new_id = last_id + 1
  date = input("Enter date (MM/DD/YYYY) or Enter for today: ") or datetime.now(
  ).date().strftime("%m/%d/%Y")
  category = category_input("expense")
  amount = amount_input("expense")
  new_transaction = [new_id, date, "expense", category, amount]
  transactions.append(new_transaction)
  write_transactions(transactions)
  print(f"Transaction {new_id}: was added.\n")


def add_income(transactions):
  last_id = 0
  if (len(transactions) != 0):
    last_id = int(transactions[-1][0])
  new_id = last_id + 1
  date = input("Enter date (MM/DD/YYYY) or Enter for today: ") or datetime.now(
  ).date().strftime("%m/%d/%Y")
  category = category_input("income")
  amount = amount_input("income")
  new_transaction = [new_id, date, "income", category, amount]
  transactions.append(new_transaction)
  write_transactions(transactions)
  print(f"Transaction {new_id}: was added.\n")


def amount_input(type):
  amount = float(input("Enter amount: "))
  if type.lower() == "expense":
    amount = 0 - amount
  return amount


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


def delete_transaction(transactions):
  found = False
  transaction_id = input("Enter the transaction ID: ")
  for i, transaction in enumerate(transactions, start=0):
    if (transaction[0] == transaction_id):
      print("transaction {} was deleted.\n".format(transaction_id))
      transactions.pop(i)
      found = True

  if (found == False):
    print("Employee was not found.\n")
  else:
    write_transactions(transactions)


def update_transaction(transactions):
  transaction_id = input("Enter the transaction ID: ")
  found = False
  for i, transaction in enumerate(transactions, start=0):
    if (transaction[0] == transaction_id):
      date = input(
          "Enter date (MM/DD/YYYY) or Enter for unchanged: ") or transaction[1]
      type = input(
          "Expense or Income) or Enter for unchanged: ").lower() or transaction[2]
      category = category_input(type)
      amount = amount_input(type)
      transactions[i] = [transaction_id, date, type, category, amount]
      print("Transaction {} was updated.\n".format(transaction_id))
      found = True
  if (found == False):
    print("Transaction was not found.\n")
  else:
    write_transactions(transactions)
  pass


def read_budget():
  try:
    budget = []
    with open(SPEC_FILENAME, newline='') as file:
      reader = csv.reader(file)
      budget = list(reader)
      budget = float(budget[0][0])
    return budget
  except Exception as e:
    print(type(e), e)
    exit_program()


transactions = read_transactions()
budget = read_budget()


def display_menu():
  print("The Budget List program")
  print("Budget: " + str(budget))
  print()
  print("LIST OF COMMANDS")
  print("list - List all transactions")
  print("income -  Add income")
  print("expense -  Add expense")
  print("add_budget - Add budget")
  print("total_income - View total income")
  print("delete -  Delete a transaction")
  print("update -  Update a transaction")
  print("exit - Exit program")
  print()


display_menu()
# print(transactions)
while True:
  command = input("Command: ")
  if command.lower() == "list":
    list_transactions(transactions)
  elif command.lower() == "income":
    add_income(transactions)
  elif command.lower() == "expense":
    add_expense(transactions)
  elif command.lower() == "total_income":
    display_total_income(transactions)
  elif command.lower() == "add_budget":
    pass
  elif command.lower() == "delete":
    delete_transaction(transactions)
    transactions = read_transactions()
  elif command.lower() == "update":
    update_transaction(transactions)
    transactions = read_transactions()
  elif command.lower() == "exit":
    print("Goodbye!")
    break
  else:
    print("Not a valid command. Please try again.\n")
