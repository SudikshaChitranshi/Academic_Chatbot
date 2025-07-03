import React, { useState } from 'react';
import ChatApp from '../components/ChatBox';
import ElectiveReco from '../components/ElectiveReco';
import AcademicInfo from '../components/AcademicInfo';
import './Dashboard.css';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('chatbot');

  const renderContent = () => {
    switch (activeTab) {
      case 'electives':
        return <ElectiveReco />;
      case 'academic info':
        return <AcademicInfo />;
      default:
        return <ChatApp />;
    }
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <h2>JIIT One</h2>
        <button onClick={() => setActiveTab('chatbot')}>💬 Chatbot</button>
        <button onClick={() => setActiveTab('electives')}>📘 Elective Recommendation</button>
        <button onClick={() => setActiveTab('academic info')}>📊 Academic Info</button>
      </aside>

      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}
