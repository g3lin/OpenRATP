# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:38:20 2017

@author: gelina
"""

import csv
import datetime
import urllib.request
import urllib
import json
import math
import ast


def valid_parstation_parjour(FICHIER):
	"""
     Compte le nombre de validations total pour n'importe quel jour
     donné en une sation donnée
 
     Args:
         le fichier csv des données
 
     Returns:
         dictionaire des données

	 >>> d = valid_parstation_parjour('validations.csv'):
     >>> d['2017-05-10']['LES HALLES']
	 41413
     """
	with open(FICHIER, 'r') as f:
		r = csv.reader(f,delimiter=';')
		l = list(r) # l'itérable est converti en liste
		
		d = dict() # on costruit un dictionnaire qui mettra en relation un jour et toutes les données de ce jour
		for line in l[1:]:
		     if(line[0] in d):
		             d[line[0]]+= [[line[4],line[6],line[7]]] #on ajoute si la date est deja dans le dictionaire
		     else:
		             d[line[0]]= [[line[4],line[6],line[7]]] # on crée l'entrée sinon
		
		for date in d.keys():
		     s = dict() # on crée un nouveau dictionaire par jour qui assosiera les stations et leur nbre de visiteur
		     for line in d[date]:
		         if(line[0] in s):
		                 if (line[2] == 'Moins de 5'):
		                 	s[line[0]]+=4
		                 	# le STIF met la mention moins de 5 pour des raisons d'anonymat
		                 else:
		                 	s[line[0]]+=int(line[2]) #on ajoute si le dictionnaire contient deja la station pour ce jour
		         else:
		                 if (line[2] == 'Moins de 5'):
		                 	s[line[0]]=4
		                 	# le STIF met la mention moins de 5 pour des raisons d'anonymat
		                 else:
		                 	s[line[0]]=int(line[2]) # on definit la station dans le dictionnaire sinon
		     d[date] = s 
		return d











def weekdaydetection(dico):
	"""
     sépare le jeu de donnée en 2 : les jours de la semaine et les autres
 
     Args:
         le dictionaire créé par la fonction valid_parstation_parjour
 
     Returns:
         liste de 2 dictionaires des données
         le 1er element (l[0]) de la liste est les jours de le semanine
         le 2eme (l[1]) les jours en weekend

	 >>> d = valid_parstation_parjour('validations.csv'):
     >>> l = weekdaydetection(d)
	 >>> '2017-01-01' in l[0]
	 False
	 >>> '2017-01-02' in l[1]
	 False
	 >>> '2017-01-03' in l[0]
	 True
	 >>> '2017-02-12' in l[1]
	 True

     """
	l = list()
	weekday = dict()
	weekend = dict()
	#On crée ici deux dictionaires et une liste
	# Les deux dictionaires contiennent soit les elements des jours qui tombent pendant une semeine ou ceux qui tombent un weekend

	for day in dico.keys():
		dayofweek = datetime.date(int(day[0:4]),int(day[5:7]),int(day[8:10])).isoweekday()
		# pour chaque date on va extraire de la string l'année, le mois et le jour
		# on construit avec cela un objet date et on appelle son attribut isoweekday ( pour lundi, 7 pour dimanche)


		if dayofweek < 6: 
			weekday[day] = dico[day]
			#si c'est un jour de semaine, le ranger dans le dictionnaire semaine

		else :
			weekend[day] = dico[day]
			# si c'est un jour de WE , le ranger dans le dico weekend

	l.append(weekday)
	l.append(weekend)

	#on met les deux dico dans l et on retourne la liste
	return l



def moyennesurannee(dico):

	moyennesta = dict()
	for day in dico.keys():
		for station in dico[day].keys():
			if station in moyennesta:
				moyennesta[station] += dico[day][station]
			else:
				moyennesta[station] = dico[day][station]

	for station in moyennesta.keys():
		moyennesta[station] = math.ceil(moyennesta[station]/len(dico.keys()))

	return moyennesta


def split_hist_data(moyennesta, limite):
	l = list()
	moy1 = dict()
	moy2 = dict()
	l=[moy1]+[moy2]
	for data in moyennesta.keys():
		if moyennesta[data] < limite :
			moy1[data] = moyennesta[data]
		else:
			moy2[data] = moyennesta[data]
	return l




def build_stations_coordonates(filegeo):

	
	with open(filegeo, 'r') as f:
		r = csv.reader(f,delimiter=';')
		l = list(r) # l'itérable est converti en liste
		geos = dict()
		for station in l[1:]:
			lat = ast.literal_eval(station[1])['coordinates'][0]
			longi = ast.literal_eval(station[1])['coordinates'][1]
			geos[station[7]] = [lat, longi]
		return geos






def build_map_data(geostation,moyennesta):
	# construit un dictionaire associant un tableau [lon, lat] avec le nombre de visiteurs
	# cela est fait pour chaque station

	mapdata = list() 
	for station in moyennesta.keys():
		data = moyennesta[station]
		if station in geostation.keys():
		
			geo = geostation[station]
			mapdata.append([data,geo])
	return mapdata
