from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class NullSprite:

    def __init__(self, name):
        self.name = name

    def unset_nsfw(self):
        pass

    def unset_spoiler(self):
        pass

    def is_cg(self):
        return False

    def is_nsfw(self):
        return False

    def is_spoiler(self):
        return False

    def get_name(self):
        return self.name

    def get_texture(self):
        texture = self.return_spoiler_texture()
        return texture

    def return_spoiler_texture(self):
        spoiler_sprite = self.load_dummy_character_sprite('4')
        return spoiler_sprite.get_texture()

    def load_dummy_character_sprite(self, sprite_name):
        from character import characters
        red_herring = characters['RedHerring']
        red_herring.load()
        return red_herring.get_sprite(sprite_name)


class Sprite:

    def __init__(self, name, texture):
        self.name = name
        self.texture = texture
        self.nsfw = False
        self.spoiler = False
        self.cg = False

    def get_texture(self):
        texture = self.texture
        if self.is_nsfw():
            texture = self.return_nsfw_texture()
        elif self.is_spoiler():
            texture = self.return_spoiler_texture()
        return texture

    def return_nsfw_texture(self):
        spoiler_sprite = self.load_dummy_character_sprite('5')
        return spoiler_sprite.get_texture()

    def return_spoiler_texture(self):
        spoiler_sprite = self.load_dummy_character_sprite('4')
        return spoiler_sprite.get_texture()

    def load_dummy_character_sprite(self, sprite_name):
        from character import characters
        red_herring = characters['RedHerring']
        red_herring.load()
        return red_herring.get_sprite(sprite_name)

    def get_name(self):
        return self.name

    def is_nsfw(self):
        return self.nsfw

    def set_nsfw(self):
        self.nsfw = True

    def unset_nsfw(self):
        self.nsfw = False

    def unset_spoiler(self):
        self.spoiler = False

    def set_spoiler(self):
        self.spoiler = True

    def is_spoiler(self):
        return self.spoiler

    def set_cg(self):
        self.cg = True

    def is_cg(self):
        return self.cg


class SpriteSettings(BoxLayout):
    check_flip_h = ObjectProperty(None)
    pos_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SpriteSettings, self).__init__(**kwargs)
        self.functions = {"flip_h": self.flip_sprite}
        self.activated = []
        self.flipped = []
        self.create_pos_drop()

    def apply_post_processing(self, sprite, setting):
        if setting == 0:
            if sprite not in self.flipped:
                self.flip_sprite(sprite.texture)
                self.flipped.append(sprite)
        else:
            if sprite in self.flipped:
                self.flip_sprite(sprite.texture)
                self.flipped.remove(sprite)
        return sprite

    def flip_sprite(self, sprite_texture):
        sprite_texture.flip_horizontal()

    def on_checked_flip_h(self, value):
        user_handler = App.get_running_app().get_user_handler()
        if value:
            user_handler.set_current_sprite_option(0)
        else:
            user_handler.set_current_sprite_option(1)
        sprite = user_handler.get_current_sprite()
        sprite_option = user_handler.get_current_sprite_option()
        sprite = self.apply_post_processing(sprite, sprite_option)
        main_scr = App.get_running_app().get_main_screen()
        main_scr.sprite_preview.set_sprite(sprite)
        Clock.schedule_once(main_scr.refocus_text, 0.2)

    def on_pos_select_clicked(self):
        self.pos_drop.open(self.pos_btn)

    def create_pos_drop(self):
        self.pos_drop = DropDown(size_hint=(None, None), size=(100, 30))
        for pos in ('center', 'right', 'left'):
            btn = Button(text=pos, size_hint=(None, None), size=(100, 30))
            btn.bind(on_release=lambda btn_: self.pos_drop.select(btn_.text))
            self.pos_drop.add_widget(btn)
        self.pos_drop.bind(on_select=self.on_pos_select)

    def on_pos_select(self, inst, pos):
        self.pos_btn.text = pos
        main_scr = App.get_running_app().get_main_screen()
        user_handler = App.get_running_app().get_user_handler()
        user_handler.set_current_pos_name(pos)
        main_scr.refocus_text()


class SpritePreview(Image):
    center_sprite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SpritePreview, self).__init__(**kwargs)

    def set_subloc(self, sub):
        self.texture = sub.get_img().texture

    def set_sprite(self, sprite):
        self.center_sprite.texture = None
        self.center_sprite.texture = sprite.get_texture()
        self.center_sprite.opacity = 1
        self.center_sprite.size = (self.center_sprite.texture.width / 3,
                                   self.center_sprite.texture.height / 3)


class SpriteWindow(Widget):
    background = ObjectProperty(None)
    sprite_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SpriteWindow, self).__init__(**kwargs)
        self.center_sprite = Image(allow_stretch=True, keep_ratio=False,
                                   opacity=0, size_hint=(None, None), size=(800, 600),
                                   pos_hint={'center_x': 0.5, 'y': 0})
        self.left_sprite = Image(opacity=0, size_hint=(None, None), size=(800, 600),
                                 pos_hint={'center_x': 0.25, 'y': 0})
        self.right_sprite = Image(opacity=0, size_hint=(None, None), size=(800, 600),
                                  pos_hint={'center_x': 0.75, 'y': 0})

    def set_sprite(self, user):
        sprite = user.get_current_sprite()
        if sprite.is_cg():
            self.set_cg(sprite)
            return
        subloc = user.get_subloc()
        pos = user.get_pos()
        self.sprite_layout.clear_widgets()
        if pos == 'right':
            self.sprite_layout.add_widget(self.center_sprite, index=2)
            self.sprite_layout.add_widget(self.right_sprite, index=0)
            self.sprite_layout.add_widget(self.left_sprite, index=1)
            subloc.add_r_user(user)
        elif pos == 'left':
            self.sprite_layout.add_widget(self.center_sprite, index=1)
            self.sprite_layout.add_widget(self.right_sprite, index=2)
            self.sprite_layout.add_widget(self.left_sprite, index=0)
            subloc.add_l_user(user)
        else:
            self.sprite_layout.add_widget(self.center_sprite, index=0)
            self.sprite_layout.add_widget(self.right_sprite, index=2)
            self.sprite_layout.add_widget(self.left_sprite, index=1)
            subloc.add_c_user(user)

        self.display_sub(subloc)

    def set_cg(self, sprite):
        self.sprite_layout.clear_widgets()
        self.sprite_layout.add_widget(self.center_sprite, index=0)
        self.center_sprite.texture = None
        self.center_sprite.texture = sprite.get_texture()
        self.center_sprite.opacity = 1
        self.center_sprite.size = 800, 600

    def set_subloc(self, subloc):
        self.background.texture = subloc.get_img().texture

    def display_sub(self, subloc):

        if subloc.c_users:
            sprite = subloc.get_c_user().get_current_sprite()
            option = subloc.get_c_user().get_sprite_option()
            main_scr = App.get_running_app().get_main_screen()
            sprite = main_scr.sprite_settings.apply_post_processing(sprite, option)
            if sprite is not None:
                self.center_sprite.texture = None
                self.center_sprite.texture = sprite.get_texture()
                self.center_sprite.opacity = 1
                self.center_sprite.size = self.center_sprite.texture.size
        else:
            self.center_sprite.texture = None
            self.center_sprite.opacity = 0
        if subloc.l_users:
            sprite = subloc.get_l_user().get_current_sprite()
            option = subloc.get_l_user().get_sprite_option()
            main_scr = App.get_running_app().get_main_screen()
            sprite = main_scr.sprite_settings.apply_post_processing(sprite, option)
            if sprite is not None:
                self.left_sprite.texture = None
                self.left_sprite.texture = sprite.get_texture()
                self.left_sprite.opacity = 1
                self.left_sprite.size = self.left_sprite.texture.size
        else:
            self.left_sprite.texture = None
            self.left_sprite.opacity = 0
        if subloc.r_users:
            sprite = subloc.get_r_user().get_current_sprite()
            option = subloc.get_r_user().get_sprite_option()
            main_scr = App.get_running_app().get_main_screen()
            sprite = main_scr.sprite_settings.apply_post_processing(sprite, option)
            if sprite is not None:
                self.right_sprite.texture = None
                self.right_sprite.texture = sprite.get_texture()
                self.right_sprite.opacity = 1
                self.right_sprite.size = self.right_sprite.texture.size
        else:
            self.right_sprite.texture = None
            self.right_sprite.opacity = 0
