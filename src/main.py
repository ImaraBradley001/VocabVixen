from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
import subprocess
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Builder.load_file("style.kv")

def readlines_from_file(file_name):
    file = open(file_name, 'r')
    data = file.readlines()
    file.close()
    return data



def query_DB(word_):
    first_letter = word_[0]
    word_ = word_.title()
    content_file = f'..\\database\\{first_letter}.csv'
    data = readlines_from_file(content_file)
    meanings = []
    for line in data:
        if line.split(' ')[0] == word_ or line.split(' ')[0] == f'"{word_}':
            meaning = line.split(')')[1][1:].strip('\n').strip('"').strip("'")
            meanings.append(meaning)
    if len(meanings) == 0:
        meanings.append('Word not found.')
    return meanings


class Controller(FloatLayout):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))
        self.meaning_widgets = []

    def get_meaning(self):
        word = self.ids.word.text
        meanings = query_DB(word)
        for m in self.meaning_widgets:
            self.ids.layout_content.remove_widget(m)
        if not meanings:
            m = TextInput(text="Word Not found")
            self.meaning_widgets.append(m)
            self.ids.layout_content.add_widget(m)
            return
        for meaning in meanings:
            """
            text_size: self.size
            halign: "center"
            valign: "center"
            """
            m = TextInput(text=meaning)
            self.meaning_widgets.append(m)
            self.ids.layout_content.add_widget(m)


class MainApp(App):
    def build(self):
        Window.size = [400, 800]
        return Controller()


MainApp().run()
