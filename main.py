import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class BaseApp(App):
    def build(self):
        return Label(text="Yay")

if __name__ == "__main__":
    BaseApp().run()