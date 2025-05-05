// src/pages/Prediksi.jsx
import React, { useState } from 'react';

function Prediksi() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(URL.createObjectURL(e.target.files[0]));
  };

  return (
    <div className="min-h-screen font-sans bg-white">
      {/* Section atas */}
      <div className="flex flex-col lg:flex-row items-center justify-between px-10 py-16">
        <div className="max-w-xl">
          <h1 className="text-4xl font-bold text-green-600">Mulai Lakukan</h1>
          <h1 className="text-4xl font-bold text-cyan-600 mb-4">Prediksi</h1>
          <p className="text-gray-600 mb-6">“Membantu Pemetikan Daun Teh secara Efisien”</p>

          {/* Upload Box */}
          <div className="bg-white shadow-md p-6 rounded-md">
            <p className="text-sm text-gray-500 mb-2">
              Harap unggah gambar persegi, ukuran kurang dari 100KB
            </p>
            <div className="flex items-center gap-4 mb-4">
              <label className="flex items-center gap-2 cursor-pointer border px-4 py-2 rounded-md bg-gray-100 text-cyan-600">
                <input type="file" accept="image/*" onChange={handleFileChange} hidden />
                Pilih Gambar
              </label>
              <span className="text-sm text-gray-500">
                {selectedFile ? '1 file dipilih' : 'No File Chosen'}
              </span>
            </div>
            <button className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600">
              Mulai Prediksi
            </button>
          </div>
        </div>

        {/* Gambar orang */}
        <div className="mt-10 lg:mt-0">
          <img src="/assets/farmer.png" alt="Petani" className="max-w-md" />
        </div>
      </div>

      {/* Section bawah */}
      <div className="bg-green-200 py-12">
        <div className="max-w-3xl mx-auto bg-white p-6 rounded-md shadow-md">
          <h2 className="text-gray-600 text-sm mb-4">Preview Gambar</h2>
          <div className="flex items-center gap-6">
            {selectedFile ? (
              <img src={selectedFile} alt="Preview" className="w-24 h-24 object-cover rounded-md" />
            ) : (
              <div className="w-24 h-24 bg-gray-200 rounded-md" />
            )}
            <div>
              <label className="cursor-pointer border px-4 py-2 rounded-md bg-white text-cyan-600 border-cyan-600 mr-4">
                <input type="file" accept="image/*" onChange={handleFileChange} hidden />
                Ganti Gambar
              </label>
              <button className="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600">
                Mulai Proses Prediksi
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Prediksi;
