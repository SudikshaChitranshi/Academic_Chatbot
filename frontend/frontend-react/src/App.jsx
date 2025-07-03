import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import { useSession } from "./useSession";

// Protected route wrapper
function ProtectedRoute({ element }) {
  const { session } = useSession();

  if (!session) {
    return <Navigate to="/" replace />;
  }

  return element;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/dashboard"
          element={<ProtectedRoute element={<Dashboard />} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
