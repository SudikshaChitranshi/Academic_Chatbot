import React, { useEffect, useState } from 'react';
import { useSession } from '../useSession';
import GPAChart from '../GPAChart';

export default function GPAView() {
  const { session } = useSession();
  const [gpaData, setGpaData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchGPA = async () => {
      setLoading(true);
      try {
        const res = await fetch('http://localhost:5000/api/gpa', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session })
        });
        const data = await res.json();
        setGpaData(data);
      } catch (e) {
        console.error("Error fetching GPA:", e);
      } finally {
        setLoading(false);
      }
    };

    if (session?.enrollment && session?.password) {
      fetchGPA();
    }
  }, [session]);

  if (loading) return <p>⏳ Loading GPA data...</p>;
  if (!gpaData?.graph_data) return <p>No GPA data available.</p>;

  const chartData = {
    labels: gpaData.graph_data.map((d) => `Sem ${d[0]}`),
    datasets: [
      {
        label: 'SGPA',
        data: gpaData.graph_data.map((d) => d[1]),
        borderColor: 'blue',
        fill: false,
        tension: 0.3,
      },
      {
        label: 'CGPA',
        data: gpaData.graph_data.map((d) => d[2]),
        borderColor: 'green',
        fill: false,
        tension: 0.3,
      }
    ]
  };

  return (
    <div>
      <p>{gpaData.summary}</p>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
        {/* Chart Container */}
        <div style={{ flexBasis: '60%', height: '75vh',  width: '75vh', position:'relative' }}>
          <GPAChart data={chartData} />
        </div>

        {/* Table Container */}
        <div style={{ flexBasis: '25%', height: '25vh',  width: '25vh', position:'relative' }}>
          <h4>📋 SGPA & CGPA Summary</h4>
          <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
            <thead>
              <tr>
                <th>Semester</th>
                <th>SGPA</th>
                <th>CGPA</th>
              </tr>
            </thead>
            <tbody>
              {gpaData.graph_data.map(([sem, sgpa, cgpa], i) => (
                <tr key={i}>
                  <td>{sem}</td>
                  <td>{sgpa}</td>
                  <td>{cgpa}</td>
                </tr>
              ))}
            </tbody>
          </table>
        <p style={{ whiteSpace: 'pre-wrap', marginBottom: '1rem' }}>{gpaData.reply}</p>
        </div>
      </div>
    </div>
  );
}

     