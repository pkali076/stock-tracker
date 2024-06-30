//import webpackConfig from "../../webpack.config";
import MyLibrary from webpackConfig

document.addEventListener('DOMContentLoaded', (event) => {
    const labels = JSON.parse(document.getElementById('labelsData').textContent);
    const data = JSON.parse(document.getElementById('chartData').textContent);

    // Make sure MyLibrary is accessible
    if (typeof MyLibrary !== 'undefined' && MyLibrary.createChart) {
        MyLibrary.createChart(labels, data);
    } else {
        console.error('MyLibrary or createChart is not defined');
    }
});
