def save_expense(amount, category):
    with open("expenses.txt", "a") as file:
        file.write(f"{amount}, {category}\n")