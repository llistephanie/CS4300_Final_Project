/**
 * http://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
 *
 * Converts an HSL color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes h, s, and l are contained in the set [0, 1] and
 * returns r, g, and b in the set [0, 255].
 *
 * @param   Number  h       The hue
 * @param   Number  s       The saturation
 * @param   Number  l       The lightness
 * @return  Array           The RGB representation
 */
function hslToRgb(h, s, l) {
  var r, g, b;

  if (s == 0) {
    r = g = b = l; // achromatic
  } else {
    function hue2rgb(p, q, t) {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    }

    var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    var p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }

  return [Math.floor(r * 255), Math.floor(g * 255), Math.floor(b * 255)];
}

// convert a number to a color using hsl
function numberToColorHsl(i) {
  // as the function expects a value between 0 and 1, and red = 0° and green = 120°
  // we convert the input to the appropriate hue value
  var hue = (i * 1.2) / 360;
  // we convert hsl to rgb (saturation 100%, lightness 50%)
  var rgb = hslToRgb(hue, 1, 0.5);
  // we format to css value and return
  return "rgb(" + rgb[0] + "," + rgb[1] + "," + rgb[2] + ")";
}

const formatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 2,
});

function updateBudgetLabels() {
  low = parseInt($("#budget").attr("value").split(",")[0]);
  high = parseInt($("#budget").attr("value").split(",")[1]);

  min = parseInt($("#budget").val().split(",")[0]);
  max = parseInt($("#budget").val().split(",")[1]);

  actualMin = ((high - low) / 100) * min;
  actualMax = ((high - low) / 100) * max;

  $(".budget-min").text(formatter.format(actualMin).slice(0, -3));
  $(".budget-max").text(formatter.format(actualMax).slice(0, -3));
}

function updateSafetyLabel() {
  score = parseInt(parseInt($("#safety").val()));
  label = "";

  switch (score) {
    case 1:
      label = "not at all important";
      break;
    case 2:
      label = "not very important";
      break;
    case 3:
      label = "somewhat important";
      break;
    case 4:
      label = "very important";
      break;
    default:
      label = "extremely important";
  }
  $(".safety").text(label);
}

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

  // $(".chosen-select").chosen({
  //   no_results_text: "Oops, nothing found!",
  // });

  if ($("#results").is(":visible")) {
    $("html, body").animate(
      {
        scrollTop: $("#results").offset().top,
      },
      1000
    );

    $('div.result:gt(8)').hide();

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
  $('div.result').show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByAge();
  $('div.result:gt(8)').hide();
}

function sortBudget(e) {
  $('div.result').show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByBudget();
  $('div.result:gt(8)').hide();
}

function sort(e) {
  $('div.result').show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoods();
  $('div.result:gt(8)').hide();
}

function sortLikes(e) {
  $('div.result').show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByLikes();
  $('div.result:gt(8)').hide();
}

function sortCommute(e) {
  $('div.result').show();
  $("#filters a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByCommute();
  $('div.result:gt(8)').hide();
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
