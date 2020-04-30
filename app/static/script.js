var currentDiv = null;

const formatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 2,
});

$(function () {
  randomBackground();

  $("select#keywords").selectize({
    plugins: ["remove_button"],
    delimiter: ",",
    persist: false,
    create: function (input) {
      return {
        value: input,
        text: input,
      };
    },
  });

  if ($("#results").is(":visible")) {
    $("html, body").animate(
      {
        scrollTop: $("#results").offset().top,
      },
      1000
    );

    $("div.result:gt(8)").hide();

    var margin = { top: 5, right: 5, bottom: 5, left: 5 },
      width = 150,
      height = 150;

    // var color = d3.scale.ordinal().range(["#EDC951", "#CC333F", "#00A0B0"]);
    var color = d3.scale.ordinal().range(["#31a05f"]);

    var radarChartOptions = {
      w: width,
      h: height,
      margin: margin,
      maxValue: 1.0,
      levels: 3,
      roundStrokes: true,
      color: color,
      opacityCircles: 0,
      opacityArea: 0.8,
    };

    //Call function to draw the Radar chart
    $(".radarChart").each(function () {
      // console.log($( this )[0]);
      var data = [
        [
          {
            axis: "Commute",
            value: parseFloat($(this)[0].getAttribute("commute-order")) / 100.0,
          },
          {
            axis: "Age",
            value: parseFloat($(this)[0].getAttribute("age-order")) / 100.0,
          },
          {
            axis: "Keywords",
            value: parseFloat($(this)[0].getAttribute("likes-order")) / 100.0,
          },
          {
            axis: "Budget",
            value: parseFloat($(this)[0].getAttribute("budget-order")) / 100.0,
          },
          {
            axis: "Happiness",
            value:
              parseFloat($(this)[0].getAttribute("happiness-order")) / 100.0,
          },
        ],
      ];

      RadarChart(
        "." + $(this)[0].getAttribute("class").split(" ")[1],
        data,
        radarChartOptions
      );

      // $( this ).addClass( "foo" );
    });
  }

  $("a[data-modal]").click(function (event) {
    currentDiv = $(this)[0].getAttribute("href").replace("#", "");
    console.log(currentDiv);
    $(this).modal({
      fadeDuration: 350,
    });
    return false;
  });
});

jQuery.fn.sortNeighborhoodsByAge = function sortNeighborhoodsByAge() {
  $(".result", this[0]).sort(dec_sort).appendTo(this[0]);
  function dec_sort(a, b) {
    return parseFloat(b.getAttribute("age-order")) <
      parseFloat(a.getAttribute("age-order"))
      ? -1
      : 1;
  }
};

jQuery.fn.sortNeighborhoodsByCommute = function sortNeighborhoodsByCommute() {
  $(".result", this[0]).sort(dec_sort).appendTo(this[0]);
  function dec_sort(a, b) {
    return parseFloat(b.getAttribute("commute-order")) <
      parseFloat(a.getAttribute("commute-order"))
      ? -1
      : 1;
  }
};

jQuery.fn.sortNeighborhoodsByBudget = function sortNeighborhoodsByBudget() {
  $(".result", this[0]).sort(dec_sort).appendTo(this[0]);
  function dec_sort(a, b) {
    return parseFloat(b.getAttribute("budget-order")) <
      parseFloat(a.getAttribute("budget-order"))
      ? 1
      : -1;
  }
};

jQuery.fn.sortNeighborhoodsByLikes = function sortNeighborhoodsByLikes() {
  $(".result", this[0]).sort(dec_sort).appendTo(this[0]);
  function dec_sort(a, b) {
    return parseFloat(b.getAttribute("likes-order")) <
      parseFloat(a.getAttribute("likes-order"))
      ? -1
      : 1;
  }
};

jQuery.fn.sortNeighborhoods = function sortNeighborhoods() {
  $(".result", this[0]).sort(dec_sort).appendTo(this[0]);
  function dec_sort(a, b) {
    return parseFloat(b.getAttribute("overall-order")) <
      parseFloat(a.getAttribute("overall-order"))
      ? -1
      : 1;
  }
};

function sortAge(e) {
  $("div.result").show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByAge();
  $("div.result:gt(8)").hide();
}

function sortBudget(e) {
  $("div.result").show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByBudget();
  $("div.result:gt(8)").hide();
}

function sort(e) {
  $("div.result").show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoods();
  $("div.result:gt(8)").hide();
}

function sortLikes(e) {
  $("div.result").show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByLikes();
  $("div.result:gt(8)").hide();
}

function sortCommute(e) {
  $("div.result").show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByCommute();
  $("div.result:gt(8)").hide();
}

function randomBackground() {
  var imgArr = [
    "people-walking-near-concrete-buildings-1557547-5.jpg",
    "concrete-bridge-near-buildings-during-golden-hour-1755683-2.jpg",
    "people-standing-near-highway-near-vehicles-1634279-2.jpg",
  ];
  var n = Math.floor(Math.random() * 3);
  var newBackground = 'url("static/' + imgArr[n] + '")';
  $("#search").css("background", newBackground);
}

function closeMap(e) {
  var n = "#" + $(e)[0].getAttribute("data-x");
  $(n + " .links a").removeClass("active");
  $(e).addClass("active");
  $(n + "-map").hide(500);
  $(n + " .radar").show(500);
  $(n + " .tags").show(500);
}

function openMap(e) {
  var n = "#" + $(e)[0].getAttribute("data-x");
  $(n + " .links a").removeClass("active");
  $(e).addClass("active");
  $(n + "-map").show(500);
  $(n + " .radar").hide(500);
  $(n + " .tags").hide(500);
}
$(document).ready(function () {
  $(document).on("keyup", function (e) {
    console.log("HELLO");
    var modal_ids = [];
    $(".snippet a").each(function () {
      modal_ids.push(this.getAttribute("href").replace('#', ''));
    });

    // left arrow
    currentId = modal_ids.indexOf(currentDiv);

    console.log(currentId);
    if (e.which === 37 && currentId > 1) {
      currentDiv = modal_ids[--currentId];
      $("#" + currentDiv).modal();
    }
    // right arrow
    else if (e.which === 39 && currentId < modal_ids.length) {
      currentDiv = modal_ids[++currentId];
      $("#" + currentDiv).modal();
    }
  });
});
