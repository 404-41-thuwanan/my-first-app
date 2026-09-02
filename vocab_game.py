import streamlit as st

# ตั้งชื่อหน้าเว็บแอปพลิเคชัน
st.title("🎮 เกมเติมคำศัพท์ภาษาอังกฤษ (Vocabulary Game)")

# ---------------------------------------------------------
# 1. กำหนดค่าเริ่มต้นใน session_state (ans1_val และ ans2_val)
# ---------------------------------------------------------
if "ans1_val" not in st.session_state:
    st.session_state.ans1_val = ""
if "ans2_val" not in st.session_state:
    st.session_state.ans2_val = ""

# เฉลยคำตอบที่ถูกต้อง (2 คำศัพท์เดิม)
CORRECT_ANS1 = "apple"
CORRECT_ANS2 = "fish"

# ---------------------------------------------------------
# 2. ช่องรับคำตอบ (ans1 และ ans2)
# ---------------------------------------------------------
st.subheader("📝 จงเติมคำศัพท์ภาษาอังกฤษให้ถูกต้อง")

ans1 = st.text_input("ข้อที่ 1: 🍎 A _ _ l e (ผลไม้สีแดง)", value=st.session_state.ans1_val)
ans2 = st.text_input("ข้อที่ 2: 🐟 F _ s h (ปลา)", value=st.session_state.ans2_val)

# ---------------------------------------------------------
# 3. อัปเดตค่าล่าสุดเข้าตัวแปร session_state
# ---------------------------------------------------------
st.session_state.ans1_val = ans1
st.session_state.ans2_val = ans2

col1, col2 = st.columns(2)

with col1:
    # ปุ่มตรวจคำตอบ
    if st.button("ส่งคำตอบ"):
        # ตัดช่องว่างและแปลงข้อความให้เป็นตัวพิมพ์เล็ก (strip & lower)
        u_ans1 = ans1.strip().lower()
        u_ans2 = ans2.strip().lower()

        # ตรวจสอบคำตอบและคำนวณคะแนน
        score = 0
        if u_ans1 == CORRECT_ANS1:
            score += 1
        if u_ans2 == CORRECT_ANS2:
            score += 1

        # แสดงผลคะแนนและข้อความแจ้งเตือน
        st.subheader(f"📊 สรุปผลคะแนน: {score} / 2 คะแนน")
        
        if score == 2:
            st.success("🎉 เก่งมาก! คุณตอบถูกต้องทั้งหมด 2 ข้อ")
        else:
            st.warning(f"คุณตอบถูก {score} ข้อ พยายามใหม่อีกครั้งนะ!")

with col2:
    # ปุ่มเริ่มใหม่ (เคลียร์ค่าคำตอบเดิม)
    if st.button("เริ่มเกมใหม่"):
        st.session_state.ans1_val = ""
        st.session_state.ans2_val = ""
        st.rerun()
