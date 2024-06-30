document.addEventListener('DOMContentLoaded', (event) => {
    const labels = JSON.parse(document.getElementById('labelsData').textContent);
    const data = JSON.parse(document.getElementById('chartData').textContent);

    const ctx = document.getElementById('stockChart').getContext('2d');

    // Function to draw a simple line chart
    function drawLineChart(ctx, labels, data) {
        const width = ctx.canvas.width;
        const height = ctx.canvas.height;
        const padding = 40;

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

        // X axis labels
        for (let i = 0; i < labels.length; i += Math.floor(labels.length / 10)) {
            const x = padding + i * xScale;
            const y = height - padding + 10;
            ctx.fillText(labels[i].split(' ')[1], x, y);
        }

        // Y axis labels
        for (let i = 0; i <= 5; i++) {
            const y = height - padding - i * (height - padding * 2) / 5;
            const text = (minData + i * range / 5).toFixed(2);
            ctx.fillText(text, padding - 30, y);
        }

        // X-axis label
        ctx.fillText("Time", width / 2, height - 10);

        // Y-axis label (rotate and then draw)
        ctx.save();
        ctx.translate(10, height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText("Price", 0, 0);
        ctx.restore();
    }

    drawLineChart(ctx, labels, data);
});
