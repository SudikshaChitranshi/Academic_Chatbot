import React, { useState } from "react";
import "./LoginPopup.css"; // optional styling

function LoginPopup({ onClose, onSubmit }) {
  const [enrollment, setEnrollment] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = () => {
    if (enrollment && password) {
      onSubmit({ enrollment, password });
      onClose();
    }
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3>Login Required</h3>
        <input
          type="text"
          placeholder="Enrollment No"
          value={enrollment}
          onChange={(e) => setEnrollment(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
}

export default LoginPopup;
