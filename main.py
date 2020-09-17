import kivy
from kivy.lang.builder import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.rst import RstDocument
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox
from kivymd.uix.list import OneLineListItem
import certifi
import json

endpoint = """https://it.wikipedia.org"""
query_search = """/w/api.php?action=query&format=json&list=search&srsearch=XXXXX&srlimit=20&srinfo=suggestion&srprop=wordcount%7Csnippet%7Csectiontitle"""
query_id = """/w/api.php?action=query&format=json&prop=extracts&pageids=122334&utf8=1"""
query_detail = """/w/api.php?action=query&format=json&prop=extracts&pageids=00000&formatversion=2&explaintext=1&exsectionformat=plain"""

class ContentNavigationDrawer(BoxLayout):
    pass

class SwapListItem(OneLineListItem):
    pageid = StringProperty('')

    def __init__(self, **kwargs):
        super(SwapListItem, self).__init__(**kwargs)

    def on_release(self, *args):
        app = MDApp.get_running_app()
        app.get_wiki_page(self.pageid)


class WikiwebApp(MDApp):
    def __init__(self, **kwargs):
        super(WikiwebApp, self).__init__(**kwargs)

    def build(self):
        """Overwrite for your App """
        self.title = 'Wikipedia Reader'
        #
        self.theme_cls.theme_style = 'Light'
        # Palette
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
        self.root.ids.screen_manager.current = 'search'
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
        self.root.ids.screen_manager.current = 'display'
        for r in response['query']['pages']:
            # self.root.ids.detail.text = r['extract'][0:2000]
            self.root.ids.detail.text=r['extract']

    def back(self):
        self.root.ids.screen_manager.current = 'search'


# if __name__ == '__main__':
WikiwebApp().run()
