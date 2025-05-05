import React from 'react';
import { useNavigate } from 'react-router-dom';
import './navbar.css';

function Navbar() {
  const navigate = useNavigate(); // Tambahkan useNavigate

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <img src="/assets/logo.png" alt="Logo" />
      </div>
      <ul className="navbar-menu">
        <button onClick={() => navigate('/')}>Home</button>
        <button onClick={() => navigate('/prediksi')}>Prediksi</button>
        <button onClick={() => navigate('/riwayat')}>Riwayat</button>
      </ul>
    </nav>
  );
}

export default Navbar;
