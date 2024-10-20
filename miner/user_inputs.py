from datetime import datetime

def get_commit_limit():
    while True:
        try:
            limit = int(input("Enter the commit limit (a positive integer): "))
            if limit > 0:
                return limit
            else:
                print("Please enter a positive integer greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def choose_analyzer():
    while True:
        try:
            print("Choose analyzer: 1) Commit analyzer 2) Test debt analyzer")
            choice = int(input("Which one?: "))
            if choice in [1, 2]:
                return choice
            else:
                print("Please choose 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")


def get_date(prompt):
    while True:
        date_input = input(f"Enter the {prompt} date (YYYY-MM-DD) or press Enter to skip: ")

        if date_input == "":
            return None

        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.")