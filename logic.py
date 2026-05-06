class Category:
    def __init__(self, name, budget):
        self.name = name
        self.budget = float(budget)
        self.balance = float(budget)

    def record_expense(self, amount):
        amount = float(amount)
        if amount <= self.balance:
            self.balance -= amount
            return True, "Success"
        return False, "Insufficient Balance"

def calculate_remaining_pool(total_funds, categories_dict):
    total_allocated = sum(cat.budget for cat in categories_dict.values())
    return total_funds - total_allocated

def validate_allocation(amount, total_funds, categories_dict):
    current_allocated = sum(cat.budget for cat in categories_dict.values())
    return (current_allocated + float(amount)) <= total_funds