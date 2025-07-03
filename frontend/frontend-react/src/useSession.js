import { useState, useEffect } from "react";

let globalSession = JSON.parse(sessionStorage.getItem("session")) || null;

export function useSession() {
  const [session, setSession] = useState(globalSession);

  const saveSession = (data) => {
    globalSession = data;
    sessionStorage.setItem("session", JSON.stringify(data));
    setSession(data);
  };

  const clearSession = () => {
    globalSession = null;
    sessionStorage.removeItem("session");
    setSession(null);
  };

  useEffect(() => {
    const stored = sessionStorage.getItem("session");
    if (stored) {
      const parsed = JSON.parse(stored);
      globalSession = parsed;
      setSession(parsed);
    }
  }, []);

  return { session, saveSession, clearSession };
}
