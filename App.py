import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# --- Medicine database (simple dictionary for demo) ---
medicines = {
    "1": {"name": "Paracetamol", "use": "Fever reducer", "dose": "500mg"},
    "2": {"name": "Amoxicillin", "use": "Antibiotic", "dose": "250mg"},
    "3": {"name": "Ibuprofen", "use": "Pain reliever", "dose": "400mg"},
}

st.set_page_config(page_title="Batchmeds QR Scanner", layout="centered")

st.title("📷 QR Code Scanner - Batchmeds")

st.sidebar.title("Options")
mode = st.sidebar.radio("Choose mode:", ["Home", "Scan QR"])

if mode == "Home":
    st.info("👈 Select *Scan QR* from the sidebar to scan a QR code.")

elif mode == "Scan QR":
    st.subheader("Show your QR code to the camera")

    # Start webcam
    camera = cv2.VideoCapture(0)

    stframe = st.empty()

    qr_data = None

    while True:
        ret, frame = camera.read()
        if not ret:
            st.error("Camera not working 😢")
            break

        # Decode QR codes
        for qr in decode(frame):
            qr_data = qr.data.decode("utf-8")
            pts = np.array([qr.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
            cv2.putText(frame, qr_data, (qr.rect.left, qr.rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        stframe.image(frame, channels="BGR")

        if qr_data:
            st.success(f"✅ QR Code Detected: {qr_data}")

            # Check if QR matches medicine database
            if qr_data in medicines:
                med = medicines[qr_data]
                st.write(f"*Medicine:* {med['name']}")
                st.write(f"*Use:* {med['use']}")
                st.write(f"*Dose:* {med['dose']}")
            else:
                st.warning("This QR code is not in the database. Maybe it’s a link?")
                st.write(f"[Open Link]({qr_data})")

            break

    camera.release()