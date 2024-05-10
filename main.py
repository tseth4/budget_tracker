import csv
import sys
from datetime import datetime
import calendar
import json

expense_categories = [
    "rent", "insurance", "utilities", "misc", "entertainment", "health",
    "groceries", "other"
]

income_categories = ["salary", "other"]

TRANSACTIONS_FILENAME = "transactions.csv"
BUDGET_FILENAME = "budget.csv"


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


def write_budget(budget):
  try:
    with open(BUDGET_FILENAME, "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerows(budget)
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
    category = input("Enter category: ").lower()
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
      type = input("Expense or Income) or Enter for unchanged: ").lower(
      ) or transaction[2]
      category = category_input(type)
      amount = amount_input(type)
      transactions[i] = [transaction_id, date, type, category, amount]
      print("Transaction {} was updated.\n".format(transaction_id))
      found = True
  if (found == False):
    print("Transaction was not found.\n")
  else:
    write_transactions(transactions)


def add_budget(budget):
  total_income = get_total_income(transactions)
  budget_float = budget_to_float(budget)
  print("Current monthly budget: " + str(budget_float))
  print(type(budget_float))
  print("Current monthly income: " + str(total_income))
  print(" ")
  while True:
    new_budget = float(
        input("Update budget or Enter for unchanged: ") or budget_float)
    if (new_budget > total_income):
      print("Budget must be less than income")
      continue
    else:
      print("Updating budget")
      break
  budget[0] = [new_budget]
  write_budget(budget)


def budget_to_float(budget):
  return float(budget[0][0])


def view_monthly_summary(transactions, budget):
  monthly_transactions = {}
  selected_month = str(datetime.now().month)
  # populate transactions by month in monthly_transactions
  for i, transaction in enumerate(transactions):
    month_num = transaction[1].split("/")[0]
    # month_name = calendar.month_name[month_num]
    if (month_num in monthly_transactions):
      monthly_transactions[month_num].append(transaction)
    else:
      monthly_transactions[month_num] = [transaction]
  print(" ")
  # handle user selected month
  for key, value in monthly_transactions.items():
    month_name = calendar.month_name[int(key)]
    print("{}) {}".format(key, month_name))
  while True:
    selected_month = str(
        input("Enter month number or Enter for current month: ")
        or "0" + str(datetime.now().month))
    print(selected_month)
    if (selected_month not in monthly_transactions):
      print("Invalid month. Please try again.")
      continue
    else:
      print("selected: " + selected_month)
      break
  print(" ")
  # calculate and print monthly expenses, income, and remaining budget for selected month
  monthly_income = 0
  monthly_expense = 0
  total_budget = budget_to_float(budget)
  remaining_budget = 0
  selected_month_transactions = monthly_transactions[selected_month]
  for transaction in selected_month_transactions:
    if (transaction[2] == "income"):
      monthly_income = monthly_income + float(transaction[4])
    else:
      monthly_expense = monthly_expense + float(transaction[4])
  remaining_budget = total_budget - abs(monthly_expense)
  print("Current budget: " + str(total_budget))
  print("Monthly Income: " + str(monthly_income))
  print(f"Monthly Expense: {monthly_expense}")
  print(f"Remaining Budget: {remaining_budget}")
  # print(json.dumps(monthly_transactions, indent=4))


def read_budget():
  try:
    budget = []
    with open(BUDGET_FILENAME, newline='') as file:
      reader = csv.reader(file)
      budget = list(reader)
    return budget
  except Exception as e:
    print(type(e), e)
    exit_program()


transactions = read_transactions()
budget = read_budget()


def display_menu():
  print("The Budget List program")
  print("Budget: " + str(budget_to_float(budget)))
  print()
  print("LIST OF COMMANDS: ")
  print("")
  print("list - List all transactions")
  print("income -  Add income")
  print("expense -  Add expense")
  print("add_budget - Add budget")
  print("total_income - View total income")
  print("delete -  Delete a transaction")
  print("update -  Update a transaction")
  print("sum -  View monthly summary")
  print("exit - Exit program")
  print()


display_menu()
while True:
  command = input("Command: ")
  if command.lower() == "list":
    list_transactions(transactions)
  elif command.lower() == "income":
    add_income(transactions)
    transactions = read_transactions()
  elif command.lower() == "expense":
    add_expense(transactions)
    transactions = read_transactions()
  elif command.lower() == "total_income":
    display_total_income(transactions)
  elif command.lower() == "add_budget":
    add_budget(budget)
    budget = read_budget()
  elif command.lower() == "delete":
    delete_transaction(transactions)
    transactions = read_transactions()
  elif command.lower() == "update":
    update_transaction(transactions)
    transactions = read_transactions()
  elif command.lower() == "sum":
    view_monthly_summary(transactions, budget)
  elif command.lower() == "exit":
    print("Goodbye!")
    break
  else:
    print("Not a valid command. Please try again.\n")
