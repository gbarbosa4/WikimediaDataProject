$( document ).ready(function() {

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

    imagesArray.push(club_shield.replace("../","static/"));
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
