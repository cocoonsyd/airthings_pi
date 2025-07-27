import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';
import 'chart.js/auto'; // Important for automatic scale registration

// Register the necessary components for Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);

// Define the structure of a single sensor reading
interface SensorReading {
  id: number;
  timestamp: string;
  temperature: number;
  humidity: number;
  radon_short_term_avg: number;
  radon_long_term_avg: number;
  co2: number;
  voc: number;
}

function App() {
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch data from our Flask backend API
    fetch('/api/v1/readings')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setReadings(data))
      .catch(error => {
        console.error("Fetch error:", error);
        setError("Failed to fetch data. Make sure the backend server is running.");
      });
  }, []);

  // Helper function to create chart data for a specific sensor metric
  const createChartData = (label: string, dataKey: keyof SensorReading) => {
    return {
      labels: readings.map(r => new Date(r.timestamp).toLocaleString()),
      datasets: [
        {
          label: label,
          data: readings.map(r => r[dataKey]),
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };
  };

  if (error) {
    return <div style={{ padding: '2rem', color: 'red' }}>{error}</div>;
  }

  if (readings.length === 0) {
    return <div style={{ padding: '2rem' }}>Loading data or no readings found...</div>;
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '1rem' }}>
      <h1>Airthings Sensor Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <div>
          <h2>Temperature (°C)</h2>
          <Line data={createChartData('Temperature', 'temperature')} />
        </div>
        <div>
          <h2>Humidity (%)</h2>
          <Line data={createChartData('Humidity', 'humidity')} />
        </div>
        <div>
          <h2>Radon (Short Term Avg - Bq/m³)</h2>
          <Line data={createChartData('Radon Short Term', 'radon_short_term_avg')} />
        </div>
        <div>
          <h2>CO₂ (ppm)</h2>
          <Line data={createChartData('CO2', 'co2')} />
        </div>
        <div>
          <h2>VOC (ppb)</h2>
          <Line data={createChartData('VOC', 'voc')} />
        </div>
      </div>
    </div>
  );
}

export default App;