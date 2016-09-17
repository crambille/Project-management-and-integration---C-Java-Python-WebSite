$carte = null;
$carte2 = null;
$marker = null;
$traceParcoursBus = null;

$(function(){
	
	listerLocation();
	listerTransport();

	setInterval("listerLocation()", 2000);
	setInterval("listerTransport()", 2000);
})

/************************************************************************
*				Fonction de listage (location & transport)				*	
*************************************************************************/
function listerTransport(){
	$.ajax({
		url: "http://172.31.1.169:5123/transports",
		method : "GET",
		dataType:"json",
		"success": function (data){
			$("#table-transport").html("");					
			
			for(var j=0;j < data.length;j++)
			{
				NbLocation = data[j].location.length;
				ListePoi = data[j].location;
				LatDrone = data[j]["drone-location"]["coord"].lat;
				LonDrone = data[j]["drone-location"]["coord"].lon;
				idTransport = data[j].id;
			
				$("#table-transport").prepend('<tr><td>' + data[j].id + '</td><td class="transport-encours">' + data[j].status + '</td><td><div class="btn-group" role="group"><button type="button" class="btn btn-success glyphicon glyphicon-eye-open" title="Position du drone" listePoi="' + ListePoi.toString() + '" NbLocation="' + NbLocation + '" LatDrone="' + LatDrone + '" LonDrone="' + LonDrone + '" ></button><button type="button" class="btn btn-danger glyphicon glyphicon-remove" title="Annuler Transport" onclick="annuler_transport( '+ idTransport +' )"></button></div></td></tr>');
			}
			$("#table-transport").prepend("<tr><th> ID</th><th> Status </th><th> Action </th></tr>");
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
		}
	});
}

function listerLocation(){
	$.ajax({
		url: "http://172.31.1.169:5123/locations",
		method : "GET",
		dataType:"json",
		"success": function(data) {
           	$("#table-location").html("");						
			$("#table-location").append("<tr> <th>Id</th> <th>Name</th> <th>Kind</th> <th>Action</th></tr>")
			
		    for(var j=0; j<data.length; j++)
		    {	
				$("#table-location").append("<tr><td>" + data[j].id + "</td><td>" + data[j].name + "</td><td>" + data[j].kind + "</td> <td> <button type='button' class='btn btn-danger glyphicon glyphicon-remove' title='Annuler Location' onclick='delete_location( "+ data[j].id +" )'></button> </td> </tr>");
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
*				Fonction d'ajout (location & transport)				*	
*************************************************************************/
function add_transport(){

}

function add_location(){
	var name = $("#add-name-location").val();
	var kind = $("#add-kind-location").val();
	var lat = $("#add-latitude-location").val();
	var lon = $("#add-longitude-location").val();

	console.log(name);
	console.log(kind);
	console.log(lat);
	console.log(lon);

	var messageJson ='{"name": "' + name + '", "kind": "' + kind + '", "coord": { "lat": ' + lat + ', "lon": ' + lon + '}}';
	console.log(messageJson);
	$.ajax({
		url: "http://172.31.1.169:5123/locations",
		method : "POST",
		dataType:"json",
		contentType : "application/json",
		data: messageJson,
		"success": function() {
			$("#alert").append('<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Success:</strong> La location a bien été postée.</div>');
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			$("#alert").append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Erreur interne:</strong> La location n\'a pas pue ètre postée.</div>');
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
function annuler_transport(idTransport){
	$.ajax({
		url: "http://172.31.1.169:5123/transports/" + idTransport,
		method : "DELETE",
		"success": function() {
           	$("#alert").append('<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Success:</strong> Le transport ' + idTransport + ' a bien été supprimé.</div>');
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			$("#alert").append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Erreur interne:</strong> Le transport ' + idTransport + ' n\'a pas été supprimé.</div>');
		}
	});
}

function delete_location(idLocation){
	$.ajax({
		url: "http://172.31.1.169:5123/locations/" + idLocation,
		method : "DELETE",
		"success": function() {
           	$("#alert").append('<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Success:</strong> La location ' + idLocation + ' a bien été supprimé.</div>');
		},
		error:function(a, b, errorThrown)
		{
			console.log(a);
			console.log(b);
			console.log(errorThrown);
			$("#alert").append('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Erreur interne:</strong> La location ' + idLocation + ' n\'a pas été supprimée.</div>');
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
	
	console.log("Nombre de POI :" + NbPoi);
	console.log("Liste des poi :" + ListePoi);
	console.log("Latitude du drone: " + LatDrone);
	console.log("Longitude du drone: " + LonDrone);
	
	listePoiId = ListePoi.split(",");
	
	var parcours = Array();
	$remainingRequest = listePoiId.length;
	
	for($x=0;$x < listePoiId.length;$x++)
	{
		$.ajax({
			url: "http://172.31.1.169:5123/locations/" + listePoiId[$x],
			method : "GET",
			dataType:"json",
			"success": function(data) 
			{
				parcours.push(new google.maps.LatLng(parseFloat(data["coord"]["lat"]), parseFloat(data["coord"]["lon"])));
				$remainingRequest--;
				
				if($remainingRequest == 0)
				{
					$traceParcoursBus = new google.maps.Polyline({
						path: parcours,//chemin du tracé
						strokeColor: "#ff0000",//couleur du tracé
						strokeOpacity: 1.0,//opacité du tracé
						strokeWeight: 2//grosseur du tracé
					});
					
					$traceParcoursBus.setMap($carte);
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

	/*coordornée drone*/
	var Xdrone=LatDrone;
	var Ydrone=LonDrone;

	var latlng = new google.maps.LatLng(LatDrone, LonDrone);
	$carte.setCenter(latlng);
	
	$marker.setMap($carte);
	$marker.setPosition(latlng);
			
});

function initialiser() {	
	
	var latlng = new google.maps.LatLng(42.6976, 2.8954);
	conteneur=document.getElementById('sonic1.gif');
	
	var options = {
		center: latlng,
		zoom: 2,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	$carte = new google.maps.Map(document.getElementById("carte"), options);

	/* 2em carte pour l'ajout d'une location*/
	var latlng2 = new google.maps.LatLng(42.6976, 2.8954);
	conteneur=document.getElementById('sonic1.gif');
	
	var options2 = {
		center: latlng2,
		zoom: 1,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	$carte2 = new google.maps.Map(document.getElementById("carte2"), options2);
	
	/* Marker du drone sur la carte principal */
	$marker = new google.maps.Marker({
		  position: null,
		  map: null,
		  title: 'Drone'
	});
}