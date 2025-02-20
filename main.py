import random

import kivy
from kivy.config import Config
from kivy.input import MotionEvent

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

scroll_view_main = ScrollView()

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
        print(f"self.month_text: {self.month_text.text}, disp_month: {rs.disp_year}, {rs.disp_month}, {rs.disp_month // 12} type: {type(self.month_text)}")
        self.month_text.text = f"{rs.month_names[rs.disp_month % 12]}, {rs.disp_year}"

    def lft_clicked(self, *args):
        rs.disp_month = (rs.disp_month - 1)
        rs.disp_year = int(datetime.date.today().year) + (rs.disp_month // 12)
        self._update_text()

    def rgt_clicked(self, *args):
        rs.disp_month = (rs.disp_month + 1)
        rs.disp_year = int(datetime.date.today().year) + (rs.disp_month // 12)
        self._update_text()

class AccountBox(FloatLayout):
    balance = NumericProperty(float((sum([x.value for x in rs.dft_acc]))))
    expense = NumericProperty(-1 * float(sum([x.entry.amount for x in rs.entry_list if x.entry.mode == False])))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background = Image(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                color=(0, 60/255, 64/255, 63/100))
        self.float_balance = 0.0
        self.float_expense = 0.0

        rs.temp_acc = self

        self.balance_label = Label(text=f"Balance:",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.26, 'center_y': 0.75},
                                   halign='center', font_size=16)
        self.expense_label = Label(text=f"Expenses:",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.75, 'center_y': 0.75},
                                   halign='center', font_size=16)
        self.balance_int = Label(text=f"{baf.sign_setter(self.float_balance)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.balance)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
                                   pos_hint={'center_x': 0.25, 'center_y': 0.25},
                                   color=baf.color_setter(self.float_balance),
                                   halign='center', font_size=16)
        self.bind(balance=self.update_text)
        self.expense_int = Label(text=f"{baf.sign_setter(self.float_expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}",
                                   text_size=(int(Config.get('graphics', 'width'))/4, None),
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
        self.balance_int.text = f"{baf.sign_setter(self.float_balance)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.float_balance)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.balance_int.color = baf.color_setter(self.float_balance)
        self.expense_int.text = f"{baf.sign_setter(self.float_expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == True else ''}{abs(self.expense)}{dft_currencies[currency_choice][0] if dft_currencies[currency_choice][1] == False else ''}"
        self.expense_int.color = baf.color_setter(self.float_expense)

class MainInterface(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.child_count = 0
        self.is_updating = False

        for x in range(10):
            temp = EntryUI(rs.Entry(rs.dft_ctg[random.randint(0, 6)], 10.00, rs.dft_acc[random.randint(0, 2)], True))
            rs.entry_list.append(temp)
            self.add_widget(temp, True)
            rs.shown_entries += 1

        self.on_child_change(self, None)

    def add_widget(self, widget, mode: bool = False, *args, **kwargs):
        super().add_widget(widget, *args, **kwargs)
        if not mode: self.on_child_change(self, None)
        rs.temp_acc.update_text()
        scroll_view_main.update_from_scroll()

    def remove_widget(self, widget, mode: bool = False, *args, **kwargs):
        super().remove_widget(widget, *args, **kwargs)
        if not mode: self.on_child_change(self, None)
        rs.temp_acc.update_text()
        scroll_view_main.update_from_scroll()

    def on_child_change(self, instance, value):
        if self.is_updating: return

        self.is_updating = True
        self.child_count = len(self.children)
        self.size_hint_y = self.child_count * rs.view_height / 700
        self.children = self.children[1:] + [self.children[0]]
        self.do_layout()
        self.is_updating = False

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
        self.add_widget(self.icon)
        self.add_widget(self.category)
        self.add_widget(self.account_icon)
        self.add_widget(self.account_text)
        self.add_widget(self.amount)
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
        self.menu_popup = Popup(title="Add Entry:", content=PopupLayout(), size_hint=(0.9, 0.8))
        self.add_widget(self.button)

    def _update_image_pos(self, *args):
        self.img.size = self.button.size
        self.img.pos = self.button.pos

    def entry_menu(self, *args):
        self.menu_popup.open()
        self.menu_popup.content.popup = self.menu_popup

class PopupLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.t_amount = 0
        self.t_mode = False
        self.t_ctg = rs.dft_ctg[0]
        self.t_desc = ""
        self.t_acc = rs.dft_acc[0] #Change this so it appears as the last used account
        self.t_date = datetime.date.today() #Change this later
        self.popup = Popup()

        self.amount_text = Label(text="Amount:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top':1.05, 'x':0.035},
                                 font_size=17)
        self.amount_text.bind(size=self.amount_text.setter('text_size'))

        self.amount_box= TextInput(size_hint=(0.935, 0.1), pos_hint={'top':0.94, 'x':0.035},
                                   multiline=False, input_type='number',
                                   padding_y=(15, 5), halign='center',
                                   background_color=(22/255, 22/255, 22/255, 1),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                   padding_x=(10, 10), text="0")
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
            self.account_choice = NumericalButton(text=rs.dft_acc[i].name, size_hint_y=None, height=20, no=i)
            self.account_choice.bind(on_release=lambda a: self.account_select.select(a.no))
            self.account_select.add_widget(self.account_choice)
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
                                  text=f"{rs.month_names[(datetime.date.today().month % 12) - 1]}, {rs.disp_year}",
                                  size_hint=(0.935, 0.07), pos_hint={'top': 0.14, 'center_x': 0.5})
        self.date_popup = Popup(title="Choose a Date:", content=DateSelection(), size_hint=(0.8, 0.5))
        self.date_choice.bind(on_press=self.open_date_popup)

        self.confirm_button = Button(size_hint=(0.935, 0.1), pos_hint={'top': 0.05, 'center_x': 0.5},
                                     text="Confirm")
        self.confirm_button.bind(on_press=self.callback)

        self.add_widget(self.amount_text)
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

    def expense(self, instance, value):
        if value == 'down':
            self.t_mode = False

    def deposit(self, instance, value):
        if value == 'down':
            self.t_mode = True

    def open_date_popup(self, *args):
        self.date_popup.open()

    def callback(self, *args):
        self.account_select.bind(on_select=lambda instance, a: setattr(self, 't_acc', rs.dft_acc[a]))
        self.t_amount = float(self.amount_box.text)
        self.t_desc = self.desc_box.text
        self.t_ctg = rs.temp_ctg
        rs.temp_entry = rs.Entry(self.t_ctg, self.t_amount, self.t_acc, self.t_mode, self.t_desc)
        rs.temp_layout.add_widget(EntryUI(rs.temp_entry))
        rs.entry_list.insert(0, EntryUI(rs.temp_entry))
        rs.temp_acc.update_text()
        self.popup.dismiss()

class DateSelection(FloatLayout):
    pass #Create a grid to put each date of a calendar object and select from it

class CtgButton(ToggleButton):
    def __init__(self, ctg: rs.Category, **kwargs):
        super().__init__(**kwargs)
        self.ctg = ctg
        self.background_color = (0, 0, 0, 0)
        self.background_down = 'white'

        self.img = Image(source=self.ctg.icon_path)
        self.bind(size=self._update_image_pos, pos=self._update_image_pos, state=self._state_change)
        self.add_widget(self.img)

    def _update_image_pos(self, *args):
        self.img.size = self.size
        self.img.pos = self.pos

    def _state_change(self, instance, value):
        if value == 'down':
            self.background_color = (200/255, 200/255, 200/255, 50/100)
            rs.temp_ctg = self.ctg
        else:
            self.background_color = (0, 0, 0, 0)

class CtgSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            self.add_widget(a)
            if i == 0: a.state = 'down'

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class NumericalButton(Button):
    def __init__(self, no: int, **kwargs):
        super().__init__(**kwargs)
        self.no = no

class BaseApp(App):
    def build(self):
        global scroll_view_main
        Window.clearcolor = (22/255, 22/255, 22/255, 1)

        main_layout = FloatLayout()

        top_layout = TitleBox(size_hint=(1, 0.07), pos_hint={'top':1})

        date_layout = DateBox(size_hint=(1, 0.05), pos_hint={'top':0.93})

        acc_layout = AccountBox(size_hint=(1, 0.07), pos_hint={'top':0.88})

        empty_layout = BoxLayout(size_hint=(1, 0.01), pos_hint={'top':0.81})

        mid_layout = ScrollView(size_hint=(1, 0.68), pos_hint={'top':0.80})
        rs.view_height = mid_layout.height

        mid_layout_ui = MainInterface(size_hint_y=rs.shown_entries * mid_layout.height / 700)
        rs.temp_layout = mid_layout_ui

        mid_layout_ui.bind(minimum_height=mid_layout_ui.setter('height'))
        mid_layout.add_widget(mid_layout_ui)

        bottom_button_ly = GridLayout(cols=4, size_hint=(1, 0.09), pos_hint={'top':0.09})
        bottom_entry_ly = EntryButton(size_hint=(1, 0.01), pos_hint={'top':0.11})

        for i in range(1, 5):
            bottom_button_ly.add_widget(Button(background_color=(0, 0.5, 0.5, 1)))

        main_layout.add_widget(top_layout)
        main_layout.add_widget(date_layout)
        main_layout.add_widget(acc_layout)
        main_layout.add_widget(empty_layout)
        main_layout.add_widget(mid_layout)
        main_layout.add_widget(bottom_button_ly)
        main_layout.add_widget(bottom_entry_ly)

        scroll_view_main = mid_layout
        return main_layout

if __name__ == "__main__":
    BaseApp().run()