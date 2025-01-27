import datetime


class Category:

    def __init__(self, name: str, icon_path: str = ""):
        self.name = name
        self.icon_path = icon_path
        self.current_total = 0.0

    def spending(self, amount: float):
        self.current_total += amount

    def reset_spending(self):
        self.current_total = 0.0

class Budget:

    def __init__(self, ctg: Category, limit: float):
        self.ctg = ctg
        self.limit = limit
        self.current_spending = ctg.current_total

    def update(self):
        self.current_spending = self.ctg.current_total

    def reset_budget(self):
        self.current_spending = 0.0

class Account:

    def __init__(self, name: str, icon_path: str = ""):
        self.name = name
        self.icon_path = icon_path
        self.value = 0.0

    def change_value(self, amount: float, mode: bool): #True for deposit, False for withdrawal
        self.value = (self.value + amount) if mode else (self.value - amount)

class Entry:

    def __init__(self, ctg: Category, amount: float, acc: Account, mode: bool):
        self.ctg = ctg
        self.amount = amount
        self.acc = acc
        self.acc.change_value(amount, mode)
        self.date = datetime.date.today()

dft_acc = [Account("Cash"), Account("Card"), Account("Savings")]
dft_ctg = [Category("Food"), Category("Transport"),
           Category("Communication"), Category("Tourism"),
           Category("Clothing"), Category("Cleaning"),
           Category("Home")]