let challenge_pk = JSON.parse(document.querySelector("#challenge-pk").textContent);
let users = [];
let colors = [];
let scores = [];

let chart = new Chart(
    document.getElementById('challenge-chart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: "",
                data: [],
                backgroundColor: []
            }]
        },
    options: {
        indexAxis: 'y',
    }
    }
);

function initializeUser(user, score) {
    users.push(user);
    scores.push(score);
    colors.push(getRandomColor());
}


function getRandomColor() {
    color = "hsl(" + Math.random() * 360 + ", 100%, 75%)";
    return color;
}

function success(data) {
    data.forEach(row => {
        if (users.includes(row.last_name + " " + row.first_name)){
            scores[users.indexOf(row.last_name + " " + row.first_name)] = row.true_answer;
        }
        else {
            initializeUser(row.last_name + " " + row.first_name, row.true_answer);
        }
    });

    chart.data.labels = users;
    chart.data.datasets[0].data = scores;
    chart.data.datasets[0].backgroundColor = colors;
    chart.update();

}


function update() {
    $.ajax({
        url: "/api/v1/get-current-data-for-chart/" + challenge_pk + "/",
        type: 'GET',
        dataType: 'json',
        success: success,
    });
}

const updater = setInterval(update, 10000);

update();