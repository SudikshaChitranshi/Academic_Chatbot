import React, { useEffect, useState } from 'react';
import { useSession } from '../useSession';

export default function AttendanceView() {
  const { session } = useSession();
  const [semesters, setSemesters] = useState([]);
  const [selectedSem, setSelectedSem] = useState('');
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch semester list on mount
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
        console.error(err);
        setError('Failed to load semesters.');
      }
    };
    fetchSemesters();
  }, [session]);

  // Fetch attendance when a semester is selected
  useEffect(() => {
    const fetchAttendance = async () => {
      if (!selectedSem) return;
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
        console.error(err);
        setError('Failed to load attendance.');
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

      {loading ? (
        <p>⏳ Loading attendance...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : attendance.length > 0 ? (
        <table border="1" cellPadding="8">
          <thead>
            <tr>
              <th>Subject</th>
              <th>Total Classes</th>
              <th>Attended</th>
              <th>Attendance %</th>
            </tr>
          </thead>
          <tbody>
            {attendance.map((sub, i) => (
              <tr key={i}>
                <td>{sub.subject}</td>
                <td>{sub.total}</td>
                <td>{sub.attended}</td>
                <td>{sub.percent}%</td>
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
