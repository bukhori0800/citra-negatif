import cv2
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Shotoshop Mini", page_icon="🎨", layout="centered")

st.title("🎨 Shotoshop Mini - Python Version")
st.write("Aplikasi mini untuk manipulasi citra digital: Negatif, Grayscale, Brighten, Rotate, Flip, Zoom, dan Blending dua gambar.")

# Upload gambar pertama
uploaded_file = st.file_uploader("📂 Upload gambar utama (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Baca dan tampilkan gambar pertama
    img1 = Image.open(uploaded_file)
    img1 = np.array(img1)
    st.image(img1, caption="Gambar Asli", use_container_width=True)

    # Pilihan operasi
    st.subheader("🧮 Pilih Operasi Citra")
    operation = st.selectbox(
        "Pilih salah satu:",
        [
            "Negatif",
            "Grayscale",
            "Brighten",
            "Rotate 45°",
            "Flip Horizontal",
            "Zoom 1.5x",
            "Blend Dua Gambar (Gabung)"
        ]
    )

    # Proses gambar sesuai pilihan
    if operation == "Negatif":
        result = 255 - img1

    elif operation == "Grayscale":
        result = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

    elif operation == "Brighten":
        brightness = st.slider("Tingkat kecerahan", min_value=10, max_value=150, value=50)
        result = cv2.convertScaleAbs(img1, alpha=1, beta=brightness)

    elif operation == "Rotate 45°":
        h, w = img1.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), 45, 1)
        result = cv2.warpAffine(img1, M, (w, h))

    elif operation == "Flip Horizontal":
        result = cv2.flip(img1, 1)

    elif operation == "Zoom 1.5x":
        h, w = img1.shape[:2]
        result = cv2.resize(img1, (int(w * 1.5), int(h * 1.5)))

    elif operation == "Blend Dua Gambar (Gabung)":
        st.subheader("➕ Upload Gambar Kedua")
        uploaded_file2 = st.file_uploader("📂 Pilih gambar kedua", type=["jpg", "jpeg", "png"])
        if uploaded_file2:
            img2 = Image.open(uploaded_file2)
            img2 = np.array(img2)

            # Ubah ukuran gambar kedua agar sama dengan gambar pertama
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

            # Opsi efek negatif dan transparansi
            make_negative = st.checkbox("Buat gambar kedua jadi negatif")
            alpha = st.slider("Tingkat transparansi penggabungan", 0.0, 1.0, 0.5, 0.05)

            if make_negative:
                img2 = 255 - img2

            # Blend kedua gambar
            result = cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)

            st.image([img1, img2, result],
                     caption=["Gambar 1", "Gambar 2 (setelah efek)", "Hasil Gabungan"],
                     use_container_width=True)
        else:
            st.info("👆 upload fotonya.")
            result = None

    # Tampilkan hasil (selain blending yang sudah ditampilkan di atas)
    if operation != "Blend Dua Gambar (Gabung)" and uploaded_file:
        st.subheader("📸 Hasil Operasi")
        st.image(result, caption=f"Hasil: {operation}", use_container_width=True)

    # Tombol simpan hasil
    if 'result' in locals() and result is not None:
        st.download_button(
            label="💾 Simpan Hasil",
            data=cv2.imencode(".jpg", cv2.cvtColor(result, cv2.COLOR_RGB2BGR))[1].tobytes()
            if len(result.shape) == 3 else cv2.imencode(".jpg", result)[1].tobytes(),
            file_name=f"hasil_{operation.lower().replace(' ', '_')}.jpg",
            mime="image/jpeg"
        )

else:
    st.info("👆 upload fotonya.")
