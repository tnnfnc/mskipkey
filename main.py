import kivy
from kivy.lang.builder import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.rst import RstDocument
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox
from kivymd.uix.list import OneLineListItem
import certifi
import json


KV = """
BoxLayout:
    orientation: 'vertical'
    
    MDToolbar:
        id: toolbar
        title: "Wikipedia Navigator"
        pos_hint: {"top": 1}
        elevation: 10
        left_action_items: [['menu', lambda x: nav_drawer.set_state()],]

    NavigationLayout:

        ScreenManager:
            id: screen_manager

            Screen:
                name: 'search'
                BoxLayout:
                    orientation: 'vertical'

                    MDTextField:
                        id: text
                        hint_text: "Input search"
                        helper_text: "Type here what you want to find"
                        helper_text_mode: "on_focus"

                    MDRaisedButton:
                        id: find
                        text: 'Find'
                        size_hint_x: 1
                        on_press: app.random_search()

                    ScrollView:
                        MDList:
                            id: list
                            padding: 0

            Screen:
                name: 'display'
                RstDocument:
                    id: detail

                MDFloatingActionButton:
                    elevation_normal: 12
                    pos_hint: {'right': 0.9, 'top': 0.15}
                    md_bg_color: app.theme_cls.primary_color
                    on_release: app.back()
            

        MDNavigationDrawer:
            id: nav_drawer

            BoxLayout:
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"

                AnchorLayout:
                    anchor_x: "left"
                    size_hint_y: None
                    height: avatar.height

                    Image:
                        id: avatar
                        size_hint: None, None
                        size: "56dp", "56dp"
                        source: "data/logo/kivy-icon-256.png"

                MDLabel:
                    text: "WikipediApp"
                    font_style: "Button"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDLabel:
                    text: "tnnfnc@gmail.com"
                    font_style: "Caption"
                    size_hint_y: None
                    height: self.texture_size[1]

                ScrollView:
"""


query_search = """/w/api.php?action=query&format=json&list=search&srsearch=XXXXX&srlimit=20&srinfo=suggestion&srprop=wordcount%7Csnippet%7Csectiontitle"""
query_id = """/w/api.php?action=query&format=json&prop=extracts&pageids=122334&utf8=1"""
query_detail = """/w/api.php?action=query&format=json&prop=extracts&pageids=00000&formatversion=2&explaintext=1&exsectionformat=plain"""
endpoint = """https://it.wikipedia.org"""

class TextArea(ScrollView):
    def __init__(self, **kwargs):
        super(TextArea, self).__init__(**kwargs)

class ListArea(ScrollView):
    def __init__(self, **kwargs):
        super(ListArea, self).__init__(**kwargs)


class SwapListItem(OneLineListItem):
    # text = StringProperty('')
    pageid = StringProperty('')
    def __init__(self, **kwargs):
        super(SwapListItem, self).__init__(**kwargs)

    def on_release(self, *args):
        app = MDApp.get_running_app()
        app.get_wiki_page(self.pageid)


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        """Overwrite for your App """
        self.title = 'Wikypedia Reader'
        #
        self.theme_cls.theme_style = 'Light'
        # Palette
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.primary_hue = '400'
        #
        self.root = Builder.load_string(KV)
        return self.root

    def random_search(self):
        """Search from wikipedia the first 20 occurrences"""
        if self.root.ids.text.text:
            query = (endpoint + query_search).replace('XXXXX', self.root.ids.text.text)
            self.request = UrlRequest(query,
                                      on_success=self.fill_list,
                                      ca_file=certifi.where())


    def fill_list(self, request, response):
        """Output search results in a selectable list"""
        self.root.ids.screen_manager.current = 'search'
        for r in response['query']['search']:
            self.root.ids.list.add_widget(SwapListItem(
                                          text=r['title'],
                                          pageid=str(r['pageid'])))

    def set_text_area(self):
        pass

    def get_wiki_page(self, pageid):
        query = (endpoint + query_detail).replace('00000', pageid)
        self.request = UrlRequest(query,
                                     on_success=self.fill_detail,
                                     ca_file=certifi.where())

    def fill_detail(self, request, response):
        """Output search results in a selectable list"""
        self.root.ids.screen_manager.current = 'display'
        for r in response['query']['pages']:
            # self.root.ids.detail.text = r['extract'][0:2000]
            self.root.ids.detail.text=r['extract']

    def back(self):
        self.root.ids.screen_manager.current = 'search'


if __name__ == '__main__':
    MyApp().run()
