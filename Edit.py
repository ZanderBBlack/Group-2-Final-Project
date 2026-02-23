# Menu options displayed to the user
menu = [
    "1. Add Income",
    "2. Add Expense",
    "3. View All Transactions",
    "4. Set Budget",
    "5. View Budget Summary",
    "6. Generate Report",
    "7. Save & Exit"
]

# Available categories for expenses
expense_categories = [
    "Food",
    "Transportation",
    "Entertainment",
    "Bills",
    "Other",
]

# Stores income sources and their amounts { "Job": 3000.00 }
income_entries = {}

# Stores expenses grouped by category { "Food": [{"description": "...", "amount": ...}] }
expense_entries = {cat: [] for cat in expense_categories}


def add_income():
    print("\n----- Add Income -----")
    income = input("Enter Income Source:")

    # Prevent duplicate income sources
    if income in income_entries:
        print("Income source already exists.")
        return

    amount = float(input("Enter Amount:"))
    income_entries[income] = amount
    print("Income added successfully.")


def add_expense():
    print("\n----- Add Expense -----")
    print("Select Cateogry:")

    # Show numbered list of categories
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")

    choice = input("Enter category (1-5): ")

    try:
        idx = int(choice) - 1  # Convert to zero-based index

        if 0 <= idx < len(expense_categories):
            category_name = expense_categories[idx]
            descript = input("Enter expense description:")

            try:
                amount = float(input("Enter Amount:"))
            except ValueError:
                print("Invalid amount. Must enter number")
                return

            # Add expense as a dict to the chosen category's list
            expense_entries[category_name].append({
                "description": descript,
                "amount": amount
            })
            print(f"Expense added successfully. ${amount:.2f} to {category_name}.")
        else:
            print("Invalid range")

    except ValueError:
        print("Invalid input. Please enter numbers only.")


# Placeholder functions (not yet implemented)
def view_transactions():
    1 + 1
def set_budget():
    1 + 1
def view_summary():
    1 + 1
def generate_report():
    1 + 1


# Maps menu choices to their corresponding functions
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
        print("\n".join(menu))

        choice = input("Choose an option (1-7): ")

        # Option 7 exits the loop
        if choice == "7":
            print("Saving and exiting program.")
            break

        # Call the matching function, or warn if input is invalid
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid option.")

        input("\nPress Enter to Continue...")

    # Catch any unexpected ValueError from the main loop
    except ValueError:
        print("Please enter a valid input.")