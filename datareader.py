#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import urllib2
import sqlite3

URL_LIST_CATEGORY = "http://jc.specs.free.fr/TeaTime/index.php/json/listcategorys/index"
URL_LIST_TEAS_FOR_CATEGORY = "http://jc.specs.free.fr/TeaTime/index.php/json/listteas/forCategory/"
URL_LIST_TEAS = "http://jc.specs.free.fr/TeaTime/index.php/json/listteas/index"


class JsonToDataBase():
	database = None
	
	def __init__(self):
		self.database = 'teatime.sdb'

	
	def loadData(self):
		json_dataCategories = self.fetchCategories(URL_LIST_CATEGORY)
		json_dataTeas = self.fetchTeas(URL_LIST_TEAS)

		self.initalizeDatabase()
		self.insertCategories(json_dataCategories)
		self.insertTeas(json_dataTeas)
		
	def fetchCategories(self, url):
		print "Fetching Category data..."
		data = urllib2.urlopen(url).read()
		json_data = json.loads(data)
		print "Data acquired..."
		return json_data
	
	def fetchTeas(self, url):
		print "Fetching Tea data..."
		data = urllib2.urlopen(url).read()
		json_data = json.loads(data)
		print "Data acquired..."
		return json_data

	def initalizeDatabase(self):
		delete_ttmcat = "delete from ttmcat"
		delete_ttmtea = "delete from ttmtea"
		con = None
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			print "Database intialisation..."
			cur.execute(delete_ttmcat);
			cur.execute(delete_ttmtea);
			con.commit()
		except Error, e:
			print "Error with database: %s" % e
			return False
		finally:
			if con:
				con.close()
	
	def insertCategories(self, json_data):
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			
			print "Data category insertion..."
			for category in json_data.values():
				#print category
				cur.execute("INSERT INTO ttmcat(catidcat, catlblib, cattxdsc) VALUES(?, ?, ?)", (category["catidcat"], category["catlblib"], category["cattxdsc"] ) )
			con.commit()

		except sqlite3.Error, e:
			print "Error with database: %s" % e
			return False
		finally:
			if con:
				con.close()
			print "ok"
		return True
	
	def insertTeas(self, json_data):
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			
			print "Data tea insertion..."
			for tea in json_data.values():
				#print tea
				cur.execute("INSERT INTO ttmtea(teaidthe, tealbnom, teaidcat, tealbdsc, teatxdet, tealbtpi, tealbdos, tealbtpe, tealbmjo) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", 
						(tea["teaidthe"], tea["tealbnom"], tea["teaidcat"], tea["tealbdsc"], tea["teatxdet"], tea["tealbtpi"], tea["tealbdos"], tea["tealbtpe"], tea["tealbmjo"]) )
			con.commit()

		except sqlite3.Error, e:
			print "Error with database: %s" % e
			return False
		finally:
			if con:
				con.close()
			print "ok"
		return True

	def getAllCategories(self):
		allCategories = {}
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			cur.execute("SELECT catidcat, catlblib, cattxdsc FROM ttmcat")
			rows = cur.fetchall()
			for row in rows:
				allCategories[row[0]] = {"catidcat":row[0] , "catlblib":row[1], "cattxdsc":row[2]}
		except sqlite3.Error, e:
			print "Error with database: %s" % e
		finally:
			if con:
				con.close()
			#print "ok"
		return allCategories

	def getAllTeasForCategory(self, categoryId):
		allTeas = {}
		try:
			con = sqlite3.connect(self.database)
			cur = con.cursor()
			cur.execute("SELECT teaidthe, tealbnom, teaidcat, tealbdsc, teatxdet, tealbtpi, tealbdos, tealbtpe, tealbmjo FROM ttmtea where teaidcat = ?", (categoryId,) )
			rows = cur.fetchall()
			for row in rows:
				allTeas[row[0]] = {"teaidthe":row[0] , "tealbnom":row[1], "teaidcat":row[2],
								"tealbdsc":row[3] , "teatxdet":row[4], "tealbtpi":row[5],
								"tealbdos":row[6] , "tealbtpe":row[7], "tealbmjo":row[8]
								}
		except sqlite3.Error, e:
			print "Error with database: %s" % e
		finally:
			if con:
				con.close()
			#print "ok"
		return allTeas
