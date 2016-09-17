#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os, sqlite3, socket, string, time, datetime
import xml.etree.ElementTree as ET
from lxml import etree
from flask import *
import subprocess
app = Flask(__name__)

def addCorsHeaders(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, DELETE, PUT'
    resp.headers['Access-Control-Max-Age'] = '21600'
    resp.headers['Access-Control-Allow-Headers'] = 'accept, origin, authorization, content-type'

##########################################################
# CREATION DES TABLES POI/TRANSORTS/TRANSPORT_POI/STATUS #
##########################################################
def create_table():
	dbConnection = sqlite3.connect('bdd.db')
	QueryCurs = dbConnection.cursor()
	QueryCurs.execute("""
			CREATE TABLE IF NOT EXISTS Poi(
				Id_poi         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				Ville_poi      TEXT UNIQUE,
				Kind_poi       TEXT ,
				Latitude_poi   REAL ,
				Longitude_poi  REAL 
			);
			""")
	QueryCurs.execute("""
			CREATE TABLE IF NOT EXISTS Transport(
				Id_transport               INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
				Date_transport             NUMERIC ,
				Drone_latitude_transport   REAL ,
				Drone_longitude_transport  REAL ,
				Id_status                  INTEGER ,
				Drone_timestamp            INTEGER,
				Id_algo			   INTEGER,
				FOREIGN KEY (id_status) REFERENCES Status(id_status)
			);
			""")
	QueryCurs.execute("""		
			CREATE TABLE IF NOT EXISTS Status(
				Id_status   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
				Nom_status  TEXT UNIQUE
			);
			""")
	QueryCurs.execute("""		
			CREATE TABLE IF NOT EXISTS Transport_Poi(
				Id_poi  INTEGER NOT NULL ,
				Id_transport  INTEGER NOT NULL ,
				PRIMARY KEY (ID_poi,ID_transport)
				FOREIGN KEY (ID_poi) REFERENCES POI(ID_poi),
				FOREIGN KEY (ID_transport) REFERENCES TRANSPORT(ID_transport)
			);
			""")
	QueryCurs.execute("""
			CREATE TABLE IF NOT EXISTS Route_Poi(
				Id_poi                 Int ,
				Id_transport           Int ,
				Order_num              Int
			);
			""")	
	dbConnection.commit()	
	
	QueryCurs.execute("""
				INSERT OR IGNORE INTO Status VALUES(null, "todo")	
			""")
	QueryCurs.execute("""
				INSERT OR IGNORE INTO Status VALUES(null, "enroute")	
			""")		
	QueryCurs.execute("""
				INSERT OR IGNORE INTO Status VALUES(null, "done")	
			""")		
	dbConnection.commit()			
	dbConnection.close()
			
	

create_table()	

@app.route('/', methods=['GET'])
def redirect_to_poi():
    return redirect('/static/index.html')

##########################################################
#                 LISTER LES LOCATIONS (POI)             #
##########################################################
@app.route("/locations", methods=['GET'])
def get_location():
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  
  resp = make_response()
  resp.mimetype = 'application/json'
  
  # Headers CORS
  addCorsHeaders(resp)
  resp.status_code = 200
  
  # On récupère tous les POI
  for row in QueryCursor.execute("SELECT * FROM Poi"):
  	resp.data += '{ "id" : ' + str(row[0]) + ', "name" : "' + str(row[1].encode("utf-8")) + '", "kind" : "' + str(row[2]) + '", "coords" : { "lat" : ' + str(row[3]) + ', "lon" : ' + str(row[4]) + '}},'
  	
  	
  # On supprime la dernière ,	
  resp.data = "[" + resp.data[0:-1] + "]"
 
  # Déconnexion
  dbConnection.close()
  
  return resp
 
##########################################################
#          AJOUTER UNE NOUVELLE LOCATION (POI)           #
##########################################################
@app.route("/locations", methods=['POST'])
def poster_location():  
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  
  resp = make_response()
  resp.status_code = 201
  
  print request.data
  
  # On décode le JSON en dict python
  try:
	jsonRequest = json.loads(request.data)
  except:
  	resp.statusCode = 400
        resp.data = '"Bad format"' + request.data
        dbConnection.close()
        return resp
  
  # Requete pour ajouter  un POI
  query = "INSERT OR IGNORE INTO Poi VALUES (null, '" + str(jsonRequest["name"].encode("utf-8")) + "', '" + str(jsonRequest["kind"].encode("utf-8")) + "', " + str(jsonRequest["coord"]["lat"]) + ", " + str(jsonRequest["coord"]["lon"]) + ")"

  # On lance la requete
  QueryCursor.execute(query)  
  dbConnection.commit()

  # Déconnexion
  dbConnection.close()
    
  # On met à jour l'entête location
  resp.headers["Location"] = str(jsonRequest["name"].encode("utf-8"))
  
  return resp

  
 
##########################################################
#            RECUPERER UNE LOCATION PAR (POI)            #
##########################################################
@app.route("/locations/<int:locationId>", methods=['GET'])
def get_info_location(locationId):  
  # Connexion à la BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  
  # Création de la réponse
  resp = make_response()
  resp.mimetype = 'application/json'
  
  # Headers CORS
  addCorsHeaders(resp)

  # On récupère le Poi avec l'id demandé
  QueryCursor.execute("SELECT * FROM Poi WHERE id_poi = " + str(locationId))
  result = QueryCursor.fetchone()
  
  # Si on a un résultat
  if result:
  	  # On crée la réponse
	  resp.status_code = 200  
	  resp.data += '{ "id" : ' + str(result[0]) + ', "name" : "' + str(result[1].encode("utf-8") )+ '", "kind" : "' + str(result[2].encode("utf-8") ) + '", "coord" : { "lat" : ' + str(result[3]) + ', "lon" : ' + str(result[4]) + '}}'
  # Si le Poi demandé n'existe pas
  else:
  	  resp.status_code = 404
  
  # Déconnexion BDD
  dbConnection.close()
  
  return resp
  
##########################################################
#            SUPPRIMER UNE LOCATION PAR (POI)            #
##########################################################
@app.route("/locations/<int:locationId>", methods=['DELETE'])
def delete_location(locationId):  
  # Connexion à la BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  
  # Création de la réponse
  resp = make_response()
  resp.mimetype = 'application/json'
  
  # Headers CORS
  addCorsHeaders(resp)
  
  # On récupère le Poi avec l'id demandé
  QueryCursor.execute("SELECT * FROM Poi WHERE id_poi = " + str(locationId))
  result = QueryCursor.fetchone()
  
  QueryCursor.execute("SELECT * FROM Transport_Poi where id_poi = " + str(locationId))
  resultTransportPoi = QueryCursor.fetchone()
  
  
  # Si le Poi existe
  if result:
  	  # Si le Poi appartient à un transport on renvoie un message d'érreur
  	  if resultTransportPoi:
  	  	resp.status_code = 405  	  
  	  # Sinon on le supprime
  	  else:
		  resp.status_code = 204
		  QueryCursor.execute("DELETE FROM Poi WHERE id_poi = " + str(locationId))
		  dbConnection.commit()
  # S'il n'existe pas erreur 404
  else:
  	  resp.status_code = 404
  
  # Déconnexion BDD  
  dbConnection.close()
  
  return resp

  
##########################################################
#                    LISTER LES TRANSPORTS               #
##########################################################
@app.route("/transports", methods=['GET'])
def get_transports():  
  status = request.args.get('status', '')  
  order = request.args.get('order', '')
  limit =request.args.get('limit', '')
  
  if len(order) < 1:
  	order = "recent-first"
  	
  if len(status) < 1:
  	status = "any"
  
  if len(limit) < 1:
  	limit = "20"
  	
  # Connexion BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  QueryCursor2 = dbConnection.cursor()
  
  # Création de la réponse
  resp = make_response()
  resp.mimetype = 'application/json'
  
  # Création tableau pour associer les status à leur identifiants et vice versa
  statusList = {}
  statusListIdToText = {}
  for row in QueryCursor.execute("SELECT * FROM Status"):
  	statusList[row[1]] = row[0]
	statusListIdToText[row[0]] = row[1]
  
  # On crée la requete pour récuperer tous les transports avec prise en compte des paramètres limit, order et status
  query = "SELECT * FROM Transport "
  
  if status != "any":
  	query += " WHERE Id_status = " + str(statusList[str(status)])
  	
  query += " ORDER BY Date_transport "
  
  if order == "recent-first":
  	query += "DESC "
  else:
  	query += "ASC "
  	
  query += "LIMIT " + str(limit)
  
  #print str(statusList[str(status)])
  response = ""

  
  for row in QueryCursor.execute(query):
	locations = "["
	
	# On récupère l'id des POI associés à ce transport
	for row2 in QueryCursor2.execute("SELECT * FROM Transport_Poi WHERE Id_transport=" + str(row[0])):
		locations += str(row2[0]) + ","
	
	# On supprime la dernière , et on ferme le tableau	
	locations = locations[0:-1] + "]"

	# Si le status = todo ou = done on ne renvoie pas les informations relatives au drone
	if str(statusListIdToText[row[4]]) == "todo" or str(statusListIdToText[row[4]]) == "done":
		response += '{ "id": ' + str(row[0]) + ', "location": ' + locations + ', "status": "' + str(statusListIdToText[row[4]]) + '"},'

	# Si le status=enroute on renvoie en plus les informations relatives au drone
	elif str(statusListIdToText[row[4]]) == "enroute":
		response +=  '{ "id": ' + str(row[0]) + ', "location": ' + locations + ', "status": "' + str(statusListIdToText[row[4]]) + '", "drone-location": { "timestamp" : ' + str(row[5]) + ', "coord": { "lat" : ' + str(row[2]) + ', "lon": ' + str(row[3]) + '}}},'

    # On construit la réponse et on supprime la dernière ,
  response = "[" + response[0:-1] + "]"
  
  # On renvoie la réponse
  resp.data = response
  
  dbConnection.close()
  
  return resp

##########################################################
#                    AJOUTER UN TRANSPORT                #
##########################################################
@app.route("/transports", methods=['POST'])
def post_transports():  
  # Connexion BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  
  # Création de la réponse
  resp = make_response()
  
  # Création tableau pour associer les status à leur identifiants et vice versa
  statusListTextToId = {}
  for row in QueryCursor.execute("SELECT * FROM Status"):
  	statusListTextToId[row[1]] = row[0]
  
  # Si on arrive pas a decoder les donnees JSON recues on renvoit une erreur 400
  try:
	  jsonResponse = json.loads(request.data)
  except:
  	resp.status_code = 400
  	dbConnection.close()	
  	return resp
  
  # On transforme la valeur locations en list python
  poiList = json.loads(str(jsonResponse["locations"]))
  
  # Si on recoit moins de 3 POI ou plus de 7 POI on renvoie une erreur 400
  if len(poiList) < 3 or len(poiList) > 7:
  	resp.status_code = 400
  	dbConnection.close()
  	return resp
  	
  print poiList
  	
  # On verifie que les ids des POI recus existent bien, sinon on renvoie une erreur 404
  for poiId in poiList:
  	#print poiId
  	QueryCursor.execute("SELECT * FROM Poi WHERE Id_poi = " + str(poiId))
  	result = QueryCursor.fetchone()
  	if result == None:
  		resp.status_code = 404
		dbConnection.close()
  		return resp
  
  # On recupere le premier POI pour assigner la position du drone aux coordonnees du premier POI
  QueryCursor.execute("SELECT * FROM Poi WHERE Id_poi = " + str(poiList[0]))
  firstPoi = QueryCursor.fetchone()

  # On ajoute le transport avec les coordonnes du premier POI en tant que position de depart du drone
  if jsonResponse["algo"] != None:
	query = "INSERT INTO Transport Values(null, '" + time.strftime('%Y-%m-%d %H:%M:%S') + "', 22.3, 66.4, " + str(statusListTextToId["todo"]) + ", 0, " + str(int(jsonResponse["algo"])-1) + ")"
  else:
  	query = "INSERT INTO Transport Values(null, '" + time.strftime('%Y-%m-%d %H:%M:%S') + "', 22.3, 66.4, " + str(statusListTextToId["todo"]) + ", 0, 0)"

  result = QueryCursor.execute(query)	  
  dbConnection.commit()
  
  # On recupere l'ID du transport qu'on vient d'ajouter
  transportLastId = QueryCursor.lastrowid
  
  print "Last Transport Id : " + str(transportLastId)

  # On cree une entree dans la table Transport_Poi pour chaque POI recu
  for poiId in poiList:
	  QueryCursor.execute("INSERT INTO Transport_Poi VALUES(" + str(poiId) + ", " + str(transportLastId) + ")")
	  dbConnection.commit()
  
  resp.status_code = 201
  dbConnection.close()
  return resp

##########################################################
#            RECUPERER INFOS TRANSPORT PAR ID            #
##########################################################
@app.route("/transports/<int:transportId>", methods=['GET'])
def get_info_transports(transportId): 
  # Connexion BDD 
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  
  # On crée la réponse
  resp = make_response()
  resp.mimetype = 'application/json'
  
  # Création tableau pour associer les status à leur identifiants et vice versa
  statusListIdToText = {}
  for row in QueryCursor.execute("SELECT * FROM Status"):
  	statusListIdToText[row[0]] = row[1]
  	
  print "here"
  print str(transportId)	

  # On récupère le transport avec l'id demandé
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_transport = " + str(transportId))
  result = QueryCursor.fetchone()
  
  # Si le transport n'existe pas, erreur 404
  if result == None:
      resp.status_code = 404
      return resp

  # On récupère les POI associés à ce transport
  locations = "["

  for data in QueryCursor.execute("SELECT ID_poi FROM Transport_Poi WHERE Id_transport = " +str(transportId)):
    locations += str(data[0]) + ","

  locations = locations[0:-1] + "]"

  # On remplit les donnés à renvoyer en json
  resp.data += '{ "id": ' + str(result[0]) + ', "location": ' + str(locations) + ', "status": "' + str(statusListIdToText[result[4]]) + '", "drone-location": { "timestamp" : ' + str(result[5]) + ', "coord": { "lat" : ' + str(result[2]) + ', "lon": ' + str(result[3]) + '}}}'
  
  resp.status_code = 200

  return resp
  
##########################################################
#            MISE A JOUR DE LA POSITION DU DRONE         #
##########################################################
@app.route("/transports/<int:transportId>", methods=['PUT'])
def get_location_drone(transportId):  
  # Connexion BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  QueryCursor2 = dbConnection.cursor()
  
  # On crée la réponse
  resp = make_response()
  resp.mimetype = 'application/json'

  # On essaie de décoder les informations JSON reçues
  try:
	jsonResponse = json.loads(request.data)
  # Erreur 404 si on ne réussit pas
  except:
  	resp.status_code = 404
  	dbConnection.close()
  	return resp
  
  
  # On récupère tous les transports
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_transport = " + str(transportId))
  result_transport = QueryCursor.fetchone()
  
  # Si le transport n'existe pas
  if result_transport == None:
      resp.status_code = 404
      dbConnection.close()
      return resp
  
  # On récupère l'id du status enroute
  enroute_status_id = None
  done_status_id = None
  longitude = 0.0
  latitude = 0.0
  
  # On associe les ids des status à leur texte
  statusList = {}
  for row in QueryCursor.execute("SELECT * FROM Status"):
  	statusList[row[0]] = row[1]    
  	if row[1] == "enroute":
	  	enroute_status_id = row[0]
	elif row[1] == "done":
		done_status_id = row[0]

  # On récupère le dernier POI (Destination FINALE)
  QueryCursor.execute("SELECT * FROM Route_Poi WHERE Id_transport=" + str(transportId) + " ORDER BY Order_num DESC")
  result_route_poi = QueryCursor.fetchone()
  
  if result_route_poi != None:
  	QueryCursor2.execute("SELECT * FROM Poi where Id_poi=" + str(result_route_poi[0]))
  	result_poi = QueryCursor2.fetchone()
  	latitude = float(result_poi[3])
	longitude = float(result_poi[4])
  
  print float(jsonResponse["drone_location"]["coord"]["lon"]) - longitude

  if ((float(jsonResponse["drone_location"]["coord"]["lon"]) - longitude) <= 0.0001) and ((float(jsonResponse["drone_location"]["coord"]["lat"]) - latitude) <= 0.0001):
	  # On met à jour la position du drone, et son status passe à "done" 
	  QueryCursor.execute("UPDATE Transport SET Drone_longitude_transport=" + str(jsonResponse["drone_location"]["coord"]["lon"]) + ", Drone_latitude_transport=" + str(jsonResponse["drone_location"]["coord"]["lat"]) + ", Id_status=" + str(done_status_id) + ", Drone_timestamp=" + str(int(time.time())) + " WHERE id_transport=" + str(transportId))
  	
  else:
	  # On met à jour la position du drone, et son status passe à "enroute" 
	  QueryCursor.execute("UPDATE Transport SET Drone_longitude_transport=" + str(jsonResponse["drone_location"]["coord"]["lon"]) + ", Drone_latitude_transport=" + str(jsonResponse["drone_location"]["coord"]["lat"]) + ", Id_status=" + str(enroute_status_id) + ", Drone_timestamp=" + str(int(time.time())) + " WHERE id_transport=" + str(transportId))

  # On envoie la requete
  dbConnection.commit()  

  resp.status_code = 200
  
  # Création de la chaine contenant l'id des POI
  locations = "["

  for data in QueryCursor.execute("SELECT Id_poi FROM Transport_Poi WHERE Id_transport = " +str(transportId)):
    locations += str(data[0]) + ","

  locations = locations[0:-1] + "]"
  
  # On récupère tous le transport à jour
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_transport = " + str(transportId))
  result_updated_transport = QueryCursor.fetchone()

  # On récupère le timestamp
  timestamp_transport = result_transport[5]
  
  
  # Création de la réponse
  resp.data = '{ "id" : ' + str(result_updated_transport[0]) + ', "locations" : "' + locations + '", "status" : "' + str(statusList[result_transport[4]]) + '", "drone_location" : { "timestamp" : ' + str(timestamp_transport) + ', "coord" : { "lat" : '+str(result_updated_transport[2]) + ', "lon" : ' + str(result_transport[3]) + ' } } }'
  
  print resp.data
    
  dbConnection.close()
  
  return resp

##########################################################
#                SUPPRIMER LE TRANSPORT PAR ID           #
##########################################################
@app.route("/transports/<int:transportId>", methods=['DELETE'])
def delete_transport(transportId): 
  # Connexion à la BDD  
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
   
  # Création de la réponse
  resp = make_response()
  
  # Headers CORS
  addCorsHeaders(resp)
  
  # On récupère le transport avec l'ID
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_transport = " + str(transportId))
  result_transport = QueryCursor.fetchone()
  
  # Si le transport n'existe pas, erreur 404
  if result_transport == None:
      resp.status_code = 404
      dbConnection.close()
      return resp
  
  # On supprime le transport avec l'id reçu et tous les POI associés
  QueryCursor.execute("DELETE FROM Transport WHERE Id_transport=" + str(transportId))
  QueryCursor.execute("DELETE FROM Transport_Poi WHERE Id_transport=" + str(transportId))
  dbConnection.commit()
  
  resp.status_code = 204
  
  dbConnection.close()
  
  return resp

############################ Donne la liste des POI que doit visiter le dronne pour transportID
@app.route("/transports/<int:transportId>/route", methods=['GET'])
def get_route_transport(transportId):   
  # Connexion à la BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  QueryCursor2 = dbConnection.cursor()
  QueryCursor3 = dbConnection.cursor()

  # Création de la réponse 
  resp = make_response()
  
  # On précise le mimetype en tant que kml...
  resp.mimetype = 'application/vnd.google-earth.kml+xml'
  
  # On récupère le transport avec l'id reçu
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_transport = " + str(transportId))
  result_transport = QueryCursor.fetchone()
  
  # Si le transport n'existe pas erreur 404
  if result_transport == None:
      resp.status_code = 404
      dbConnection.close()
      return resp
      
  QueryCursor2.execute("SELECT * FROM Route_Poi WHERE id_transport=" + str(result_transport[0]) + " ORDER BY order_num ASC")
  result_route_poi = QueryCursor2.fetchone()

  QueryCursor2.execute("DELETE FROM Route_Poi")
  dbConnection.commit()
  
  # Si la route n'est pas encore generée
  if result_route_poi == None:
	print "Route not found"

	# On lance le programme en C
	outputBuffer = ""

	nbVille = 0

	for transport_poi in QueryCursor.execute("SELECT * FROM Transport_Poi where Id_transport=" + str(transportId)):
		for poi in QueryCursor2.execute("SELECT * FROM Poi where Id_poi=" + str(transport_poi[0])):
			print str(poi[0])
			print str(poi[1].encode("utf-8"))
			
			outputBuffer += '{"id": ' + str(poi[0]) + ', "coord" : {"lat": ' + str(poi[3]) + ', "lon": ' + str(poi[4]) + '}, "name": "' + str(poi[1].encode("utf-8")) + '", "kind": "city"},'
			nbVille += 1

	outputBuffer = "[" + outputBuffer[0:-1] + "]"

	print outputBuffer

	fichierJson = open("json_" + str(transportId) + ".json", "w")
	fichierJson.write(outputBuffer)
	fichierJson.close()
	
	tableauAlgo = ["algo_aleat", "algo_alpha", "algo_hamil"]
		
 	subprocess.call([os.getcwd() + "/cCalculator",  str(nbVille), "--in", "json_" + str(transportId) + ".json",  "--out",  "kml_" + str(transportId) + ".kml",  "--algo", tableauAlgo[int(result_transport[6])]])
 	
	if os.path.isfile("kml_" + str(transportId) + ".kml") == False:
		resp.status_code = 404
		dbConnection.close()
		return resp

	# Une fois qu'on a le fichier on le stock dans la BDD
	tree = ET.parse("kml_" + str(transportId) + ".kml")
	root = tree.getroot()
	
	# On crée deux liste pour y stocker les POI ordonnés et non ordonnés en lisant le fichier KML
	unorderedCoordinates = {}
	orderedCoordinates = []
	
	# On lit Placemark/name dans le kml
	PlacemarksName = root[0].findall("{https://www.opengis.net/kml/2.2}Placemark/{https://www.opengis.net/kml/2.2}name")
	
	# On lit Placemark/Point/coordinates dans le kml
	PlacemarksCoordinate = root[0].findall("{https://www.opengis.net/kml/2.2}Placemark/{https://www.opengis.net/kml/2.2}Point/{https://www.opengis.net/kml/2.2}coordinates")
	

	# On crée un dict associant les coordonnés au nom de la ville
	for n in range(0, len(PlacemarksName)):
		coord = str(PlacemarksCoordinate[n].text)
		coord = coord[0:-2] #"
		coord = "".join(coord.split())
		unorderedCoordinates[coord] = PlacemarksName[n].text
	
	
	# On récupère les coordonnées ordonnés dans une variable string temporaire	
	tempOrderedCoordinates = root[0].find("{https://www.opengis.net/kml/2.2}Placemark/{https://www.opengis.net/kml/2.2}LineString/{https://www.opengis.net/kml/2.2}coordinates").text
	
	# On remplace les sauts de lignes/espace par rien pour mettre les coordonnés de toute les villes sur la même ligne
	tempOrderedCoordinates = "".join(tempOrderedCoordinates.split())
	
	tempCoordinate = ""
	
	# On sépare les coordonnées en utilisant , en délimiteur
	splitOrderedCoordinates = tempOrderedCoordinates.split(",")	
	
	x = 1

	
	# On crée un tableau avec les coordonnées ordonnées
	for n in splitOrderedCoordinates:
		if x%2 == 0:
			tempCoordinate += "," + n
			print "TempCoordinate : ", tempCoordinate
			orderedCoordinates.append(tempCoordinate)
			tempCoordinate = ""
		else:
			tempCoordinate += n
  		x += 1
  	x = 1

	
  	# On ajoute la route
  	for coordinate in orderedCoordinates:
  		# On vérifie que chaque ville existe bien dans la BDD
  		QueryCursor.execute("SELECT * FROM Poi where Ville_poi='" + str(unorderedCoordinates[str(coordinate)].encode("utf-8")) + "'")
		result_poi = QueryCursor.fetchone()
		
		# Si la ville n'existe pas on renvoie 404
		if result_poi == None: # POI NOT FOUND
			resp.status_code = 404
			return resp
			
		# On ajoute une entrée dans Route_Poi
		QueryCursor.execute("INSERT OR IGNORE INTO Route_Poi VALUES(" + str(result_poi[0]) + ", " + str(transportId) + ", " + str(x) + ")")
		dbConnection.commit()
		x += 1
  else:
  	print "Route found"
  	
  # On lit le fichier KML reçu et on l'envoie au client
  try:
	# Si on demande la réponse ne JSON
  	if "application/json" in request.headers["Accept"]:
  		n=0
  		
  		# On récupère tous les ids de POI associés à une route
  		for route in QueryCursor.execute("SELECT * FROM Route_Poi where id_transport=" + str(transportId) + " ORDER BY Order_num ASC"):
  		
  			# On récupère chaque POI par son id pour en extraire les longitudes et latitudess
  			for poi in QueryCursor2.execute("SELECT * FROM Poi where Id_poi=" + str(route[0])):
				resp.data += '{"id": ' + str(poi[0]) + ', "coord" : {"lat": ' + str(poi[3]) + ', "lon": ' + str(poi[4]) + '}, "name": "' + str(poi[1]) + '", "kind": "city"},'
				
			n += 1
		resp.data = '[' + resp.data[0:-1] + ']' # resp.data[0:-1] => Supprime la dernière virgule
		
		# Deconnexion BDD
		dbConnection.close()
		
		return resp
	# Sinon en KML
  	else:
  		# Le fichier kml porte le nom suivant : kml_<idtransport>.kml
		f = open("kml_" + str(transportId) + ".kml", "r")
		resp.data = f.read() 
		f.close()
  except:
  	resp.status_code=404
  	dbConnection.close()
  	return resp
  
  dbConnection.close()
  
  return resp

############################ 
@app.route("/transports/autofetch", methods=['GET'])
def autofetch_transport():  
  # Connexion à la BDD
  dbConnection = sqlite3.connect('bdd.db')
  QueryCursor = dbConnection.cursor()
  QueryCursor2 = dbConnection.cursor()
  
  # Création de la réponse
  resp = make_response()
  resp.mimetype = 'application/json'
  
  # Associations des status à leur ID et inversement
  statusListTextToId = {}
  statusListIdToText = {}
  for row in QueryCursor.execute("SELECT * FROM Status"):
  	statusListTextToId[row[1]] = row[0]
	statusListIdToText[row[0]] = row[1]        
  
  # On récupère le transport demandé avec le status todo	
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_status='" + str(statusListTextToId["todo"]) + "' LIMIT 1")
  result_transport = QueryCursor.fetchone()
  
  # S'il y'en a aucun renvoyer 404
  if result_transport == None:
      resp.status_code = 404
      dbConnection.close()
      return resp
      
  # On renvoie le tableau des ids de locations
  locations = "["
  for row_transport_poi in QueryCursor.execute("SELECT * FROM Transport_Poi WHERE Id_transport=" + str(result_transport[0])):
	locations += str(row_transport_poi[0]) + ","
		
  locations = locations[0:-1] + "]"
  
  QueryCursor.execute("UPDATE Transport SET Id_status=" + str(statusListTextToId["enroute"]) + " WHERE Id_transport=" + str(result_transport[0]))
  dbConnection.commit()
  
  # On récupère le transport demandé avec le status todo	
  QueryCursor.execute("SELECT * FROM Transport WHERE Id_transport=" + str(result_transport[0]))
  result_transport = QueryCursor.fetchone()
  
  resp.status_code = 200
  
  print statusListTextToId["todo"]
  print statusListIdToText
  print result_transport[4]
  # On crée le corps de la réponse
  resp.data = '{ "id" : ' + str(result_transport[0]) + ', "locations" : ' + locations + ', "status" : "' + str(statusListIdToText[result_transport[4]]) +'"}'
  
  dbConnection.close()
  
  return resp

if __name__ == "__main__":
  #app.run(host="192.168.1.55", port=5123, debug=True)
  #app.run(host="172.31.1.169", port=5124, debug=True)
  app.run(host="172.20.200.173", port=5124, debug=True)
  #app.run(host="172.31.1.107", port=5124, debug=True)
  #app.run(host="172.31.1.57", port=5124, debug=True)
  #app.run(port=5123, debug=True)

