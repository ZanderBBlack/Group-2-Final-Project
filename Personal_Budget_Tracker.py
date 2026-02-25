import os
import datetime

# Display instructions before the first run
try:
    with open("README.md", "r") as f:
        print("\n" + "="*50)
        print(f.read().strip())
        print("="*50 + "\n")
    input("Press Enter to start the Personal Budget Tracker...")
except FileNotFoundError:
    pass

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
        formatted_date = self.date.strftime("%Y-%m-%d %H:%M")
        print(f"  [{formatted_date}] {self.description} | {self.category} | ${self.amount:.2f}")



def load_data():
    # Check if the save file exists before attempting to open it — avoids a crash on first run
    if not os.path.exists("budget_data.txt"):
        print("No saved data found. Starting fresh.")
        return False

    try:
        with open("budget_data.txt", "r") as file:
            for line in file:
                # Remove the trailing newline character from each line before processing
                line = line.strip()

                # Skip any blank lines that may exist in the file
                if not line:
                    continue

                # Split the line into individual fields using | as the delimiter
                fields = line.split("|")
                entry_type = fields[0]

                if entry_type == "income" or entry_type == "expense":
                    # Reconstruct a Transaction object from the saved fields
                    transaction = Transaction(
                        type=fields[0],
                        description=fields[1],
                        # Convert the stored string back to a float for calculations
                        amount=float(fields[2]),
                        category=fields[3],
                        # strptime() parses the date string back into a datetime object
                        date=datetime.datetime.strptime(fields[4], "%Y-%m-%d %H:%M:%S")
                    )
                    if entry_type == "income":
                        income_entries.append(transaction)
                    else:
                        expense_entries.append(transaction)

                elif entry_type == "budget":
                    # Rebuild the budgets dictionary — { category: amount }
                    budgets[fields[1]] = float(fields[2])

        print("Data loaded successfully.")
        # Return True to indicate the file was found and loaded without errors
        return True

    except FileNotFoundError:
        print("Save file missing. Starting fresh.")
        return False
    # Catch any other unexpected errors such as corrupted or malformed lines
    except Exception:
        print("Error loading data.")
        return False



def save_data():
    try:
        # Open in write mode — creates the file if it doesn't exist, overwrites it if it does
        with open("budget_data.txt", "w") as file:
            for transaction in income_entries:
                # Write each field separated by | so load_data() can split them back apart
                file.write(f"{transaction.type}|{transaction.description}|{transaction.amount}|{transaction.category}|{transaction.date.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for transaction in expense_entries:
                file.write(f"{transaction.type}|{transaction.description}|{transaction.amount}|{transaction.category}|{transaction.date.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for category, amount in budgets.items():
                # Prefix budget lines with "budget" so load_data() can identify the entry type
                file.write(f"budget|{category}|{amount}\n")

        print("Data saved successfully.")
        # Return True to indicate all data was written to the file without errors
        return True

    # Catch any errors during writing — e.g. permission denied or disk full
    except Exception:
        print("Error saving data.")
        return False



def add_income():
    print("\n----- Add Income -----")
    description = input("Enter Income Description: ")

    try:
        # Convert input string to a float so it can be stored and calculated with later
        amount = float(input("Enter Amount: $"))
    except ValueError:
        print("Invalid amount. Must enter a number.")
        # Return False to indicate the income entry was not successfully added
        return False

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
    # Return True to indicate the income entry was successfully added
    return True



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
                # Return False to indicate the expense entry was not successfully added
                return False

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
            # check_budget_warning() returns a message string or None — only print if a message exists
            message = check_budget_warning(category_name)
            if message:
                print(message)

            # Return True to indicate the expense entry was successfully added
            return True
        else:
            print("Invalid range.")
            return False

    # Catches non-numeric input when the user enters a category choice that can't be converted to int
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return False



def view_transactions():
    print("\n-------- View All Transactions ---------")

    # Get todays date and format it for display at the top of the view
    date = datetime.date.today()
    formatted_date = date.strftime("%B %d, %Y")
    print(f"Report Date: {formatted_date}")

    # Calculate total income by summing the amount field across all income Transaction objects
    total_income = sum(transaction.amount for transaction in income_entries)

    print(f"\n  --- Income Sources ---")

    # An empty list evaluates to False — so "not income_entries" is True when nothing is recorded
    if not income_entries:
        print("  No income recorded.")
    else:
        # Print column headers with fixed-width formatting to align the table
        # '<' = left-align, '>' = right-align, the number sets the column width
        print(f"\n  {'Source':<20} {'Date':<18} {'Amount':>10}")
        print(f"  {'-'*20} {'-'*18} {'-'*10}")

        for transaction in income_entries:
            # strftime() formats the datetime object into a human-readable string
            formatted_date = transaction.date.strftime("%Y-%m-%d %H:%M")
            print(f"  {transaction.description:<20} {formatted_date:<18} ${transaction.amount:>9.2f}")

        # Divider line and total row to close out the income table
        print(f"  {'-'*20} {'-'*18} {'-'*10}")
        print(f"  {'Total Income:':<20} {'':18} ${total_income:>9.2f}")

    # Calculate total expenses by summing the amount field across all expense Transaction objects
    total_expenses = sum(transaction.amount for transaction in expense_entries)

    print(f"\n  --- Expenses ---")

    if not expense_entries:
        print("  No expenses recorded.")
    else:
        # Print column headers — Category is added here since expenses are grouped by category
        print(f"\n  {'Description':<20} {'Date':<18} {'Category':<16} {'Amount':>10}")
        print(f"  {'-'*20} {'-'*18} {'-'*16} {'-'*10}")

        for transaction in expense_entries:
            # strftime() formats the datetime object into a human-readable string
            formatted_date = transaction.date.strftime("%Y-%m-%d %H:%M")
            print(f"  {transaction.description:<20} {formatted_date:<18} {transaction.category:<16} ${transaction.amount:>9.2f}")

        # Divider line and total row to close out the expense table
        print(f"  {'-'*20} {'-'*18} {'-'*16} {'-'*10}")
        print(f"  {'Total Expenses:':<20} {'':18} {'':16} ${total_expenses:>9.2f}")



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
        return None

    # Sum all expense amounts in expense_entries that belong to the given category
    total_spent = sum(transaction.amount for transaction in expense_entries if transaction.category == category)
    limit = budgets[category]
    remaining = limit - total_spent

    # Return the appropriate warning string based on how close spending is to the budget limit
    if remaining <= 0:
        return f"  Warning: You are OVER budget for {category}!"
    elif remaining <= (limit * 0.20):
        # Within 20% of the limit — return a caution message
        return f"  Warning: You are approaching your budget limit for {category}."
    else:
        return f"  Budget remaining for {category}: ${remaining:.2f}"



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

    # Column headers for the budget breakdown table
    print(f"\n  {'Category':<16} {'Spent':>10} {'Budget':>10} {'Remaining':>10} {'Used':>8}")
    print(f"  {'-'*16} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")

    for category, limit in budgets.items():
        # Calculate how much has been spent in this category by filtering expense_entries
        total_spent = sum(transaction.amount for transaction in expense_entries if transaction.category == category)
        remaining = limit - total_spent
        # Calculate the percentage of the budget used — multiply by 100 to convert to a whole number
        percentage = (total_spent / limit) * 100
        print(f"  {category:<15} ${total_spent:>9.2f} ${limit:>9.2f} ${remaining:>9.2f} {percentage:>7.1f}%")

    # Closing divider beneath the budget table
    print(f"  {'-'*16} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")
    print(f"\nTotal Expenses: ${total_expenses:.2f}")
    print(f"Current Balance: ${current_balance:.2f}")
    print(f"Total Budget:   ${total_budget:.2f}")

    # Use abs() to remove the negative sign and display the value cleanly
    if overunder_budget < 0:
        print(f"Over Budget:    ${abs(overunder_budget):.2f}")
    else:
        print(f"Under Budget:   ${abs(overunder_budget):.2f}")



def generate_report():
    print("\n------ Financial Report ------")

    # Get todays date and format it for display at the top of the report
    date = datetime.date.today()
    formatted_date = date.strftime("%B %d, %Y")
    print(f"Report Date: {formatted_date}")

    # Calculate summary totals by summing amounts across all income and expense Transaction objects
    total_income = sum(transaction.amount for transaction in income_entries)
    total_expenses = sum(transaction.amount for transaction in expense_entries)
    # Net income = income minus expenses — negative value means spending exceeded earnings
    net_income = total_income - total_expenses
    # Savings rate as a percentage — guarded against division by zero if no income exists
    saving_rate = (net_income / total_income) * 100 if total_income > 0 else 0

    print(f"\n  --- Summary ---")
    print(f"  {'-'*40}")
    print(f"  {'Total Income:':<20} ${total_income:>10.2f}")
    print(f"  {'Total Expenses:':<20} ${total_expenses:>10.2f}")
    print(f"  {'Net Income:':<20} ${net_income:>10.2f}")
    # :.1f formats the savings rate to one decimal place
    print(f"  {'Savings Rate:':<20} {saving_rate:>10.1f}%")
    print(f"  {'-'*40}")

    # Alert the user if they've spent more than they've earned this period
    if net_income < 0:
        print("  Warning: Expenses exceed income.")

    print(f"\n  --- Income Sources ---")
    if not income_entries:
        print("  No income recorded.")
    else:
        # Column headers — widths match those used in each row below for alignment
        print(f"\n  {'Source':<20} {'Date':<18} {'Amount':>10}")
        print(f"  {'-'*20} {'-'*18} {'-'*10}")

        for transaction in income_entries:
            # strftime() formats the datetime object into a human-readable string
            formatted_date = transaction.date.strftime("%Y-%m-%d %H:%M")
            print(f"  {transaction.description:<20} {formatted_date:<18} ${transaction.amount:>9.2f}")

        # Closing divider beneath the income table
        print(f"  {'-'*20} {'-'*18} {'-'*10}")

    print(f"\n  --- Budget Status ---")
    if not budgets:
        print("  No budgets set.")
    else:
        over_count = 0

        # Column headers for the budget status table
        print(f"\n  {'Category':<20} {'Spent':>10} {'Limit':>10} {'Status':>10}")
        print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*10}")

        for category, limit in budgets.items():
            # Sum all expenses that belong to this category to get total spending
            spent = sum(t.amount for t in expense_entries if t.category == category)

            # Assign a status label based on how close spending is to the budget limit
            if spent > limit:
                over_count += 1     # Track how many categories exceeded their budget
                status = "OVER"
            elif spent >= limit * 0.80:
                # At or above 80% of the limit — flag as CLOSE to warn the user
                status = "CLOSE"
            else:
                status = "OK"

            print(f"  {category:<20} ${spent:>9.2f} ${limit:>9.2f} {status:>10}")

        # Closing divider beneath the budget table
        print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*10}")

        # Summary line — tells the user at a glance how many categories need attention
        if over_count == 0:
            print("\n  All categories within budget.")
        else:
            print(f"\n  {over_count} category/categories over budget.")



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

load_data()

# Main loop — keeps running until the user chooses to exit
while True:
    try:
        print("=" * 50)
        print("           Personal Budget Tracker")
        print("  Calculate your budget, Track your expenses")
        print("=" * 50)
        # "\n".join() combines the menu list into a single string with each option on its own line
        print("\n".join(menu))
        print("-" * 50)

        choice = input("Choose an option (1-7): ")

        # Option 7 exits the loop using break — skips the rest of the loop body and ends the program
        if choice == "7":
            print("\nSaving and exiting program.")
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