let chart = new Chart(
    document.getElementById('challenge-chart').getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['user', "hell"],
            datasets: [{
                data: [10, 40],
                backgroundColor: ['violet', "red"]
            }]
        },
    options: {}
    }
);
chart.data.labels = ["sel", "hell"];