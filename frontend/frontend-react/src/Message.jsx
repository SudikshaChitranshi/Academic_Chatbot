import React from "react";
import "./ChatApp.css";

export default function Message({ from, text }) {
  return (
    <div className={`message ${from === "user" ? "user" : "bot"}`}>
      <p>{text}</p>
    </div>
  );
}
