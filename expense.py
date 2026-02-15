
import json, argparse, os, csv
from datetime import datetime

DATA_FILE = "expenses.json"

def load_expenses():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)

                if not isinstance(data, list):
                    raise ValueError("Invalid data format")

                return data
        else:
            with open(DATA_FILE, "w") as f:
                json.dump([], f)
                return []

    except json.JSONDecodeError:
        print("File is corrupted")
        return []

def save_expenses(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent = 4)
    except Exception as e:
        print(f"Something went wrong: {e}")

def add_expenses(amount, category, desc):

    if amount <= 0:
        print("The amount must be positive.")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    expenses = load_expenses()

    if expenses:
        new_id = max(exp["id"] for exp in expenses) + 1
    else:
        new_id = 1

    new_expense = {
        "id": new_id,
        "amount": round(amount, 2),
        "category": category.lower(),
        "description": desc,
        "date": date
    }

    expenses.append(new_expense)

    save_expenses(expenses)

    print("Expense added succsesfully")

def list_expenses(category, sort_by):
    expenses = load_expenses()

    if category:
        expenses = [exp for exp in expenses if exp["category"].lower() == category.lower()]

    if not expenses:
        print("No expenses found")
        return

    if sort_by == "date":
        expenses = sorted(expenses, key = lambda x: x["date"])

    elif sort_by == "amount":
        expenses = sorted(expenses, key = lambda x: x["amount"])

    print("ID | Amount    | Description  | Category   | Date         ")
    print("----------------------------------------------------------")

    for exp in expenses:
        print(f"{exp['id']:<3}| {exp['amount']:<10.2f}| {exp['description']:<13}| {exp['category']:<11}| {exp['date']:<10}")

def calculate_total(category):
    expenses = load_expenses()

    if category:
        expenses = [exp for exp in expenses if exp["category"].lower() == category.lower()]

    if not expenses:
        print("No expenses found")
        return

    total = sum(exp["amount"] for exp in expenses)

    if category:
        print(f"Total spendings for {category}: {round(total, 2)}$")
    else:
        print(f"Total spendings: {round(total, 2)}$")

def delete_expense(expense_id):
    expenses = load_expenses()
    new_expenses = [exp for exp in expenses if exp["id"] != expense_id]

    if len(expenses) == len(new_expenses):
        print("Expense not found")
        return

    save_expenses(new_expenses)
    print("Expense removed successfully")

def update_expense(expense_id, new_amount, new_category, new_desc):
    expenses = load_expenses()
    found = False
    updated = False

    for exp in expenses:
        if exp["id"] == expense_id:
            found = True

            if new_amount is not None:
                exp["amount"] = round(new_amount, 2)
                print(f"Amount updated to {new_amount}")
                updated = True

            if new_category is not None:
                exp["category"] = new_category.lower()
                print(f"Category updated to {new_category}")
                updated = True

            if new_desc is not None:
                exp["description"] = new_desc
                print(f"Description updated to {new_desc}")
                updated = True

            break

    if not found:
        print(f"ID {expense_id} not found")
        return

    if not updated:
        print(f"The value has not updated")
        return

    save_expenses(expenses)
    print("Changes completed.")

def monthly_summary():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found")
        return

    summary = {}

    for exp in expenses:
        month = exp["date"][:7]

        if month not in summary:
            summary[month] = 0

        summary[month] += exp["amount"]

    print("Month       | Total   ")
    print("-----------------------------")

    for month in sorted(summary):
        print(f"{month:<12}| {summary[month]:.2f}$")

def export_to_csv():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found")
        return

    with open("expenses.csv", "w", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = ["id", "amount", "category", "description", "date"])
        writer.writeheader()
        writer.writerows(expenses)

    print("Exported to csv successfully")

def main():

    parser = argparse.ArgumentParser(description = "Expense tracker")

    if len(os.sys.argv) == 1:
        parser.print_help()
        return

    subparsers = parser.add_subparsers(dest = "command")

    add_parser = subparsers.add_parser("add", help = "Add expenses")
    add_parser.add_argument("amount", type = float, help = "How much was the expense")
    add_parser.add_argument("--category", default = "miscellaneous",help = "Whats the category of the expense")
    add_parser.add_argument("--desc", default = "No description", help = "Add a description")

    list_parser = subparsers.add_parser("list", help = "List the expenses data")
    list_parser.add_argument("--category", default = None, help = "Only show matching category")
    list_parser.add_argument("--sort", choices = ["date", "amount"], help = "Sort by date or amount")

    total_parser = subparsers.add_parser("total", help = "Calculate the total expenses")
    total_parser.add_argument("--category", default = None, help = "Only calculate matching category")

    delete_parser = subparsers.add_parser("delete", help ="Delete an expense")
    delete_parser.add_argument("id", type = int, help = "Id of the data to delete")

    update_parser = subparsers.add_parser("update", help="Update an expense")
    update_parser.add_argument("id", type=int, help="ID of the data to update")
    update_parser.add_argument("--amount", default = None, type=float, help="New amount")
    update_parser.add_argument("--category", default = None, help="New category")
    update_parser.add_argument("--desc", default = None, help="New description")

    summary_parser = subparsers.add_parser("summary", help = "Monthly summary")

    export_parser = subparsers.add_parser("export", help = "Export to csv")

    args = parser.parse_args()

    if args.command == "add":
        add_expenses(args.amount, args.category, args.desc)
    elif args.command == "list":
        list_expenses(args.category, args.sort)
    elif args.command == "total":
        calculate_total(args.category)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "update":
        update_expense(args.id, args.amount, args.category, args.desc)
    elif args.command == "summary":
        monthly_summary()
    elif args.command == "export":
        export_to_csv()

if __name__ == "__main__":
    main()

