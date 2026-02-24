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

# Stores income sources and their amounts as key-value pairs { "Job": 3000.00 }
income_entries = {}

# Builds a dictionary where each category name is a key mapped to an empty list
# These lists will hold expense dicts: { "Food": [{"description": "...", "amount": ...}] }
expense_entries = {cat: [] for cat in expense_categories}

# Empty dictionary to store the monthly budget limit for each expense category { "Food": 500.00 }
budgets = {}


def add_income():
    print("\n----- Add Income -----")
    income = input("Enter Income Source:")

    # Prevent duplicate income sources — each source name must be unique in the dictionary
    if income in income_entries:
        print("Income source already exists.")
        return

    # Convert input string to a float so it can be stored and calculated with later
    amount = float(input("Enter Amount:"))
    # Add the new income source as a key with its amount as the value
    income_entries[income] = amount
    print("Income added successfully.")


def add_expense():
    print("\n----- Add Expense -----")
    print("Select Cateogry:")

    # enumerate() gives both the index and value — starting at 1 for user-friendly numbering
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")

    choice = input("Enter category (1-5): ")

    try:
        # Subtract 1 to convert the user's 1-based choice to a 0-based list index
        idx = int(choice) - 1

        # Check that the index falls within the valid range of the categories list
        if 0 <= idx < len(expense_categories):
            category_name = expense_categories[idx]
            descript = input("Enter expense description:")

            # Nested try/except handles invalid amount input separately from invalid category input
            try:
                amount = float(input("Enter Amount:"))
            except ValueError:
                print("Invalid amount. Must enter number")
                return

            # append() adds a new expense dict to the end of the existing list for that category
            expense_entries[category_name].append({
                "description": descript,
                "amount": amount
            })
            # :.2f formats the float to always show exactly 2 decimal places (e.g. 5.00)
            print(f"Expense added successfully. ${amount:.2f} to {category_name}.")
        else:
            print("Invalid range")

    # Catches non-numeric input when the user enters a category choice that can't be converted to int
    except ValueError:
        print("Invalid input. Please enter numbers only.")


def view_transactions():
    print("\n--------View All Transactions---------")  # Title

    # Show Income
    print("\nIncome:")
    # An empty dictionary evaluates to False — so "not income_entries" is True when nothing is recorded
    if not income_entries:
        print("  No income recorded.")
    # .items() returns each key-value pair as (source, amount) so both can be printed together
    else:
        for source, amount in income_entries.items():
            print(f"  {source}: ${amount:.2f}")

    # Show Expenses
    print("\nExpenses:")
    # Flag to track whether any category had expenses — used to show a message if none were found
    has_expenses = False
    # Loop through every category and its list of expenses
    for category, expenses in expense_entries.items():
        # Only print the category header if it actually has at least one expense entry
        if expenses:
            has_expenses = True
            print(f"\n  {category}:")
            # Loop through each expense dict in the category and print its description and amount
            for expense in expenses:
                print(f"    - {expense['description']}: ${expense['amount']:.2f}")
    # Checked after the loop — if has_expenses was never set to True, no expenses exist at all
    if not has_expenses:
        print("  No expenses recorded.")


def set_budget():
    print("------ Set Monthly Budgets ------")
    print("Select Cateogry:")  # Prompt user to choose an expense category

    # enumerate() starts at 1 so the displayed numbers match what the user is expected to enter
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")
    choice = input("Enter category (1-5): ")  # User input stored as a variable

    try:
        # Subtract 1 to convert the user's 1-based choice to a 0-based list index
        idx = int(choice) - 1
        # Verify the index is within the valid range before accessing the list
        if 0 <= idx < len(expense_categories):
            category_name = expense_categories[idx]
            amount = float(input(f"Enter monthly budget for {category_name}: "))
            # Store the budget — if a budget already exists for this category it will be overwritten
            budgets[category_name] = amount
            print(f"Budget set: ${amount:.2f} for {category_name}")
        else:
            print("Invalid category number.")
    # Catches non-numeric input for either the category choice or the budget amount
    except ValueError:
        print("Invalid input. Please enter numbers only.")


# Placeholder — budget summary display not yet implemented
def view_summary():
    1 + 1


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
    "5": view_summary,
    "6": generate_report
}

# Main loop — keeps running until the user chooses to exit
while True:
    try:
        print("\n--------- Personal Budget Tracker ----------")
        # "\n".join() combines the menu list into a single string with each option on its own line
        print("\n".join(menu))

        choice = input("Choose an option (1-7): ")

        # Option 7 exits the loop using break — skips the rest of the loop body and ends the program
        if choice == "7":
            print("Saving and exiting program.")
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