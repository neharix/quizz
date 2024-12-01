let true_answers = JSON.parse(
  document.querySelector("#true-answers").textContent
);
let false_answers = JSON.parse(
  document.querySelector("#false-answers").textContent
);
let empty_answers = JSON.parse(
  document.querySelector("#empty-answers").textContent
);

new Chart(document.getElementById("chart").getContext("2d"), {
  type: "doughnut",
  data: {
    labels: ["Dogry", "Ýalňyş", "Jogapsyz"],
    datasets: [
      {
        label: "Jogaplar",
        data: [true_answers, false_answers, empty_answers],
        backgroundColor: ["#27ee7f", "#ee277d", "#a29c9e"],
      },
    ],
  },
  options: {},
});
