import streamlit as st
import pandas as pd
import os
import requests

# LINE Notify Token (Replace with your actual token)
LINE_NOTIFY_TOKEN = "gF2wiELf5fMoOnRdTMud8dJ0xpMrh3mo7oPevPifUVB"

def send_line_notification(message):
    """Send order notification to LINE Notify."""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

# Streamlit App Title
st.title("✨ Sugar Shade")
st.subheader("เค้กปอนด์")

# Customer Details
customer_name = st.text_input("💌ชื่อลูกค้า", placeholder="ใส่ชื่อเดียวกับชื่อ Line")
phone_number = st.text_input("เบอร์โทรศัพท์", max_chars=15, placeholder=" XXX-XXX-XXXX")

# Cake Selection
cake_base = st.selectbox("เนื้อเค้ก:", ["วานิลลา", "ช็อคโกแลต"])
cake_filling = st.selectbox("ไส้:", [" 🍓สตรอเบอร์รี่", " 🍫ช็อคโกแลต", " 🫐บลูเบอร์รี่", " 🍯คาราเมล"])
cake_size = st.selectbox("ขนาด:", ["0.5 ปอนด์", "1 ปอนด์", "1.5 ปอนด์"])

# Cake Color Selection
cake_color_options = ["🩷ชมพู", "🩵ฟ้า", "🤍ขาว", "🖤ดำ", "💜ม่วง", "สีอื่นๆโปรดระบุ"]
cake_color_choice = st.selectbox("สีเค้ก:", cake_color_options)

if cake_color_choice == "สีอื่นๆโปรดระบุ":
    custom_cake_color = st.text_input("สีอื่นๆ")
    cake_color = custom_cake_color if custom_cake_color else "Not Specified"
else:
    cake_color = cake_color_choice

cake_text = st.text_input("ข้อความที่ต้องการเขียนบนเค้ก/ฐาน", placeholder="เช่น Happy birthday!")
cake_specification = st.text_input("บรีฟอื่นๆ(หากมี)", placeholder="เช่น ขอเปลี่ยนจากโบว์สีแดงเป็นสีดำ")

# Selecting candle
candle_type = st.radio("เทียน(แท่งละ 10บาท):", ["เทียนเกลียว", "เทียนสั้นสีชมพู", "ไม่รับเทียน"])

if candle_type == "เทียนเกลียว":
    num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1)
elif candle_type == "เทียนสั้นสีชมพู":
    num_candles = st.slider("จำนวน (แท่ง):", min_value=1, max_value=10, value=1)
else:
    num_candles = 0
    st.write("ไม่รับเทียน")

# Delivery details
delivery_date = st.date_input("วันรับเค้ก")
delivery_time = st.time_input("เวลารับเค้ก (หากยังไม่ชัวร์ใส่ 09.00 ก่อนวันรับเค้กจะคอนเฟิร์มเวลาอีกครั้ง)")
delivery_option = st.radio("วิธีส่ง:", ["มารับเอง", "รถมอเตอร์ไซต์","รถยนต์"])

if delivery_option == "รถมอเตอร์ไซต์":
    st.warning(
        "เนื่องจากเค้กมีความละเอียดในการส่ง รบกวนลูกค้าอ่านรายละเอียดก่อนนะคะ\n"
        "\n"
        "การส่งเค้กของทางร้านใช้บริการจาก lalamove / bolt / grab\n"
        "\n"
        "❌ ข้อจำกัดการส่งมอเตอร์ไซต์\n"
        "1. เค้ก 1.5 ปอนด์ขึ้นไปไม่สามารถส่งด้วยมอเตอร์ไซต์ได้\n"
        "2. ไม่แนะนำส่งในระยะทางเกิน 10 กม.\n"
        "3. ไม่แนะนำส่งงาน 3D หรือที่มีความสูง\n"
        "4. ไม่แนะนำส่งงานผลไม้\n" 
        "\n"
        "⛔️ ทางร้านไม่รับผิดชอบเค้กที่เสียหายจากการขนส่งในทุกกรณีนะคะ🙏🏻"
    )
delivery_location = st.text_input("สถานที่ส่ง (หากมารับเองไม่ต้องใส่)", placeholder="สามารถใส่เป็น google link หรือชื่อสถานที่ได้")

# File to store orders
ORDER_FILE = "sugarshade_orders.csv"

# Order Placement
if st.button("ยืนยันออเดอร์"):
    if not customer_name or not phone_number or not delivery_location:
        st.error("⚠️ โปรดระบุข้อมูลให้ครบ (ชื่อลูกค้า, เบอร์โทรศัพท์ , and สถานที่ส่ง).")
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
            "Delivery Date": [delivery_date],
            "Delivery Time": [delivery_time],
            "Deliver Option" : [delivery_option],
            "Delivery Location": [delivery_location],
        }

        df = pd.DataFrame(order_data)

        try:
            if os.path.exists(ORDER_FILE):
                df.to_csv(ORDER_FILE, mode="a", index=False, header=False)
            else:
                df.to_csv(ORDER_FILE, mode="w", index=False, header=True)

            st.success("✅ได้รับข้อมูลของคุณแล้ว")

            # Generate Order Summary
            order_summary = f"""
            **💌K.{customer_name}**
            - **เบอร์โทร:** {phone_number}

            **🎂รายละเอียดเค้ก**
            - **เนื้อเค้ก:** {cake_base}
            - **ไส้:** {cake_filling}
            - **ขนาด:** {cake_size}
            - **สีเค้ก:** {cake_color}
            - **ข้อความ:** {cake_text}
            - **บรีฟอื่นๆ:** {cake_specification}

            **🕯️เทียน**
            - **เทียน:** {candle_type} {num_candles} **แท่ง**

            **🚗ข้อมูลการจัดส่ง**
            - **วันรับเค้ก:** {delivery_date}
            - **เวลา:** {delivery_time}
            - **วิธีจัดส่ง:** {delivery_option}
            - **สถานที่รับ:** {delivery_location}
            """

            # Generate Order Summary for LINE
            order_summaryforLINE = f"""
 💌K.{customer_name}
 เบอร์โทร: {phone_number}

🎂รายละเอียดเค้ก
    -เนื้อเค้ก: {cake_base}
    -ไส้: {cake_filling}
    -ขนาด:{cake_size}
    -สีเค้ก: {cake_color}
    -ข้อความ: {cake_text}
    -บรีฟอื่นๆ: {cake_specification}

🕯️เทียน
    -เทียน: {candle_type} {num_candles} **แท่ง**

🚗ข้อมูลการจัดส่ง**
    -วันรับเค้ก:{delivery_date}
    -เวลา: {delivery_time}
    -วิธีจัดส่ง: {delivery_option}
    -สถานที่รับ: {delivery_location}
            """

            # Send order notification to LINE
            send_line_notification(order_summaryforLINE)

            # Show Order Summary Immediately
            st.subheader("📋 สรุปออเดอร์")
            st.write(order_summary)

        except Exception as e:
            st.error(f"⚠️ Error saving order: {e}")

# Admin Section (Hidden from customers)
st.divider()
st.subheader("🔒 Admin Access")
st.text("เฉพาะแอดมินเท่านั้น")

admin_password = st.text_input("Enter Admin Password", type="password")

if admin_password == "PurseAdmin":  # Change this password!
    if st.button("View Orders"):
        try:
            orders_df = pd.read_csv(ORDER_FILE)
            st.write(orders_df)
        except FileNotFoundError:
            st.error("No orders found yet.")
else:
    st.warning("🔐 Enter the admin password to view orders.")