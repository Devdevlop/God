import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4 flex gap-4">
      <Link to="/" className="hover:underline">Home</Link>
      <Link to="/dashboard" className="hover:underline">Dashboard</Link>
      <Link to="/upload" className="hover:underline">Upload</Link>
    </nav>
  );
}
