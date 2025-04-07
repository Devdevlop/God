import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

// Get Token from Local Storage
const getToken = () => localStorage.getItem("access_token");

// Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Automatically attach token to all requests
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ 1️⃣ Admin Login
export const adminLogin = async (username, password) => {
  try {
    const response = await apiClient.post("/admin/login", { username, password });

    if (response.data.mfa_required) {
      return { success: false, mfaRequired: true, username };
    }

    if (response.data.access_token) {
      localStorage.setItem("access_token", response.data.access_token);
      return { success: true };
    }

    return { success: false };
  } catch (error) {
    throw error.response?.data?.detail || "Login failed. Try again.";
  }
};

// ✅ 2️⃣ Is Authenticated
export const isAuthenticated = () => {
  return !!getToken();
};

// ✅ 3️⃣ Get Admin Protected Data
export const getAdminData = async () => {
  try {
    const response = await apiClient.get("/admin/protected");
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || "Authentication failed.";
  }
};

// ✅ 4️⃣ Logout
export const logoutAdmin = () => {
  localStorage.removeItem("access_token");
};

// ✅ 5️⃣ Generate MFA QR
export const generateQRCode = async (username) => {
  try {
    const response = await apiClient.get(`/mfa/generate/${username}`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || "Failed to generate MFA QR Code.";
  }
};

// ✅ 6️⃣ Verify OTP
export const verifyOTP = async (username, otp) => {
  try {
    const response = await apiClient.post("/mfa/debug", {
      username,
      token: otp,
    });

    if (response.data.access_token) {
      localStorage.setItem("access_token", response.data.access_token);
    }

    return {
      success: response.data.verified === true || !!response.data.access_token,
      access_token: response.data.access_token || null,
    };
  } catch (error) {
    throw error.response?.data?.detail || "Invalid OTP. Try again.";
  }
};

// ✅ 7️⃣ Upload File After MFA
export const uploadFile = async (file, otp) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await apiClient.post("/upload-data", formData, {
      headers: {
        Authorization: `Bearer ${getToken()}`,
        "X-MFA-TOKEN": otp,
      },
    });

    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || "File upload failed.";
  }
};
