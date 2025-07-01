import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement);

const GPAChart = ({ data }) => {
  if (!data || !Array.isArray(data)) {
  return <div>No chart data available.</div>;
  }

  const chartData = {
    labels: data.map(d => `Sem ${d[0]}`),
    datasets: [
      {
        label: 'SGPA',
        data: data.map(d => d[1]),
        borderColor: 'blue',
        backgroundColor: 'blue',
        fill: false,
      },
      {
        label: 'CGPA',
        data: data.map(d => d[2]),
        borderColor: 'green',
        backgroundColor: 'green',
        fill: false,
      }
    ]
  };

  return <Line data={chartData} />;
};

export default GPAChart;
