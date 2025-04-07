import { useState } from "react";
import { uploadFile } from "../services/api";
import useAuth from "../context/useAuth";

export default function UploadPage() {
  const { isMFACompleted } = useAuth();
  const [file, setFile] = useState(null);
  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleUpload = async () => {
    setMessage("");
    setError("");

    if (!file) {
      setError("Please select a file.");
      return;
    }

    if (!otp) {
      setError("Please enter your MFA OTP.");
      return;
    }

    try {
      const response = await uploadFile(file, otp);
      setMessage(`✅ Success: ${response.message}`);
    } catch (uploadError) {
      console.error("File Upload Error:", uploadError);
      setError("❌ File upload failed. Invalid OTP or server error.");
    }
  };

  if (!isMFACompleted) {
    return <p className="text-red-500 text-center mt-6">❌ Access Denied. Please verify MFA first.</p>;
  }

  return (
    <div className="p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold">Upload Data</h1>

      {/* File Input */}
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mt-4 border p-2 rounded w-full"
      />

      {/* OTP Input */}
      <input
        type="text"
        placeholder="Enter MFA OTP"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        className="mt-4 border p-2 rounded w-full"
      />

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        className="bg-blue-500 text-white px-4 py-2 mt-4 rounded hover:bg-blue-700 transition"
      >
        Upload
      </button>

      {/* Success or Error Message */}
      {message && <p className="text-green-500 mt-4">{message}</p>}
      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
}
