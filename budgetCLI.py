import argparse
import shlex
from budget import BudgetAndExpense

def get_parser():
    parser = argparse.ArgumentParser(description="Interactive Budget Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("add", help="Add a new expense")
    subparsers.add_parser("show", help="Display budget info in a grid")
    subparsers.add_parser("delete", help="Delete an expense")

    search_parser = subparsers.add_parser("search", help="Search expenses")
    search_parser.add_argument(
        "type", 
        choices=["entry", "category", "price"], 
        help="Type of search to perform"
    )

    subparsers.add_parser("range", help="Get sum of expenses within a date range")

    return parser

def main():
    parser = get_parser()
    app = BudgetAndExpense()

    print("Welcome to the Budget Tracker CLI!")
    print("Type '-h' for a list of commands, or 'quit' to exit.")

    #program loop
    while True:
        try:
            user_input = input("\nbudget> ").strip()
            
            #looks for exit commands
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("Goodbye!")
                break
                
            #skips if user presses enter with no input
            if not user_input:
                continue

            #uses shlex to split user string 
            args_list = shlex.split(user_input)
            
            #program persists on error, need quit or exit to terminate
            try:
                args = parser.parse_args(args_list)
            except SystemExit:
                continue

            if args.command == "add":
                app.addExpense()
                
            elif args.command == "show":
                app.displayBudgetInfo()
                
            elif args.command == "delete":
                app.deleteExpense()
                
            elif args.command == "search":
                if args.type == "entry":
                    print(app.searchEntry())
                elif args.type == "category":
                    print(app.searchCategory())
                elif args.type == "price":
                    print(app.searchByPrice())
                    
            elif args.command == "range":
                result = app.expenseSumDateRange()
                if result is not None:
                    print(f"${result:.2f}")

        except KeyboardInterrupt:
            #catch force quit with Ctrl+C
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()