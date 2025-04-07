
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const gologin = async() =>{
    navigate("/login")
  }
    return (
      <div className="p-6">
        <h1 className="text-3xl font-bold">Home - Video List</h1>
        <p onClick={gologin}>Videos from the database will be displayed here.</p>

      </div>
    );
  }
  