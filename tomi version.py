menu = [ #dictionary to store option types 
    "1. Add Income",
    "2. Add Expense",
    "3. View All Transactions",
    "4. Set Budget",
    "5. View Budget Summary",
    "6. Generate Report",
    "7. Save & Exit"
]

expense_categories = [ #dictonary to store expense options 
    "Food",
    "Transportation",
    "Entertainment",
    "Bills",
    "Other",
]

income_entries = {} #empty dictionary to store user input for incomes 
expense_entries = {cash: [] for cash in expense_categories} #dictionary to store expenses 
budgets={} #empty dictionary to store set budget for each expense category


def add_income(): #function to add income 
    print("\n----- Add Income -----") #title
    income = input("Enter Income Source:") # user input stored as a variable 
    
    if income in income_entries: #if there is income previously saved, print that income already exists 
        print("Income source already exists.")
        return  #calling back the function
    amount = float(input("Enter Amount:")) #user input for amount of income stored as variable
    income_entries[income] = amount #matching amount to income to save it as user income 
    print("Income added successfully.") #print success message to let user know income as been saved 



def add_expense(): #function to add expenses 
    print("\n----- Add Expense -----") #title 
    print("Select Cateogry:") # to choose expense category 
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")
    choice = input("Enter category (1-5): ")
    
    try:
        idx = int(choice) - 1
        if 0 <=  idx < len(expense_categories):
            category_name = expense_categories[idx]
            descript = input("Enter expense description:")
            try:
                amount = float(input("Enter Amount:"))
            except ValueError:
                print("Invalid amount. Must enter number")
                return
            expense_entries[category_name].append({
            "description": descript,
            "amount": amount
            })
            print(f"Expense added successfully. ${amount:.2f} to {category_name}.")
        else:
            print("Invalid range")
    except ValueError:
        print("Invalid input. Please enter numbers only.")



def view_transactions(): #function to show all transactions 
    print("\n--------View All Transactions---------") #title 
    
    # Show Income
    print("\nIncome:") #income title 
    if not income_entries: #if there is no previously recorded income, print error message 
        print("  No income recorded.")
    else:
        for source, amount in income_entries.items(): #if there is previously saved income, print amount 
            print(f"  {source}: ${amount:.2f}")
    
    # Show Expenses
    print("\nExpenses:") #expenses title 
    has_expenses = False 
    
    for category, expenses in expense_entries.items():
        if expenses:
            has_expenses = True #if there is expenses print it out 
            print(f"\n  {category}:")
            for expense in expenses:
                print(f"    - {expense['description']}: ${expense['amount']:.2f}")
    
    if not has_expenses: #if no expenses, print error message 
        print("  No expenses recorded.")



def set_budget():
    print("------ Set Monthly Budgets ------")
    print("Select Cateogry:") # to choose expense category 
    for i, category in enumerate(expense_categories, 1):
        print(f"{i}. {category}")
    choice = input("Enter category (1-5): ") #user input stored as a variable 
    
    try:
        idx = int(choice) - 1
        if 0 <=  idx < len(expense_categories):
            category_name = expense_categories[idx]
            amount = float(input(f"Enter monthly budget for {category_name}: "))
            budgets[category_name] = amount
            print(f"Budget set: ${amount:.2f} for {category_name}")
            print(budgets)
        else:
            print("Invalid category number.")
    except ValueError:
        print("Invalid input. Please enter numbers only.")

        
def view_summary():
    1 + 1
def generate_report():
    1 + 1

    

actions = {
    "1": add_income,
    "2": add_expense,
    "3": view_transactions,
    "4": set_budget,
    "5": view_summary,
    "6": generate_report
}
    
while True:
    print ("\n----------- Personal Budget Tracker --------------")
    print ("    Calculate your budget, Track your expenses   ")
    print ("")

    
    print("\n".join(menu))
    
    choice = input("Choose an option (1-7): ")

    if choice == "7":
        print("Saving and exiting program.")
        break
    
    if choice in actions:
        actions[choice]()
    else:
        print("Invalid option.")

    input("\nPress Enter to Continue...")
    