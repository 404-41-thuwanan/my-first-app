import streamlit as st
import datetime

# 1. ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="PoohBanyen Cafe POS", page_icon="☕", layout="wide")

# 2. จัดการ State ความจำของระบบ
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "sales_history" not in st.session_state:
    st.session_state.sales_history = []
if "use_discount_10" not in st.session_state:
    st.session_state.use_discount_10 = False
if "cash_input_val" not in st.session_state:
    st.session_state.cash_input_val = 0.0

# 3. ส่วนหัวของแอปพลิเคชัน
st.title("☕ PoohBanyen Cafe POS")
st.caption(f"วันที่: {datetime.date.today().strftime('%d/%m/%Y')}")

# แยกหน้าจอเป็น 2 ฝั่ง (ฝั่งซ้ายเลือกสินค้า 7 ส่วน / ฝั่งขวาตะกร้าคิดเงิน 5 ส่วน)
col_left, col_right = st.columns([7, 5])

# รายการสินค้าแนะนำ
preset_products = [
    {"name": "กาแฟอเมริกาโน่", "price": 50.0, "icon": "☕"},
    {"name": "ชาไทยเย็น", "price": 45.0, "icon": "🧋"},
    {"name": "เค้กช็อกโกแลต", "price": 85.0, "icon": "🍰"},
    {"name": "ครัวซองต์", "price": 60.0, "icon": "🥐"},
    {"name": "ชาเขียวมัทฉะลาเต้", "price": 65.0, "icon": "🍵"},
]

# --- ฝั่งซ้าย: เพิ่มและเลือกสินค้า ---
with col_left:
    st.subheader("➕ เพิ่มรายการสินค้าด่วน")
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        custom_name = st.text_input("ชื่อสินค้า", placeholder="เช่น ลาเต้เย็น", key="c_name")
    with c2:
        custom_price = st.number_input("ราคา (บาท)", min_value=0.0, step=5.0, key="c_price")
    with c3:
        st.write(" ")
        st.write(" ")
        if st.button("เพิ่มลงตะกร้า", type="primary", use_container_width=True):
            if custom_name and custom_price > 0:
                if custom_name in st.session_state.cart:
                    st.session_state.cart[custom_name]["qty"] += 1
                else:
                    st.session_state.cart[custom_name] = {"price": custom_price, "qty": 1}
                st.rerun()
            else:
                st.error("กรุณากรอกชื่อและราคาให้ถูกต้อง")

    st.subheader("📋 เมนูลัดประจำร้าน PoohBanyen")
    grid_cols = st.columns(3)
    for idx, prod in enumerate(preset_products):
        with grid_cols[idx % 3]:
            if st.button(f"{prod['icon']} {prod['name']}\n\n฿{prod['price']:.2f}", key=f"p_{idx}", use_container_width=True):
                name = prod["name"]
                if name in st.session_state.cart:
                    st.session_state.cart[name]["qty"] += 1
                else:
                    st.session_state.cart[name] = {"price": prod["price"], "qty": 1}
                st.rerun()

    st.divider()
    st.subheader("📊 สรุปยอดขายวันนี้")
    total_bills = len(st.session_state.sales_history)
    total_sales = sum(item["total"] for item in st.session_state.sales_history)
    
    sc1, sc2 = st.columns(2)
    sc1.metric("จำนวนบิลวันนี้", f"{total_bills} บิล")
    sc2.metric("ยอดขายรวมสุทธิ", f"฿{total_sales:,.2f}")
    
    if st.button("ล้างประวัติการขาย"):
        st.session_state.sales_history = []
        st.rerun()

# --- ฝั่งขวา: ตะกร้าสินค้า การคิดเงิน และทอนเงิน ---
with col_right:
    st.subheader("🛒 ตะกร้าสินค้า")
    
    if not st.session_state.cart:
        st.info("ยังไม่มีสินค้าในตะกร้า")
    else:
        for name, details in list(st.session_state.cart.items()):
            ic1, ic2, ic3 = st.columns([4, 3, 1])
            ic1.write(f"**{name}**\n\n฿{details['price']:.2f}")
            
            # ปุ่มเพิ่ม/ลด จำนวน
            qty = ic2.number_input("จำนวน", min_value=1, value=details['qty'], key=f"q_{name}", label_visibility="collapsed")
            st.session_state.cart[name]["qty"] = qty
            
            if ic3.button("❌", key=f"del_{name}"):
                del st.session_state.cart[name]
                st.rerun()

        if st.button("ล้างตะกร้าทั้งหมด", type="secondary"):
            st.session_state.cart = {}
            st.rerun()

    st.divider()
    
    # การคำนวณราคารวม
    subtotal = sum(d["price"] * d["qty"] for d in st.session_state.cart.values())
    
    st.subheader("🏷️ ส่วนลด & ภาษี")
    
    # ปุ่มเลือกส่วนลด 10%
    st.session_state.use_discount_10 = st.checkbox("🏷️ ใช้ส่วนลด 10%", value=st.session_state.use_discount_10)
    
    if st.session_state.use_discount_10:
        discount_amount = subtotal * 0.10
    else:
        discount_amount = st.number_input("ส่วนลดเพิ่มเติม (บาท)", min_value=0.0, max_value=float(subtotal), value=0.0)
        
    after_discount = subtotal - discount_amount
    vat_amount = after_discount * 0.07  # คิด VAT 7%
    grand_total = after_discount + vat_amount
    
    st.write(f"**ราคารวม (Subtotal):** ฿{subtotal:,.2f}")
    st.write(f"**ส่วนลด:** -฿{discount_amount:,.2f}")
    st.write(f"**ภาษี VAT (7%):** ฿{vat_amount:,.2f}")
    st.markdown(f"### **ยอดชำระสุทธิ:** :green[฿{grand_total:,.2f}]")
    
    st.divider()
    
    st.subheader("💵 รับเงิน & คำนวณเงินทอน")
    
    # ปุ่มรับเงินด่วน
    qc1, qc2, qc3, qc4 = st.columns(4)
    if qc1.button("พอดี", use_container_width=True):
        st.session_state.cash_input_val = float(grand_total)
        st.rerun()
    if qc2.button("100", use_container_width=True):
        st.session_state.cash_input_val = 100.0
        st.rerun()
    if qc3.button("500", use_container_width=True):
        st.session_state.cash_input_val = 500.0
        st.rerun()
    if qc4.button("1000", use_container_width=True):
        st.session_state.cash_input_val = 1000.0
        st.rerun()
        
    cash = st.number_input("รับเงินมา (บาท)", min_value=0.0, value=float(st.session_state.cash_input_val), step=10.0, key="cash_field")
    st.session_state.cash_input_val = cash
    
    change = cash - grand_total
    
    if cash > 0 and cash < grand_total:
        st.error(f"⚠️ เงินยังขาดอีก ฿{grand_total - cash:,.2f}")
    elif cash >= grand_total and grand_total > 0:
        st.success(f"### **เงินทอน:** ฿{change:,.2f}")

    # ปุ่มจบการขาย
    can_checkout = len(st.session_state.cart) > 0 and cash >= grand_total and grand_total > 0
    if st.button("✅ จบการขาย & รับเงินทอน", type="primary", use_container_width=True, disabled=not can_checkout):
        # บันทึกยอดขาย
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.session_state.sales_history.append({"timestamp": now, "total": grand_total})
        
        st.balloons()
        st.success("🎉 ชำระเงินสำเร็จ!")
        
        # แสดงใบเสร็จรับเงิน
        st.markdown("### 📄 ใบเสร็จรับเงิน (PoohBanyen Cafe)")
        st.caption(f"เวลา: {now}")
        st.write("---")
        for item_name, item_info in st.session_state.cart.items():
            st.write(f"{item_name} x{item_info['qty']} — ฿{item_info['price']*item_info['qty']:.2f}")
        st.write("---")
        st.write(f"ราคารวม: ฿{subtotal:.2f}")
        st.write(f"ส่วนลด: -฿{discount_amount:.2f}")
        st.write(f"VAT 7%: ฿{vat_amount:.2f}")
        st.write(f"**ยอดชำระสุทธิ: ฿{grand_total:.2f}**")
        st.write(f"รับเงินมา: ฿{cash:.2f}")
        st.markdown(f"### **เงินทอน: ฿{change:.2f}**")
        st.write("---")
        
        # ล้างตะกร้าหลังจบการขาย
        st.session_state.cart = {}
        st.session_state.cash_input_val = 0.0
        st.session_state.use_discount_10 = False
