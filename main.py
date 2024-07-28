import csv
import sys
from datetime import datetime
import calendar
import re

# Specified expense categories
expense_categories = [
    "rent", "insurance", "utilities", "misc", "entertainment", "health",
    "groceries", "other"
]

# Specified income categories
income_categories = ["salary", "other"]

# csv paths
TRANSACTIONS_FILENAME = "transactions.csv"
BUDGET_FILENAME = "budget.csv"

# exit program
def exit_program():
  print("Terminating program.")
  sys.exit()

# check if date matches MM/DD/YYYY format
def is_valid_date(date_str):
  pattern = r"^(0?[1-9]|1[0-2])/(0?[1-9]|[12]\d|3[01])/(\d{4})$"
  if re.match(pattern, date_str):
    return True
  else:
    return False

# Sum all income transaction amounts
def get_total_income(transactions):
  total_income = 0
  for i, transaction in enumerate(transactions):
    transaction_type = transaction[2]
    if (transaction_type == "income"):
      total_income += float(transaction[4])
  return total_income


# print total income transaction amounts
def display_total_income(transactions):
  total_income = get_total_income(transactions)
  print(f"Total Income: ${total_income:.2f}")


# List all categorozations depending on type "expense" | "income"
def list_categories(type):
  print("CATEGORIES: ")
  if type == "expense":
    for i, category in enumerate(expense_categories):
      print(f"{category}")
  else:
    for i, category in enumerate(income_categories):
      print(f"{i + 1}. {category}")

# Helper function to write transactions back to csv
def write_transactions(transactions):
  try:
    with open(TRANSACTIONS_FILENAME, "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerows(transactions)
  except Exception as e:
    print(type(e), e)
    exit_program()

# Function to write budget back to budget.csv
def write_budget(budget):
  try:
    with open(BUDGET_FILENAME, "w", newline="") as file:
      writer = csv.writer(file)
      writer.writerows(budget)
  except Exception as e:
    print(type(e), e)
    exit_program()


# Printing all transactions to the console
def list_transactions(transactions):
  if (len(transactions) == 0):
    print("No transactions found.")
    return
  for i, transaction in enumerate(transactions):
    print(
        f"Transaction ID: {transaction[0]} (Date: {transaction[1]}) (Type: {transaction[2]}) (Category: {transaction[3]}) (Amount: {transaction[4]})"
    )
  print()


# Handle and validate category input
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

# Handle and validate date input
def get_date_input(spec_date=None):
  while True:
    if (spec_date):
      date = input("Enter date (MM/DD/YYYY) or Enter to skip: ") or spec_date
      pass
    else:
      date = input("Enter date (MM/DD/YYYY) or Enter for today: "
                   ) or datetime.now().date().strftime("%m/%d/%Y")
    if is_valid_date(date):
      return date
    else:
      print(
          "Invalid date format. Please enter date in MM/DD/YYYY format or Enter for today."
      )
      continue


# Add transaction based to type "expense" | "income", use helper write_transactions to write to csv
def add_transaction(transactions, type):
  last_id = 0
  if (len(transactions) != 0):
    last_id = int(transactions[-1][0])
  new_id = last_id + 1
  date = get_date_input()
  category = category_input(type)
  amount = amount_input(type)
  new_transaction = [new_id, date, type, category, amount]
  transactions.append(new_transaction)
  write_transactions(transactions)
  print(f"Transaction {new_id}: was added.\n")

# Handle and validate amount input
def amount_input(type):
  while True:
    try:
      amount = float(input("Enter amount: "))
      if (amount > 0):
        if type.lower() == "expense":
          amount = 0 - amount
        return amount
      else:
        print("Invalid amount, must be greater than 0. Please try again")
        continue
    except ValueError:
      print("Invalid input, must be positive number. Please try again.")

# Helper to read and return all transactions from csv
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

# Delete transaction method and write to csv
def delete_transaction(transactions):
  found = False
  transaction_id = input("Enter the transaction ID: ")
  for i, transaction in enumerate(transactions, start=0):
    if (transaction[0] == transaction_id):
      print("transaction {} was deleted.\n".format(transaction_id))
      transactions.pop(i)
      found = True

  if (found == False):
    print("Transaction was not found.\n")
  else:
    write_transactions(transactions)

# Update transaction method and write back to csv
def update_transaction(transactions):
  transaction_id = input("Enter the transaction ID: ")
  found = False
  for i, transaction in enumerate(transactions, start=0):
    if (transaction[0] == transaction_id):
      date = get_date_input(transaction[1])
      type = transaction[2]
      category = category_input(type)
      amount = amount_input(type)
      transactions[i] = [transaction_id, date, type, category, amount]
      print("Transaction {} was updated.\n".format(transaction_id))
      found = True
  if (found == False):
    print("Transaction was not found.\n")
  else:
    write_transactions(transactions)

# add a budget and use helper write_budget to write to csv
def add_budget(budget):
  total_income = get_total_income(transactions)
  budget_float = budget_to_float(budget)
  print(" ")
  new_budget = amount_input("budget")
  budget[0] = [new_budget]
  write_budget(budget)
  print("Monthly budget updated")


  # Helper to convert budget to float
def budget_to_float(budget):
  return float(budget[0][0])

# Function to view monthly summary
def view_monthly_summary(transactions, budget):
  if (len(transactions) == 0):
    print("No transactions found.")
    return
  monthyear_transactions = {}
  selected_month = str(datetime.now().month)
  # populate transactions by month in monthly_transactions
  for i, transaction in enumerate(transactions):
    month_num = transaction[1].split("/")[0]
    year_num = transaction[1].split("/")[2]
    month_year = month_num + "/" + year_num
    if (month_year in monthyear_transactions):
      monthyear_transactions[month_year].append(transaction)
    else:
      monthyear_transactions[month_year] = [transaction]
  print(" ")
  # handle user selected month
  for key, value in monthyear_transactions.items():
    month_key = key.split("/")[0]
    year_key = key.split("/")[1]
    month_name = calendar.month_name[int(month_key)]
    # year_name = calendar.year_name[int(year_key)]
    print("{}) {}".format(key, month_name) + " " + year_key)
  print("month year_transactions: ")
  # print(json.dumps(monthyear_transactions, indent=4))
  while True:
    current_month_year = "0" + str(datetime.now().month) + "/" + str(
        datetime.now().year)
    selected_month_year = input(
        "Enter date key (MM/YYYY) or Enter for current month and year: "
    ) or current_month_year
    if (selected_month_year not in monthyear_transactions):
      print("Invalid month and year. Please try again.")
      continue
    else:
      print("Selected month year: " + selected_month_year)
      break
  print(" ")
  # calculate and print monthly expenses, income, and remaining budget for selected month
  monthly_income = 0
  monthly_expense = 0
  total_budget = budget_to_float(budget)
  remaining_budget = 0
  selected_monthyear_transactions = monthyear_transactions[selected_month_year]
  for transaction in selected_monthyear_transactions:
    if (transaction[2] == "income"):
      monthly_income = monthly_income + float(transaction[4])
    else:
      monthly_expense = monthly_expense + float(transaction[4])
  remaining_budget = total_budget - abs(monthly_expense)
  print("Monthly Income: " + str(monthly_income))
  print("Current budget: " + str(total_budget))
  print(f"Monthly Expense: {monthly_expense}")
  print(f"Remaining Budget: {remaining_budget}")
  # print expenses by category
  print(" ")
  print("CATEGORIES OF EXPENSES: ")
  expense_categories = {}
  # Populate expense_categories with expense categories and their total amount
  for transaction in selected_monthyear_transactions:
    if (transaction[2] == "expense" and transaction[3] in expense_categories):
      expense_categories[
          transaction[3]] = expense_categories[transaction[3]] + abs(
              float(transaction[4]))
    elif (transaction[2] == "expense"):
      expense_categories[transaction[3]] = abs(float(transaction[4]))
  # Print expense categories and their total amount
  for key, value in expense_categories.items():
    print(f"{key}: {value}")

# Read budget.csv
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

# call functions on initial run
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

# Call display menu on initial run
display_menu()
# Listen to user initial user input
while True:
  command = input("Command: ")
  if command.lower() == "list":
    list_transactions(transactions)
  elif command.lower() == "income":
    add_transaction(transactions, "income")
    transactions = read_transactions()
  elif command.lower() == "expense":
    add_transaction(transactions, "expense")
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
