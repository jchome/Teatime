#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Nov 11, 2013

@author: julien
'''

import kivy
kivy.require('1.0.5')

from kivy.app import App

from customscreen import CustomScreen

class TheDetail(CustomScreen):
	
	def chargeInfos(self, dataDict, nameOfCategorie):
		self.nomcategorieLabel.text = "TeaTime > %s" % nameOfCategorie
		
		self.detail_nom.text = dataDict["tealbnom"]
		self.detail_temp.text = dataDict["tealbtpe"]
		self.detail_duree.text = dataDict["tealbtpi"]
		self.detail_dose.text = dataDict["tealbdos"]
		self.detail_description.text = dataDict["teatxdet"]
		
		self.scrollableContent.bind(minimum_height=self.scrollableContent.setter('height'))
		
		
		
class TheDetailApp(App):
		
	def build(self, ):
		return TheDetail(name='TheDetail')

	