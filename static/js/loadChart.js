// import { Chart } from "chart.js/auto";
// import 'chartjs-adapter-date-fns';
// import {enUs} from 'date-fns/locale'

function createChart(labels, data) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Stock Price',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    const labels = JSON.parse(document.getElementById('labelsData').textContent);
    const data = JSON.parse(document.getElementById('chartData').textContent);
    createChart(labels, data);
});











// document.addEventListener('DOMContentLoaded', (event) => {
//     const labels = JSON.parse(document.getElementById('labelsData').textContent);
//     const data = JSON.parse(document.getElementById('chartData').textContent);

//     const ctx = document.getElementById('stockChart').getContext('2d');
//     new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: labels,
//             datasets: [{
//                 label: 'Stock Price',
//                 data: data,
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 borderWidth: 1,
//                 fill: false
//             }]
//         },
//         options: {
//             scales: {
//                 x: {
//                     type: 'time',
//                     time: {
//                         unit: 'minute'
//                     }
//                 },
//                 y: {
//                     beginAtZero: false
//                 }
//             }
//         }
//     });
// });
