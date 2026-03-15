import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

st.title("QR Code Generator")

# User input
data = st.text_input("Enter text or link")

if st.button("Generate QR"):
    if data:
        qr = qrcode.make(data)

        # Convert image to bytes
        buf = BytesIO()
        qr.save(buf)
        buf.seek(0)

        st.image(buf, caption="Your QR Code", width=250)
        st.success("QR Code Generated Successfully!")
    else:
        st.warning("Please enter something")
        
