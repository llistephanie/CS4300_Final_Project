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
  }
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
      ? -1
      : 1;
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
  $("a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByAge();
}

function sortBudget(e) {
  $("a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByBudget();
}

function sort(e) {
  $("a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoods();
}

function sortLikes(e) {
  $("a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByLikes();
}

function sortCommute(e) {
  $("a").removeClass("active");
  $(e).addClass("active");
  $("#results").sortNeighborhoodsByCommute();
}
