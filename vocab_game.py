import streamlit as st

# ตั้งชื่อหน้าเว็บแอปพลิเคชัน
st.title("🎮 เกมเติมคำศัพท์ภาษาอังกฤษ (Vocabulary Game)")

# ---------------------------------------------------------
# จุดที่ 1: กำหนดค่าเริ่มต้นใน session_state (ans1_val - ans4_val)
# ---------------------------------------------------------
if "ans1_val" not in st.session_state:
    st.session_state.ans1_val = ""
if "ans2_val" not in st.session_state:
    st.session_state.ans2_val = ""
if "ans3_val" not in st.session_state:
    st.session_state.ans3_val = ""
if "ans4_val" not in st.session_state:
    st.session_state.ans4_val = ""

# กำหนดเฉลยคำตอบที่ถูกต้อง (สามารถเปลี่ยนคำศัพท์ตามต้องการได้)
CORRECT_ANS1 = "apple"
CORRECT_ANS2 = "banana"
CORRECT_ANS3 = "orange"
CORRECT_ANS4 = "pencil"

# ---------------------------------------------------------
# จุดที่ 6: เพิ่มช่องรับคำตอบ ans1 - ans4
# ---------------------------------------------------------
st.subheader("📝 จงเติมคำศัพท์ภาษาอังกฤษให้ถูกต้อง")

ans1 = st.text_input("ข้อที่ 1: 🍎 A _ _ l e (ผลไม้สีแดง)", value=st.session_state.ans1_val)
ans2 = st.text_input("ข้อที่ 2: 🍌 B _ n _ n _ (ผลไม้สีเหลือง)", value=st.session_state.ans2_val)
ans3 = st.text_input("ข้อที่ 3: 🍊 O _ a _ g e (ผลไม้สีส้ม)", value=st.session_state.ans3_val)
ans4 = st.text_input("ข้อที่ 4: ✏️ P _ n _ i l (ดินสอ)", value=st.session_state.ans4_val)

# ---------------------------------------------------------
# จุดที่ 7: อัปเดตค่าล่าสุดเข้าตัวแปร session_state
# ---------------------------------------------------------
st.session_state.ans1_val = ans1
st.session_state.ans2_val = ans2
st.session_state.ans3_val = ans3
st.session_state.ans4_val = ans4

col1, col2 = st.columns(2)

with col1:
    # ปุ่มตรวจคำตอบ
    if st.button("ส่งคำตอบ"):
        # ---------------------------------------------------------
        # จุดที่ 3: จัดการตัดช่องว่างและแปลงเป็นตัวพิมพ์เล็ก (strip & lower)
        # ---------------------------------------------------------
        u_ans1 = ans1.strip().lower()
        u_ans2 = ans2.strip().lower()
        u_ans3 = ans3.strip().lower()
        u_ans4 = ans4.strip().lower()

        # ---------------------------------------------------------
        # จุดที่ 4: ตรวจสอบคำตอบและคำนวณคะแนน
        # ---------------------------------------------------------
        score = 0
        if u_ans1 == CORRECT_ANS1:
            score += 1
        if u_ans2 == CORRECT_ANS2:
            score += 1
        if u_ans3 == CORRECT_ANS3:
            score += 1
        if u_ans4 == CORRECT_ANS4:
            score += 1

        # ---------------------------------------------------------
        # จุดที่ 5 & 8: เพิ่มคะแนน (score == 4) และแสดง Dialog/ผลลัพธ์
        # ---------------------------------------------------------
        st.subheader(f"📊 สรุปผลคะแนน: {score} / 4 คะแนน")
        
        if score == 4:
            st.success("🎉 เก่งมาก! คุณตอบถูกต้องทั้งหมด 4 ข้อ")
        else:
            st.warning(f"คุณตอบถูก {score} ข้อ พยายามใหม่อีกครั้งนะ!")

with col2:
    # ---------------------------------------------------------
    # จุดที่ 2: เคลียร์ค่าเมื่อกดปุ่มเริ่มใหม่
    # ---------------------------------------------------------
    if st.button("เริ่มเกมใหม่"):
        st.session_state.ans1_val = ""
        st.session_state.ans2_val = ""
        st.session_state.ans3_val = ""
        st.session_state.ans4_val = ""
        st.rerun()
