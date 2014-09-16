#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 11, 2013

@author: julien
'''


import kivy
kivy.require('1.0.5')

from kivy.app import App

from kivy.adapters.listadapter import ListAdapter
from kivy.lang import Builder

from datareader import JsonToDataBase
from customscreen import CustomScreen

#
Builder.load_string("""
[CustomListItemThes@SelectableView+BoxLayout]:
	orientation: 'horizontal'
	spacing: '10sp'
	padding: (sp(20), 0)
	size_hint_y: None
	height: '100sp'
	index: ctx.index
	canvas.before:
		Color:
			rgba: 1,1,1, 1
		Rectangle:
			source: "images/bg-list-blanc.png"
			pos: self.pos
			size: self.size
	
	ListItemButton:
		selected_color: 0,0,0, 0
		deselected_color: 1,1,1, 0
		background_color: 1,1,1, 0
		background_normal: ""
		background_down: ""
		
		halign: 'left'
		text_size: (self.width , None)
		color: [0,0,0, 0.95]
		text: ctx.text
		font_name: "font/Ubuntu-L.ttf"
		font_size: '22sp'
	
	# Chevron
	ListItemButton:
		text: " "
		selected_color: 1,1,1, 0.75
		deselected_color: 1,1,1, 0.5
		background_color: 1,1,1, 0.25
		
		background_normal: "images/appbar.chevron.right.png"
		background_down: ""
		size_hint_x: None
		width: sp(30)
		border: 0,0,0,0
""")

class Thes(CustomScreen):
	currentCategorie = None
	def __init__(self, **kwargs):
		super(Thes, self).__init__(**kwargs)
		# initialisation avec liste vide
		self.initializeListAdapter( [] )
	
	
	def initializeListAdapter(self, dataObject):
		list_item_args_converter = \
			lambda row_index, obj: {'text': self.currentCategorie["teas"][obj]['tealbnom'],
									'id': "theindex_%d" % row_index, 
									'is_selected': False,
									'size_hint_y': None,
									'height': 25}
			
		self.my_adapter = ListAdapter(data = dataObject,
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemThes') 
		
		self.my_adapter.bind(on_selection_change=self.the_changed)
		self.containerListView.adapter = self.my_adapter
		
		
	def the_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		
		theId = adapter.data[adapter.selection[0].parent.index]
		theSelectionne = self.currentCategorie["teas"][theId]
		adapter.selection[0].deselect()
		
		self.manager.go_next()
		self.manager.current_screen.chargeInfos(theSelectionne, self.currentCategorie["catlblib"])
		
	def setCurrentCategorie(self, categorie):
		'''Mise à jour de la liste de thés disponibles
		'''
		categoryId = categorie['catidcat']
		categorie["teas"] = JsonToDataBase().getAllTeasForCategory(categoryId)
		
		self.currentCategorie = categorie
		self.nomcategorieLabel.text = "TeaTime > %s" % self.currentCategorie["catlblib"]
		self.initializeListAdapter( self.currentCategorie["teas"] )
		self.logLabel.text = "Nombre de thés: %s" % len(self.currentCategorie["teas"])
		
		
class ThesApp(App):
		
	def build(self):
		return Thes(name = 'Thes')
		
if __name__ == '__main__':
	ThesApp().run()
