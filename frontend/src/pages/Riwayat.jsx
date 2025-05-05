// src/pages/Riwayat.jsx
import React from 'react';

const dummyData = [
  {
    id: 1,
    imageUrl: '/assets/daun1.jpg',
    date: '2025-04-08',
    result: 'Daun Siap Petik',
  },
  {
    id: 2,
    imageUrl: '/assets/daun2.jpg',
    date: '2025-04-07',
    result: 'Belum Siap Petik',
  },
];

function Riwayat() {
  return (
    <div className="min-h-screen bg-white px-8 py-16 font-sans">
      <h1 className="text-3xl font-bold text-green-600 mb-4">Riwayat Prediksi</h1>
      <p className="text-gray-600 mb-8">Berikut adalah daftar hasil prediksi daun teh yang telah Anda lakukan.</p>

      <div className="grid gap-6">
        {dummyData.map((item) => (
          <div
            key={item.id}
            className="flex flex-col md:flex-row items-center justify-between bg-white border rounded-md shadow-sm p-6"
          >
            <div className="flex items-center gap-6">
              <img src={item.imageUrl} alt="preview" className="w-24 h-24 object-cover rounded-md" />
              <div>
                <p className="font-semibold text-gray-700">{item.result}</p>
                <p className="text-sm text-gray-500">Tanggal: {item.date}</p>
              </div>
            </div>
            <div className="mt-4 md:mt-0">
              <button className="text-sm bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 mr-2">
                Lihat Detail
              </button>
              <button className="text-sm bg-cyan-600 text-white px-4 py-2 rounded-md hover:bg-cyan-700">
                Download
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Riwayat;
