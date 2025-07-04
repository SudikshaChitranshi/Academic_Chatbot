import React, { useEffect, useState } from 'react';
import { useSession } from '../useSession';

export default function AttendanceView() {
  const { session } = useSession();
  const [semesters, setSemesters] = useState([]);
  const [selectedSem, setSelectedSem] = useState('');
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [goal, setGoal] = useState(85); // default goal

  const calculateClassesNeeded = (attended, total, goal) => {
  const currentPercent = (attended / total) * 100;
  if (currentPercent >= goal) return '✅ Goal met';
  const required = Math.ceil((goal * total - 100 * attended) / (100 - goal));
  return `➕ ${required} more`;
};

  // 1️⃣ Fetch available semesters
  useEffect(() => {
    const fetchSemesters = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/semesters/attendance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session })
        });
        const data = await res.json();
        setSemesters(data);
        if (data.length > 0) setSelectedSem(data[0].registration_id);
      } catch (err) {
        console.error("Failed to load semesters:", err);
      }
    };
    fetchSemesters();
  }, [session]);

  // 2️⃣ Fetch attendance when a semester is selected
  useEffect(() => {
    if (!selectedSem) return;

    const fetchAttendance = async () => {
      setLoading(true);
      try {
        const res = await fetch('http://localhost:5000/api/attendance', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session, semester_id: selectedSem })
        });
        const data = await res.json();
        setAttendance(data);
      } catch (err) {
        console.error("Failed to fetch attendance:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAttendance();
  }, [selectedSem]);

  return (
    <div>
      <h3>📊 Attendance Viewer</h3>

      {semesters.length > 0 && (
        <select
          value={selectedSem}
          onChange={(e) => setSelectedSem(e.target.value)}
          style={{ marginBottom: '1rem', padding: '8px' }}
        >
          {semesters.map((sem) => (
            <option key={sem.registration_id} value={sem.registration_id}>
              {sem.registration_code}
            </option>
          ))}
        </select>
      )}
      
      <div style={{ marginBottom: '1rem' }}>
        🎯 Set Attendance Goal:
        <input
          type="number"
          value={goal}
          onChange={(e) => setGoal(Number(e.target.value))}
          min={1}
          max={100}
          style={{ marginLeft: '10px', padding: '5px', width: '60px' }}
        />
        <span>%</span>
      </div>

      {loading ? (
        <p>⏳ Loading attendance...</p>
      ) : attendance.length ? (
        <table border="1" cellPadding="8">
          <thead>
            <tr>
              <th>Subject</th>
              <th>Total</th>
              <th>Attended</th>
              <th>Percent</th>
              <th>🎯 To Reach {goal}%</th>
            </tr>
          </thead>
          <tbody>
            {attendance.map((row, i) => (
              <tr key={i}>
                <td>{row.subject}</td>
                <td>{row.total}</td>
                <td>{row.attended}</td>
                <td>{row.percent}%</td>
                <td>{calculateClassesNeeded(row.attended, row.total, goal)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No attendance data available.</p>
      )}
    </div>
  );
}
