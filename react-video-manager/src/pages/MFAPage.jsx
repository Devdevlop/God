import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { generateQRCode, verifyOTP } from "../services/api";
import useAuth from "../context/useAuth";

export default function MFAPage() {
  const { user, setUser, setIsMFACompleted, isMFACompleted } = useAuth();
  const [qrCode, setQrCode] = useState("");
  const [secret, setSecret] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);
  const navigate = useNavigate();

  // ✅ Check for missing JWT token or unauthenticated access
  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setError("❌ Access Denied. You must be logged in.");
    }
  }, []);

  useEffect(() => {
    const fetchQRCode = async () => {
      try {
        if (!user || !user.username) {
          setError("User not found. Please log in again.");
          return;
        }

        const data = await generateQRCode(user.username);
        setQrCode(`data:image/png;base64,${data.qr_code}`);
        setSecret(data.mfa_secret);

        if (data.mfa_enabled === true) {
          navigate("/dashboard");
        }
      } catch (err) {
        console.error("QR Code Generation Error:", err);
        setError("Failed to generate QR Code. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (localStorage.getItem("access_token")) {
      fetchQRCode();
    }
  }, [user, setIsMFACompleted, navigate]);

  const handleVerify = async () => {
    setError("");

    try {
      setVerifying(true);
      const response = await verifyOTP(user.username, otp);

      if (response.success) {
        setIsMFACompleted(true);
        setUser({ username: user.username });
        navigate("/dashboard");
      } else {
        setError("⚠️ Unexpected response. Try again.");
      }
    } catch (err) {
      console.error("❌ OTP Verification Error:", err);
      setError(err.message || "Invalid OTP. Try again.");
    } finally {
      setVerifying(false);
    }
  };

  // ✅ Block unauthorized access (no MFA and no token)
  if (!localStorage.getItem("access_token") || isMFACompleted) {
    return (
      <p className="text-red-500 text-center mt-6">
        ❌ Access Denied. Please verify MFA first.
      </p>
    );
  }

  return (
    <div className="p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold">Multi-Factor Authentication</h1>

      {loading ? (
        <p className="text-gray-500 mt-4">Loading QR Code...</p>
      ) : qrCode ? (
        <div className="mt-4 text-center">
          <img src={qrCode} alt="Scan QR for MFA" className="w-48 h-48 mx-auto" />
          <p className="mt-2 font-semibold">Secret Key (for manual setup):</p>
          <code className="bg-gray-200 p-2 rounded">{secret}</code>
        </div>
      ) : (
        <p className="text-red-500 mt-4">
          {error || "QR Code not available."}
        </p>
      )}

      {!loading && qrCode && (
        <p className="mt-4 text-center">
          Scan the QR code with your authenticator app, then enter your OTP below.
        </p>
      )}

      {!loading && !qrCode && (
        <p className="mt-4 text-center">
          Enter the OTP from your authenticator app to verify MFA.
        </p>
      )}

      <input
        type="text"
        placeholder="Enter OTP"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        className="border p-2 rounded w-full mt-4 max-w-xs"
        disabled={verifying}
      />

      <button
        onClick={handleVerify}
        disabled={verifying}
        className="bg-green-500 text-white px-4 py-2 mt-4 rounded disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {verifying ? "Verifying..." : "Verify MFA"}
      </button>

      {error && !loading && (
        <p className="text-red-500 mt-2">{error}</p>
      )}
    </div>
  );
}
