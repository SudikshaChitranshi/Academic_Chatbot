import React, { useState, useEffect } from 'react';
import { useSession } from '../useSession';
import AttendanceView from './AttendanceView';
import GPAView from './GPAView';
import MarksView from './MarksView';


export default function AcademicInfo() {
  const { session } = useSession();
  const [activeTab, setActiveTab] = useState('gpa');
  const [loading, setLoading] = useState(false);
  const [examData, setExamData] = useState(null);

  useEffect(() => {
    if (!session?.enrollment || !session?.password) return;
  }, [activeTab, session]);

  const renderTabContent = () => {
    if (loading) return <p>⏳ Loading...</p>;

    switch (activeTab) {
      case 'gpa':
        return <GPAView />; 

      case 'attendance':
        return <AttendanceView />;

      case 'marks':
        return <MarksView />;

      case 'exams':
        return "No exams scheduled as of now."

      default:
        return null;
    }
  };

  return (
    <div>
      <h2>📊 Performance Tracker</h2>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <button onClick={() => setActiveTab('gpa')}>📈 CGPA Trend</button>
        <button onClick={() => setActiveTab('attendance')}>📊 Attendance</button>
        <button onClick={() => setActiveTab('marks')}>📝 Marks</button>
        <button onClick={() => setActiveTab('exams')}>📅 Exam Schedule</button>
      </div>
      <div>{renderTabContent()}</div>
    </div>
  );
}
