import streamlit as st
import time

# ตั้งชื่อหน้าเว็บแอปพลิเคชัน
st.title("🎮 เกมเติมคำศัพท์ภาษาอังกฤษ (Vocabulary Game)")

# ---------------------------------------------------------
# 1. กำหนดค่าเริ่มต้นใน session_state (รวมตัวจับเวลา 30 วินาที)
# ---------------------------------------------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "ans1_val" not in st.session_state:
    st.session_state.ans1_val = ""
if "ans2_val" not in st.session_state:
    st.session_state.ans2_val = ""

# คำนวณเวลาที่เหลือ (30 วินาที)
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(0, 30 - int(elapsed_time))
is_time_up = remaining_time <= 0

# แสดงผลตัวจับเวลา
if not is_time_up:
    st.metric(label="⏳ เวลาที่เหลือ", value=f"{remaining_time} วินาที")
else:
    st.error("⏰ หมดเวลา 30 วินาทีแล้ว! กดปุ่ม 'เริ่มเกมใหม่' เพื่อเล่นอีกครั้ง")

# เฉลยคำตอบที่ถูกต้อง
CORRECT_ANS1 = "apple"
CORRECT_ANS2 = "fish"

# ---------------------------------------------------------
# 2. ช่องรับคำตอบ (ล็อคช่องกรอกเมื่อหมดเวลา)
# ---------------------------------------------------------
st.subheader("📝 จงเติมคำศัพท์ภาษาอังกฤษให้ถูกต้อง")

ans1 = st.text_input("ข้อที่ 1: 🍎 A _ _ l e (ผลไม้สีแดง)", value=st.session_state.ans1_val, disabled=is_time_up)
ans2 = st.text_input("ข้อที่ 2: 🐟 F _ s h (ปลา)", value=st.session_state.ans2_val, disabled=is_time_up)

# อัปเดตค่าล่าสุดเข้า session_state
st.session_state.ans1_val = ans1
st.session_state.ans2_val = ans2

col1, col2 = st.columns(2)

with col1:
    # ปุ่มส่งคำตอบ (กดไม่ได้ถ้าหมดเวลา)
    if st.button("ส่งคำตอบ", disabled=is_time_up):
        u_ans1 = ans1.strip().lower()
        u_ans2 = ans2.strip().lower()

        # ตรวจสอบคำตอบ
        score = 0
        if u_ans1 == CORRECT_ANS1:
            score += 1
        if u_ans2 == CORRECT_ANS2:
            score += 1

        # แสดงผลคะแนน
        st.subheader(f"📊 สรุปผลคะแนน: {score} / 2 คะแนน")
        
        if score == 2:
            st.success("🎉 เก่งมาก! คุณตอบถูกต้องทั้งหมด 2 ข้อ")
        else:
            st.warning(f"คุณตอบถูก {score} ข้อ พยายามใหม่อีกครั้งนะ!")

with col2:
    # ปุ่มเริ่มเกมใหม่ (รีเซ็ตทั้งคำตอบและตัวจับเวลา 30 วินาที)
    if st.button("เริ่มเกมใหม่"):
        st.session_state.ans1_val = ""
        st.session_state.ans2_val = ""
        st.session_state.start_time = time.time()
        st.rerun()
