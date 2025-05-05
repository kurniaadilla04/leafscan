import {useState, useEffect} from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Beranda from './pages/Beranda';
import Prediksi from './pages/Prediksi';
import Riwayat from './pages/Riwayat';
import axios from 'axios';
import ExampleComponent from './components/ExampleComponent'; 
import { useNavigate } from 'react-router-dom'; 


const  App = () => {

  const [cont, setCount] = useState(0);
  const [array, setArray] = useState([]);

  const fetchAPI = async () => {
    const response = await axios.get("http://localhost:8080/api/users"); // Updated to match Flask route
    setArray(response.data.users);
  }

  useEffect(() => {
    fetchAPI();
  }, []);
    
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Beranda />} />
        <Route path="/prediksi" element={<Prediksi />} />
        <Route path="/riwayat" element={<Riwayat />} />
        <Route path="*" element={<h1>404 - Page Not Found</h1>} /> {/* Rute fallback */}
      </Routes>
      {/* Menampilkan daftar pengguna */}
      {array.map((user, index) => (
        <div key={index}>
          <span>{user}</span>
          <br />
        </div>
      ))}
    </>
  );
}

export default App;
