class Main:

    @staticmethod
    def Menu():
        print("""
        [1] Add Income
        [2] Add Expense
        [3] View All Transactions
        [4] Set Budget
        [5] View Budget Summary
        [6] Generate Report
        [exit] Save And Exit
        """)

    @staticmethod
    def HandleInput():
        selection = input("> ")

        match selection:
            case "1":
                return "Add Income Selected"
            
            case "2":
                return "Add Expense Selected"
            
            case "3":
                return "View All Transactions Selected"
            
            case "4":
                return "Set Budget Selected"
            
            case "5":
                return "View Budget Summary Selected"
            
            case "6":
                return "Generate Report Selected"
            
            case "exit":
                return "Exiting..."
            
            case _:
                return "Invalid Selection"


Main.Menu()
print(Main.HandleInput())