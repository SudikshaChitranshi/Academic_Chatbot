import React, { useState, useEffect } from "react";
import "./ElectiveReco.css"; 
export default function ElectiveReco() {
  const [form, setForm] = useState({
    student_id: "",
    name: "",
    branch: "CSE",
    semester: 1,
    cgpa: 0.0,
    preferences: "",
    taken_courses: [],
  });

  const [courses, setCourses] = useState([]);
  const [allCourseIDs, setAllCourseIDs] = useState([]);
  const [domains, setDomains] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("/Data/Course_data.csv")
      .then((res) => res.text())
      .then((csv) => {
        const lines = csv.trim().split("\n");
        const headers = lines[0].split(",").map(h => h.trim().replace(/\r/g, ""));
        console.log("Headers:", headers);
        const domainIndex = headers.indexOf("Domain");
        const idIndex = headers.indexOf("Course ID");
        const nameIndex = headers.indexOf("Name");
        const diffIndex = headers.indexOf("Difficulty");

        const parsed = lines.slice(1).map((line) => {
          const cols = line.split(",").map(cell => cell.replace(/^"|"$/g, "").trim());
          return {
            id: cols[idIndex],
            name: cols[nameIndex],
            domain: cols[domainIndex],
            diff: cols[diffIndex],
           };
        });
        setCourses(parsed);
        setAllCourseIDs(parsed.map((c) => c.id));
        console.log("Domains parsed:", parsed.map(p => p.domain));
        setDomains([...new Set(parsed.map((c) => c.domain))]);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === "semester" ? Number(value) : value,
    }));
  };

  const handleMultiSelect = (e) => {
    const options = Array.from(e.target.selectedOptions).map((o) => o.value);
    setForm((prev) => ({ ...prev, taken_courses: options }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      setRecommendations(data);
    } catch (err) {
      console.error("Recommendation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reco-container">
      <h2 className="reco-title">🎓 Elective Recommendation System</h2>
      <form className="reco-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <input name="student_id" placeholder="Enrollment Number" required onChange={handleChange} />
          <input name="name" placeholder="Name" required onChange={handleChange} />
        </div>

        <div className="form-group">
          <select name="branch" value={form.branch} onChange={handleChange}>
            <option value="CSE">CSE</option>
            <option value="ECE">ECE</option>
          </select>

          <input
            name="semester"
            type="number"
            min="1"
            max="8"
            value={form.semester}
            onChange={handleChange}
            placeholder="Semester"
          />

          <input
            name="cgpa"
            type="number"
            step="0.1"
            min="0"
            max="10"
            placeholder="CGPA"
            onChange={handleChange}
          />
        </div>

        
          <select name="preferences" value={form.preferences} onChange={handleChange}>
            <option value="">Select Domain</option>
            {domains.map((domain, i) => (
              <option key={i} value={domain}>{domain}</option>
            ))}
          </select>
        <div className="form-group">
          <select multiple value={form.taken_courses} onChange={handleMultiSelect}>
            {allCourseIDs.map((cid, i) => (
              <option key={i} value={cid}>{cid}</option>
            ))}
          </select>
        </div>

        <button className="reco-button" type="submit" disabled={loading}>
          {loading ? "Generating..." : "Get Recommendations"}
        </button>
      </form>

      {recommendations && recommendations.length > 0 && (
        <div className="recommendation-section">
          <h3>✅ Recommended Courses</h3>
          <table>
            <thead>
              <tr>
                <th>Course ID</th>
                <th>Name</th>
                <th>Domain</th>
                <th>Difficulty</th>
              </tr>
            </thead>
            <tbody>
              {recommendations.map((course, i) => (
                <tr key={i}>
                  <td>{course["Course ID"]}</td>
                  <td>{course["Name"]}</td>
                  <td>{course["Domain"]}</td>
                  <td>{course["Difficulty"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
