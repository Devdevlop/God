import { createContext, useState } from "react";
import { adminLogin } from "../services/api"; // ✅ Import API function

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isMFACompleted, setIsMFACompleted] = useState(false);

  // ✅ Login Function - Calls API
  const login = async (username, password) => {
    const response = await adminLogin(username, password);

    if (response.mfaRequired) {
      return { mfaRequired: true, username }; // ✅ Ask for MFA in frontend
    }

    if (response.success) {
      setUser({ username }); // ✅ Set user after successful login
      return { success: true };
    }
  };

  // ✅ Logout Function
  const logout = () => {
    setUser(null);
    setIsMFACompleted(false);
    localStorage.removeItem("access_token"); // ✅ Remove token on logout
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout, isMFACompleted, setIsMFACompleted }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
