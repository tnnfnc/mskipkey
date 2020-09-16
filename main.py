import kivy
from kivy.lang.builder import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox
from kivymd.uix.list import OneLineListItem
import certifi
import json

KV1 = """
Screen:
    ScrollView:
    MDRectangleFlatButton:
        text: 'Button 1'
        pos_hint: {'x': 0.1, 'y': 0.9}
        md_bg_color: app.theme_cls.primary_dark

    MDRectangleFlatButton:
        pos_hint: {'x': 0.1, 'y': 0.5}
        text: 'Button 2'
        md_bg_color: app.theme_cls.primary_dark
"""

KV = """
Screen:

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

        BoxLayout:
            id: container
            orientation: 'vertical'
            height: self.minimum_height

<TextArea>:
    MDLabel:
        id: detail
        size_hint_y: None
        padding_x: 0
        text: 'Welcome to Wikipedia.net'
        height: self.texture_size[1]

<ListArea>:
    MDList:
        id: list
        padding: 0
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


class SwapListItem(MDCardSwipe):
    text = StringProperty('')
    pageid = StringProperty('')
    def __init__(self, **kwargs):
        super(SwapListItem, self).__init__(**kwargs)
        md_lb = MDCardSwipeLayerBox()
        md_fb = MDCardSwipeFrontBox()
        list_item = OneLineListItem(_no_ripple_effect=True)
        md_fb.add_widget(list_item)
        md_lb.add_widget(md_fb)
        #
        self.add_widget(md_lb)
        list_item.text = self.text
        

    def on_swipe_complete(self, *args):
        if self.state == 'opened':
            print(self.text, self.pageid)
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
        self.container = self.root.ids.container
        self.container.add_widget(TextArea())
        return self.root

    def random_search(self):
        """Search from wikipedia the first 20 occurrences"""
        # self.root.ids.mdlab.text = 'Loading data from wikipedia...'
        if self.root.ids.text.text:
            query = (endpoint + query_search).replace('XXXXX', self.root.ids.text.text)
            self.request = UrlRequest(query,
                                        on_success=self.fill_list,
                                        ca_file=certifi.where())


    def fill_list(self, request, response):
        """Output search results in a selectable list"""
        if len(self.container.children) > 0:
            self.container.remove_widget(self.container.children[0])
        list_area = ListArea()
        self.container.add_widget(list_area)
        for r in response['query']['search']:
            # print('-->', r['title'], r['pageid'])
            # self.root.ids.list.add_widget(SwapListItem(height='40dp', text=r['title'], pageid=str(r['pageid'])))
            list_area.ids.list.add_widget(SwapListItem(height='40dp', text=r['title'], pageid=str(r['pageid'])))

    def set_text_area(self):
        pass

    def get_wiki_page(self, pageid):
        query = (endpoint + query_detail).replace('00000', pageid)
        self.request = UrlRequest(query,
                                     on_success=self.fill_detail,
                                     ca_file=certifi.where())

    def fill_detail(self, request, response):
        """Output search results in a selectable list"""
        if len(self.container.children) > 0:
            self.container.remove_widget(self.container.children[0])
        text_area = TextArea()
        for r in response['query']['pages']:
            # print('-->', r['title'], r['extract'])
            text_area.ids.detail.text = r['extract']
        self.container.add_widget(text_area)


if __name__ == '__main__':
    MyApp().run()
