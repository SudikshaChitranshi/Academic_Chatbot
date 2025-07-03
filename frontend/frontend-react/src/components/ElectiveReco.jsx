import React, { useState, useEffect } from 'react';
import { useSession } from '../useSession';

export default function ElectiveReco() {
  const { session } = useSession();
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!session?.enrollment || !session?.password) {
      setError("🔐 Please log in to view elective recommendations.");
      return;
    }

    const fetchRecommendations = async () => {
      setLoading(true);
      setError('');
      try {
        const res = await fetch("http://localhost:8001/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            student_id: session.enrollment,
            password: session.password,  // if used in future
            name: "Student",
            branch: "CSE",               // default/fallback
            semester: 5,                 // fallback semester
            cgpa: 7.0,                   // fallback CGPA
            preferences: "ML",           // default domain
            taken_courses: ["CS101", "CS201"]  // dummy courses
          })
        });
        const data = await res.json();
        if (data.recommendations) {
          setRecommendations(data.recommendations);
        } else {
          setError("No recommendations received.");
        }
      } catch (err) {
        console.error(err);
        setError("Failed to fetch recommendations.");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [session]);

  return (
    <div>
      <h2>📘 Elective Recommendations</h2>
      {loading && <p>⏳ Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {recommendations.length > 0 ? (
        <ul>
          {recommendations.map((rec, index) => (
            <li key={index}>
              <strong>{rec["Course ID"]}</strong> - {rec.Name} ({rec.Domain}) | Difficulty: {rec.Difficulty}
            </li>
          ))}
        </ul>
      ) : (
        !loading && !error && <p>No recommendations found.</p>
      )}
    </div>
  );
}
