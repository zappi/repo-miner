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

def choose_analyzer(analyzers):
    while True:
        print("Choose an analyzer:")
        for idx, (name, info) in enumerate(analyzers.items(), start=1):
            print(f"{idx}) {name} ({info['description']})")

        try:
            choice = int(input("Which one?: "))
            if 1 <= choice <= len(analyzers):
                return list(analyzers.keys())[choice - 1]
            else:
                print(f"Please select a number between 1 and {len(analyzers)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

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

def get_filepath():
    return input("Enter the filepath: ")