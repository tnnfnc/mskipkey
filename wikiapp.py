# 
import kivy
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
import certifi
# import json

__version__ = "0.0.3"

endpoint = """https://it.wikipedia.org"""
query_search = """/w/api.php?action=query&format=json&list=search&srsearch=XXXXX&srlimit=20&srinfo=suggestion&srprop=wordcount%7Csnippet%7Csectiontitle"""
query_id = """/w/api.php?action=query&format=json&prop=extracts&pageids=122334&utf8=1"""
query_detail = """/w/api.php?action=query&format=json&prop=extracts&pageids=00000&formatversion=2&explaintext=1&exsectionformat=plain"""

# KV = '''
# <ContentNavigationDrawer>:

#     ScrollView:

#         MDList:

#             OneLineListItem:
#                 text: "Search"
#                 on_press:
#                     root.nav_drawer.set_state("close")
#                     root.screen_manager.current = "scr 1"

#             OneLineListItem:
#                 text: "Detail"
#                 on_press:
#                     root.nav_drawer.set_state("close")
#                     root.screen_manager.current = "scr 2"


# Screen:
#     BoxLayout:
#         orientation: 'vertical'
#         MDToolbar:
#             id: toolbar
#             pos_hint: {"top": 1}
#             elevation: 10
#             title: "Menu"
#             left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

#         NavigationLayout:
#             x: toolbar.height

#             ScreenManager:
#                 id: screen_manager

#                 Screen:
#                     name: "scr 1"
#                     BoxLayout:
#                         orientation: 'vertical'

#                         MDTextField:
#                             id: text
#                             hint_text: "Input search"
#                             helper_text: "Type here what you want to find"
#                             helper_text_mode: "on_focus"

#                         MDRaisedButton:
#                             id: find
#                             text: 'Find'
#                             size_hint_x: 1
#                             on_press: app.random_search()

#                         ScrollView:
#                             MDList:
#                                 id: list


#                 Screen:
#                     name: "scr 2"
#                     BoxLayout:
#                         orientation: 'vertical'
#                         MDLabel:
#                             id: selected_title
#                             text: 'Search title'
#                             font_style: "Button"
#                             size_hint: 1, None

#                         ScrollView:
#                             MDLabel:
#                                 id: detail
#                                 text: 'Detail wikipedia found here!'
#                                 padding_x: '10dp'
#                                 size_hint_y: None
#                                 height: self.texture_size[1]

#             MDNavigationDrawer:
#                 id: nav_drawer

#                 ContentNavigationDrawer:
#                     screen_manager: screen_manager
#                     nav_drawer: nav_drawer
# '''

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class AdaptableLabel(MDLabel):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class SwapListItem(OneLineListItem):
    pageid = StringProperty('')

    def __init__(self, **kwargs):
        super(SwapListItem, self).__init__(**kwargs)

    def on_release(self, *args):
        app = MDApp.get_running_app()
        app.get_wiki_page(self.pageid)


class WikiwebApp(MDApp):
    def build(self):
        self.title = 'Wikipedia Reader'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.primary_hue = '400'
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
        self.root.ids.screen_manager.current = 'scr 1'
        for r in response['query']['search']:
            self.root.ids.list.add_widget(SwapListItem(
                                          text=r['title'],
                                          pageid=str(r['pageid'])))

    def get_wiki_page(self, pageid):
        query = (endpoint + query_detail).replace('00000', pageid)
        self.request = UrlRequest(query,
                                     on_success=self.fill_detail,
                                     ca_file=certifi.where())

    def fill_detail(self, request, response):
        """Output search results in a selectable list"""
        self.root.ids.long_text.clear_widgets()
        self.root.ids.screen_manager.current = 'scr 2'
        t = ''
        for r in response['query']['pages']:
            # self.root.ids.detail.text = r['extract'][0:2000]
            self.root.ids.selected_title.text = r['title']
            t = t + ' ' + r['extract']
        maxbuffer = 2000
        text = ''
        while len(t) > 0:
            if len(t) > maxbuffer:
                text = text + t[:maxbuffer]
                t = t[maxbuffer:]
            else:
                text = text + t
                t = ''
            label = AdaptableLabel(text=text)
            self.root.ids.long_text.add_widget(label)
            # self.root.ids.long_text.height = self.root.ids.long_text.height + label.height


    def back(self):
        self.root.ids.screen_manager.current = 'scr 1'


if __name__ == '__main__':
    WikiwebApp().run()
