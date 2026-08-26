import streamlit as st

st.set_page_config(page_title="แอปคำนวณ BMI", page_icon="⚖️")

st.title("⚖️ แอปพลิเคชันคำนวณค่าดัชนีมวลกาย (BMI)")
st.write("กรุณากรอกน้ำหนักและส่วนสูงของคุณเพื่อคำนวณ")

weight = st.number_input("กรอกน้ำหนัก (กิโลกรัม)", min_value=0.0, value=50.0, step=0.1)
height = st.number_input("กรอกส่วนสูง (เซนติเมตร)", min_value=0.0, value=160.0, step=0.1)

if st.button("คำนวณค่า BMI"):
    if weight > 0 and height > 0:
        height_m = height / 100.0
        bmi = weight / (height_m ** 2)
        st.info(f"ค่า BMI ของคุณคือ: {bmi:.2f}")
        if bmi < 18.5:
            st.write("แปลผล: **ผอม**")
        elif 18.5 <= bmi < 23.0:
            st.write("แปลผล: **สุขภาพดี**")
        elif 23.0 <= bmi < 25.0:
            st.write("แปลผล: **ท้วม**")
        else:
            st.write("แปลผล: **อ้วน**")
    else:
        st.error("กรุณากรอกน้ำหนักและส่วนสูงให้มากกว่า 0")

st.divider()
st.write("📌 **ข้อมูลผู้จัดทำ**")
st.write("ชื่อ-นามสกุล: ธุวานันท์ จิรัฏฐ์ธนากุล")
st.write("เลขที่: 41")
