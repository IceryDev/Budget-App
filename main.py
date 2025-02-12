import kivy
from kivy.config import Config

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
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button

from functools import partial
import resources as rs
import ba_funcs as baf
import datetime

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

class MainInterface(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1

        for x in range(100):
            self.add_widget(EntryUI(rs.Entry(rs.dft_ctg[0], 10, rs.dft_acc[0], True)))
            self.add_widget(Image(source="Images/bar.png"))

class EntryUI(BoxLayout):
    def __init__(self, entry: rs.Entry, **kwargs):
        super().__init__(**kwargs)

        self.height = rs.view_height
        self.description = Label(text=f"{entry.ctg.name}, {entry.amount}",
                                 text_size=(int(Config.get('graphics', 'width')), None))
        self.add_widget(self.description)

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
        self.menu_popup = Popup(title="Add Entry:", content=PopupLayout(), size_hint=(0.9, 0.7))
        self.add_widget(self.button)

    def _update_image_pos(self, *args):
        self.img.size = self.button.size
        self.img.pos = self.button.pos

    def entry_menu(self, *args):
        self.menu_popup.open()

class PopupLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.amount_text = Label(text="Amount:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top':1.01, 'x':0.035},
                                 font_size=17)
        self.amount_text.bind(size=self.amount_text.setter('text_size'))

        self.amount_box= TextInput(size_hint=(0.935, 0.1), pos_hint={'top':0.9, 'x':0.035},
                                   multiline=False, input_type='number',
                                   padding_y=(15, 5), halign='center',
                                   background_color=(22/255, 22/255, 22/255, 1),
                                   cursor_color=(1, 1, 1, 1), foreground_color=(1, 1, 1, 1),
                                   padding_x=(10, 10))
        self.currency_text = Label(text=rs.dft_currencies[rs.currency_choice][0], size_hint=(0.1, 0.1),
                                   pos_hint={'top':0.9, 'x':baf.align_currency_text(rs.dft_currencies[rs.currency_choice][1], place='text_box')},
                                   font_size=17)

        self.ctg_text = Label(text="Category:", size_hint=(1, 0.1),
                                 halign="left", pos_hint={'top': 0.79, 'x': 0.035},
                                 font_size=17)
        self.ctg_text.bind(size=self.ctg_text.setter('text_size'))

        self.ctg_scroll = ScrollView(do_scroll_x=True,
                                     do_scroll_y=False, size_hint=(0.935, 0.2),
                                     pos_hint={'top': 0.68, 'x':0.035})

        self.ctg_scroll_ui = CtgSelector(size_hint_x=self.ctg_scroll.width/12)
        self.ctg_scroll_ui.bind(minimum_width=self.ctg_scroll_ui.setter('width'))

        self.ctg_scroll.add_widget(self.ctg_scroll_ui)

        self.add_widget(self.amount_text)
        self.add_widget(self.amount_box)
        self.add_widget(self.currency_text)
        self.add_widget(self.ctg_text)
        self.add_widget(self.ctg_scroll)
        #self.add_widget(TextInput(size_hint=(1, 0.1)))

class CtgSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(22/255, 22/255, 22/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.rows = 1
        self.spacing = 1
        self.padding = [0, 5, 0, 0]
        #self.width = rs.ctg_view_width
        for x in range(30):
            self.add_widget(Image(source="Images/Analytics.png"))

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class BaseApp(App):
    def build(self):
        Window.clearcolor = (22/255, 22/255, 22/255, 1)

        main_layout = FloatLayout()

        top_layout = TitleBox(size_hint=(1, 0.08), pos_hint={'top':1})

        date_layout = DateBox(size_hint=(1, 0.05), pos_hint={'top':0.92})

        mid_layout = ScrollView(size_hint=(1, 0.73), pos_hint={'top':0.87})

        mid_layout_ui = MainInterface(size_hint_y=mid_layout.height/7)
        rs.view_height = mid_layout.height/7
        mid_layout_ui.bind(minimum_height=mid_layout_ui.setter('height'))
        mid_layout.add_widget(mid_layout_ui)

        bottom_button_ly = GridLayout(cols=4, size_hint=(1, 0.09), pos_hint={'top':0.09})
        bottom_entry_ly = EntryButton(size_hint=(1, 0.05), pos_hint={'top':0.11})

        for i in range(1, 5):
            bottom_button_ly.add_widget(Button(background_color=(0, 0.5, 0.5, 1)))

        main_layout.add_widget(top_layout)
        main_layout.add_widget(date_layout)
        main_layout.add_widget(mid_layout)
        main_layout.add_widget(bottom_button_ly)
        main_layout.add_widget(bottom_entry_ly)


        return main_layout

if __name__ == "__main__":
    BaseApp().run()