import { useState, useEffect } from "react";

let globalSession = null;

export function useSession() {
  const [session, setSession] = useState(globalSession);

  const saveSession = (data) => {
    globalSession = data;
    setSession(data);
  };

  const clearSession = () => {
    globalSession = null;
    setSession(null);
  };

  return { session, saveSession, clearSession };
}
