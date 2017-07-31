$( document ).ready(function() {

$("#menu_item1").click(function () {

  imagesArray = ["","static/img/wikidata.png", "static/img/dataanalysis.png", "static/img/kmlfile.png"];
  labelArray = ["","Wikidata query. \t Most Populated Cities in the World", "Analyzing data. \t Getting information about the cities.", "Generating KML file. \t The tour will be ready in a moment."];

  count = 0;
  $("#modal").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });
  $("#modal2").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });

  setInterval(function () {
    count = count + 1;
    $("#image").fadeOut(0, function () {
      $(this).attr("src", imagesArray[count]).fadeIn(0);
    });
    $("#header2").fadeOut(0, function () {
      $(this).text(labelArray[count]).fadeIn(0);
    });
  }, 3400);
});


$("#menu_item2").click(function () {

  imagesArray = ["","static/img/wikidata.png","static/img/dataanalysis.png","static/img/premierleague.png"];
  labelArray = ["","Wikidata query.\t Premier League 2016-2017 Stadiums","Analyzing Data.\t Getting information about clubs and stadiums.",""];

  count = 0;
  $("#modal").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });
  $("#modal2").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });

  setInterval(function () {
    count = count + 1;
    $("#image").fadeOut(0, function () {
      $(this).attr("src", imagesArray[count]).fadeIn(0);
    });
    $("#header2").fadeOut(0, function () {
      $(this).text(labelArray[count]).fadeIn(0);
    });
  }, 3400);
});

$("#menu_item3").click(function () {

  imagesArray = ["","static/img/wikidata.png","static/img/dataanalysis.png","static/img/premierleague.png","static/img/kmlfile.png"];
  labelArray = ["","Wikidata query.\t The Longest Rivers in the World.","Analyzing Data.\t Getting rivers information.","Generating KML file.\t The rotation will be ready in a few seconds..."];

  count = 0;
  $("#modal").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });
  $("#modal2").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });

  setInterval(function () {
    count = count + 1;
    $("#image").fadeOut(0, function () {
      $(this).attr("src", imagesArray[count]).fadeIn(0);
    });
    $("#header2").fadeOut(0, function () {
      $(this).text(labelArray[count]).fadeIn(0);
    });
  }, 3400);
});

$("#get_stadium").click(function () {
  count = 0;
  $("#modal").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });
  $("#modal2").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });

  setInterval(function () {
    count = count + 1;
    $("#image").fadeOut(0, function () {
      $(this).attr("src", imagesArray[count]).fadeIn(0);
    });
    $("#header2").fadeOut(0, function () {
      $(this).text(labelArray[count]).fadeIn(0);
    });
  }, 1500);
});

});

function combo_selected_team(hash_club_shield) {

    imagesArray = ["static/img/kmlfile.png"];
    labelArray = ["Generating KML file. \t The tour for the selected stadium will be ready in a moment."];

    var a = document.getElementById('combo_list').selectedIndex;
    var club_selected = document.getElementById('combo_list')[a].text;

    var i = 0;
    while ( i<20 ){
      club_name = hash_club_shield.split("|")[i].split("=")[0];
      if ( club_name.localeCompare(club_selected) == 0 ){
            club_shield = hash_club_shield.split("|")[i].split("=")[1];
            i=20;
      }
      i++;
    }
    imagesArray.push(club_shield);
    labelArray.push("Flying to the stadium ... "+club_selected);
}

var cookies;
function readCookie(name,c,C,i){
    if(cookies){ return cookies[name]; }

    c = document.cookie.split('; ');
    cookies = {};

    for(i=c.length-1; i>=0; i--){
       C = c[i].split('=');
       cookies[C[0]] = C[1];
    }

    return cookies[name];
}

function selected_river_button(river_name){

    document.getElementById('overlay_river').style.display = "block";
    document.getElementById('label_river').innerText = river_name;

    const csrfmiddlewaretoken = readCookie('csrftoken');
    console.info(csrfmiddlewaretoken);

    fetch('/longest_rivers', {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: `csrfmiddlewaretoken=${csrfmiddlewaretoken}&river_name=${river_name}`,
      credentials: 'include'
    }).then(() => {
      ///alert('done');
    });
}
