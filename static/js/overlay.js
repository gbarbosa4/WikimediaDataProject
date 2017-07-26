<script>

$("#menu_item1").click(function () {

  imagesArray = ["","static/img/wikidata.png", "static/img/dataanalysis.png", "static/img/kmlfile.png"];
  labelArray = ["","Wikidata query. \n Most Populated Cities in the World", "Analyzing data. \n Getting information about the cities.", "Generating KML file. \n The tour will be ready in a moment."];

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
  }, 1600);
});


$("#menu_item2").click(function () {
  count = 0;
  $("#modal").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });
  $("#modal2").fadeOut(0, function () {
    $(this).css("display", "block").fadeIn(0);
  });

  imagesArray = ["","static/img/wikidata.png"];
  labelArray = ["","Wikidata query"];

  setInterval(function () {
    count = count + 1;
    $("#image").fadeOut(0, function () {
      $(this).attr("src", imagesArray[count]).fadeIn(0);
    });
    $("#header2").fadeOut(0, function () {
      $(this).text(labelArray[count]).fadeIn(0);
    });
  }, 1600);
});

</script>
