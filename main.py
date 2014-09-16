#!/usr/bin/python
# -*- coding: utf-8 -*-
import kivy
from kivy.uix.popup import Popup
from kivy.uix.settings import Settings
kivy.require('1.0.5')

__version__ = '2.0'

from kivy.config import Config

# Samsung S4 : 1080x1920
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')

## install & run with 
# buildozer android debug deploy run

## see logs with
# adb logcat -s "python"

from kivy.app import App

from categories import CategoriesApp
from thes import ThesApp
from theDetail import TheDetailApp

#from multiprocessing import Pool
from threading import Thread

from datareader import JsonToDataBase

from customscreen import CustomScreenManager, CustomScreen


class AsyncLoader(Thread):
	def __init__(self, callback, *largs, **kwargs):
		super(AsyncLoader, self).__init__(*largs, **kwargs)
		self.daemon = True
		self.quit = False
		self.callback = callback

	def run(self):
		d = JsonToDataBase()
		d.loadData()
		self.callback(loadingDone=True)
		

class Welcome(CustomScreen):
	allCategories = {}
	
	def startLoadingJson(self):
		self.logLabel.text = "Chargement des données..."
		
		loader = AsyncLoader(callback = self.callback_after_loading_json)
		loader.start()
		
		
	def callback_after_loading_json(self, loadingDone):
		if loadingDone:
			self.logLabel.text = "Chargement OK. (%s)" % len(JsonToDataBase().getAllCategories())
		else:
			self.logLabel.text = "Erreur lors du chargement."
		

	def do_enter(self):
		self.manager.go_next()
		self.manager.current_screen.setCategories(JsonToDataBase().getAllCategories())


class WelcomeApp(App):
	
	def build(self):
		manager = CustomScreenManager()
		
		# ajout de l'instance de page d'accueil
		welcomeScreen = Welcome(name='Welcome')
		manager.add_screen(welcomeScreen)
		
		for app in [CategoriesApp(), ThesApp(), TheDetailApp()]:
			app.load_kv()
			manager.add_screen( app.build() )
			
		return manager
	

if __name__ == '__main__':
	WelcomeApp().run()

