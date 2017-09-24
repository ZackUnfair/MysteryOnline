from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from character import characters, series_list
from math import ceil


class CharacterToggle(ToggleButton):

    def __init__(self, char, **kwargs):
        super(CharacterToggle, self).__init__(**kwargs)
        self.char = char
        self.background_normal = self.char.avatar
        self.size_hint = (None, None)
        self.size = (60, 60)


class CharacterSelectSaved:

    def __init__(self, main_lay):
        self.main_lay = main_lay
        self.is_saved = False

    def save(self):
        self.is_saved = True

    def get_saved(self):
        return self.main_lay


class CharacterSelect(Popup):

    button_lay = ObjectProperty(None)
    scroll_lay = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CharacterSelect, self).__init__(**kwargs)
        self.title = "Select your character"
        self.size_hint = (0.7, 0.7)
        self.auto_dismiss = False
        self.background_color = [0, 0, 0, 0]
        self.picked_char = None
        self.main_lay = BoxLayout(orientation='vertical', size_hint=(1, None), height=self.height-100)
        self.scroll_lay.add_widget(self.main_lay)
        self.save = CharacterSelectSaved(self.main_lay)
        self.fill_with_chars()

    def on_size(self, *args):
        self.fill_with_chars()

    def fill_with_chars(self):
        self.scroll_lay.clear_widgets()
        if self.save.is_saved:
            main_lay = self.save.get_saved()
            self.scroll_lay.add_widget(main_lay)
            return

        grids = {}
        for s in series_list:
            temp = list(filter(lambda x: x.series == s, characters.values()))
            mod = ceil(len(temp) / 7)
            self.main_lay.add_widget(Label(text=s, size_hint=(1, None), height=40))
            grids[s] = GridLayout(cols=7, size_hint=(1, None), height=60 * mod)
            self.main_lay.add_widget(grids[s])

        for g in grids:
            chars = list(filter(lambda x: x.series == g, characters.values()))
            chars = sorted(chars, key=lambda x: x.name)
            for c in chars:
                btn = CharacterToggle(c, group='char')
                btn.bind(on_press=self.character_chosen)
                grids[g].add_widget(btn)
        ok_btn = Button(text="OK", size_hint=(1, None), height=40, pos_hint={'y': 0, 'x': 0})
        ok_btn.bind(on_press=self.dismiss)
        self.button_lay.add_widget(ok_btn)
        self.main_lay.bind(minimum_height=self.main_lay.setter('height'))
        self.save.save()
        self.scroll_lay.add_widget(self.main_lay)

    def character_chosen(self, inst):
        self.picked_char = inst.char

    def dismiss(self, inst):
        super(CharacterSelect, self).dismiss(animation=False)
