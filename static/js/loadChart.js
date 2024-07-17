document.addEventListener('DOMContentLoaded', (event) => {
    // Function to draw a simple line chart
    function drawLineChart(canvasId, labels, data, title) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        const width = ctx.canvas.width = window.innerWidth - 80; // Set canvas width
        const height = ctx.canvas.height = 800; // Set canvas height
        const padding = 80;

        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = 'rgba(75, 192, 192, 1)';
        ctx.lineWidth = 2;

        const maxData = Math.max(...data);
        const minData = Math.min(...data);
        const range = maxData - minData;

        const xScale = (width - padding * 2) / (labels.length - 1);
        const yScale = (height - padding * 2) / range;

        ctx.beginPath();
        for (let i = 0; i < data.length; i++) {
            const x = padding + i * xScale;
            const y = height - padding - (data[i] - minData) * yScale;
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.stroke();

        // Draw axes
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;

        // Y axis
        ctx.beginPath();
        ctx.moveTo(padding, padding);
        ctx.lineTo(padding, height - padding);
        ctx.stroke();

        // X axis
        ctx.beginPath();
        ctx.moveTo(padding, height - padding);
        ctx.lineTo(width - padding, height - padding);
        ctx.stroke();

        // Draw labels
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.font = '16px Arial';

        // X axis labels
        for (let i = 0; i < labels.length; i += Math.floor(labels.length / 10)) {
            const x = padding + i * xScale;
            const y = height - padding + 30;
            ctx.fillText(labels[i].split(' ')[1], x, y);
        }

        // Y axis labels
        for (let i = 0; i <= 5; i++) {
            const y = height - padding - i * (height - padding * 2) / 5;
            const text = (minData + i * range / 5).toFixed(2);
            ctx.fillText(text, padding - 50, y);
        }

        // Chart title
        ctx.fillText(title, width / 2, padding / 2);

        // X-axis label
        ctx.fillText("Time", width / 2, height - 40);

        // Y-axis label (rotate and then draw)
        ctx.save();
        ctx.translate(40, height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText("Price", 0, 0);
        ctx.restore();
    }

    // Fetch data for each chart and draw the charts
    const chartConfigs = [
        { canvasId: 'intradayChart', labelsId: 'intradayLabels', dataId: 'intradayData', title: 'Intraday' },
        { canvasId: 'dailyChart', labelsId: 'dailyLabels', dataId: 'dailyData', title: 'Daily' },
        { canvasId: 'weeklyChart', labelsId: 'weeklyLabels', dataId: 'weeklyData', title: 'Weekly' },
        { canvasId: 'monthlyChart', labelsId: 'monthlyLabels', dataId: 'monthlyData', title: 'Monthly' }
    ];

    chartConfigs.forEach(config => {
        const labels = JSON.parse(document.getElementById(config.labelsId).textContent);
        const data = JSON.parse(document.getElementById(config.dataId).textContent);
        drawLineChart(config.canvasId, labels, data, config.title);
    });
});

