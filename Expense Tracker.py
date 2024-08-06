import json
from datetime import datetime

# Constants
FILENAME = 'expenses.json'
CATEGORIES = ['Food', 'Transportation', 'Entertainment', 'Other']

def get_expense():
    """
    Prompts the user to input an expense amount and description.

    Returns:
        tuple: A tuple containing the expense amount (float) and description (str).
    """
    try:
        amount = float(input("Enter the expense amount: "))
        description = input("Enter a brief description of the expense: ")
        return amount, description
    except ValueError:
        print("Invalid input. Please enter a numeric value for the amount.")
        return None, None

def get_category():
    """
    Prompts the user to select an expense category.

    Returns:
        str: The selected category or 'Other' if the input is invalid.
    """
    print("Categories:", CATEGORIES)
    category = input("Enter the expense category: ")
    if category not in CATEGORIES:
        print("Invalid category. Defaulting to 'Other'.")
        category = 'Other'
    return category

def load_data(filename=FILENAME):
    """
    Loads expense data from a JSON file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        list: A list of expense records.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(expenses, filename=FILENAME):
    """
    Saves expense data to a JSON file.

    Args:
        expenses (list): A list of expense records.
        filename (str): The path to the JSON file.
    """
    with open(filename, 'w') as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses, amount, description, category):
    """
    Adds an expense record to the list of expenses.

    Args:
        expenses (list): A list of expense records.
        amount (float): The amount of the expense.
        description (str): A brief description of the expense.
        category (str): The category of the expense.
    """
    date = datetime.now().strftime("%Y-%m-%d")
    expenses.append({"amount": amount, "description": description, "category": category, "date": date})

def summarize_expenses(expenses):
    """
    Summarizes expenses by month and category.

    Args:
        expenses (list): A list of expense records.

    Returns:
        dict: A dictionary with monthly and category-wise expense summaries.
    """
    summary = {}
    for expense in expenses:
        date = expense['date']
        month = date[:7]
        if month not in summary:
            summary[month] = {'total': 0, 'categories': {}}
        summary[month]['total'] += expense['amount']
        if expense['category'] not in summary[month]['categories']:
            summary[month]['categories'][expense['category']] = 0
        summary[month]['categories'][expense['category']] += expense['amount']
    return summary

def display_summary(summary):
    """
    Displays the summary of expenses.

    Args:
        summary (dict): A dictionary with monthly and category-wise expense summaries.
    """
    for month, data in summary.items():
        print(f"\nMonth: {month}")
        print(f"Total: ${data['total']:.2f}")
        for cat, amt in data['categories'].items():
            print(f"  {cat}: ${amt:.2f}")

def main():
    """
    Main function to interact with the user and manage expenses.
    """
    expenses = load_data()
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amount, description = get_expense()
            if amount is not None:
                category = get_category()
                add_expense(expenses, amount, description, category)
                save_data(expenses)
                print("Expense added successfully!")
        elif choice == '2':
            summary = summarize_expenses(expenses)
            display_summary(summary)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
