import datetime
import calendar

month_names = ["January", "February", "March", "April",
               "May", "June", "July", "August",
               "September", "October", "November", "December"]

current_month = datetime.datetime.today().month
chosen_date: datetime.date.today()

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
        self.mode = mode
        self.description = description
        self.acc.change_value(amount, mode)
        self.date = date

dft_acc = [Account("Cash", "Images/cash_acc.png"), Account("Card","Images/card_acc.png"), Account("Savings", "Images/Analytics.png")]
dft_ctg = [Category("Food", "Images/food_ctg.png"), Category("Transport", "Images/transport_ctg.png"),
           Category("Communication", "Images/comms_ctg.png"), Category("Tourism", "Images/tourism_ctg.png"),
           Category("Clothing", "Images/clothing_ctg.png"), Category("Cleaning", "Images/cleaning_ctg.png"),
           Category("Home", "Images/home_ctg.png")]
view_height = 0 #Adjusts the main scroll view
ctg_view_width = 0 #Adjusts the new entry popup scroll view
dft_currencies = [["€", True], ["$",True], ["TRY",False]] #True if the symbol is to the left, False if it is to the right.
currency_choice = 0 #The index of the currency above
temp_ctg = dft_ctg[0] #Passes the value from the child button object to parent object
temp_entry = None #Passes the value to create it in the main view
temp_layout = None #Passes the main-layout
temp_acc = None #Passes the account-box
entry_list = []
shown_entries = 10


class PlaceDoesNotExistError(Exception):
    #See ba_funcs, align_currency_text
    pass
