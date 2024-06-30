document.addEventListener('DOMContentLoaded', (event) => {
    const labels = JSON.parse(document.getElementById('labelsData').textContent);
    const data = JSON.parse(document.getElementById('chartData').textContent);

    import('./bundle.js').then(module => {
        module.createChart(labels, data);
    }).catch(error => {
        console.error('Error importing module:', error);
    });
});
