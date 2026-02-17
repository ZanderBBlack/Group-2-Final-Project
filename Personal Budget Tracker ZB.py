menu = [
    "1. Add Income",
    "2. Add Expense",
    "3. View All Transactions",
    "4. Set Budget",
    "5. View Budget Summary",
    "6. Generate Report",
    "7. Save & Exit",
]

income_entries = {}
expense_entries = {}

def add_income():
    income = input("Enter Income Source:")
    
    if income in income_entries:
        print("Income source already exists.")
        return
    amount = float(input("Enter Amount:"))
    income_entries[income] = amount
    print("Income added successfully.")
    
def add_expense():
    expense = input("Enter Expense Source:")
    
    if expense in expense_entries:
        print("Expense source already exists.")
        return
    amount = float(input("Enter Amount:"))
    expense_entries[expense] = amount
    print("Expense added successfully.")
    
    
while True:
    print ("\n--------- Personal Budget Tracker ----------")
    for option in menu:
        print(option)

    choice = input("Choose an option (1-7):")

    if choice == "1":
        add_income()
    
    elif choice == "2":
        add_expense()
    
    elif choice == "3":
        view_transactions()

    elif choice == "4":
        set_budget()
        
    elif choice == "5":
        view_summary()
        
    elif choice == "6":
        generate_report()

    elif choice == "7":
        print("Saving and exiting program.")
        break

    else:
        print("Invalid option.")