import streamlit as st
import qrcode
from io import BytesIO

st.title("QR Code Generator")

# User input
data = st.text_input("Enter text or link")

if st.button("Generate QR"):
    if data:
        qr = qrcode.make(data)

        buf = BytesIO()
        qr.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption="Your QR Code", width=250)
        st.success("QR Code Generated Successfully!")

        st.download_button(
            label="Download QR",
            data=buf.getvalue(),
            file_name="qr.png",
            mime="image/png"
        )

    else:
        st.warning("Please enter something")