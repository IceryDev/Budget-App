import calendar
import itertools
import random
import math

import kivy
from kivy.config import Config

from resources import dft_currencies, currency_choice

Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '620')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import NumericProperty

from functools import partial
import resources as rs
import ba_funcs as baf
import datetime

'''Legend for button groups:
   ctg: Assigned to the category selection buttons in the entry creation menu
   ctg_budget: Assigned to the category selection buttons in the budget creation menu
   date: Assigned to the date selection buttons in the entry creation menu
   main: Assigned to the main navigation buttons
   transaction: Assigned to Expense/Deposit buttons in the entry creation menu'''

scroll_view_main = ScrollView()

def re_construct_save():
    try:
        input_file = baf.load_entry_groups()
        for key, value in input_file.items():
            rs.entry_groups[key] = rs.EntryGroup(key, entries=[EntryUI(x) for x in value.entries])
        return 0
    except AttributeError:
        return 1

class TitleBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "horizontal"

        with self.canvas.before:
            Color(0, 149/255, 166/255, 63/100)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.padding = [10, 0, 0, 0]

        self.menu_button = Button(size_hint_x=None,
                             width=30,
                             background_color=(0, 0, 0, 0))
        self.menu_button.bind(on_press=self.menu_clicked)

        self.img = Image(source="Images/3bars.png")
        self.menu_button.bind(size=self._update_image_pos, pos=self._update_image_pos)

        self.menu_button.add_widget(self.img)

        self.add_widget(self.menu_button)

        self.add_widget(Label(text="Icery's Finance App",
                              font_name="Fonts/KaushanScript-Regular.ttf",
                              font_size=25,
                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              halign="center"))

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def _update_image_pos(self, *args):
        self.img.size = self.menu_button.size
        self.img.pos = self.menu_button.pos

    def menu_clicked(self, *args):
        print(f"Yay {self}")

class DateBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rs.temp_date_box = self

        with self.canvas.before:
            Color(0, 116/255, 129/255, 63/100)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.left_button = Button(size_hint_x=None,
                                  width=30,
                                  background_color=(0, 0, 0, 0))
        self.left_button.bind(on_press=self.lft_clicked)

        self.left_arrow = Image(source="Images/arrow_left.png")
        self.left_button.bind(size=partial(self._update_image_pos, self.left_arrow, self.left_button), pos=partial(self._update_image_pos, self.left_arrow, self.left_button))

        self.left_button.add_widget(self.left_arrow)
        self.add_widget(self.left_button)

        self.month_text = Label(text=f"{rs.month_names[rs.disp_month % 12]}, {rs.disp_year}",
                              pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.month_text.bind(text=self.month_text.setter("text"))

        self.add_widget(self.month_text)

        self.right_button = Button(size_hint_x=None,
                                   width=30,
                                   background_color=(0, 0, 0, 0))
        self.right_button.bind(on_press=self.rgt_clicked)

        self.right_arrow = Image(source="Images/arrow_right.png")
        self.right_button.bind(size=partial(self._update_image_pos, self.right_arrow, self.right_button),
                              pos=partial(self._update_image_pos, self.right_arrow, self.right_button))

        self.right_button.add_widget(self.right_arrow)
        self.add_widget(self.right_button)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    @staticmethod
    def _update_image_pos(img, button, *args):
        img.size = button.size
        img.pos = button.pos

    def _update_text(self):
        #print(f"self.month_text: {self.month_text.text}, disp_month: {rs.disp_year}, {rs.disp_month}, {rs.disp_month // 12} type: {type(self.month_text)}")
        self.month_text.text = f"{rs.month_names[rs.disp_month % 12]}, {rs.disp_year}"

    def lft_clicked(self, *args):
        rs.disp_month = (rs.disp_month - 1)
        rs.disp_year = int(datetime.date.today().year) + (rs.disp_month // 12)
        self.change_children()
        rs.main_widgets['acc_bdg_exp'].update_text()
        self._update_text()

    def rgt_clicked(self, *args):
        rs.disp_month = (rs.disp_month + 1)
        rs.disp_year = int(datetime.date.today().year) + (rs.disp_month // 12)
        self.change_children()
        rs.main_widgets['acc_bdg_exp'].update_text()
        self._update_text()

    @staticmethod
    def change_children(*args):
        rs.entry_list.clear()
        if rs.entry_groups.get(baf.rtrn_disp()) is not None:
            for item in rs.entry_groups.get(baf.rtrn_disp()).entries: rs.entry_list.append(item)
        rs.temp_layout.is_updating = True
        rs.temp_layout.clear_widgets()
        rs.temp_layout.is_updating = False
        for item in reversed(rs.entry_list):
            rs.temp_layout.add_widget(item)

        rs.budgetUIs.clear()
        if rs.budget_groups.get(baf.rtrn_disp()) is not None:
            for key, value in rs.budget_groups.get(baf.rtrn_disp()).budgets.items(): rs.budgetUIs[key] = BudgetUI([x for x in rs.dft_ctg if x.name == key][0], value)
        rs.main_widgets['budget_scroll'].is_updating = True
        rs.main_widgets['budget_scroll'].clear_widgets()
        rs.main_widgets['budget_scroll'].is_updating = False
        for item in reversed(rs.budgetUIs.values()):
            rs.main_widgets['budget_scroll'].add_widget(item)
            item.amount_spent += 1
        rs.main_widgets['budget_scroll'].add_widget(rs.main_widgets['budget_scroll'].add_budget)

class AccountBox(FloatLayout):
    balance = NumericProperty(float((sum([x.value for x in rs.dft_acc]))))
    expense = NumericProperty(-1 * float(sum([x.entry.amount for x in rs.entry_list if x.entry.mode == False])))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Image(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                color=(0, 60/255, 64/255, 63/100))
        self.float_balance = 0.0
        self.float_expense = 0.0

        #rs.main_widgets['acc_bal_exp'] = self

        self.balance_label = Label(text=f"Balance:",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.26, 'center_y': 0.75},
                                   halign='center', font_size=16)
        self.expense_label = Label(text=f"Expenses:",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.75, 'center_y': 0.75},
                                   halign='center', font_size=16)
        self.balance_int = Label(text=f"{baf.sign_setter(self.float_balance)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.balance, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                   text_size=(int(Config.get('graphics', 'width'))/3.5, None),
                                   pos_hint={'center_x': 0.25, 'center_y': 0.25},
                                   color=baf.color_setter(self.float_balance),
                                   halign='center', font_size=16)
        self.bind(balance=self.update_text)
        self.expense_int = Label(text=f"{baf.sign_setter(self.float_expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.expense, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                   text_size=(int(Config.get('graphics', 'width'))/3.5, None),
                                   pos_hint={'center_x': 0.75, 'center_y': 0.25},
                                   color=baf.color_setter(self.float_expense),
                                   halign='center', font_size=16)
        self.bind(expense=self.update_text)

        self.add_widget(self.background)
        self.add_widget(self.balance_label)
        self.add_widget(self.expense_label)
        self.add_widget(self.balance_int)
        self.add_widget(self.expense_int)

    def update_text(self, *args):
        self.balance = float((sum([x.value for x in rs.dft_acc])))
        self.expense = float(-1 * sum([x.entry.amount for x in rs.entry_list if x.entry.mode == False]))

        self.float_balance = self.balance
        self.float_expense = self.expense
        self.balance_int.text = f"{baf.sign_setter(self.float_balance)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.float_balance, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.balance_int.color = baf.color_setter(self.float_balance)
        self.expense_int.text = f"{baf.sign_setter(self.float_expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.expense, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.expense_int.color = baf.color_setter(self.float_expense)

class AccountBoxBudget(FloatLayout):
    budget_total = NumericProperty(float((sum([x.budget_amount for x in rs.budgetUIs.values()]))))
    expense = NumericProperty(-1 * float(sum([x.entry.amount for x in rs.entry_list if x.entry.mode == False])))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Image(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                color=(0, 60/255, 64/255, 63/100))
        self.float_total = float((sum([x.budget_amount for x in rs.budgetUIs.items()])))
        self.float_expense = float((sum([x.value for x in rs.dft_acc])))
        #print(float((sum([x.value for x in rs.dft_acc]))))

        self.budget_label = Label(text=f"Total Budget:",
                                   text_size=(int(Config.get('graphics', 'width'))/3, None),
                                   pos_hint={'center_x': 0.26, 'center_y': 0.75},
                                   halign='center', font_size=16)
        self.expense_label = Label(text=f"Expenses:",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.75, 'center_y': 0.75},
                                   halign='center', font_size=16)
        self.budget_int = Label(text=f"{baf.sign_setter(self.float_total)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.budget_total)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.25, 'center_y': 0.25},
                                   color=baf.color_setter(self.float_total),
                                   halign='center', font_size=16)
        self.bind(budget_total=self.update_text)
        self.expense_int = Label(text=f"{baf.sign_setter(self.float_expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.75, 'center_y': 0.25},
                                   color=baf.color_setter(self.float_expense),
                                   halign='center', font_size=16)
        self.bind(expense=self.update_text)

        self.add_widget(self.background)
        self.add_widget(self.budget_label)
        self.add_widget(self.expense_label)
        self.add_widget(self.budget_int)
        self.add_widget(self.expense_int)

    def update_text(self, *args):
        self.budget_total = float((sum([x.budget_amount for x in rs.budgetUIs.values()])))
        self.expense = -1 * float(sum([x.entry.amount for x in rs.entry_list if x.entry.mode == False]))

        #print(float((sum([x.value for x in rs.dft_acc]))))
        self.float_total = self.budget_total
        self.float_expense = self.expense
        self.budget_int.text = f"{baf.sign_setter(self.float_total)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.float_total)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.budget_int.color = baf.color_setter(self.float_total)
        self.expense_int.text = f"{baf.sign_setter(self.float_expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.expense_int.color = baf.color_setter(self.float_expense)

class BudgetScroll(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.child_count = 0
        self.is_updating = False
        self.add_popup = None

        self.add_budget = Button(background_color=(0, 0, 0, 0), size_hint=(0.7, 0.7))
        self.budget_img = Image(source="Images/AddNewBudget.png", size_hint=(1, 1),
                                         pos_hint={'center_x':0.5, 'top':1}, color=(1, 1, 1, 0.8))
        self.budget_text = Label(text="Add new budget")
        self.add_budget.bind(pos=self.fix_img_pos, size=self.fix_img_pos, on_press=self.open_popup)
        self.add_budget.add_widget(self.budget_img)
        self.add_budget.add_widget(self.budget_text)
        self.add_widget(self.add_budget)

    def fix_img_pos(self, *args):
        self.budget_img.pos = self.add_budget.pos
        self.budget_text.pos = self.add_budget.pos
        self.budget_img.size = self.add_budget.size
        self.budget_text.size = self.add_budget.size
        self.budget_img.width *= 1
        self.budget_img.height *= 1
        #self.budget_img.x += int(Config.get('graphics', 'width')) / 75
        #self.budget_img.y -= int(Config.get('graphics', 'height')) / 120
        #self.budget_text.y += int(Config.get('graphics', 'height')) / 140
        self.budget_text.x += int(Config.get('graphics', 'width')) / 16

    def add_widget(self, widget, mode: bool = False, *args, **kwargs):
        super().add_widget(widget, *args, **kwargs)
        if not mode: self.on_child_change(self, None)
        scroll_view_main.update_from_scroll()

    def remove_widget(self, widget, mode: bool = False, *args, **kwargs):
        super().remove_widget(widget, *args, **kwargs)
        if not mode: self.on_child_change(self, None)
        scroll_view_main.update_from_scroll()

    def on_child_change(self, instance, value):
        if self.is_updating: return

        self.is_updating = True
        self.child_count = len(self.children)
        self.size_hint_y = self.child_count * rs.view_height / 500
        self.do_layout()
        self.is_updating = False

    def open_popup(self, *args):
        rs.temp_ctg_budget = None
        temp_popup = Popup(title="Add Budget:", content=AddBudget(), size_hint=(0.9, 0.6))
        self.add_popup = temp_popup
        temp_popup.open()

    def close_popup(self, *args):
        self.add_popup.dismiss()

    @staticmethod
    def open_info_popup(budget, *args):
        temp_popup = Popup(title="Budget Info", content=BudgetInfoPopup(budget), size_hint=(0.8, 0.5))
        temp_popup.content.popup = temp_popup
        temp_popup.open()

class BudgetUI(FloatLayout):
    amount_spent = NumericProperty(0.0)

    def __init__(self, ctg: rs.Category, amount: float, **kwargs):
        super().__init__(**kwargs)

        self.ctg = ctg
        self.budget_amount = amount
        self.amount_spent = float(sum([x.entry.amount for x in rs.entry_list if x.entry.ctg == self.ctg]))
        self.fill_width = (self.amount_spent / self.budget_amount) * 210 if self.amount_spent < self.budget_amount else 210

        self.height = rs.view_height
        self.icon = Image(source=self.ctg.icon_path, pos_hint={'x':-0.165, 'center_y':0.75},
                          size_hint=(0.5, 0.5))
        self.category = Label(text=f"{self.ctg.name}",
                              text_size=(int(Config.get('graphics', 'width'))/2, None),
                              halign='left',
                              pos_hint={'center_x':0.39, 'center_y':0.9},
                              font_size=16)
        self.progress_bar_fill = Image(color=((127+(64*(self.amount_spent/self.budget_amount)))/255, (199+(-169*(self.amount_spent/self.budget_amount)))/255, (127+(-97*(self.amount_spent/self.budget_amount)))/255, 1),
                                       size_hint=(None, None), height=14,
                                       width=self.fill_width, pos_hint={'x':0.194, 'center_y':0.32})
        self.progress_bar_img_b = Image(color=(1, 1, 1, 1), size_hint=(None, None),
                                      height=17, width=213, pos_hint={'center_x':0.457, 'center_y':0.32})
        self.progress_bar_img_f = Image(color=(22 / 255, 22 / 255, 22 / 255, 1), size_hint=(None, None),
                                        height=14, width=210, pos_hint={'center_x': 0.457, 'center_y':0.32})
        self.progress_bar_fill.bind()
        self.amount = Label(text=f"Budget: {dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.budget_amount, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                            text_size=(int(Config.get('graphics', 'width')) / 2, None),
                            pos_hint={'center_x': 0.77, 'center_y': 0.9},
                            halign='right', shorten=True,
                            font_size=16)

        self.remaining = Label(text=f"Remaining: {dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.budget_amount - self.amount_spent, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                            text_size=(int(Config.get('graphics', 'width')) / 1.5, None),
                            pos_hint={'center_x': 0.458, 'center_y': 0.5},
                            halign='left', shorten=True,
                            font_size=16)
        self.spent = Label(text=f"Spent: {dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.amount_spent, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                               text_size=(int(Config.get('graphics', 'width')) / 1.5, None),
                               pos_hint={'center_x': 0.458, 'center_y': 0.68},
                               halign='left', shorten=True,
                               font_size=16)
        self.exceeded = Label(text=f"Budget Exceeded",
                              text_size=(int(Config.get('graphics', 'width')) / 2, None),
                              halign='left', color=(1, 1, 1, 0),
                              pos_hint={'center_x': 0.39, 'center_y': 0.18},
                              font_size=12)
        self.percentage_img = Image(color=(0, 60/255, 64/255, 80/100), size_hint=(0.18, 0.54),
                                    pos_hint={'x':0.77, 'top':0.7})
        self.percentage_img_overlay = Image(color=(0, 116/255, 129/255, 80/100), size_hint=(0.18, 0.01),
                                            pos_hint={'x': 0.77, 'y': 0.16})
        self.percentage_txt = Label(text=f"100%", text_size=(int(Config.get('graphics', 'width')) / 4, None),
                                    pos_hint={'center_x': 0.86, 'center_y': 0.45},
                                    font_size=22, halign='center')
        self.bar = Image(pos_hint={'x': 0.05, 'center_y': 0.1},
                         size_hint=(0.9, 0.02), color=(88/255, 88/255, 88/255, 1))
        self.overlay_button = Button(background_color=(0, 0, 0, 0))
        self.overlay_button.bind(on_press=self.show_info, pos=self.update_pos, size=self.update_pos)
        self.bind(amount_spent=self.update_bar)
        self.add_widget(self.icon)
        self.add_widget(self.category)
        self.add_widget(self.progress_bar_img_b)
        self.add_widget(self.progress_bar_img_f)
        self.add_widget(self.progress_bar_fill)
        self.add_widget(self.amount)
        self.add_widget(self.remaining)
        self.add_widget(self.spent)
        self.add_widget(self.exceeded)
        self.add_widget(self.percentage_img)
        self.add_widget(self.percentage_img_overlay)
        self.add_widget(self.percentage_txt)
        self.add_widget(self.bar)
        self.add_widget(self.overlay_button)

    def show_info(self, *args):
        #rs.temp_layout.open_info_popup(self.entry, self)
        rs.main_widgets['budget_scroll'].open_info_popup(self)

    def update_pos(self, *args):
        self.overlay_button.pos = self.pos
        self.overlay_button.size = self.size

    def update_bar(self, *args): #This being triggered twice is NOT a bug, bind code is affected as this code changes the property again
        self.amount_spent = float(sum([x.entry.amount for x in rs.entry_list if x.entry.ctg == self.ctg]))
        self.progress_bar_fill.width = (self.amount_spent / self.budget_amount) * 210 if self.amount_spent < self.budget_amount else 210 #The width of the bar
        self.amount.text = f"Budget: {dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.budget_amount, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.remaining.text = f"Remaining: {dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.budget_amount - self.amount_spent, 2)) if self.budget_amount - self.amount_spent > 0 else 0}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.spent.text = f"Spent: {dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(round(self.amount_spent, 2))}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.percentage_txt.text = f"{(self.amount_spent*100)/self.budget_amount:.1f}%" if self.budget_amount >= self.amount_spent else "100%"
        #self.remaining.color = baf.color_setter(self.budget_amount-self.amount_spent, dft_more=(1, 1, 1, 1), dft_less=(246 / 255, 68 / 255, 61 / 255, 1))
        self.progress_bar_fill.color = ((127+(119*(self.amount_spent/self.budget_amount)))/255, (199+(-131*(self.amount_spent/self.budget_amount)))/255, (127+(-66*(self.amount_spent/self.budget_amount)))/255, 1)
        self.exceeded.color = (246 / 255, 68 / 255, 61 / 255, 1) if self.budget_amount - self.amount_spent < 0 else (0, 0, 0, 0)
        self.percentage_img_overlay.size_hint_y = 0.54 * (self.amount_spent/self.budget_amount) if self.budget_amount >= self.amount_spent else 0.54
        self.percentage_img_overlay.color = (0, 116/255, 129/255, 80/100) if self.budget_amount >= self.amount_spent else (246 / 255, 68 / 255, 61 / 255, 8/10)

class BudgetInfoPopup(FloatLayout):
    def __init__(self, budget: BudgetUI, **kwargs):
        super().__init__(**kwargs)
        self.budget = budget
        self.popup = None

        self.banner = Image(color=baf.color_setter(-1 if self.budget.amount_spent > self.budget.budget_amount else 1, dft_less=(141 / 255, 10 / 255, 10 / 255, 1),
                                                   dft_more=(40/255, 40/255, 40/255, 1)),
                            pos_hint={'center_x': 0.5, 'top': 1.18},
                            size_hint=(1.055, None), height=80)

        self.title = Label(text=self.budget.ctg.name, pos_hint={'center_x': 0.5, 'top': 1.25},
                           size_hint=(1, None), width=self.width,
                           font_size=24)

        self.icon = Image(source=self.budget.ctg.icon_path, pos_hint={'center_x':0.5, 'top':1.03},
                          size_hint=(0.25, 0.25))

        self.error_text = Label(text="Invalid amount!", size_hint=(0.5, 0.1),
                                halign="center", pos_hint={'top': 0.81, 'x': 0.5},
                                font_size=17, color=(1, 0.2, 0.2, 0))

        self.budget_text = Label(text="Change Budget:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top': 0.825, 'x': 0.035},
                                 font_size=17)
        self.budget_text.bind(size=self.budget_text.setter('text_size'))

        self.budget_box = TextInput(size_hint=(0.935, 0.133), pos_hint={'top': 0.7, 'x': 0.035},
                                    multiline=False, input_type='number',
                                    padding_y=(10, 5), halign='center',
                                    background_color=(22 / 255, 22 / 255, 22 / 255, 1),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                    padding_x=(10, 10), text=str(self.budget.budget_amount))
        self.budget_box.bind(focus=self.on_focus)

        self.currency_text = Label(text=rs.dft_currencies[rs.currency_choice][0], size_hint=(0.1, 0.1),
                                   pos_hint={'top': 0.685,
                                             'x': baf.align_currency_text(rs.dft_currencies[rs.currency_choice][1],
                                                                          place='text_box')},
                                   font_size=17)

        self.confirm_edit_button = Button(size_hint=(0.935, 0.1), pos_hint={'top': 0.55, 'center_x': 0.5},
                                     text="Change Budget(s)")

        self.confirm_edit_button.bind(on_press=self.edit_func)

        self.tick_box_img_b = Image(color=(1, 1, 1, 1), size_hint=(None, None),
                                    height=32, width=32, pos_hint={'center_x': 0.15, 'center_y': 0.28})
        self.tick_box_img_f = Image(color=(22 / 255, 22 / 255, 22 / 255, 1), size_hint=(None, None),
                                    height=29, width=29, pos_hint={'center_x': 0.15, 'center_y': 0.28})
        self.tick_box = ToggleButton(size_hint=(None, None), background_color=(0, 0, 0, 0),
                                     height=29, width=29, pos_hint={'center_x': 0.15, 'center_y': 0.28})
        self.tick_box_img = Image(source="Images/Tick.png", size_hint=(None, None),
                                  height=29, width=29, pos_hint={'center_x': 0.15, 'center_y': 0.28},
                                  color=(1, 1, 1, 0))
        self.tick_box.bind(state=self.do_toggle)

        self.repeat_label_top = Label(text="Apply changes to the following", size_hint=(0.5, 0.1),
                                      text_size=(int(Config.get('graphics', 'width')) / 2.2, None),
                                      halign="center", pos_hint={'top': 0.42, 'center_x': 0.55},
                                      font_size=17)
        self.repeat_box = TextInput(size_hint=(0.2, 0.08), pos_hint={'top': 0.30, 'center_x': 0.55},
                                    multiline=False, input_type='number',
                                    padding_y=(0, 2), halign='center',
                                    background_color=(22 / 255, 22 / 255, 22 / 255, 1),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                    padding_x=(10, 10), text="0")
        self.repeat_box.bind(focus=self.on_focus_rpt)
        self.repeat_label_bottom = Label(text="instances of this budget. (max 12)", size_hint=(0.5, 0.1),
                                         text_size=(int(Config.get('graphics', 'width')) / 2.2, None),
                                         halign="center", pos_hint={'top': 0.22, 'center_x': 0.55},
                                         font_size=17)

        self.confirm_popup = Popup(title="Are you sure?", content=ConfirmPopup(self.del_func), size_hint=(0.6, 0.2))

        self.confirm_delete_button = Button(size_hint=(0.935, 0.1), pos_hint={'top': 0.05, 'center_x': 0.5},
                                          text="Delete Budget(s)")

        self.confirm_delete_button.bind(on_press=self.del_button)

        self.error_text_repeat = Label(text="Please type a valid integer!", size_hint=(0.5, 0.1),
                                       halign="center", pos_hint={'top': 0.13, 'center_x': 0.55},
                                       font_size=17, color=(1, 0.2, 0.2, 0))

        self.add_widget(self.banner)
        self.add_widget(self.title)
        self.add_widget(self.icon)
        self.add_widget(self.error_text)
        self.add_widget(self.budget_text)
        self.add_widget(self.budget_box)
        self.add_widget(self.currency_text)
        self.add_widget(self.confirm_edit_button)
        self.add_widget(self.tick_box_img_b)
        self.add_widget(self.tick_box_img_f)
        self.add_widget(self.tick_box)
        self.add_widget(self.tick_box_img)
        self.add_widget(self.repeat_label_top)
        self.add_widget(self.repeat_label_bottom)
        self.add_widget(self.repeat_box)
        self.add_widget(self.confirm_delete_button)
        self.add_widget(self.error_text_repeat)

    def edit_func(self, *args):
        try:
            self.budget.budget_amount = float(self.budget_box.text)
            if self.budget.budget_amount <= 0 or str(self.budget.budget_amount).split(".")[1].__len__() > 2: raise ValueError
            self.budget.amount_spent += 1
            rs.budget_groups[baf.rtrn_disp()].budgets[self.budget.ctg.name] = float(self.budget_box.text)

            if self.tick_box.state == 'down':
                if self.repeat_box.text.isdigit() == False or not 12 >= int(self.repeat_box.text) > 0:
                    raise rs.TickBoxValueError
                repeat_amount = int(self.repeat_box.text)

                for x in range(1, repeat_amount):
                    temp_month = (rs.disp_month + x)
                    temp_year = int(datetime.date.today().year) + (temp_month // 12)
                    t_date = datetime.date(temp_year, temp_month % 12 + 1, 1)
                    if rs.budget_groups.get(t_date) is None:
                        continue
                    if rs.budget_groups.get(t_date).budgets.get(self.budget.ctg.name) is not None:
                        rs.budget_groups[t_date].budgets[self.budget.ctg.name] = self.budget.budget_amount
            baf.save_entry_groups()
            self.error_text.color = (1, 0.2, 0.2, 0)
            self.error_text_repeat.color = (1, 0.2, 0.2, 0)
            self.budget_box.foreground_color = (1, 1, 1, 1)
            self.repeat_box.foreground_color = (1, 1, 1, 1)
            self.popup.dismiss()
        except ValueError:
            self.error_text.color = (1, 0.2, 0.2, 1)
            self.budget_box.foreground_color = (1, 0.2, 0.2, 1)
        except rs.TickBoxValueError:
            self.error_text_repeat.color = (1, 0.2, 0.2, 1)
            self.repeat_box.foreground_color = (1, 0.2, 0.2, 1)

    def del_button(self, *args):
        try:
            if self.repeat_box.text.isdigit() == False or not 12 >= int(self.repeat_box.text) > 0:
                raise rs.TickBoxValueError
            self.error_text_repeat.color = (1, 0.2, 0.2, 0)
            self.repeat_box.foreground_color = (1, 1, 1, 1)
            self.confirm_popup.open()
        except rs.TickBoxValueError:
            self.error_text_repeat.color = (1, 0.2, 0.2, 1)
            self.repeat_box.foreground_color = (1, 0.2, 0.2, 1)
    def del_func(self, *args):
        try:
            rs.main_widgets['budget_scroll'].remove_widget(self.budget)
            del rs.budget_groups[baf.rtrn_disp()].budgets[self.budget.ctg.name]
            if self.tick_box.state == 'down':
                if self.repeat_box.text.isdigit() == False or not 12 >= int(self.repeat_box.text) > 0:
                    raise rs.TickBoxValueError
                repeat_amount = int(self.repeat_box.text)

                for x in range(1, repeat_amount):
                    temp_month = (rs.disp_month + x)
                    temp_year = int(datetime.date.today().year) + (temp_month // 12)
                    t_date = datetime.date(temp_year, temp_month % 12 + 1, 1)
                    if rs.budget_groups.get(t_date) is None:
                        continue
                    if rs.budget_groups.get(t_date).budgets.get(self.budget.ctg.name) is not None:
                        del rs.budget_groups[t_date].budgets[self.budget.ctg.name]
            baf.save_entry_groups()
            self.error_text_repeat.color = (1, 0.2, 0.2, 0)
            self.repeat_box.foreground_color = (1, 1, 1, 1)
            self.confirm_popup.dismiss()
            self.popup.dismiss()
        except rs.TickBoxValueError:
            self.error_text_repeat.color = (1, 0.2, 0.2, 1)
            self.repeat_box.foreground_color = (1, 0.2, 0.2, 1)

    def do_toggle(self, instance, value):
        if value == 'down':
            self.tick_box_img.color = (1, 1, 1, 1)
        else:
            self.tick_box_img.color = (1, 1, 1, 0)

    def on_focus(self, instance, value):
        if value:
            self.budget_box.foreground_color = (1, 1, 1, 1)

    def on_focus_rpt(self, instance, value):
        if value:
            self.repeat_box.foreground_color = (1, 1, 1, 1)

class AddBudget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.budget_text = Label(text="Budget:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top': 1.025, 'x': 0.035},
                                 font_size=17)
        self.error_text = Label(text="Please enter a valid amount!", size_hint=(0.5, 0.1),
                                halign="center", pos_hint={'top': 1.0, 'x': 0.4},
                                font_size=17, color=(1, 0.2, 0.2, 0))
        self.budget_text.bind(size=self.budget_text.setter('text_size'))
        self.budget_box = TextInput(size_hint=(0.935, 0.133), pos_hint={'top': 0.9, 'x': 0.035},
                                    multiline=False, input_type='number',
                                    padding_y=(15, 5), halign='center',
                                    background_color=(22 / 255, 22 / 255, 22 / 255, 1),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                    padding_x=(10, 10), text="0")
        self.budget_box.bind(focus=self.on_focus)

        self.currency_text = Label(text=rs.dft_currencies[rs.currency_choice][0], size_hint=(0.1, 0.1),
                                   pos_hint={'top': 0.885, 'x': baf.align_currency_text(rs.dft_currencies[rs.currency_choice][1], place='text_box')},
                                   font_size=17)

        self.ctg_text = Label(text="Category:", size_hint=(1, 0.1),
                              halign="left", pos_hint={'top': 0.78, 'x': 0.035},
                              font_size=17)
        self.ctg_text.bind(size=self.ctg_text.setter('text_size'))

        self.ctg_scroll = ScrollView(do_scroll_x=True,
                                     do_scroll_y=False, size_hint=(0.935, 0.22),
                                     pos_hint={'top': 0.65, 'x': 0.035})

        self.ctg_scroll_ui = CtgBudget(size_hint_x=self.ctg_scroll.width / (rs.dft_ctg.__len__() ** 2))
        self.ctg_scroll_ui.bind(minimum_width=self.ctg_scroll_ui.setter('width'))
        self.ctg_scroll.add_widget(self.ctg_scroll_ui)

        self.error_text_ctg = Label(text="Please choose a category!", size_hint=(0.5, 0.1),
                                halign="center", pos_hint={'top': 0.76, 'x': 0.4},
                                font_size=17, color=(1, 0.2, 0.2, 0))

        self.tick_box_img_b = Image(color=(1, 1, 1, 1), size_hint=(None, None),
                                        height=32, width=32, pos_hint={'center_x': 0.15, 'center_y': 0.25})
        self.tick_box_img_f = Image(color=(22 / 255, 22 / 255, 22 / 255, 1), size_hint=(None, None),
                                        height=29, width=29, pos_hint={'center_x': 0.15, 'center_y': 0.25})
        self.tick_box = ToggleButton(size_hint=(None, None), background_color=(0, 0, 0, 0),
                                     height=29, width=29, pos_hint={'center_x': 0.15, 'center_y': 0.25})
        self.tick_box_img = Image(source="Images/Tick.png", size_hint=(None, None),
                                  height=29, width=29, pos_hint={'center_x': 0.15, 'center_y': 0.25},
                                  color=(1, 1, 1, 0))
        self.tick_box.bind(state=self.do_toggle)

        self.repeat_label_top = Label(text="Repeat this budget for", size_hint=(0.5, 0.1),
                                halign="center", pos_hint={'top': 0.38, 'center_x': 0.55},
                                font_size=17)
        self.repeat_box = TextInput(size_hint=(0.2, 0.08), pos_hint={'top': 0.29, 'center_x': 0.55},
                                    multiline=False, input_type='number',
                                    padding_y=(5, 5), halign='center',
                                    background_color=(22 / 255, 22 / 255, 22 / 255, 1),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                    padding_x=(10, 10), text="0")
        self.repeat_box.bind(focus=self.on_focus_rpt)
        self.repeat_label_bottom = Label(text="month(s). (max 12)", size_hint=(0.5, 0.1),
                                      halign="center", pos_hint={'top': 0.22, 'center_x': 0.55},
                                      font_size=17)

        self.error_text_repeat = Label(text="Please type a valid integer!", size_hint=(0.5, 0.1),
                                    halign="center", pos_hint={'top': 0.17, 'center_x': 0.55},
                                    font_size=17, color=(1, 0.2, 0.2, 0))

        self.confirm_button = Button(size_hint=(0.935, 0.1), pos_hint={'top': 0.05, 'center_x': 0.5},
                                     text="Confirm")
        self.confirm_button.bind(on_press=self.callback)

        self.add_widget(self.budget_text)
        self.add_widget(self.error_text)
        self.add_widget(self.budget_box)
        self.add_widget(self.currency_text)
        self.add_widget(self.ctg_text)
        self.add_widget(self.ctg_scroll)
        self.add_widget(self.error_text_ctg)
        self.add_widget(self.tick_box_img_b)
        self.add_widget(self.tick_box_img_f)
        self.add_widget(self.tick_box)
        self.add_widget(self.tick_box_img)
        self.add_widget(self.repeat_label_top)
        self.add_widget(self.repeat_label_bottom)
        self.add_widget(self.repeat_box)
        self.add_widget(self.error_text_repeat)
        self.add_widget(self.confirm_button)

    def on_focus(self, instance, value):
        if value:
            self.budget_box.foreground_color = (1, 1, 1, 1)

    def on_focus_rpt(self, instance, value):
        if value:
            self.repeat_box.foreground_color = (1, 1, 1, 1)

    def do_toggle(self, instance, value):
        if value == 'down':
            self.tick_box_img.color = (1, 1, 1, 1)
        else:
            self.tick_box_img.color = (1, 1, 1, 0)

    def callback(self, *args):
        try:
            t_budget = float(self.budget_box.text)
            if t_budget <= 0 or str(t_budget).split(".")[1].__len__() > 2: raise ValueError
            if rs.temp_ctg_budget is None or rs.temp_ctg_budget.name in rs.budgetUIs.keys(): raise rs.CategoryError
            t_ctg = rs.temp_ctg_budget
            t_budget_ui = BudgetUI(t_ctg, t_budget)
            rs.budgetUIs[t_ctg.name] = t_budget_ui
            rs.main_widgets['acc_bdg_exp'].update_text()
            if rs.budget_groups.get(baf.rtrn_disp()) is None:
                rs.budget_groups[baf.rtrn_disp()] = rs.BudgetGroup(baf.rtrn_disp())
            if rs.budget_groups.get(baf.rtrn_disp()).budgets.get(t_ctg.name) is None:
                rs.budget_groups[baf.rtrn_disp()].budgets[t_ctg.name] = t_budget
            if self.tick_box.state == 'down':
                if self.repeat_box.text.isdigit() == False or not 12 >= int(self.repeat_box.text) > 0:
                    raise rs.TickBoxValueError
                repeat_amount = int(self.repeat_box.text)

                for x in range(1, repeat_amount):
                    temp_month = (rs.disp_month + x)
                    temp_year = int(datetime.date.today().year) + (temp_month // 12)
                    t_date = datetime.date(temp_year, temp_month % 12 + 1, 1)
                    if rs.budget_groups.get(t_date) is None:
                        rs.budget_groups[t_date] = rs.BudgetGroup(t_date)
                    if rs.budget_groups.get(t_date).budgets.get(t_ctg.name) is None:
                        rs.budget_groups[t_date].budgets[t_ctg.name] = t_budget

            baf.save_entry_groups()
            rs.main_widgets['budget_scroll'].add_widget(t_budget_ui)
            rs.main_widgets['budget_scroll'].children = rs.main_widgets['budget_scroll'].children[1:] + [rs.main_widgets['budget_scroll'].children[0]]
            t_budget_ui.amount_spent += 1
            self.error_text.color = (1, 0.2, 0.2, 0)
            self.error_text_ctg.color = (1, 0.2, 0.2, 0)
            self.budget_box.foreground_color = (1, 1, 1, 1)
            self.error_text_repeat.color = (1, 0.2, 0.2, 0)
            self.repeat_box.foreground_color = (1, 1, 1, 1)
            self.ctg_scroll_ui.update_buttons()
            rs.main_widgets['budget_scroll'].close_popup()
        except ValueError:
            self.error_text.color = (1, 0.2, 0.2, 1)
            self.budget_box.foreground_color = (1, 0.2, 0.2, 1)
        except rs.CategoryError:
            self.error_text_ctg.color = (1, 0.2, 0.2, 1)
        except rs.TickBoxValueError:
            self.error_text_repeat.color = (1, 0.2, 0.2, 1)
            self.repeat_box.foreground_color = (1, 0.2, 0.2, 1)

class CtgBudget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.child_buttons = []
        self.remaining_ctg = [x for x in rs.dft_ctg if x.name not in rs.budgetUIs.keys()]

        with self.canvas.before:
            Color(22/255, 22/255, 22/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.rows = 1
        self.spacing = 1
        self.padding = [0, 0, 0, 0]
        #self.width = rs.ctg_view_width
        for i in range(rs.dft_ctg.__len__()):
            a = CtgButtonBudget(rs.dft_ctg[i], self, group="ctg_budget")
            if a.ctg not in self.remaining_ctg:
                a.disabled = True
                a.img.color = (0.7, 0.7, 0.7, 0.7)
            self.child_buttons.append(a)
            self.add_widget(a)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_buttons(self, *args):
        self.clear_widgets()
        self.child_buttons.clear()
        self.remaining_ctg = [x for x in rs.dft_ctg if x.name not in rs.budgetUIs.keys()]

        for i in range(rs.dft_ctg.__len__()):
            a = CtgButtonBudget(rs.dft_ctg[i], self, group="ctg_budget")
            if a.ctg not in self.remaining_ctg:
                a.disabled = True
                a.img.color = (0.2, 0.2, 0.2, 0.4)
            self.child_buttons.append(a)
            self.add_widget(a)

class CtgButtonBudget(ToggleButton):
    def __init__(self, ctg: rs.Category, parent, **kwargs):
        super().__init__(**kwargs)
        self.ctg = ctg
        self.parent_widget = parent
        self.background_color = (0, 0, 0, 0)
        self.background_down = 'white'

        self.img = Image(source=self.ctg.icon_path)
        self.name = Label(text=self.ctg.name, font_size=14)
        self.bind(size=self._update_image_pos, pos=self._update_image_pos, state=self._state_change)
        self.add_widget(self.img)
        self.add_widget(self.name)

    def _update_image_pos(self, *args):
        self.img.size = self.size
        self.img.pos = self.pos
        self.img.width *= 7/9
        self.img.height *= 7/9
        self.img.y += 16
        self.img.x += 9
        self.name.pos = self.pos
        self.name.y -= 40
        self.name.x -= 5

    def _state_change(self, instance, value):
        if value == 'down':
            self.background_color = (200/255, 200/255, 200/255, 50/100)
            rs.temp_ctg_budget = self.ctg
        else:
            self.background_color = (0, 0, 0, 0)

    def _do_press(self, *args):
        if (not self.allow_no_selection and
                self.group and self.state == 'down'):
            return
        self._release_group(self)
        if self.state == 'normal': self.state = 'down'
        else:
            if sum(x.state == 'down' for x in self.parent_widget.child_buttons) == 1: return
            self.state = 'normal'

#region Records
class MainInterface(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.child_count = 0
        self.is_updating = False

    def add_widget(self, widget, mode: bool = False, *args, **kwargs):
        super().add_widget(widget, *args, **kwargs)
        if not mode: self.on_child_change(self, None)
        rs.main_widgets['acc_bal_exp'].update_text()
        scroll_view_main.update_from_scroll()

    def remove_widget(self, widget, mode: bool = False, *args, **kwargs):
        super().remove_widget(widget, *args, **kwargs)
        if not mode: self.on_child_change(self, None)
        rs.main_widgets['acc_bal_exp'].update_text()
        scroll_view_main.update_from_scroll()

    def on_child_change(self, instance, value):
        if self.is_updating: return

        self.is_updating = True
        self.check_dates(self.children[0].entry)
        self.child_count = len(self.children)
        self.size_hint_y = self.child_count * rs.view_height / 700
        self.do_layout()
        self.is_updating = False

    def check_dates(self, added_entry: rs.Entry, *args):
        if len(self.children) == 1: #The first case is important as otherwise we would get an index error.
            self.add_widget(DateEntryUI(added_entry), True)
            self.children = [self.children[1]] + [self.children[0]]
            return
        if added_entry.date < self.children[1].entry.date: #Add to end with older dates
            self.add_widget(DateEntryUI(added_entry), True)
            self.children = [self.children[1]] + [self.children[0]] + self.children[2:]
        elif self.children[-1].entry.date >= added_entry.date >= self.children[0].entry.date: #Existing dates or dates in between
            for x in reversed(range((self.children.__len__()))):
                if added_entry.date == self.children[x].entry.date:
                    self.children = self.children[1:x] + [self.children[0]] + self.children[x:]
                    break
                elif added_entry.date > self.children[x].entry.date:
                    self.add_widget(DateEntryUI(added_entry), True)
                    self.children = self.children[2:x+2] + [self.children[1], self.children[0]] + self.children[x+2:]
                    break

        elif self.children[-1].entry.date < added_entry.date: #Add to beginning
            self.add_widget(DateEntryUI(added_entry), True)
            self.children = self.children[2:] + [self.children[1]] + [self.children[0]]
        else:
            raise rs.IndexMissingError(f"An index that is being used is not defined. This may cause problems.")

    @staticmethod
    def open_info_popup(entry: rs.Entry, entry_ui, *args):
        temp_popup = Popup(title="Entry Info", content=EntryInfoPopup(entry, entry_ui), size_hint=(0.8, 0.5))
        rs.temp_popup = temp_popup
        temp_popup.open()

class EntryUI(FloatLayout):
    def __init__(self, entry: rs.Entry, **kwargs):
        super().__init__(**kwargs)

        self.entry = entry

        self.height = rs.view_height
        self.icon = Image(source=entry.ctg.icon_path, pos_hint={'x':-0.25, 'center_y':0.5},
                          size_hint=(0.7, 0.7))
        self.category = Label(text=f"{entry.ctg.name}",
                                 text_size=(int(Config.get('graphics', 'width'))/2, None),
                                 pos_hint={'center_x':0.4, 'center_y':0.7})
        self.account_icon = Image(source=entry.acc.icon_path, pos_hint={'x':0.03, 'center_y':0.35},
                                  size_hint=(0.4, 0.4))
        self.account_text = Label(text=f"{entry.acc.name}",
                              text_size=(int(Config.get('graphics', 'width')), None),
                              pos_hint={'center_x': 0.68, 'center_y': 0.35},
                              font_size=15)
        self.amount = Label(text=f"{'-' if entry.mode == False else '+'}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{entry.amount}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                            text_size=(int(Config.get('graphics', 'width')), None),
                            pos_hint={'center_x': 0.52, 'center_y': 0.5},
                            halign='right', color=(191/255, 30/255, 30/255, 1) if entry.mode == False else (127/255, 199/255, 127/255, 1),
                            font_size=22)
        self.bar = Image(pos_hint={'x': 0.2, 'center_y': 0.1},
                         size_hint=(0.75, 0.02), color=(88/255, 88/255, 88/255, 1))
        self.overlay_button = Button(background_color=(0, 0, 0, 0))
        self.overlay_button.bind(on_press=self.show_info, pos=self.update_pos, size=self.update_pos)
        self.add_widget(self.icon)
        self.add_widget(self.category)
        self.add_widget(self.account_icon)
        self.add_widget(self.account_text)
        self.add_widget(self.amount)
        self.add_widget(self.bar)
        self.add_widget(self.overlay_button)

    def show_info(self, *args):
        rs.temp_layout.open_info_popup(self.entry, self)

    def update_pos(self, *args):
        self.overlay_button.pos = self.pos
        self.overlay_button.size = self.size

class EntryInfoPopup(FloatLayout):
    def __init__(self, entry: rs.Entry, entry_ui, **kwargs):
        super().__init__(**kwargs)
        self.entry = entry
        self.entry_ui = entry_ui
        self.a = 0.2 if not self.entry.mode else 0.8
        self.b = 0.8 if not self.entry.mode else 0.2

        self.banner = Image(color=baf.color_setter(1 if self.entry.mode else -1, dft_less=(141 / 255, 10 / 255, 10 / 255, 1)),
                            pos_hint={'center_x':0.5, 'top':1.18},
                            size_hint=(1.055, None), height=80)
        self.title = Label(text="Expense" if not self.entry.mode else "Income", pos_hint={'center_x':0.5, 'top':1.25},
                           size_hint=(1, None), width=self.width,
                           font_size=24)
        self.acc_icon = Image(source=self.entry.acc.icon_path,
                              size_hint=(None, None), width=70,
                              height=70, pos_hint={'center_x':self.a, 'top':0.8})
        self.ctg_icon = Image(source=self.entry.ctg.icon_path,
                              size_hint=(None, None), width=70,
                              height=70, pos_hint={'center_x': self.b, 'top': 0.8})
        self.a1 = Image(source="Images/arrow_right.png",
                              size_hint=(None, None), width=50,
                              height=50, pos_hint={'center_x':0.47, 'top':0.77})
        self.a2 = Image(source="Images/arrow_right.png",
                        size_hint=(None, None), width=50,
                        height=50, pos_hint={'center_x': 0.56, 'top': 0.77})
        self.amount_text = Label(text=f"{'-' if entry.mode == False else '+'}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{entry.amount}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                 pos_hint={'center_x': 0.5, 'top': 1},
                                 size_hint=(1, None), width=self.width,
                                 color=(191/255, 30/255, 30/255, 1) if entry.mode == False else (127/255, 199/255, 127/255, 1),
                                 font_size=24)
        self.acc_text = Label(text=self.entry.acc.name,
                              pos_hint={'center_x': self.a, 'top': 0.7},
                              size_hint=(1, None), width=50)
        self.ctg_text = Label(text=self.entry.ctg.name,
                              pos_hint={'center_x': self.b, 'top': 0.7},
                              size_hint=(1, None), width=50)
        self.desc_text = Label(text="Description",
                              pos_hint={'center_x': 0.5, 'top': 0.62},
                              size_hint=(1, None), width=50)
        self.desc_box = FloatLayout(size_hint=(1, None),
                             height=120, pos_hint={'center_x': 0.5, 'top': 0.4})
        self.desc_bg = Image(size_hint=(1, 1),
                             pos_hint={'center_x': 0.5, 'center_y':0.5},
                             color=(22/255, 22/255, 22/255, 1))
        self.desc_box.add_widget(self.desc_bg)

        self.desc = Label(text="", pos_hint={'center_x': 0.5, 'center_y':0.46},
                          size_hint=(1, None), height=100,
                          text_size=(250, None))
        self.fix_lines()

        self.confirm_popup = Popup(title="Are you sure?", content=ConfirmPopup(self.del_entry), size_hint=(0.6, 0.2))
        rs.mini_popup = self.confirm_popup
        self.delete_entry = Button(size_hint=(None, None), width=45,
                                   height=45, pos_hint={'center_x': 0.9, 'top': 1.15},
                                   background_color=(0, 0, 0, 0))
        self.delete_img = Image(source="Images/delete_entry.png", color=(1, 1, 1, 0.5))
        self.delete_entry.bind(size=self._update_img, pos=self._update_img, on_press=lambda instance: self.confirm_popup.open())
        self.delete_entry.add_widget(self.delete_img)

        self.edit_entry = Button(size_hint=(None, None), width=65,
                                   height=65, pos_hint={'center_x': 0.1, 'top': 1.175},
                                   background_color=(0, 0, 0, 0))
        self.edit_img = Image(source="Images/edit_entry.png", color=(1, 1, 1, 0.5))
        self.edit_entry.bind(size=self._update_img, pos=self._update_img, on_press=self.ed_entry)
        self.edit_entry.add_widget(self.edit_img)

        self.desc_box.add_widget(self.desc)

        self.add_widget(self.banner)
        self.add_widget(self.title)
        self.add_widget(self.acc_icon)
        self.add_widget(self.a1)
        self.add_widget(self.a2)
        self.add_widget(self.ctg_icon)
        self.add_widget(self.amount_text)
        self.add_widget(self.acc_text)

        self.add_widget(self.ctg_text)
        self.add_widget(self.desc_box)
        self.add_widget(self.desc_text)
        self.add_widget(self.delete_entry)
        self.add_widget(self.edit_entry)

    def _update_img(self, *args):
        self.delete_img.pos = self.delete_entry.pos
        self.delete_img.size = self.delete_entry.size
        self.edit_img.pos = self.edit_entry.pos
        self.edit_img.size = self.edit_entry.size

    def del_entry(self, *args):
        self.entry.acc.change_value(self.entry.amount, True if not self.entry.mode else False)
        rs.entry_groups[baf.rtrn_disp()].entries.remove(self.entry_ui)
        rs.temp_date_box.change_children()
        baf.save_entry_groups()
        rs.temp_popup.dismiss()
        rs.mini_popup.dismiss()

    def ed_entry(self,*args):
        entry_popup = Popup(title="Edit Entry:", content=PopupLayout(is_edit=True, edit_entry=self.entry_ui), size_hint=(0.9, 0.8))
        entry_popup.content.popup = entry_popup
        entry_popup.content.amount_box.text = str(self.entry.amount)
        if self.entry.mode:
            entry_popup.content.d_button.state = 'down'
            entry_popup.content.e_button.state = 'normal'
        else:
            entry_popup.content.ctg_scroll_ui.child_buttons[rs.dft_ctg.index(self.entry.ctg)].state = 'down'
            entry_popup.content.ctg_scroll_ui.child_buttons[0].state = 'normal'
        entry_popup.content.account_select.select(rs.dft_acc.index(self.entry.acc))
        entry_popup.content.t_acc = self.entry.acc
        entry_popup.content.t_desc = self.entry.description
        entry_popup.content.desc_box.text = self.entry.description
        rs.chosen_date = self.entry.date
        entry_popup.content.date_choice.text = f"{rs.month_names[(self.entry.date.month % 12) - 1]} {self.entry.date.day}, {self.entry.date.year}"

        entry_popup.open()

    def fix_lines(self, *args):
        switch = True
        temp = ''
        line_count = (self.desc.texture_size[1] / self.desc.line_height) / 22
        self.desc.text = temp
        self.desc.texture_update()
        for x in range(self.entry.description.__len__()):
            temp = temp + self.entry.description[x]
            self.desc.text = temp
            line_count = (self.desc.texture_size[1] / self.desc.line_height) / 22
            self.desc.texture_update()
            if line_count > 4:
                switch = False
                break
        if not switch:
            temp = temp[:temp.__len__() - 4] + "..."
        self.desc.text_size = (250, 100)
        self.desc.valign = 'top'
        self.desc.text = temp
        self.desc.texture_update()

class ConfirmPopup(FloatLayout):
    def __init__(self, func, **kwargs):
        super().__init__(**kwargs)
        self.button = Button(text="Confirm", size_hint=(1, None), height=40,
                             pos_hint={'center_x':0.5, 'top':0.3})
        self.button.bind(on_press=func)
        self.add_widget(self.button)

class DateEntryUI(FloatLayout):
    def __init__(self, entry: rs.Entry, **kwargs):
        super().__init__(**kwargs)
        self.entry = entry

        self.height = rs.view_height
        self.bar = Image(pos_hint={'x': 0.03, 'center_y': 0.11},
                         size_hint=(0.94, 0.02), color=(1, 1, 1, 1))

        self.add_widget(Label(text=entry.date.strftime("%b %d, %A"), pos_hint={'center_x':0.44, 'center_y':0.32},
                              halign='left', text_size=(int(Config.get('graphics', 'width')), None)))
        self.add_widget(self.bar)

class EntryButton(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.button = Button(size_hint=(None, None),
                             pos_hint={'center_x':0.5, 'center_y':0.3},
                             size=(75, 75),
                             background_color=(0, 0, 0, 0))
        self.img = Image(source="Images/addentry.png")
        self.button.add_widget(self.img)
        self.button.bind(size=self._update_image_pos, pos=self._update_image_pos, on_press=self.entry_menu)
        self.menu_popup = Popup(title="Add Entry:", content=PopupLayout(is_edit=False), size_hint=(0.9, 0.8))
        self.add_widget(self.button)

    def _update_image_pos(self, *args):
        self.img.size = self.button.size
        self.img.pos = self.button.pos

    def entry_menu(self, *args):
        #rs.chosen_date = datetime.date.today()
        self.menu_popup.open()
        self.menu_popup.content.popup = self.menu_popup

class PopupLayout(FloatLayout):
    def __init__(self, is_edit = False, edit_entry = None, **kwargs): #edit_entry is an EntryUI object
        super().__init__(**kwargs)
        self.t_amount = 0
        self.t_mode = False
        self.t_ctg = rs.dft_ctg[0]
        self.t_desc = ""
        self.t_acc = rs.dft_acc[0] #Change this so it appears as the last used account
        if is_edit:
            self.edit_entry = edit_entry
            rs.chosen_date = self.edit_entry.entry.date
        self.is_edit = is_edit
        self.popup = Popup()

        self.amount_text = Label(text="Amount:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top':1.05, 'x':0.035},
                                 font_size=17)
        self.error_text = Label(text="Please enter a valid amount!", size_hint=(0.5, 0.1),
                                 halign="center", pos_hint={'top': 1.02, 'x': 0.4},
                                 font_size=17, color=(1, 0.2, 0.2, 0))
        self.amount_text.bind(size=self.amount_text.setter('text_size'))

        self.amount_box= TextInput(size_hint=(0.935, 0.1), pos_hint={'top':0.94, 'x':0.035},
                                   multiline=False, input_type='number',
                                   padding_y=(15, 5), halign='center',
                                   background_color=(22/255, 22/255, 22/255, 1),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                   padding_x=(10, 10), text="0")
        self.amount_box.bind(focus=self.on_focus)
        self.currency_text = Label(text=rs.dft_currencies[rs.currency_choice][0], size_hint=(0.1, 0.1),
                                   pos_hint={'top':0.94, 'x':baf.align_currency_text(rs.dft_currencies[rs.currency_choice][1], place='text_box')},
                                   font_size=17)
        self.transaction_choice = GridLayout(cols=2, rows=1,
                                             size_hint=(0.735, 0.05), pos_hint={'top':0.84, 'center_x':0.5})

        self.e_button = ToggleButton(text="Expense", group="transaction", state="down")
        self.d_button = ToggleButton(text="Deposit", group="transaction")
        self.e_button.bind(state=self.expense)
        self.d_button.bind(state=self.deposit)

        self.transaction_choice.add_widget(self.e_button)
        self.transaction_choice.add_widget(self.d_button)

        self.account_select = DropDown()
        for i in range(rs.dft_acc.__len__()):
            self.account_ui = AccountUI(i, size_hint_y=None, height=40)
            self.account_choice = self.account_ui.button
            self.account_choice.bind(on_release=lambda a: self.account_select.select(a.no))
            self.account_select.bind(on_select=lambda instance, a: setattr(self, 't_acc', rs.dft_acc[a]))
            self.account_select.add_widget(self.account_ui)
        self.account_button = Button(size_hint=(0.935, 0.1), pos_hint={'top': 0.75, 'center_x': 0.5},
                                     text="Cash")
        self.account_button.bind(on_press=self.account_select.open)
        self.account_select.bind(on_select=lambda instance, a: setattr(self.account_button, 'text', rs.dft_acc[a].name))

        self.ctg_text = Label(text="Category:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top': 0.7, 'x': 0.035},
                                 font_size=17)
        self.ctg_text.bind(size=self.ctg_text.setter('text_size'))

        self.ctg_scroll = ScrollView(do_scroll_x=True,
                                     do_scroll_y=False, size_hint=(0.935, 0.18),
                                     pos_hint={'top': 0.59, 'x':0.035})
        self.ctg_cover = Image(size_hint=(0.935, 0.18),
                               pos_hint={'top': 0.59, 'x': 0.035}, color=(0.2, 0.2, 0.2, 0))

        self.ctg_scroll_ui = CtgSelector(size_hint_x=self.ctg_scroll.width/(rs.dft_ctg.__len__()**2))
        self.ctg_scroll_ui.bind(minimum_width=self.ctg_scroll_ui.setter('width'))
        self.ctg_scroll.add_widget(self.ctg_scroll_ui)

        self.desc_text = Label(text="Description:", size_hint=(1, 0.1),
                              halign="left", pos_hint={'top': 0.46, 'x': 0.035},
                              font_size=17)
        self.desc_text.bind(size=self.desc_text.setter('text_size'))

        self.desc_box = TextInput(size_hint=(0.935, 0.2), pos_hint={'top': 0.35, 'x': 0.035},
                                    multiline=True, padding_y=(15, 5), halign='center',
                                    background_color=(22 / 255, 22 / 255, 22 / 255, 1),
                                    cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                    padding_x=(10, 10))

        self.date_choice = Button(background_color=(66 / 255, 66 / 255, 66 / 255, 1),
                                  text=f"{rs.month_names[(datetime.date.today().month % 12) - 1]} {datetime.date.today().day}, {rs.disp_year}",
                                  size_hint=(0.935, 0.07), pos_hint={'top': 0.14, 'center_x': 0.5})
        self.date_popup = Popup(title="Choose a Date:", content=DateSelection(is_edit=self.is_edit), size_hint=(0.8, 0.5))
        self.date_popup.content.popup = self.date_popup
        self.date_choice.bind(on_press=self.open_date_popup)

        self.confirm_button = Button(size_hint=(0.935, 0.1), pos_hint={'top': 0.05, 'center_x': 0.5},
                                     text="Confirm")
        self.confirm_button.bind(on_press=self.callback)

        self.add_widget(self.amount_text)
        self.add_widget(self.error_text)
        self.add_widget(self.amount_box)
        self.add_widget(self.currency_text)
        self.add_widget(self.transaction_choice)
        self.add_widget(self.account_button)
        self.add_widget(self.ctg_text)
        self.add_widget(self.ctg_scroll)
        self.add_widget(self.desc_text)
        self.add_widget(self.desc_box)
        self.add_widget(self.date_choice)
        self.add_widget(self.confirm_button)
        self.add_widget(self.ctg_cover)

    def expense(self, instance, value):
        if value == 'down':
            self.t_mode = False
            self.ctg_cover.color = (0.2, 0.2, 0.2, 0)

    def deposit(self, instance, value):
        if value == 'down':
            self.t_mode = True
            self.ctg_cover.color = (0.2, 0.2, 0.2, 0.9)

    def open_date_popup(self, *args):
        self.date_popup.content.parent_layout = self
        self.date_popup.open()

    def on_focus(self, instance, value):
        if value:
            self.amount_box.foreground_color = (1, 1, 1, 1)

    def callback(self, *args):
        temp_date = datetime.date(rs.chosen_date.year, rs.chosen_date.month, 1)
        try:
            self.t_amount = float(self.amount_box.text)
            if self.t_amount <= 0 or str(self.t_amount).rsplit(".")[1].__len__() > 2: raise ValueError
            self.account_select.bind(on_select=lambda instance, a: setattr(self, 't_acc', rs.dft_acc[a]))
            self.t_desc = self.desc_box.text
            self.t_ctg = rs.temp_ctg
            rs.temp_entry = rs.Entry(self.t_ctg, self.t_amount, self.t_acc, self.t_mode, self.t_desc, rs.chosen_date)

            switch = True
            if self.is_edit and self.edit_entry.entry.date == rs.chosen_date:
                rs.temp_layout.remove_widget(self.edit_entry)
                rs.entry_groups[datetime.date(rs.chosen_date.year, rs.chosen_date.month, 1)].entries[rs.entry_groups[datetime.date(rs.chosen_date.year, rs.chosen_date.month, 1)].entries.index(self.edit_entry)] = EntryUI(rs.temp_entry)
                rs.entry_list[rs.entry_list.index(self.edit_entry)] = EntryUI(rs.temp_entry)
                self.edit_entry.entry.acc.change_value(self.edit_entry.entry.amount, True if not self.edit_entry.entry.mode else False)
                #rs.temp_entry.acc.change_value(rs.temp_entry.amount, rs.temp_entry.mode)
                rs.temp_popup.dismiss()
                switch = False
            if switch:
                if baf.rtrn_disp() == temp_date:
                    rs.temp_layout.add_widget(EntryUI(rs.temp_entry))
                    rs.entry_list.insert(0, EntryUI(rs.temp_entry))
                    if rs.entry_groups.get(baf.rtrn_disp()) is None:
                        rs.entry_groups[baf.rtrn_disp()] = rs.EntryGroup(baf.rtrn_disp())
                    rs.entry_groups[baf.rtrn_disp()].entries.insert(0, EntryUI(rs.temp_entry))
                else:
                    if rs.entry_groups.get(temp_date) is None:
                        rs.entry_groups[temp_date] = rs.EntryGroup(temp_date)
                    rs.entry_groups[temp_date].entries.insert(0, EntryUI(rs.temp_entry))
                if self.is_edit:
                    self.edit_entry.entry.acc.change_value(self.edit_entry.entry.amount, True if not self.edit_entry.entry.mode else False)
                    rs.entry_groups[datetime.date(self.edit_entry.entry.date.year, self.edit_entry.entry.date.month, 1)].entries.remove(self.edit_entry)
                    rs.temp_popup.dismiss()
            rs.temp_date_box.change_children()
            rs.main_widgets['acc_bal_exp'].update_text()
            rs.main_widgets['acc_bdg_exp'].update_text()

            for item in self.account_select.children:
                for item_2 in item.children:
                    item_2.update_text() #All this does is update the text of the accounts in dropdown

            if rs.budgetUIs.get(rs.temp_entry.ctg.name):
                rs.budgetUIs[rs.temp_entry.ctg.name].amount_spent += 1
            baf.save_entry_groups()
            self.error_text.color = (1, 0.2, 0.2, 0)
            self.popup.dismiss()

        except ValueError:
            self.amount_box.foreground_color = (1, 0.2, 0.2, 1)
            self.error_text.color = (1, 0.2, 0.2, 1)

        except IndexError:
            self.amount_box.foreground_color = (1, 0.2, 0.2, 1)
            self.error_text.color = (1, 0.2, 0.2, 1)

class DateSelection(FloatLayout):
    def __init__(self, is_edit = False, **kwargs):
        super().__init__(**kwargs)
        self.month_calendar = calendar.Calendar()
        self.is_updating = False
        self.popup = Popup()
        self.parent_layout = None
        self.is_edit = is_edit
        if not is_edit: rs.temp_date_select = self
        else: rs.temp_date_select_edit = self
        self.x_positions = itertools.cycle([0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95])
        self.y_positions = itertools.cycle(reversed([0.25, 0.4, 0.55, 0.7, 0.85]))
        self.y_positions_6wk = itertools.cycle(reversed([0.25, 0.37, 0.49, 0.61, 0.73, 0.85]))
        self.y_positions_4wk = itertools.cycle(reversed([0.25, 0.45, 0.65, 0.85]))
        self.y_pos_list = [self.y_positions_4wk, self.y_positions, self.y_positions_6wk]
        if not is_edit:
            self.displayed_month = rs.current_month
            self.displayed_year = datetime.date.today().year
            self.chosen_month_dates = list(self.month_calendar.itermonthdates(self.displayed_year, self.displayed_month))
            self.chosen_date = datetime.date.today()
        else:
            self.displayed_month = rs.chosen_date.month
            self.displayed_year = rs.chosen_date.year
            self.chosen_month_dates = list(self.month_calendar.itermonthdates(self.displayed_year, self.displayed_month))
            self.chosen_date = rs.chosen_date

        self.l_button = Button(size_hint=(None, None),
                               width=30,
                               height=30,
                               pos_hint={'x':0, 'top':0.97},
                               background_color=(0, 0, 0, 0))
        self.l_button.bind(on_press=self.l_clicked)
        self.l_image = Image(source="Images/arrow_left.png")
        self.l_button.bind(size=partial(self._update_image_pos, self.l_image, self.l_button),
                           pos=partial(self._update_image_pos, self.l_image, self.l_button))
        self.l_button.add_widget(self.l_image)
        self.add_widget(self.l_button)

        self.date_text = Label(text=f"{rs.month_names[self.displayed_month % 12 - 1]}, {self.displayed_year}",
                               pos_hint={'center_x':0.5, 'top':0.97}, size_hint=(None, None), height=30)
        self.add_widget(self.date_text)

        self.r_button = Button(size_hint=(None, None),
                               width=30,
                               height=30,
                               pos_hint={'x': 0.89, 'top': 0.97},
                               background_color=(0, 0, 0, 0))
        self.r_button.bind(on_press=self.r_clicked)
        self.r_image = Image(source="Images/arrow_right.png")
        self.r_button.bind(size=partial(self._update_image_pos, self.r_image, self.r_button),
                           pos=partial(self._update_image_pos, self.r_image, self.r_button))
        self.r_button.add_widget(self.r_image)
        self.add_widget(self.r_button)

        self.temp_y_pos = next(self.y_pos_list[1])
        self.temp_y_pos_6wk = next(self.y_pos_list[2])
        self.temp_y_pos_4wk = next(self.y_pos_list[0])
        self.temp_y_pos_list = [self.temp_y_pos_4wk, self.temp_y_pos, self.temp_y_pos_6wk]
        self.temp_x_pos = next(self.x_positions)
        self.temp_buttons = []

        if self.chosen_month_dates.__len__() == 42:
            self._create_buttons(6)
        elif self.chosen_month_dates.__len__() == 35:
            self._create_buttons(5)
        else:
            self._create_buttons(4)

        self.confirm_button = Button(pos_hint={'top':0.1, 'center_x':0.5}, size_hint=(None, None),
                                     width=120, height=30, text="Confirm")
        self.confirm_button.bind(on_press=self.callback)
        self.add_widget(self.confirm_button)


    @staticmethod
    def _update_image_pos(img, button, *args):
        img.size = button.size
        img.pos = button.pos

    def callback(self, *args):
        rs.chosen_date = self.chosen_date
        self.parent_layout.date_choice.text = f"{rs.month_names[self.chosen_date.month % 12 - 1]} {self.chosen_date.day}, {self.chosen_date.year}"
        self.popup.dismiss()

    def l_clicked(self, *args):
        self.displayed_month -= 1
        self.displayed_year = int(datetime.date.today().year) + ((self.displayed_month - 1) // 12)
        self._update_text()

    def r_clicked(self, *args):
        self.displayed_month = (self.displayed_month + 1)
        self.displayed_year = int(datetime.date.today().year) + ((self.displayed_month - 1) // 12)
        self._update_text()

    def _update_text(self):
        if self.is_updating: return

        self.is_updating = True
        self.chosen_month_dates = list(self.month_calendar.itermonthdates(self.displayed_year, self.displayed_month % 12 if self.displayed_month % 12 != 0 else 12))
        self.date_text.text = f"{rs.month_names[self.displayed_month % 12 - 1]}, {self.displayed_year}"
        for x in range(self.temp_buttons.__len__()):
            self.remove_widget(self.temp_buttons[x])
        self.temp_buttons.clear()

        if self.chosen_month_dates.__len__() == 42:
            self._create_buttons(6)
        elif self.chosen_month_dates.__len__() == 35:
            self._create_buttons(5)
        else:
            self._create_buttons(4)


        self.do_layout()
        self.is_updating = False

    def _create_buttons(self, weeks):
        for a in range(weeks):
            for b in range(7):
                temp_button = DateButton(self.chosen_month_dates[7*a+b],
                                           pos_hint={'top': self.temp_y_pos_list[weeks-4], 'center_x': self.temp_x_pos},
                                           group="date", size_hint=(0.1, 0.1),
                                           text=str(self.chosen_month_dates[7*a+b].day),
                                           background_color=(0, 0, 0, 0),
                                         is_edit=self.is_edit)
                if self.chosen_month_dates[7].month == self.chosen_month_dates[7*a+b].month:
                    temp_button.category = "e"
                elif self.chosen_month_dates[7].month > self.chosen_month_dates[7*a+b].month:
                    temp_button.category = "b"
                    temp_button.color = (1, 1, 1, 100/255)
                else:
                    temp_button.category = "a"
                    temp_button.color = (1, 1, 1, 100/255)

                if self.chosen_month_dates[7*a+b] == self.chosen_date and self.chosen_month_dates[7*a+b].month == self.displayed_month:
                    temp_button.state = "down"
                self.add_widget(temp_button)
                self.temp_x_pos = next(self.x_positions)
                self.temp_buttons.append(temp_button)
            self.temp_y_pos_list[weeks-4] = next(self.y_pos_list[weeks-4])

class DateButton(ToggleButton):
    def __init__(self, date: datetime.date, is_edit = False, **kwargs):
        super().__init__(**kwargs)
        self.date = date
        self.is_edit = is_edit
        self.category = "e" # b, e, a for before, exact and after
        self.bind(state=self._state_change)
        self.background_down = 'white'

    def _state_change(self, instance, value):
        if value == 'down':
            match self.category:
                case "e":
                    self.background_color = (100 / 255, 100 / 255, 100 / 255, 1)
                    if not self.is_edit: rs.temp_date_select.chosen_date = self.date
                    else: rs.temp_date_select_edit.chosen_date = self.date
                case "b":
                    if not self.is_edit: rs.temp_date_select.l_clicked()
                    else: rs.temp_date_select_edit.l_clicked()
                case "a":
                    if not self.is_edit: rs.temp_date_select.r_clicked()
                    else: rs.temp_date_select_edit.r_clicked()
                case _:
                    pass
        else:
            self.background_color = (0, 0, 0, 0)

class CtgButton(ToggleButton):
    def __init__(self, ctg: rs.Category, **kwargs):
        super().__init__(**kwargs)
        self.ctg = ctg
        self.background_color = (0, 0, 0, 0)
        self.background_down = 'white'

        self.img = Image(source=self.ctg.icon_path)
        self.name = Label(text=self.ctg.name, font_size=14)
        self.bind(size=self._update_image_pos, pos=self._update_image_pos, state=self._state_change)
        self.add_widget(self.img)
        self.add_widget(self.name)

    def _update_image_pos(self, *args):
        self.img.size = self.size
        self.img.pos = self.pos
        self.img.width *= 8/9
        self.img.height *= 8/9
        self.img.y += 13
        self.img.x += 5
        self.name.pos = self.pos
        self.name.y -= 40
        self.name.x -= 5

    def _state_change(self, instance, value):
        if value == 'down':
            self.background_color = (200/255, 200/255, 200/255, 50/100)
            rs.temp_ctg = self.ctg
        else:
            self.background_color = (0, 0, 0, 0)

class CtgSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.child_buttons = []

        with self.canvas.before:
            Color(22/255, 22/255, 22/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.rows = 1
        self.spacing = 1
        self.padding = [0, 0, 0, 0]
        #self.width = rs.ctg_view_width
        for i in range(rs.dft_ctg.__len__()):
            a = CtgButton(rs.dft_ctg[i], group="ctg")
            self.child_buttons.append(a)
            self.add_widget(a)
            if i == 0: a.state = 'down'

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class NumericalButton(Button):
    def __init__(self, no: int, **kwargs):
        super().__init__(**kwargs)
        self.no = no

class AccountUI(FloatLayout):
    amount = NumericProperty(0.0)
    def __init__(self, no: int, **kwargs):
        super().__init__(**kwargs)
        self.no = no
        self.amount = rs.dft_acc[self.no].value
        self.float_amount = 0.0
        self.background = Image(color=(22/255, 22/255, 22/255, 1), size_hint=(1,1), pos_hint={'top':1})
        self.button = NumericalButton(text=rs.dft_acc[no].name, size_hint_y=None, height=40, no=no,
                                      background_color=(0, 0, 0, 0), pos_hint={'top':1})
        self.icon = Image(source=rs.dft_acc[no].icon_path, pos_hint={'top':1, 'x':-0.4})
        self.balance_int = Label(
            text=f"{baf.sign_setter(rs.dft_acc[no].value)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(rs.dft_acc[no].value)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
            pos_hint={'top': 1.245, 'center_x':0.8},
            color=baf.color_setter(rs.dft_acc[no].value),
            size_hint_x=1, halign='right', text_size=self.size)
        self.bind(amount=self.update_text)
        self.add_widget(self.background)
        self.add_widget(self.button)
        self.add_widget(self.icon)
        self.add_widget(self.balance_int)

    def update_text(self, *args):
        self.amount = rs.dft_acc[self.no].value
        self.float_amount = self.amount
        self.balance_int.text = f"{baf.sign_setter(self.float_amount)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.float_amount)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.balance_int.color = baf.color_setter(self.float_amount)
#endregion

class ScreenButton(ToggleButton):
    def __init__(self, img_path: str, text: str, function, no: int, **kwargs):
        super().__init__(**kwargs)

        self.func = function
        self.no = no
        self.initial_switch = False # Makes sure that the program does not run the change screen code while initialising

        self._state_change(None, 'down' if self.no == 2 else 'normal')
        self.background_down = 'white'

        self.bg = Image(color=(0, 116/255, 129/255, 63/100))
        self.img = Image(source=img_path)
        self.name = Label(text=text, font_size=14)
        self.bind(size=self._update_image_pos, pos=self._update_image_pos, state=self._state_change)
        self.add_widget(self.bg)
        self.add_widget(self.img)
        self.add_widget(self.name)

    def _update_image_pos(self, *args):
        self.img.size = self.size
        self.bg.size = self.size
        self.img.pos = self.pos
        self.bg.pos = self.pos
        self.img.width *= 11/14
        self.img.height *= 11/14
        self.img.y += 13
        self.name.pos = self.pos
        self.name.y -= 40
        match self.no:
            case 1:
                self.name.x -= 1
                self.img.x += 10
            case 2:
                self.name.x -= 10
                self.img.x -= 0
            case 3:
                self.name.x += 5
                self.img.x += 15
            case 4:
                self.name.x -= 0
                self.img.x += 10

    def _state_change(self, instance, value):
        if value == 'down':
            self.background_color = (200/255, 200/255, 200/255, 50/100)
            if self.initial_switch or self.no != 2:
                self.func()
            else:
                self.initial_switch = True
        else:
            self.background_color = (0, 0, 0, 0)

class BaseApp(App):
    def build(self):
        global scroll_view_main
        temp = re_construct_save()
        Window.clearcolor = (22/255, 22/255, 22/255, 1)

        main_layout = FloatLayout()
        rs.main_widgets['main'] = main_layout

        top_layout = TitleBox(size_hint=(1, 0.07), pos_hint={'top':1})
        rs.main_widgets['top'] = top_layout

        date_layout = DateBox(size_hint=(1, 0.05), pos_hint={'top':0.93})
        rs.main_widgets['date'] = date_layout

        acc_layout = AccountBox(size_hint=(1, 0.07), pos_hint={'top': 0.88})
        acc_layout_budget = AccountBoxBudget(size_hint=(1, 0.07), pos_hint={'top': 0.88})
        rs.main_widgets['acc_bal_exp'] = acc_layout
        rs.main_widgets['acc_bdg_exp'] = acc_layout_budget

        empty_layout = BoxLayout(size_hint=(1, 0.01), pos_hint={'top':0.81})
        rs.main_widgets['empty'] = empty_layout

        mid_layout = ScrollView(size_hint=(1, 0.68), pos_hint={'top':0.80})
        rs.view_height = mid_layout.height

        mid_layout_ui = MainInterface(size_hint_y=rs.shown_entries * mid_layout.height / 700)
        mid_layout_budget = BudgetScroll(size_hint_y=rs.shown_entries * mid_layout.height / 500)
        rs.temp_layout = mid_layout_ui
        rs.main_widgets['budget_scroll'] = mid_layout_budget

        mid_layout_ui.bind(minimum_height=mid_layout_ui.setter('height'))
        mid_layout.add_widget(mid_layout_ui)
        bottom_button_ly = GridLayout(cols=4, size_hint=(1, 0.09), pos_hint={'top':0.09})
        bottom_entry_ly = EntryButton(size_hint=(1, 0.01), pos_hint={'top':0.11})

        funcs = [self.analysis_screen, self.records_screen, self.budget_screen, self.accounts_screen]
        button_text = ["Analysis", "Records", "Budgets", "Edit"]
        button_img = ["Images/Analytics.png", "Images/Records.png", "Images/Analytics.png", "Images/Analytics.png"]

        for i in range(1, 5):
            bottom_button_ly.add_widget(ScreenButton(button_img[i-1], button_text[i-1], funcs[i-1], i, background_color=(0, 0, 0, 0), group="main",
                                                     state='down' if i == 2 else 'normal'))
        rs.main_widgets['m_buttons'] = bottom_button_ly
        rs.main_widgets['entry_button'] = bottom_entry_ly

        main_layout.add_widget(top_layout)
        main_layout.add_widget(date_layout)
        main_layout.add_widget(acc_layout)
        main_layout.add_widget(empty_layout)
        main_layout.add_widget(mid_layout)
        main_layout.add_widget(bottom_button_ly)
        main_layout.add_widget(bottom_entry_ly)

        scroll_view_main = mid_layout
        if temp == 0:
            rs.temp_date_box.change_children()
        rs.main_widgets['acc_bdg_exp'].update_text()
        return main_layout

    @staticmethod
    def budget_screen(): # Fix this when you implement the third tab, because some of the widgets removed here won't be in that one
        rs.main_widgets['main'].remove_widget(rs.main_widgets['acc_bal_exp'])
        rs.main_widgets['main'].remove_widget(rs.main_widgets['empty'])
        rs.main_widgets['main'].remove_widget(rs.main_widgets['entry_button'])
        rs.main_widgets['main'].add_widget(rs.main_widgets['acc_bdg_exp'])
        scroll_view_main.remove_widget(rs.temp_layout)
        scroll_view_main.add_widget(rs.main_widgets['budget_scroll'])
        for ctg in rs.dft_ctg:
            if rs.budgetUIs.get(ctg.name):
                rs.budgetUIs[ctg.name].amount_spent += 1
        rs.main_widgets['main'].do_layout()

    @staticmethod
    def records_screen():
        rs.main_widgets['main'].add_widget(rs.main_widgets['acc_bal_exp'])
        rs.main_widgets['main'].add_widget(rs.main_widgets['empty'])
        rs.main_widgets['main'].add_widget(rs.main_widgets['entry_button'])
        rs.main_widgets['main'].remove_widget(rs.main_widgets['acc_bdg_exp'])
        scroll_view_main.remove_widget(rs.main_widgets['budget_scroll'])
        scroll_view_main.add_widget(rs.temp_layout)
        rs.main_widgets['main'].do_layout()

    @staticmethod
    def analysis_screen():
        print("Analysis")

    @staticmethod
    def accounts_screen():
        print("Accounts")

if __name__ == "__main__":
    BaseApp().run()