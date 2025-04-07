import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { adminLogin, verifyOTP } from "../services/api";
import useAuth from "../context/useAuth";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [mfaRequired, setMfaRequired] = useState(false);
  const navigate = useNavigate();
  const { setUser, setIsMFACompleted } = useAuth();

  // ✅ Debugging: Ensure component is rendering
  useEffect(() => {
    console.log("🔄 Login Component Rendered");
  }, []);

  const handleLogin = async () => {
    setError("");
    setMfaRequired(false); // ✅ Reset MFA requirement on new login attempt

    try {
      console.log("🟢 Attempting Login...");
      const response = await adminLogin(username, password);

      if (response.mfaRequired) {
        console.log("🔒 MFA Required, Showing OTP Input");
        setMfaRequired(true); // ✅ Show OTP input field
      } else if (response.success) {
        console.log("✅ Login Successful! Navigating to dashboard...");
        setUser({ username });
        navigate("/dashboard"); // ✅ Redirect after successful login
      } else {
        setError("⚠️ Unexpected login response. Please try again.");
      }
    } catch (err) {
      console.error("❌ Login Error:", err);
      setError(err || "Login failed. Try again.");
    }
  };

  const handleVerifyOTP = async () => {
    setError("");

    try {
      console.log("🔑 Verifying OTP...");
      const response = await verifyOTP(username, otp);

      if (response.success) {
        console.log("✅ MFA Verification Successful! Navigating to dashboard...");
        setIsMFACompleted(true);
        setUser({ username });
        navigate("/mfa"); // ✅ Redirect after MFA verification
      } else {
        setError("⚠️ Unexpected response. Try again.");
      }
    } catch (err) {
      console.error("❌ OTP Verification Error:", err);
      setError(err.message || "Invalid OTP. Try again.");
    }
  };

  return (
    <div className="p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold">Admin Login</h1>

      {!mfaRequired ? (
        <>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border p-2 rounded w-full mt-4"
            onKeyDown={(e) => e.key === "Enter" && handleLogin()} // ✅ Press Enter to login
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border p-2 rounded w-full mt-4"
            onKeyDown={(e) => e.key === "Enter" && handleLogin()} // ✅ Press Enter to login
          />

          <button
            onClick={handleLogin}
            className="bg-blue-500 text-white px-4 py-2 mt-4 rounded hover:bg-blue-700 transition"
          >
            Login
          </button>
        </>
      ) : (
        <>
          <p className="mt-4">Enter the OTP from Google Authenticator:</p>
          <input
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            className="border p-2 rounded w-full mt-4"
            onKeyDown={(e) => e.key === "Enter" && handleVerifyOTP()} // ✅ Press Enter to verify OTP
          />

          <button
            onClick={handleVerifyOTP}
            className="bg-green-500 text-white px-4 py-2 mt-4 rounded hover:bg-green-700 transition"
          >
            Verify OTP
          </button>
        </>
      )}

      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}
