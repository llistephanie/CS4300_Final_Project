$(function () {
  // updateBudget();

  $(".chosen-select").chosen({
    no_results_text: "Oops, nothing found!",
  });

});

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
  label = ""

  switch (score) {
    case 1:
      label="not at all important"
      break;
    case 2:
      label="not very important"
      break;
    case 3:
      label="somewhat important"
      break;
    case 4:
      label="very important"
      break;
    default:
      label="extremely important"
  }
  $(".safety").text(label);


}