import streamlit as st
import pandas as pd
import os
import requests
from PIL import Image

# LINE Notify Token (Replace with your actual token)
LINE_NOTIFY_TOKEN = "cFNP09HM6p72xrzSbqeiTrXHN81WYfbL1d8Spjp3Izi"

# Streamlit App Title
st.title("✨ Sugar Shade")
st.subheader("เค้กปอนด์")

# Customer Details
customer_name = st.text_input("💌ชื่อลูกค้า", placeholder="ใส่ชื่อเดียวกับชื่อ Line")
phone_number = st.text_input("เบอร์โทรศัพท์", max_chars=15, placeholder=" XXX-XXX-XXXX")

# Cake Selection
cake_base = st.selectbox("เนื้อเค้ก:", ["วานิลลา", "ช็อคโกแลต"])
cake_filling = st.selectbox("ไส้:", ["🍓 สตรอเบอร์รี่", "🍫 ช็อคโกแลต", "🫐 บลูเบอร์รี่", "🍯 คาราเมล"])
cake_size = st.selectbox("ขนาด:", ["0.5 ปอนด์", "1 ปอนด์", "1.5 ปอนด์"])

# Cake Color Selection
cake_color_options = ["ชมพู", "ฟ้า", "ขาว", "ดำ", "ม่วง", "สีอื่นๆโปรดระบุ"]
cake_color_choice = st.selectbox("สีเค้ก:", cake_color_options)

if cake_color_choice == "สีอื่นๆโปรดระบุ":
    custom_cake_color = st.text_input("สีอื่นๆ")
    cake_color = custom_cake_color if custom_cake_color else "Not Specified"
else:
    cake_color = cake_color_choice

cake_text = st.text_input("ข้อความที่ต้องการเขียนบนเค้ก/ฐาน", placeholder="เช่น Happy birthday!")
cake_specification = st.text_input("บรีฟอื่นๆ (หากมี)", placeholder="เช่น ขอเปลี่ยนจากโบว์สีแดงเป็นสีดำ")

# Upload Cake Reference Image
uploaded_file = st.file_uploader("📷 อัพโหลดภาพตัวอย่างเค้ก (ถ้ามี)", type=["jpg", "png", "jpeg"])

# Save uploaded file
image_path = None
if uploaded_file is not None:
    image_path = os.path.join("uploaded_images", uploaded_file.name)
    os.makedirs("uploaded_images", exist_ok=True)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.image(image_path, caption="ตัวอย่างเค้ก", use_column_width=True)

# Selecting candle
candle_type = st.radio("เทียน (แท่งละ 10 บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "ไม่รับเทียน"])

if candle_type != "ไม่รับเทียน":
    num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1)
else:
    num_candles = 0

# Delivery details
delivery_date = st.date_input("วันรับเค้ก")
delivery_time = st.time_input("เวลารับเค้ก")
delivery_option = st.radio("วิธีส่ง:", ["มารับเอง", "รถมอเตอร์ไซต์", "รถยนต์"])
delivery_location = st.text_input("สถานที่ส่ง (หากมารับเองไม่ต้องใส่)", placeholder="สามารถใส่เป็น Google Link หรือชื่อสถานที่ได้")

# File to store orders
ORDER_FILE = "sugarshade_orders.csv"

# Order Placement
if st.button("ยืนยันออเดอร์"):
    if not customer_name or not phone_number:
        st.error("⚠️ โปรดระบุข้อมูลให้ครบ (ชื่อลูกค้า และ เบอร์โทรศัพท์)")
    else:
        order_data = {
            "Customer Name": [customer_name],
            "Phone Number": [phone_number],
            "Cake Base": [cake_base],
            "Cake Filling": [cake_filling],
            "Cake Size": [cake_size],
            "Cake Color": [cake_color],
            "Cake Text": [cake_text],
            "Cake Specification": [cake_specification],
            "Candle Type": [candle_type],
            "Candle Count": [num_candles],
            "Delivery Date": [delivery_date],
            "Delivery Time": [delivery_time],
            "Deliver Option": [delivery_option],
            "Delivery Location": [delivery_location],
            "Cake Image": [image_path if image_path else "No Image"]
        }

        df = pd.DataFrame(order_data)

        try:
            if os.path.exists(ORDER_FILE):
                df.to_csv(ORDER_FILE, mode="a", index=False, header=False)
            else:
                df.to_csv(ORDER_FILE, mode="w", index=False, header=True)

            st.success("✅ ได้รับข้อมูลของคุณแล้ว")

            # Generate Order Summary for LINE
            order_summary = f"""
💌 K.{customer_name}
📞 เบอร์โทร: {phone_number}

🎂 รายละเอียดเค้ก
- เนื้อเค้ก: {cake_base}
- ไส้: {cake_filling}
- ขนาด: {cake_size}
- สีเค้ก: {cake_color}
- ข้อความ: {cake_text}
- บรีฟอื่นๆ: {cake_specification}

🕯️ เทียน
- ประเภท: {candle_type} ({num_candles} แท่ง)

🚗 ข้อมูลการจัดส่ง
- วันรับเค้ก: {delivery_date}
- เวลา: {delivery_time}
- วิธีจัดส่ง: {delivery_option}
- สถานที่รับ: {delivery_location}
            """

            # Send order notification to LINE with image
            requests.post(
                "https://notify-api.line.me/api/notify",
                headers={"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"},
                data={"message": order_summary},
                files={"imageFile": open(image_path, "rb")} if image_path else None
            )

            # Show Order Summary Immediately
            st.subheader("📋 สรุปออเดอร์")
            st.write(order_summary)

            if image_path:
                st.image(image_path, caption="ตัวอย่างเค้ก", use_column_width=True)

        except Exception as e:
            st.error(f"⚠️ Error saving order: {e}")

# Admin Section (Hidden from customers)
st.divider()
st.subheader("🔒 Admin Access")
st.text("เฉพาะแอดมินเท่านั้น")

admin_password = st.text_input("Enter Admin Password", type="password")

if admin_password == "PurseAdmin":
    if st.button("View Orders"):
        try:
            orders_df = pd.read_csv(ORDER_FILE)
            st.write(orders_df)
        except FileNotFoundError:
            st.error("No orders found yet.")
else:
    st.warning("🔐 Enter the admin password to view orders.")
