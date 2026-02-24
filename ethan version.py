# To do:
    # Handle data persistance - save data to text file, load previous data when program starts and basic error handling for file operations
    # Report (Basic Reporting) - report date, summary, top spending categories, budget status
    # date and time more gracefully?
import os
import datetime

SAVE_FILE = "data.txt"

def load_data():
    # Check if the save file exists before trying to open it
    if not os.path.exists(SAVE_FILE):
        print("No saved data found. Starting fresh.")
        return

    try:
        # Open the file in read mode ('r')
        with open(SAVE_FILE, 'r') as file:
            # Read the file line by line
            for line in file:
                try:
                    # Clean up any extra spaces or newlines at the end of the line
                    line = line.strip()
                    if not line:
                        continue # Skip empty lines
                    
                    # Split the line into parts using our separator '|'
                    parts = line.split('|')
                    
                    # If the line is a transaction entry:
                    if parts[0] == "transaction" and len(parts) == 6:
                        t_type = parts[1]
                        description = parts[2]
                        amount = float(parts[3]) # Convert text to decimal number
                        category = parts[4]
                        
                        # Convert the text date back into a datetime object for the program
                        date = datetime.datetime.strptime(parts[5], "%Y-%m-%d %H:%M:%S")
                        
                        # Recreate the Transaction object
                        tx = Transaction(t_type, description, amount, category, date)
                        
                        # Add it to the correct list
                        if t_type == "income":
                            income_entries.append(tx)
                        elif t_type == "expense":
                            expense_entries.append(tx)
                            
                    # If the line is a budget entry:
                    elif parts[0] == "budget" and len(parts) == 3:
                        category = parts[1]
                        amount = float(parts[2]) # Convert text to decimal number
                        
                        # Add it to the budgets dictionary
                        budgets[category] = amount
                except Exception:
                    # If any single line is corrupted, basic defense: skip it and move to the next line
                    continue

        print("Data loaded successfully.")
    except FileNotFoundError:
        print("Save file missing. Starting fresh.")
    except Exception:
        print("Error loading data.")

def save_data():
    try:
        # Open the file in write mode ('w'), which completely overwrites old data
        with open(SAVE_FILE, 'w') as file:
            
            # 1. Save all income transactions
            for tx in income_entries:
                # Convert the datetime object back into a text string
                date_str = tx.date.strftime("%Y-%m-%d %H:%M:%S")
                # Format: transaction|type|description|amount|category|date
                file.write(f"transaction|{tx.type}|{tx.description}|{tx.amount}|{tx.category}|{date_str}\n")
                
            # 2. Save all expense transactions
            for tx in expense_entries:
                date_str = tx.date.strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"transaction|{tx.type}|{tx.description}|{tx.amount}|{tx.category}|{date_str}\n")
                
            # 3. Save all budget categories
            for category, amount in budgets.items():
                # Format: budget|category|amount
                file.write(f"budget|{category}|{amount}\n")
                
        print("Data saved successfully.")
    except Exception:
        print("Error saving data.")

# Menu options displayed to the user as a numbered list in the main loop
menu = [
    "1. Add Income",
    "2. Add Expense",
    "3. View All Transactions",
    "4. Set Budget",
    "5. View Budget Summary",
    "6. Generate Report",
    "7. Save & Exit"
]

# Available categories for expenses — used to populate menus and organize expense_entries
expense_categories = [
    "Food",
    "Transportation",
    "Entertainment",
    "Bills",
    "Other",
]

# Stores Transaction objects for all recorded income entries
income_entries = []

# Stores Transaction objects for all recorded expense entries
expense_entries = []

# Stores the monthly budget limit for each expense category { "Food": 500.00 }
budgets = {}

class Transaction:
    # Constructor — called when a new Transaction object is created
    def __init__(self, type, description, amount, category, date):
        self.type = type                # "income" or "expense"
        self.description = description
        self.amount = amount            # stored as a float
        self.category = category        # expense category or income source name
        self.date = date                # datetime timestamp of when it was recorded

    def display(self):
        # strftime() formats the datetime object into a readable string
        print(self.date)
        formatted_date = self.date.strftime("%Y-%m-%d %H:%M")
        print(f"  [{formatted_date}] {self.description} | {self.category} | ${self.amount:.2f}")



def add_income():
    print("\n----- Add Income -----")
    description = input("Enter Income Description: ")

    try:
        # Convert input string to a float so it can be stored and calculated with later
        amount = float(input("Enter Amount: $"))
    except ValueError:
        print("Invalid amount. Must enter a number.")
        return

    # Capture the current date and time using the datetime module
    date = datetime.datetime.now()

    # Create a new Transaction object with type "income" and append it to the income list
    transaction = Transaction(
        type="income",
        description=description,
        amount=amount,
        category=description,
        date=date
    )
    income_entries.append(transaction)
    print(f"Income added successfully. ${amount:.2f} from {description}.")



def add_expense():
    print("\n----- Add Expense -----")
    print("Select Category:")

    # enumerate() gives both the index and value — starting at 1 for user-friendly numbering
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")

    try:
        choice = input("Enter Category (1-5): ")
        # Subtract 1 to convert the user's 1-based choice to a 0-based list index
        idx = int(choice) - 1

        # Check that the index falls within the valid range of the categories list
        if 0 <= idx < len(expense_categories):
            category_name = expense_categories[idx]
            description = input("Enter Expense Description: ")

            # Nested try/except handles invalid amount input separately from invalid category input
            try:
                amount = float(input("Enter Amount: $"))
            except ValueError:
                print("Invalid amount. Must enter a number.")
                return

            # Capture the current date and time using the datetime module
            date = datetime.datetime.now()

            # Create a new Transaction object with type "expense" and append it to the expense list
            transaction = Transaction(
                type="expense",
                description=description,
                amount=amount,
                category=category_name,
                date=date
            )
            expense_entries.append(transaction)

            # :.2f formats the float to always show exactly 2 decimal places (e.g. 5.00)
            print(f"Expense added successfully. ${amount:.2f} to {category_name}.")

            # Check if this expense has pushed spending close to or over the budget limit
            check_budget_warning(category_name)
        else:
            print("Invalid range.")
            return

    # Catches non-numeric input when the user enters a category choice that can't be converted to int
    except ValueError:
        print("Invalid input. Please enter numbers only.")



def view_transactions():
    print("\n-------- View All Transactions ---------")

    # Show Income
    print("\nIncome:")
    # An empty list evaluates to False — so "not income_entries" is True when nothing is recorded
    if not income_entries:
        print("  No income recorded.")
    else:
        # Call each Transaction object's display() method to print its formatted details
        for transaction in income_entries:
            transaction.display()

    # Show Expenses
    print("\nExpenses:")
    if not expense_entries:
        print("  No expenses recorded.")
    else:
        # Call each Transaction object's display() method to print its formatted details
        for transaction in expense_entries:
            transaction.display()



def set_budget():
    print("\n------ Set Monthly Budget ------")
    print("Select Category:")

    # enumerate() starts at 1 so the displayed numbers match what the user is expected to enter
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")

    try:
        choice = input("Enter Category (1-5): ")
        # Subtract 1 to convert the user's 1-based choice to a 0-based list index
        idx = int(choice) - 1

        # Verify the index is within the valid range before accessing the list
        if 0 <= idx < len(expense_categories):
            category_name = expense_categories[idx]

            try:
                amount = float(input(f"Enter monthly budget for {category_name}: $"))
                # Store the budget — if one already exists for this category it will be overwritten
                budgets[category_name] = amount
                print(f"Budget set successfully: ${amount:.2f} for {category_name}.")
            except ValueError:
                print("Invalid amount. Must enter a number.")
                return
        else:
            print("Invalid range.")

    # Catches non-numeric input for the category choice
    except ValueError:
        print("Invalid input. Please enter numbers only.")



def check_budget_warning(category):
    # If no budget has been set for this category, there is nothing to check
    if category not in budgets:
        return

    # Sum all expense amounts in expense_entries that belong to the given category
    total_spent = sum(transaction.amount for transaction in expense_entries if transaction.category == category)
    limit = budgets[category]
    remaining = limit - total_spent

    # Warn the user based on how close they are to the budget limit
    if remaining <= 0:
        print(f"  Warning: You are OVER budget for {category}!")
    elif remaining <= (limit * 0.20):
        # Within 20% of the limit — print a caution message
        print(f"  Warning: You are approaching your budget limit for {category}.")
    else:
        print(f"  Budget remaining for {category}: ${remaining:.2f}")



def view_budget_summary():
    print("\n------ Budget Summary ------")

    # Sum the amount field across all Transaction objects in each list
    total_income = sum(transaction.amount for transaction in income_entries)
    total_expenses = sum(transaction.amount for transaction in expense_entries)
    current_balance = total_income - total_expenses

    # Sum all budget limits that have been set across categories
    total_budget = sum(budgets.values())
    # Positive means under budget, negative means over budget
    overunder_budget = total_budget - total_expenses

    print(f"\nTotal Income:   ${total_income:.2f}")

    print("\nExpenses by Category:")
    # If no budgets have been set, there is nothing to display
    if not budgets:
        print("  No budgets set.")
        return

    for category, limit in budgets.items():
        # Calculate how much has been spent in this category by filtering expense_entries
        total_spent = sum(transaction.amount for transaction in expense_entries if transaction.category == category)
        remaining = limit - total_spent
        # Calculate the percentage of the budget used — multiply by 100 to convert to a whole number
        percentage = (total_spent / limit) * 100
        print(f"  {category}: ${total_spent:.2f} / ${limit:.2f} ({percentage:.1f}% used)")

    print(f"\nTotal Expenses: ${total_expenses:.2f}")
    print(f"Current Balance: ${current_balance:.2f}")
    print(f"Total Budget:   ${total_budget:.2f}")

    # Use abs() to remove the negative sign and display the value cleanly
    if overunder_budget < 0:
        print(f"Over Budget:    ${abs(overunder_budget):.2f}")
    else:
        print(f"Under Budget:   ${abs(overunder_budget):.2f}")



# Placeholder — report generation not yet implemented
def generate_report():
    1 + 1


# Maps menu choices (as strings) to their corresponding functions
# Storing functions as values allows calling them dynamically with actions[choice]()
actions = {
    "1": add_income,
    "2": add_expense,
    "3": view_transactions,
    "4": set_budget,
    "5": view_budget_summary,
    "6": generate_report
}

# Main loop — keeps running until the user chooses to exit
load_data()

while True:
    try:
        print("\n--------- Personal Budget Tracker ----------")
        print ("--- Calculate your budget, Track your expenses ---")
        # "\n".join() combines the menu list into a single string with each option on its own line
        print("\n".join(menu))

        choice = input("Choose an option (1-7): ")

        # Option 7 exits the loop using break — skips the rest of the loop body and ends the program
        if choice == "7":
            print("Saving and exiting program.")
            save_data()
            break

        # Look up the choice in the actions dictionary and call the matching function if it exists
        if choice in actions:
            actions[choice]()
            
        else:
            print("Invalid option.")

        # Pauses the program after each action so the user can read the output before the menu reappears
        input("\nPress Enter to Continue...")

    # Catch any unexpected ValueError that wasn't handled inside the individual functions
    except ValueError:
        print("Please enter a valid input.")