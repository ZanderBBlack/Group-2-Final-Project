class Main:


    bankDetails = {
        "Income": 0,
        "Expense": 0,
        "Transactions": "",
        "Budget": 0,
    }


    @staticmethod
    def Menu():
        print("""
[1] Add Income
[2] Add Expense
[3] Add Transaction
[4] View All Transactions
[5] Set Budget
[6] View Budget Summary
[7] Generate Report
[exit] Save And Exit
""")


    @staticmethod
    def HandleInput():
        while True:
            Main.Menu()
            selection = input("> ")
            details = Main.bankDetails

            match selection:
                case "1":
                    details["Income"] = float(input("Income: "))
                    print(f"Current Income: {details['Income']}")

                case "2":
                    details["Expense"] = float(input("Expense: "))
                    print(f"Current Income: {details['Expense']}")

                case "3":
                    details["Transactions"] += input("Details: ")
                    print(f"Transactions: {details['Transactions']}, ")

                case "4":
                    print(f"Transactions: {details['Transactions']}, ")

                case "5":
                    details["Budget"] += input("Budget: ")
                    print(f"Budget: {details['Budget']}, ")

                case "6":
                    print("View Budget Summary Selected")

                case "7":
                    print("Generate Report Selected")

                case "exit":
                    print("Exiting...")
                    break
                case _:
                    print("Invalid Selection")


Main.HandleInput()