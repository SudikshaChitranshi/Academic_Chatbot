import React, { useEffect, useState } from 'react';
import { useSession } from '../useSession';
import './MarksView.css';

export default function MarksView() {
  const { session } = useSession();
  const [semesters, setSemesters] = useState([]);
  const [selectedSem, setSelectedSem] = useState(null);
  const [marks, setMarks] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch semesters for marks
  useEffect(() => {
    const fetchSemesters = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/semesters/marks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session })
        });
        const data = await res.json();
        setSemesters(data);
        if (data.length > 0) setSelectedSem(data[0]);
      } catch (err) {
        console.error("Failed to load semesters:", err);
      }
    };
    fetchSemesters();
  }, [session]);

  // Fetch marks for selected semester
  useEffect(() => {
    if (!selectedSem) return;

    const fetchMarks = async () => {
      setLoading(true);
      try {
        const res = await fetch('http://localhost:5000/api/marks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session,
            student: {
              registration_id: selectedSem.registration_id,
              registration_code: selectedSem.registration_code
            }
          })
        });
        const data = await res.json();
        if (data.error) {
          setMarks(null);
          return;
        }
        setMarks(data);
      } catch (err) {
        console.error("Failed to fetch marks:", err);
        setMarks(null);
      } finally {
        setLoading(false);
      }
    };

    fetchMarks();
  }, [selectedSem]);

  return (
    <div>
      <h3>📝 Marks Viewer</h3>

      {semesters.length > 0 && (
        <select
          value={selectedSem?.registration_id || ''}
          onChange={(e) => {
            const regId = e.target.value;
            const selected = semesters.find(sem => sem.registration_id === regId);
            setSelectedSem(selected);
          }}
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
        <p>⏳ Loading marks...</p>
      ) : marks && marks.courses?.length > 0 ? (
        <div>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={thStyle}>Subject</th>
                {marks.meta.exams.map((exam, i) => (
                  <th key={i} style={thStyle}>{exam}</th>
                ))}
              </tr>
            </thead>
            <tbody>
                {marks.courses.map((course, i) => (
                  <tr key={i}>
                    <td style={tdStyle}>
                      <strong>{course.name}</strong><br />
                      <small>({course.code})</small>
                    </td>
                    {marks.meta.exams.map((exam, j) => {
                      const data = course.exams[exam];
                       if (!data) {
                        return <td key={j} className="cell">-</td>;
                      }
                      const percentage = (data.OM / data.FM) * 100;
                      let performanceClass = '';
                      if (percentage >= 70) performanceClass = 'green';
                      else if (percentage >= 40) performanceClass = 'yellow';
                      else performanceClass = 'red';

                      return (
                        <td key={j} className={`cell ${performanceClass}`}>
                          {data.OM}/{data.FM}
                        </td>
                      );
                    })}
                  </tr>
                ))} 
              </tbody>
            </table>
          </div>
        ) : (     
        <p>📭 No marks available for this semester.</p>
      )}
    </div>
  );
}

const thStyle = {
  border: '1px solid #ddd',
  padding: '8px',
  backgroundColor: '#f2f2f2',
  textAlign: 'left'
};

const tdStyle = {
  border: '1px solid #ddd',
  padding: '8px',
  verticalAlign: 'top'
};


