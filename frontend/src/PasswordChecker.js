import React, { useState } from "react";
import axios from "axios";
import { FaEye, FaEyeSlash } from "react-icons/fa"; // Eye icons import
import "./App.css";

function PasswordChecker() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [generated, setGenerated] = useState("");
  const [showPassword, setShowPassword] = useState(false); // toggle eye
  const [copied, setCopied] = useState(false); // 👈 new state

  const checkPassword = async (pwd) => {
    if (!pwd) {
      setResult(null);
      return;
    }
    try {
      const res = await axios.post("http://127.0.0.1:5000/check_password", {
        password: pwd,
      });
      setResult(res.data);
    } catch (error) {
      console.error("Error checking password:", error);
    }
  };

  const generatePassword = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/generate_password");
      if (res.data && res.data.generated_password) {
        setGenerated(res.data.generated_password);
        setPassword(res.data.generated_password);
        checkPassword(res.data.generated_password);
        setCopied(false); // reset copy state jab naya password aayega
      }
    } catch (error) {
      console.error("Error generating password:", error);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generated);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000); // 2s baad reset
  };

  return (
    <div className="card">
      <h1>Password Strength Checker 🔐</h1>

      {/* Password input with eye toggle */}
      <div className="password-input-container">
        <input
          type={showPassword ? "text" : "password"}
          placeholder="Enter your password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            checkPassword(e.target.value);
          }}
        />
        <span
          className="eye-icon"
          onClick={() => setShowPassword(!showPassword)}
        >
          {showPassword ? <FaEyeSlash /> : <FaEye />}
        </span>
      </div>

      <button onClick={() => checkPassword(password)}>Check Strength</button>
      <button
        onClick={generatePassword}
        style={{ marginTop: "10px", background: "#28a745" }}
      >
        Generate Secure Password 🔑
      </button>

      {generated && (
        <p style={{ color: "#00ffcc", marginTop: "10px" }}>
          Generated: <b>{generated}</b>{" "}
          <button onClick={handleCopy} style={{ marginLeft: "10px" }}>
            {copied ? "✅ Copied!" : "📋 Copy"}
          </button>
        </p>
      )}

      {result && (
        <>
          <div className={`strength-bar ${result.strength.toLowerCase()}`}></div>
          <div className="strength-text">{result.strength}</div>
          <p style={{ color: "#ddd" }}>Entropy: {result.entropy} bits</p>
          <p
            style={{
              color: result.breach_status.includes("⚠️") ? "red" : "lime",
            }}
          >
            {result.breach_status}
          </p>
          <ul style={{ textAlign: "left", color: "white" }}>
            {result.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default PasswordChecker;
