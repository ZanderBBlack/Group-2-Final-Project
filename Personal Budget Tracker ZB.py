menu = [
    "1. Add Income",
    "2. Add Expense",
    "3. View All Transactions",
    "4. Set Budget",
    "5. View Budget Summary",
    "6. Generate Report",
    "7. Save & Exit",
]

while True:
    # prints all options in option list
    print ("\n--------- Personal Budget Tracker ----------")
    for option in menu:
        print(option)

    # user inputs choice of option
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

    # exits program (infinite loop)
    elif choice == "7":
        print("Saving and exiting program.")
        break

    # if choice something else its invalid
    else:
        print("Invalid option.")