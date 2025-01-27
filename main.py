import kivy
from kivy.config import Config

Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '620')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from kivy.uix.button import Button

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

        self.img = Image(source="Images/3bars.png", allow_stretch=True, keep_ratio=True)
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
        pass

class BaseApp(App):
    def build(self):
        Window.clearcolor = (22/255, 22/255, 22/255, 1)

        main_layout = BoxLayout(orientation="vertical", spacing=0)

        top_layout = TitleBox(size_hint=(1, 0.05))

        mid_layout = BoxLayout(size_hint=(1, 0.85))

        bottom_button_ly = GridLayout(cols=4, size_hint=(1, 0.09))
        bottom_text_ly = GridLayout(cols=4, size_hint=(1, 0.01))
        for i in range(1, 5):
            bottom_button_ly.add_widget(Button(background_color=(0, 0, 0, 1)))

        main_layout.add_widget(top_layout)
        main_layout.add_widget(mid_layout)
        main_layout.add_widget(bottom_button_ly)
        main_layout.add_widget(bottom_text_ly)

        return main_layout

if __name__ == "__main__":
    BaseApp().run()