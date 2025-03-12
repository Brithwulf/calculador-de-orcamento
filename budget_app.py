class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        output = f'{self.name:*^30}\n'
        for entry in self.ledger:
            description = entry['description'][:23]
            amount = f"{entry['amount']:.2f}"
            output += f'{description:<23}{amount:>7}\n'
        output += f'Total: {self.get_balance():.2f}'
        return output

    def deposit(self, amount, description=""):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({'amount': amount * -1, 'description': description})
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for dic in self.ledger:
            balance += dic['amount']
        return balance

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {other_category.name}')
            other_category.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        if amount <= self.get_balance():
            return True

def create_spend_chart(categories):
    total_spent = 0
    spending = []

    for category in categories:
        spent = sum(-entry['amount'] for entry in category.ledger if entry['amount'] < 0)
        spending.append(spent)
        total_spent += spent

    percentages = [int((sp / total_spent) * 100 // 10) * 10 for sp in spending]

    output = "Percentage spent by category\n"

    for i in range(100, -1, -10):
        output += f"{i:>3}| "
        for pct in percentages:
            output += "o  " if pct >= i else "   "
        output += "\n"

    output += "    -" + "---" * len(categories) + "\n"

    max_length = max(len(category.name) for category in categories)
    names = [category.name.ljust(max_length) for category in categories]

    for i in range(max_length):
        output += "     "
        for name in names:
            output += f"{name[i]}  "
        output += "\n"

    return output.rstrip("\n")
