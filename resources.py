import datetime

month_names = ["January", "February", "March", "April",
               "May", "June", "July", "August",
               "September", "October", "November", "December"]

disp_month = int(datetime.date.today().month) - 1
disp_year = int(datetime.date.today().year)

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

    def __init__(self, ctg: Category, amount: float, acc: Account, mode: bool, description: str = "", date: datetime.date = datetime.date.today()):
        self.ctg = ctg
        self.amount = amount
        self.acc = acc
        self.description = description
        self.acc.change_value(amount, mode)
        self.date = date

dft_acc = [Account("Cash"), Account("Card"), Account("Savings")]
dft_ctg = [Category("Food", "Images/food_ctg.png"), Category("Transport", "Images/Analytics.png"),
           Category("Communication", "Images/Analytics.png"), Category("Tourism", "Images/Analytics.png"),
           Category("Clothing", "Images/Analytics.png"), Category("Cleaning", "Images/Analytics.png"),
           Category("Home", "Images/Analytics.png")]
view_height = 0 #Adjusts the main scroll view
ctg_view_width = 0 #Adjusts the new entry popup scroll view
dft_currencies = [["€", True], ["$",True], ["TRY",False]] #True if the symbol is to the left, False if it is to the right.
currency_choice = 0 #The index of the currency above
temp_ctg = dft_ctg[0] #Passes the value from the child button object to parent object
temp_entry = None #Passes the value to create it in the main view

class PlaceDoesNotExistError(Exception):
    #See ba_funcs, align_currency_text
    pass
