$carte = null;
$carte2 = null;
$marker = null;
$traceParcoursBus = null;
$traceParcoursBus = null;
$serverIp = "172.20.200.173"
$port = "5124"
$compteur = 0;
$selectedTransport = null;
$statusSelectedTransport = null;
$LatitudeDrone = null;
$LongitudeDrone = null;
$listePoi = Array();

/************************************************************************
*				Fonction appeler au chargement du DOM					*	
*************************************************************************/
$(function(){
	
	listerLocation();
	listerTransport();

	// toutes les 2 sec on acctualise les transports et les locations
	setInterval("listerLocation()", 2000);
	setInterval("listerTransport()", 2000);
})

/************************************************************************
*				Fonction de listage (location & transport)				*	
*************************************************************************/
function listerTransport(){
	$.ajax({
		url: "http://" + $serverIp + ":" + $port + "/transports",
		method : "GET",
		dataType:"json",
		success: function (data){

				// on vide la div pour afficher sur une div vierge
				$("#table-transport").html("");					
			
				// parcour tous les transport
				for(var j=0;j < data.length;j++)
				{
					
					// si le transport est en route
					if(data[j].status == "enroute"){
						NbLocation = data[j].location.length;
						ListePoi = data[j].location;
						$LatitudeDrone = data[j]["drone-location"]["coord"].lat;
						$LongitudeDrone = data[j]["drone-location"]["coord"].lon;
						idTransport = data[j].id;
						
						// si un transport est suivi par l'utilisateur
						if($selectedTransport != null && data[j]["id"] == $selectedTransport)
						{
								// on place le marker représentant le dronne avec les coord du drone
								var latlng = new google.maps.LatLng($LatitudeDrone, $LongitudeDrone);
								$carte.setCenter(latlng);
					
								$marker.setMap($carte);
								$marker.setPosition(latlng);
								
						}
			
						// on affiche les 2 bouton 1 pour annuler et un pour suivre
						// si on click sur le bouton a suivre d'un transport cela déclanche une fonction qui récup les attributs du button
						$("#table-transport").prepend('<tr><td>' + data[j].id + '</td><td class="transport-encours" title="' + ListePoi + '">' + data[j].status + '</td><td><div class="btn-group" role="group"><button type="button" class="btn btn-success glyphicon glyphicon-eye-open" title="Position du drone" listePoi="' + ListePoi.toString() + '" NbLocation="' + NbLocation + '" LatDrone="' + $LatitudeDrone + '" LonDrone="' + $LongitudeDrone + '" idTransport="' + idTransport + '" ></button><button type="button" class="btn btn-danger glyphicon glyphicon-remove" data-toggle="tooltip" data-placement="left" title="Annuler Transport" onclick="annuler_transport( '+ idTransport +' )"></button></div></td></tr>');
						
					}
					// si le transport est a faire
					else if(data[j].status == "todo"){
						idTransport = data[j].id;
						ListePoi = data[j].location;
						
						/* on affihe que le bouton annuler et pas le bouton suivre 
						car on ne peu pas suivre le dronne
						étant donner qu'il n'y en pas pas d'assigner a ce transport*/
						$("#table-transport").prepend('<tr><td>' + data[j].id + '</td><td class="transport-encours" title="' + ListePoi + '">' + data[j].status + '</td><td><div class="btn-group" role="group"><button type="button" class="btn btn-danger glyphicon glyphicon-remove" data-toggle="tooltip" data-placement="left" title="Annuler Transport" onclick="annuler_transport( '+ idTransport +' )"></button></div></td></tr>');
						
					}
				}
				
				
			// titre du tableau (html)
			$("#table-transport").prepend("<tr><th> ID</th><th> Status </th><th> Action </th></tr>");
		},
		// erreur du get transport
		error: function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
		}
	});
}

function listerLocation(){
	$.ajax({
		url: "http://" + $serverIp + ":" + $port + "/locations",
		method : "GET",
		dataType:"json",
		success: function(data) {
			//vide la div
           	$("#table-location").html("");
			// titre du tableau (html)
			$("#table-location").append("<tr> <th>Id</th> <th>Name</th> <th>Kind</th> <th>Action</th></tr>")
			
			//parcour toutes les locations puis les affiche avec un button pour la supprimer et un button pour ajouter la location a la div d'avout de transport
		    for(var j=0; j<data.length; j++)
		    {	
				$("#table-location").append("<tr><td>" + data[j].id + "</td><td>" + data[j].name + "</td><td>" + data[j].kind + "</td> <td> <div class='btn-group' role='group'><button type='button' class='btn btn-danger glyphicon glyphicon-remove' title='Annuler Location' onclick='delete_location( "+ data[j].id +" )'></button><button type='button' class='btn btn-primary glyphicon glyphicon-arrow-right' title='Ajouter transport' onclick='move_transport(\"" + data[j].name + "\"," + data[j].id +")'></button></div></td></tr>");
			}
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
		}
	});
}

/************************************************************************
*				Fonction d'ajout (location & transport)					*	
*************************************************************************/
function add_transport(){	//fonction appeler quand on click sur le button add de a page html

	// tableau de location qui constitue le transport
	var listePoi = [];
	
	// on récupère toutes les div (chacune représente une location) dans la div panel-nouveau-trajet
	$.each($(".panel-nouveau-trajet > div"), function($id, $etiquette)
	{
		var id_poi = $($etiquette).attr("idPoi");
		var poi = parseInt(id_poi);
		// puis on ajoute ce poi dans la liste
		listePoi.push(poi);
	});
	
	// on recup la valeur du select dans le html pour l'algo
	var algo = $(".select-algo").val();
	console.log(algo);
	
	// Fabrication du Json pour l'envoyer en Ajax
	var message = '{"locations": [' + listePoi + '], "algo": ' + algo + '}';
	console.log(message);
	
	$.ajax({
		url: "http://" + $serverIp + ":" + $port + "/transports",
		method : "POST",
		contentType : "application/json",
		data: message, // donnée envoyée
		success: function() {
			// Notifcation en haut a gauche de l'écran
			$.notify("Le transport à été ajoutée avec succès.", "success");
			// On vide la div qui contient les div qui represente chacune une location
			clear_add_transport();
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			$.notify("Erreur lors de l'ajout du transport.", "error");
		}
	});
}

//Cet fonction récupère les donee dans les champ du modal de l'ajout d'une location
function add_location(){
	
	// recup les 4 valeurs des inpute
	var name = $("#add-name-location").val();
	var kind = $("#add-kind-location").val();
	var lat = $("#add-latitude-location").val();
	var lon = $("#add-longitude-location").val();

	console.log(name);
	console.log(kind);
	console.log(lat);
	console.log(lon);

	// creation du message json avec les bonne donnee
	var messageJson ='{"name": "' + name + '", "kind": "' + kind + '", "coord": { "lat": ' + lat + ', "lon": ' + lon + '}}';
	console.log(messageJson);
	
	$.ajax({
		url: "http://" + $serverIp + ":" + $port + "/locations",
		method : "POST",
		contentType : "application/json",
		dataType:"plain/text",
		data: messageJson, // Json a envoyer
		success:function() {
			// notif de success
			$.notify("La location à été ajoutée avec succès.", "success");
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			$.notify("Erreur lors de l'ajout de la location.", "error");
		}
	});

	// remte a 0 les inputes
	$("#add-name-location").val("");
	$("#add-kind-location").val("");
	$("#add-latitude-location").val("");
	$("#add-longitude-location").val("");
}

/************************************************************************
*			Fonction de Suppression (location & transport)				*	
*************************************************************************/
function annuler_transport(idTransport){ // fonction appeler au click sur un bouton a caute d'un transport (grace a l'id passé en paramètre)
	$.ajax({
		url: "http://" + $serverIp + ":" + $port + "/transports/" + idTransport,
		method : "DELETE",
		success: function() {
           	$.notify("La location " + idTransport + " à bien été supprimé.", "success");
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			$.notify("Impossible de supprimer ce transport erreur interne.", "error");
		}
	});
}

function delete_location(idLocation){ // fonction appeler au click sur un bouton a caute d'une location (grace a l'id passé en paramètre)
	$.ajax({
		url: "http://" + $serverIp + ":" + $port + "/locations/" + idLocation,
		method : "DELETE",
		success: function() {
           	$.notify("La location " + idLocation + " à bien été supprimé.", "success");
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			
			if(a.status == 405)
				$.notify("Impossible de supprimer cet location car elle est utilisée dans un transport.", "error");
		}
	});
}


/************************************************************************
*				Fonction pour suivre un transport-encours				*	
*************************************************************************/
$(document).on("click", "button[listePoi]", function(){
	
	NbPoi = $(this).attr("nblocation") // nbPoi
	ListePoi = $(this).attr("ListePoi") // liste string, exemple : 1,2,3
	LatDrone = $(this).attr("LatDrone")
	LonDrone = $(this).attr("LonDrone")
	idTransport = $(this).attr("idTransport");
	
	// set la varaible global pour savoir sur quel transport l'utilisateur a click
	$selectedTransport = idTransport;
	
	console.log("Nombre de POI :" + NbPoi);
	console.log("Liste des poi :" + ListePoi);
	console.log("Latitude du drone: " + LatDrone);
	console.log("Longitude du drone: " + LonDrone);
	console.log("Id du transport:" + idTransport);
	
	// split les id location 
	listePoiId = ListePoi.split(",");
	
	var parcours = Array();
	$remainingRequest = listePoiId.length;
	
	// on parcour la liste de location du  vieu transport pour supprimer les marquer de la map
	for($n = 0; $n < $listePoi.length;$n++)
	{
		$listePoi[$n].setMap(null);
	}
		
	// vide la liste
	$listePoi.splice(0,$listePoi.length);
	
	// parcour la liste des id des location
	for($x=0;$x < listePoiId.length;$x++)
	{
		// pour chaque location on fait une requette pour récup les coord de la location
		$.ajax({
			url: "http://" + $serverIp + ":" + $port + "/locations/" + listePoiId[$x],
			method : "GET",
			dataType:"json",
			success: function(data) 
			{
				// on place le marker représentant le dronne location avec les coord
				var latlng = new google.maps.LatLng(parseFloat(data["coord"]["lat"]), parseFloat(data["coord"]["lon"]));
				$carte.setCenter(latlng);
					
				$marker.setMap($carte);
				$marker.setPosition(latlng);
				// parametre du marker
				$poi =  new google.maps.Marker({ 
				      position: latlng,
				      map: $carte, 	// carte sur la quelle dessiner les markers
				      title: data["name"] // titre du drone (nom de la location)
				});
				$listePoi.push($poi);
				$poi.setMap($carte); // place la location sur la map 
				
			},
			error:function(a, b, errorThrown)
			{
				console.log(a);
				console.log(b);
				console.log(errorThrown);
			}
		});
	}
});

// fonction appeler au chargement du body
function initialiser(){	
	
	// Prmeiere carte 
	var latlng = new google.maps.LatLng(42.6976, 2.8954);
	
	// option de la carte 
	var options = {
		center: latlng,
		zoom: 2,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	$carte = new google.maps.Map(document.getElementById("carte"), options);
	
	/* Marker du drone initialiser a null*/
	$marker = new google.maps.Marker({
		  position: null,
		  map: null,
		  title: 'Drone',
		  icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
	});
	

	
	// fonction appeler a l'ouverture du modal pour ajouter une location
	// Obligé car si non la carte ne se charge pas corectement
	$('#Modal_add_location').on('shown.bs.modal', function () {
	  
		/* 2em carte pour l'ajout d'une location que l'on centre sur Perpignan*/
		var latlng2 = new google.maps.LatLng(42.67839711889057, 2.8900909423828125);
		
		//parmetre pour l'affichage par defaut de la carte
		var options2 = {
			center: latlng2,
			zoom: 8,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		
		$carte2 = new google.maps.Map(document.getElementById("carte2"), options2);
		
		// fonction appeler au click sur la 2 eme carte (modal)
		google.maps.event.addListener($carte2, "click", function(event) {
			var lat = event.latLng.lat(); // recup lat de position du click
			var lon = event.latLng.lng(); // recup lat de position du click
			
			// creer un geocoder pour recupe le nom et le kind sur la map
			geocoder = new google.maps.Geocoder();
			
			geocoder.geocode({'latLng': event.latLng}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					console.log(results);
					for(var x=0; x < results.length;x++)
					{
						for(var y=0;y < results[x]["types"].length;y++)
						{
							if(results[x]["types"][y] == "locality") // test si c'est une city
							{
								$("#add-kind-location").val("city"); // si c'est une city on remplie le champ en question du modal
								for(var j=0;j < results[x]["address_components"].length;j++)
								{
									for(var k = 0;k < results[x]["address_components"][j]["types"].length;k++)
									{
										if(results[x]["address_components"][j]["types"][k] == "locality"){
											$("#add-name-location").val(results[x]["address_components"][j]["long_name"]); // recup le nom de la ville et l'ecrit dans l'inpute du modal
											
										}	
									}
								}
							}
						}
					}
				}
				else{
					$.notify("Veuilliez choisir une zone valide.", "error");
				}
			});
			// remplie les 2 impute du modal pour la lat et la lon
			$("#add-longitude-location").val(lon);
			$("#add-latitude-location").val(lat);
		});
	})
}


/************************************************************************
*				Fonction pour ajouter des locations a un transport		*	
*************************************************************************/
function move_transport(name, id) // fonction pour creer des div dans la div de creation de transport chaque div est crer avec un id corespondant a une location
{
	$alreadyAdded = false;
	// parcour toutes les div corespondant a une location
	$.each($(".panel-nouveau-trajet span[type=ville]"), function($id, $etiquette)
	{		
		// si la location est deja dans la div general on ajoute pas  
		if($($etiquette).text() == name)
		{
			$alreadyAdded = true;
		}
		
		// si la div general contient plus de 7 location on ajoute pas
		if($compteur >= 7)
		{
			$alreadyAdded = true;
		}
			
	});
	// si les condition du dessu sont ok on ajout une div dans la div general
	if(!$alreadyAdded)
	{
		$(".panel-nouveau-trajet").append('<div class="col-md-4" idPoi=' + id + '><div class="alert alert-info alert-dismissible fade in" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><span type="ville">'+ name +'</span></div></div>');
		$().alert('close');
		$(".alert-info").on("close.bs.alert", function()
		{
			$(this).parent().remove();
		})
	}
	$compteur = $(".panel-nouveau-trajet > div").length
}

/************************************************************************
*				Fonction pour vider le cadre d'ajout de transport		*	
*************************************************************************/
function clear_add_transport(){
	$(".panel-nouveau-trajet").empty();
}
