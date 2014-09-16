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

from customscreen import CustomScreen

#
Builder.load_string("""
[CustomListItemCategories@SelectableView+BoxLayout]:
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
	
	# Text of item
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

class Categories(CustomScreen):
	categories = None
	def __init__(self, **kwarg):
		super(Categories, self).__init__(**kwarg)
		#prepare display
		self.setCategories([])
		self.updateDisplay()
		
	def updateDisplay(self):
		list_item_args_converter = \
			lambda row_index, obj: {'text': self.categories[obj]['catlblib'],
									'index': row_index,
									'id': "categorieindex_%d" % row_index, 
									'is_selected': False,
									'size_hint_y': None,
									'height': 25}
		
		my_adapter = ListAdapter(data = self.categories,
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemCategories')
		
		my_adapter.bind(on_selection_change=self.categorie_changed)
		self.containerListView.adapter = my_adapter

	def categorie_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		categorieId = adapter.data[adapter.selection[0].parent.index]
		categorieSelectionnee = self.categories[categorieId]
		# pour le graphisme, ne pas changer la couleur du bouton
		adapter.selection[0].deselect()
		
		self.manager.go_next()
		self.manager.current_screen.setCurrentCategorie( categorieSelectionnee )
		
		
	def setCategories(self, data):
		self.categories = data
		self.logLabel.text = "Nombre de catégories : %s" % len(self.categories)
		self.updateDisplay()
		
		
class CategoriesApp(App):
		
	def build(self):
		return Categories(name = 'Categories')
	
