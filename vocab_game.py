import streamlit as st
import time

# ตั้งชื่อหน้าเว็บแอปพลิเคชัน
st.title("🎮 เกมเติมคำศัพท์ภาษาอังกฤษ (Vocabulary Game)")

# ---------------------------------------------------------
# 1. กำหนดค่าเริ่มต้นใน session_state (เพิ่ม ans3_val และ ans4_val)
# ---------------------------------------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "ans1_val" not in st.session_state:
    st.session_state.ans1_val = ""
if "ans2_val" not in st.session_state:
    st.session_state.ans2_val = ""
if "ans3_val" not in st.session_state:
    st.session_state.ans3_val = ""
if "ans4_val" not in st.session_state:
    st.session_state.ans4_val = ""

# เฉลยคำตอบที่ถูกต้อง (4 คำศัพท์: คำเดิม 2 คำ + คำใหม่ 2 คำ)
CORRECT_ANS1 = "apple"
CORRECT_ANS2 = "fish"
CORRECT_ANS3 = "banana"
CORRECT_ANS4 = "pencil"

# ---------------------------------------------------------
# ฟังก์ชันสร้างหน้าต่าง Dialog สรุปผลลัพธ์ (Popup สรุปคะแนน 4 ข้อ)
# ---------------------------------------------------------
@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog(score, total, u_ans1, u_ans2, u_ans3, u_ans4):
    st.write(f"### ได้รับคะแนน: {score} / {total} คะแนน")
    st.write("---")
    st.write(f"• **ข้อที่ 1 (apple):** คำตอบของคุณคือ `{u_ans1 if u_ans1 else '-'}`")
    st.write(f"• **ข้อที่ 2 (fish):** คำตอบของคุณคือ `{u_ans2 if u_ans2 else '-'}`")
    st.write(f"• **ข้อที่ 3 (banana):** คำตอบของคุณคือ `{u_ans3 if u_ans3 else '-'}`")
    st.write(f"• **ข้อที่ 4 (pencil):** คำตอบของคุณคือ `{u_ans4 if u_ans4 else '-'}`")
    st.write("---")
    
    if score == total:
        st.balloons()  # แสดงเอฟเฟกต์ลูกโป่งเมื่อได้คะแนนเต็ม 4 คะแนน
        st.success("🎉 เก่งมาก! คุณตอบถูกต้องทั้งหมด 4 ข้อ!")
    else:
        st.warning("พยายามใหม่อีกครั้งนะ!")

# ---------------------------------------------------------
# 2. ตรวจสอบสถานะการเริ่มเกม
# ---------------------------------------------------------
if not st.session_state.game_started:
    st.info("💡 พร้อมแล้วกดปุ่ม **'🚀 เริ่มเกม'** ด้านล่างเพื่อจับเวลา 30 วินาที")
    
    # ปุ่มเริ่มเกม (กดแล้วค่อยเริ่มจับเวลา)
    if st.button("🚀 เริ่มเกม", type="primary"):
        st.session_state.game_started = True
        st.session_state.start_time = time.time()
        st.session_state.ans1_val = ""
        st.session_state.ans2_val = ""
        st.session_state.ans3_val = ""
        st.session_state.ans4_val = ""
        st.rerun()

else:
    # คำนวณเวลาที่เหลือ (30 วินาที)
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, 30 - int(elapsed_time))
    is_time_up = remaining_time <= 0

    # แสดงผลตัวจับเวลา
    if not is_time_up:
        st.metric(label="⏳ เวลาที่เหลือ", value=f"{remaining_time} วินาที")
    else:
        st.error("⏰ หมดเวลา 30 วินาทีแล้ว! กดปุ่ม 'เริ่มเกมใหม่' เพื่อเล่นอีกครั้ง")

    # ---------------------------------------------------------
    # 3. ช่องรับคำตอบ (รวมเป็น 4 ข้อ)
    # ---------------------------------------------------------
    st.subheader("📝 จงเติมคำศัพท์ภาษาอังกฤษให้ถูกต้อง")

    ans1 = st.text_input("ข้อที่ 1: 🍎 A _ _ l e (ผลไม้สีแดง)", value=st.session_state.ans1_val, disabled=is_time_up)
    ans2 = st.text_input("ข้อที่ 2: 🐟 F _ s h (ปลา)", value=st.session_state.ans2_val, disabled=is_time_up)
    ans3 = st.text_input("ข้อที่ 3: 🍌 B _ n _ n _ (ผลไม้สีเหลือง)", value=st.session_state.ans3_val, disabled=is_time_up)
    ans4 = st.text_input("ข้อที่ 4: ✏️ P _ n _ i l (ดินสอ)", value=st.session_state.ans4_val, disabled=is_time_up)

    # อัปเดตค่าล่าสุดเข้า session_state
    st.session_state.ans1_val = ans1
    st.session_state.ans2_val = ans2
    st.session_state.ans3_val = ans3
    st.session_state.ans4_val = ans4

    col1, col2 = st.columns(2)

    with col1:
        # ปุ่มส่งคำตอบ
        if st.button("ส่งคำตอบ", disabled=is_time_up):
            u_ans1 = ans1.strip().lower()
            u_ans2 = ans2.strip().lower()
            u_ans3 = ans3.strip().lower()
            u_ans4 = ans4.strip().lower()

            # ตรวจสอบคำตอบทั้ง 4 ข้อ
            score = 0
            if u_ans1 == CORRECT_ANS1:
                score += 1
            if u_ans2 == CORRECT_ANS2:
                score += 1
            if u_ans3 == CORRECT_ANS3:
                score += 1
            if u_ans4 == CORRECT_ANS4:
                score += 1

            # แสดงผล Popup Dialog สรุปผลลัพธ์
            show_result_dialog(score, 4, u_ans1, u_ans2, u_ans3, u_ans4)

    with col2:
        # ปุ่มเริ่มเกมใหม่ (รีเซ็ตคำตอบทั้ง 4 ข้อ และเวลา 30 วินาที)
        if st.button("🔄 เริ่มเกมใหม่"):
            st.session_state.game_started = True
            st.session_state.start_time = time.time()
            st.session_state.ans1_val = ""
            st.session_state.ans2_val = ""
            st.session_state.ans3_val = ""
            st.session_state.ans4_val = ""
            st.rerun()
