import React from 'react';
import { Link } from 'react-router-dom';
import './Beranda.css'; // kalau kamu punya style terpisah

function Beranda() {
  return (
    <div className="beranda-container">
      <nav className="navbar">
        <Link to="/" className="navbar-logo" aria-label="Logo Aplikasi">
          <img src="/assets/logo.png" alt="Logo Aplikasi" className="logo" />
        </Link>
        <div className="navbar-menu">
          <Link to="/">Beranda</Link>
          <Link to="/prediksi">Prediksi</Link>
          <Link to="/riwayat">Riwayat</Link>
        </div>
      </nav>

      <h1 className="greeting">Haloo! Selamat datang</h1>

      <section id="beranda" className="beranda-section">
        <div className="text-container">
          <h1 className="hero-title gradient-text">Pemetikan Daun Teh dengan Citra</h1>
          <p className="hero-subtitle">"Membantu Pemetikan Daun Teh secara Efisien"</p>
          <div className="hero-buttons">
            <Link to="/prediksi" className="cta-button">Ayo Jelajahi</Link>
            <Link to="/riwayat" className="action-btn">Coba Sekarang</Link>
          </div>
        </div>
        <img src="/assets/daun-teh.png" alt="Pemetikan Daun Teh" className="tea-leaf-image" />
      </section>

      <section className="process-header">
        <div className="process-header-content">
          <h2 className="process-title">Tentang Website</h2>
          <p className="process-description">
            Website ini dirancang untuk memberikan rekomendasi pemetikan daun teh dengan memanfaatkan data dari citra, menghasilkan hasil analisis yang praktis bagi petani teh.
          </p>
          <div className="process-divider"></div>
        </div>
      </section>

      <section className="how-it-works-section">
        <h2 className="section-title">Bagaimana Cara Kerjanya?</h2>
        <p className="section-subtitle">
          Karena kita membuat website ini untuk petani, berikut panduan penggunaannya:
        </p>

        <div className="steps-container">
          <div className="step-box">
            <img src="/assets/1.png" alt="Upload Gambar" />
            <p className="step-text">Klik "Upload Gambar"</p>
          </div>
          <div className="step-box">
            <img src="/assets/2.png" alt="Pilih Gambar Daun Teh" />
            <p className="step-text">Pilih Gambar Daun Teh di perangkat Anda</p>
          </div>
          <div className="step-box">
            <img src="/assets/3.png" alt="Mulai Prediksi" />
            <p className="step-text">Klik Proses Untuk Memulai Prediksi</p>
          </div>
          <div className="step-box">
            <img src="/assets/4.png" alt="Lihat Hasil" />
            <p className="step-text">Lihat Hasil Prediksi Dilayar</p>
          </div>
        </div>
      </section>

      <section className="faq-section">
        <div className="faq-container">
          <h2 className="faq-title">FAQ – Sistem Prediksi Kematangan Daun Teh</h2>
          <div className="faq-grid">
            {/* FAQ 1 */}
            <details className="faq-item">
              <summary>
                <span className="faq-question">Apa fungsi dari website ini?</span>
                <span className="icon">▼</span>
              </summary>
              <div className="content">
                <p>Website ini berfungsi sebagai alat bantu digital bagi petani atau pelaku industri teh untuk memprediksi tingkat kematangan daun teh berdasarkan citra digital (gambar).</p>
              </div>
            </details>

            {/* Tambahan FAQ lain (singkat) */}
            <details className="faq-item">
              <summary>
                <span className="faq-question">Bagaimana cara kerja sistem ini?</span>
                <span className="icon">▼</span>
              </summary>
              <div className="content">
                <p>Sistem akan menganalisis gambar daun teh menggunakan algoritma KNN.</p>
              </div>
            </details>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-top">
          <div className="footer-logo">
            <img src="/assets/logo.png" alt="LeafScan Logo" />
            <div className="social-icons">
              <a href="#"><i className="fab fa-tiktok"></i></a>
              <a href="#"><i className="fab fa-instagram"></i></a>
              <a href="#"><i className="fab fa-youtube"></i></a>
              <a href="#"><i className="fab fa-facebook"></i></a>
            </div>
          </div>
          <div className="footer-nav">
            <Link to="/">Beranda</Link>
            <Link to="/prediksi">Prediksi</Link>
            <Link to="/riwayat">Riwayat</Link>
          </div>
          <div className="footer-logout">
            <a href="#" className="logout-btn">
              <i className="fas fa-sign-out-alt"></i> Back
            </a>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2025 KURNIA ADILLA</p>
        </div>
      </footer>
    </div>
  );
}

export default Beranda;
