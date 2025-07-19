import React, { useState } from "react";
import CameraCapture from "../components/cameracapture";
import { Link } from "react-router-dom";
import Footer from "../components/Footer";

const Prediksi = () => {
  const [imageData, setImageData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [showCamera, setShowCamera] = useState(false);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageData(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCaptureImage = (capturedImage) => {
    setPreviewUrl(capturedImage);
    // Konversi base64 ke File object
    const byteString = atob(capturedImage.split(",")[1]);
    const mimeString = capturedImage.split(",")[0].split(":")[1].split(";")[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    const blob = new Blob([ab], { type: mimeString });
    const file = new File([blob], "captured.jpg", { type: mimeString });
    setImageData(file);
    setShowCamera(false);
  };

  const handlePredict = async () => {
    if (!imageData) {
      setPrediction("Silakan pilih gambar terlebih dahulu.");
      return;
    }
    const formData = new FormData();
    formData.append("image", imageData, "image.jpg");
    setPrediction("Memproses...");
    try {
      const response = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        setPrediction(
          "Gagal menghubungi server. Silakan coba lagi.",
          response.text()
        );
        return;
      }

      const data = await response.json();

      if (data.class === "non_tea") {
        setPrediction("Gambar ini bukan daun teh, silakan ganti gambar.");
      } else if (data.class === "siap_petik") {
        setPrediction("Siap Petik");
      } else if (data.class === "belum_siap_petik") {
        setPrediction("Belum Siap Petik");
      } else {
        setPrediction("Hasil tidak dikenali");
      }
    } catch (err) {
      setPrediction(
        "Terjadi kesalahan saat memproses gambar. Silakan coba lagi."
      );
      setPrediction(null); // Tidak tampilkan pesan error
    }
  };

  return (
    <div className="min-h-screen bg-white font-poppins flex flex-col">
      <div className="flex-1 w-full relative px-4 sm:px-6 md:px-10 py-16 sm:py-8 overflow-hidden">
        {/* Background Petani untuk Mobile */}
        <div
          className="absolute inset-0 md:hidden bg-[url('/assets/petani.png')] bg-no-repeat bg-cover bg-bottom opacity-10 z-0"
          aria-hidden="true"
        ></div>

        <div className="relative z-10 flex flex-col md:flex-row items-center gap-12">
          {/* Kiri: Form Prediksi */}
          <div className="flex-1 w-full max-w-2xl">
            <div className="md:ml-10">
              <h1 className="text-3xl sm:text-4xl md:text-6xl font-extrabold mb-2 leading-tight text-center md:text-left">
                <span className="text-gradient block">Mulai Lakukan</span>
                <span className="text-gradient block">Prediksi</span>
              </h1>
              <p className="italic text-gray-600 text-base sm:text-lg mb-6 mt-2 text-center md:text-left">
                "Membantu Pemetikan Daun Teh secara Efisien"
              </p>

              {/* Form Upload */}
              <div className="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 flex flex-col lg:flex-row gap-6 items-center mb-4 min-w-max">
                {/* Preview */}
                <div className="w-28 h-28 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300 shrink-0">
                  {previewUrl ? (
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="max-w-full max-h-full rounded-md object-cover"
                    />
                  ) : (
                    <img
                      src="/assets/upicon.png"
                      alt="Upload"
                      className="w-16 h-16 opacity-70"
                    />
                  )}
                </div>

                {/* Upload Options */}
                <div className="flex-1 flex flex-col justify-center min-w-max">
                  <p className="text-gray-500 mb-4 text-sm sm:text-base font-semibold text-center md:text-left">
                    Harap unggah gambar persegi, ukuran kurang dari 100KB
                  </p>
                  <div className="flex flex-col sm:flex-row gap-3 mb-4 w-full">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                      style={{ display: "none" }}
                      id="image-upload"
                    />
                    <label
                      htmlFor="image-upload"
                      className="flex-1 flex items-center gap-2 px-4 py-3 bg-gray-200 rounded-lg cursor-pointer transition text-sm sm:text-base font-extrabold text-gray-700 justify-center shadow-none hover:bg-gray-300"
                    >
                      <img
                        src="/assets/upgambar.png"
                        alt="icon"
                        className="w-5 h-5"
                      />
                      Pilih Gambar
                    </label>
                    <button
                      type="button"
                      onClick={() => setShowCamera(true)}
                      className="flex-1 flex items-center gap-2 px-4 py-3 bg-gray-200 rounded-lg cursor-pointer transition text-sm sm:text-base font-extrabold text-gray-700 justify-center shadow-none hover:bg-gray-300"
                    >
                      <img
                        src="/assets/usecamera.png"
                        alt="icon"
                        className="w-5 h-5"
                      />
                      Gunakan Kamera
                    </button>
                  </div>

                  <button
                    type="button"
                    onClick={handlePredict}
                    className="w-full px-6 py-3 rounded-lg font-extrabold text-base text-white"
                    style={{
                      background:
                        "linear-gradient(90deg, #61BC43 0%, #10ACC6 100%)",
                      boxShadow: "0 4px 16px 0 rgba(16,185,129,0.15)",
                    }}
                  >
                    Mulai Prediksi
                  </button>
                </div>
              </div>

              {/* Kamera Popup */}
              {showCamera && (
                <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
                  <div className="bg-white rounded-lg p-6 shadow-lg max-w-md w-full">
                    <CameraCapture
                      onCapture={handleCaptureImage}
                      onClose={() => setShowCamera(false)}
                    />
                  </div>
                </div>
              )}

              {/* Hasil Prediksi */}
              {prediction && (
                <div className="mt-6 p-4 bg-green-100 border border-green-300 rounded-lg text-green-800 font-semibold text-center shadow">
                  Hasil: {prediction}
                </div>
              )}
            </div>
          </div>

          {/* Kanan: Gambar Petani (hanya desktop) */}
          <div className="hidden md:flex flex-1 justify-center md:justify-end">
            <img
              src="/assets/petani.png"
              alt="Petani"
              className="h-auto max-w-xs sm:max-w-md md:max-w-lg w-full"
            />
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Prediksi;
