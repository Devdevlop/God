import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import MFAPage from "./pages/MFAPage";
import UploadPage from "./pages/UploadPage";
import Home from "./pages/Home";


function App() {
  return (
    <Routes> {/* ✅ Only keep <Routes>, no <Router> here */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/mfa" element={<MFAPage />} />
      <Route path="/upload" element={<UploadPage />} />
    </Routes>
  );
}

export default App;
