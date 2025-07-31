// src/components/CameraCapture.jsx
import React, { useRef } from 'react';

const CameraCapture = ({ onCapture, onClose }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  React.useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      });
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const handleCapture = () => {
    const context = canvasRef.current.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, 320, 240);
    const image = canvasRef.current.toDataURL('image/jpeg');
    onCapture(image);
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
          <video ref={videoRef} width={320} height={240} autoPlay className="rounded" />
          <canvas ref={canvasRef} width={320} height={240} style={{ display: 'none' }} />
          <div className="flex gap-2 mt-4">
            <button
              onClick={handleCapture}
              className="px-4 py-2 bg-green-600 text-white rounded"
            >
              Ambil Gambar
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-400 text-white rounded"
            >
              Tutup
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CameraCapture;
