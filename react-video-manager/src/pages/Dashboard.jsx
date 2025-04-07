import { useEffect, useState } from "react";
import { getAdminData, isAuthenticated } from "../services/api";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated()) {
      setError("❌ Access Denied. Please log in.");
      return;
    }

    const fetchData = async () => {
      try {
        const data = await getAdminData();
        setMessage(data.message);
      } catch (err) {
        setError(err || "❌ Authentication failed.");
      }
    };

    fetchData();
  }, []);

  // ✅ Show access denial if token is missing or invalid
  if (error) {
    return (
      <div className="p-6 text-center">
        <h1 className="text-red-500 text-xl">{error}</h1>
        <button
          className="mt-4 bg-gray-700 text-white px-4 py-2 rounded"
          onClick={() => navigate("/")}
        >
          Back to Login
        </button>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* ✅ Button to upload route (after MFA) */}
      <button
        onClick={() => navigate("/upload")}
        className="bg-blue-500 text-white px-4 py-2 rounded mt-4 hover:bg-blue-700 transition"
      >
        Upload Data
      </button>

      {/* ✅ Show admin welcome or protected message */}
      <p className="mt-4">{message}</p>
    </div>
  );
}
