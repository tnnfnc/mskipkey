import kivy
from kivy.lang.builder import Builder
from kivymd.app import MDApp

KV = """
Screen:
    MDRectangleFlatButton:
        text: 'Button 1'
        pos_hint: {'x': 0.1, 'y': 0.9}
        md_bg_color: app.theme_cls.primary_light
    MDRectangleFlatButton:
        pos_hint: {'x': 0.1, 'y': 0.5}
        text: 'Button 2'
        md_bg_color: app.theme_cls.primary_dark
"""

class MyApp(MDApp):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
    	"""Overwrite for your App """
        self.theme_cls.theme_style = 'Light' #'Dark'
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.primary_hue = '500'
        self.root = Builder.load_string(KV)
        return self.root

if __name__ == '__main__':
    MyApp().run()
