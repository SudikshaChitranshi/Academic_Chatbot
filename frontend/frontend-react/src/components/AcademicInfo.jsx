import React, { useState, useEffect } from 'react';
import { useSession } from '../useSession';
import { Line } from 'react-chartjs-2';
import AttendanceView from './AttendanceView';

export default function AcademicInfo() {
  const { session } = useSession();
  const [activeTab, setActiveTab] = useState('gpa');
  const [loading, setLoading] = useState(false);
  const [gpaData, setGpaData] = useState(null);
  const [attendanceData, setAttendanceData] = useState(null);
  const [marksData, setMarksData] = useState(null);
  const [examData, setExamData] = useState(null);

  useEffect(() => {
    if (!session?.enrollment || !session?.password) return;

    
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
    console.error(e);
  } finally {
    setLoading(false);
  }
};
    
    const fetchAttendance = async () => {
      setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session })
    });
    const data = await res.json();
    setAttendanceData(data);
  } catch (e) {
    console.error(e);
  } finally {
    setLoading(false);
  }
};

    const fetchMarks = async () => {
      setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/api/marks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session })
    });
    const data = await res.json();
    setMarksData(data);
  } catch (e) {
    console.error(e);
  } finally {
    setLoading(false);
  }
};

    if (activeTab === 'gpa' && !gpaData) fetchGPA();
    if (activeTab === 'attendance' && !attendanceData) fetchAttendance();
    if (activeTab === 'marks' && !marksData) fetchMarks();
    if (activeTab === 'exams' && !examData) fetchData();
  }, [activeTab, session]);

  const renderTabContent = () => {
    if (loading) return <p>⏳ Loading...</p>;

    switch (activeTab) {
      case 'gpa':
        return gpaData?.graph_data ? (
          <div>
            <p>{gpaData.reply}</p>
            <Line
              data={{
                labels: gpaData.graph_data.map((d) => `Sem ${d[0]}`),
                datasets: [
                  {
                    label: 'SGPA',
                    data: gpaData.graph_data.map((d) => d[1]),
                    borderColor: 'blue',
                    fill: false
                  },
                  {
                    label: 'CGPA',
                    data: gpaData.graph_data.map((d) => d[2]),
                    borderColor: 'green',
                    fill: false
                  }
                ]
              }}
            />
          </div>
        ) : <p>No GPA data available.</p>;

      case 'attendance':
        return attendanceData?.length ? (
          <table>
            <thead>
              <tr>
                <th>Subject</th>
                <th>Total Classes</th>
                <th>Attended</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              {attendanceData.map((sub, i) => (
                <tr key={i}>
                  <td>{sub.subject}</td>
                  <td>{sub.total}</td>
                  <td>{sub.attended}</td>
                  <td>{sub.percent}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p>No attendance data.</p>;

      case 'marks':
        return marksData?.length ? (
          <div>
            {marksData.map((subj, i) => (
              <div key={i}>
                <h4>{subj.subject}</h4>
                <ul>
                  {subj.tests.map((test, j) => (
                    <li key={j}>{test.type}: {test.marks}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        ) : <p>No marks data available.</p>;

      case 'exams':
        return examData?.length ? (
          <table>
            <thead>
              <tr>
                <th>Subject</th>
                <th>Exam</th>
                <th>Date</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {examData.map((exam, i) => (
                <tr key={i}>
                  <td>{exam.subject}</td>
                  <td>{exam.examType}</td>
                  <td>{exam.date}</td>
                  <td>{exam.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p>No exam schedule available.</p>;

      default:
        return null;
    }
  };

  return (
    <div>
      <h2>📚 Academic Info</h2>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <button onClick={() => setActiveTab('gpa')}>📈 GPA Trend</button>
        <button onClick={() => setActiveTab('attendance')}>📊 Attendance</button>
        <button onClick={() => setActiveTab('marks')}>📝 Marks</button>
        <button onClick={() => setActiveTab('exams')}>📅 Exam Schedule</button>
      </div>
      <div>{renderTabContent()}</div>
    </div>
  );
}
