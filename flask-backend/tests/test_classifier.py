import os
import sys
import cv2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.tea_leaf_classifier import TeaLeafClassifier

def test_single_image(classifier, image_path):
    """Test model dengan satu gambar"""
    print(f"\nMenguji gambar: {image_path}")
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Tidak dapat membaca gambar dari {image_path}")
        return
        
    # Lakukan prediksi
    result = classifier.predict(img)
    print(f"Hasil Prediksi:")
    print(f"Kelas: {result['class']}")
    print(f"Confidence: {result['confidence']:.2f}")
    
    # Tampilkan gambar
    cv2.imshow('Test Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_model():
    # Inisialisasi classifier
    classifier = TeaLeafClassifier()
    
    try:
        # Load model yang sudah dilatih
        classifier.load_model()
        print("Model berhasil dimuat!")
        
        # Test dengan beberapa gambar dari dataset
        dataset_path = "dataset"
        categories = ['siap_petik', 'belum_siap_petik']
        
        for category in categories:
            category_path = os.path.join(dataset_path, category)
            if not os.path.exists(category_path):
                print(f"Folder {category_path} tidak ditemukan")
                continue
                
            print(f"\nMenguji gambar dari kategori: {category}")
            # Ambil 3 gambar pertama dari setiap kategori
            images = os.listdir(category_path)[:3]
            
            for img_name in images:
                img_path = os.path.join(category_path, img_name)
                test_single_image(classifier, img_path)
                
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("\nLangkah-langkah yang perlu dilakukan:")
        print("1. Pastikan folder 'dataset' sudah dibuat")
        print("2. Pastikan ada subfolder 'siap_petik' dan 'belum_siap_petik'")
        print("3. Masukkan gambar test ke folder yang sesuai")
        print("4. Jalankan train_model.py untuk melatih model terlebih dahulu")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_model() 