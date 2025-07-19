// src/components/CameraCapture.jsx
import React, { useRef, useState } from 'react';

const CameraCapture = ({ onCapture, onClose }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [captured, setCaptured] = useState(null);

  // Aktifkan kamera
  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    videoRef.current.play();
  };

  // Tangkap gambar
  const takePicture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    canvas.width = 100; // ukuran sesuai model
    canvas.height = 100;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/jpeg');
    setCaptured(imageData);
    if (onCapture) onCapture(imageData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Ambil Foto</h3>
          <button 
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>
        <div className="flex flex-col items-center">
          {!captured && (
            <>
              <video ref={videoRef} className="w-[200px] h-[150px] rounded" />
              <button onClick={startCamera} className="mt-2 bg-sky-500 text-white px-4 py-2 rounded">
                Aktifkan Kamera
              </button>
              <button onClick={takePicture} className="mt-2 bg-green-500 text-white px-4 py-2 rounded">
                Ambil Gambar
              </button>
            </>
          )}
          {captured && (
            <img src={captured} alt="Preview" className="mt-4 w-[100px] h-[100px] rounded border" />
          )}
          <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>
      </div>
    </div>
  );
};

export default CameraCapture;
