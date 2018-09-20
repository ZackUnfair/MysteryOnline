from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App
from character_select import CharacterSelect


class KeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(KeyboardListener, self).__init__(**kwargs)
        self.keyboard_shortcuts = None
        self.load_shortcuts()

    def load_shortcuts(self):
        config = App.get_running_app().config
        self.keyboard_shortcuts = {
            config.get('keybindings', 'open_character_select'): self.open_character_select,
            config.get('keybindings', 'open_inventory'): self.open_inventory
        }

    def bind_keyboard(self):
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, inst, value, keycode, text, modifiers):
        if text is None:
            return
        shortcut = ""
        if modifiers:
            for mod in modifiers:
                shortcut += str(mod)
                shortcut += "+"
        shortcut += text
        if shortcut in self.keyboard_shortcuts:
            shortcut_hook = self.keyboard_shortcuts[shortcut]
            shortcut_hook()
            return True

    def open_character_select(self):
        cs = CharacterSelect()
        cs.bind(on_dismiss=self.on_picked)
        cs.open()

    def on_picked(self, inst):
        user = App.get_running_app().get_user()
        if inst.picked_char is not None:
            user.set_char(inst.picked_char)
            user.get_char().load()
            main_scr = App.get_running_app().get_main_screen()
            main_scr.on_new_char(user.get_char())

    def open_inventory(self):
        main_scr = App.get_running_app().get_main_screen()
        user = App.get_running_app().get_user()
        user.inventory.open()
        toolbar = main_scr.get_toolbar()
        toolbar.text_item_btn.text = "no item"