import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSession } from '../useSession'; // ← use your custom hook
import './Login.css';

export default function Login() {
  const [enrollment, setEnrollment] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { saveSession } = useSession(); // ← use it here directly

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!enrollment || !password) {
      setError("Both fields are required");
      return;
    }

    try {
      // You can make an API request here if needed
      // For now, just saving locally
      saveSession({ enrollment, password }); // ← save session
      navigate('/dashboard'); // ← redirect after login
    } catch (err) {
      console.error(err);
      setError("Login failed.");
    }
  };

  return (
    <div className="login-container">
      <h2>Student Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Enrollment Number"
          value={enrollment}
          onChange={(e) => setEnrollment(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
}
