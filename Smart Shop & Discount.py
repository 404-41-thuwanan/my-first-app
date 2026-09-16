import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าจอ Streamlit
st.set_page_config(page_title="PoohBanyen Cafe POS", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PoohBanyen - แอปคิดเงินประจำร้าน</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Kanit', sans-serif; }
    </style>
</head>
<body class="bg-slate-100 min-h-screen text-slate-800 pb-10">

    <!-- Navbar -->
    <nav class="bg-amber-800 text-white shadow-md">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid fa-mug-hot text-2xl"></i>
                <h1 class="text-xl font-bold">PoohBanyen Cafe</h1>
            </div>
            <div class="text-sm">
                <span id="current-date" class="bg-amber-900 px-3 py-1 rounded-full"></span>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto p-4 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left Column: Catalog & Custom Add (7 Cols) -->
        <div class="lg:col-span-7 space-y-6">
            
            <!-- Custom Product Input -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <h2 class="text-lg font-semibold mb-4 text-amber-900"><i class="fa-solid fa-cart-plus mr-2"></i>เพิ่มรายการสินค้าด่วน</h2>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <input type="text" id="custom-name" placeholder="ชื่อสินค้า (เช่น ลาเต้เย็น)" class="p-2.5 border rounded-lg focus:ring-2 focus:ring-amber-500 outline-none">
                    <input type="number" id="custom-price" placeholder="ราคา (บาท)" class="p-2.5 border rounded-lg focus:ring-2 focus:ring-amber-500 outline-none">
                    <button onclick="addCustomProduct()" class="bg-amber-700 hover:bg-amber-800 text-white font-medium py-2.5 px-4 rounded-lg transition">
                        <i class="fa-solid fa-plus mr-1"></i> เพิ่มลงตะกร้า
                    </button>
                </div>
            </div>

            <!-- Quick Catalog -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <h2 class="text-lg font-semibold mb-4 text-amber-900"><i class="fa-solid fa-utensils mr-2"></i>เมนูลัดประจำร้าน PoohBanyen</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-3" id="quick-catalog"></div>
            </div>

            <!-- Sales Summary -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-semibold text-amber-900"><i class="fa-solid fa-chart-line mr-2"></i>สรุปยอดขายวันนี้</h2>
                    <button onclick="clearHistory()" class="text-xs text-red-500 hover:underline">ล้างประวัติ</button>
                </div>
                <div class="grid grid-cols-2 gap-4 text-center">
                    <div class="bg-amber-50 p-3 rounded-lg">
                        <div class="text-xs text-amber-700 font-medium">จำนวนบิลวันนี้</div>
                        <div id="total-bills" class="text-2xl font-bold text-amber-900">0</div>
                    </div>
                    <div class="bg-emerald-50 p-3 rounded-lg">
                        <div class="text-xs text-emerald-600 font-medium">ยอดขายรวมสุทธิ</div>
                        <div id="total-sales-amount" class="text-2xl font-bold text-emerald-900">฿0.00</div>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Column: Cart & Payment (5 Cols) -->
        <div class="lg:col-span-5 space-y-6">
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <div class="flex justify-between items-center mb-4 border-b pb-3">
                    <h2 class="text-lg font-bold text-slate-800"><i class="fa-solid fa-receipt mr-2 text-amber-700"></i>ตะกร้าสินค้า</h2>
                    <button onclick="clearCart()" class="text-xs text-red-500 hover:text-red-700">ล้างตะกร้า</button>
                </div>

                <!-- Items List -->
                <div id="cart-items" class="max-h-56 overflow-y-auto divide-y mb-4">
                    <p class="text-slate-400 text-center py-8 text-sm">ยังไม่มีสินค้าในตะกร้า</p>
                </div>

                <!-- Calculations -->
                <div class="space-y-3 border-t pt-4 text-sm">
                    <div class="flex justify-between text-slate-600">
                        <span>ราคารวม (Subtotal)</span>
                        <span id="subtotal">฿0.00</span>
                    </div>

                    <!-- Discount Choices -->
                    <div class="bg-amber-50 p-3 rounded-lg space-y-2 border border-amber-200">
                        <div class="flex justify-between items-center">
                            <span class="font-semibold text-amber-900 text-xs"><i class="fa-solid fa-tags mr-1"></i>ตัวเลือกส่วนลด</span>
                        </div>
                        
                        <!-- Quick Discount 10% Button -->
                        <div class="flex gap-2 mb-2">
                            <button id="btn-discount-10" onclick="toggleTenPercentDiscount()" class="w-full py-1.5 px-3 rounded-lg text-xs font-bold border border-amber-600 text-amber-800 bg-white hover:bg-amber-100 transition">
                                <i class="fa-solid fa-percent mr-1"></i> ส่วนลด 10%
                            </button>
                        </div>

                        <!-- Manual Custom Discount -->
                        <div class="flex gap-2">
                            <select id="discount-type" onchange="calculateTotal()" class="p-2 text-xs border rounded-lg bg-white outline-none">
                                <option value="percent">กำหนด (%)</option>
                                <option value="flat">กำหนด (บาท)</option>
                            </select>
                            <input type="number" id="discount-value" value="0" min="0" oninput="calculateTotal()" placeholder="0" class="p-2 text-xs border rounded-lg bg-white w-full outline-none">
                        </div>
                    </div>

                    <!-- VAT Always Included -->
                    <div class="flex justify-between items-center text-slate-600">
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="vat-toggle" checked onchange="calculateTotal()" class="rounded text-amber-700">
                            <span>ภาษี VAT 7%</span>
                        </label>
                        <span id="vat-amount">฿0.00</span>
                    </div>

                    <!-- Net Total -->
                    <div class="flex justify-between items-center text-lg font-bold text-slate-900 border-t pt-2">
                        <span>ยอดชำระสุทธิ</span>
                        <span id="grand-total" class="text-2xl text-amber-700">฿0.00</span>
                    </div>

                    <!-- Cash & Change -->
                    <div class="pt-3 border-t space-y-2">
                        <label class="block text-xs font-medium text-slate-600">รับเงินมา (บาท)</label>
                        <input type="number" id="cash-received" oninput="calculateChange()" placeholder="0.00" class="p-2.5 border rounded-lg w-full text-lg font-semibold focus:ring-2 focus:ring-amber-500 outline-none">
                        <div class="grid grid-cols-4 gap-1 text-xs">
                            <button onclick="quickCash('exact')" class="bg-slate-200 hover:bg-slate-300 py-1.5 rounded font-medium">พอดี</button>
                            <button onclick="quickCash(100)" class="bg-slate-200 hover:bg-slate-300 py-1.5 rounded font-medium">100</button>
                            <button onclick="quickCash(500)" class="bg-slate-200 hover:bg-slate-300 py-1.5 rounded font-medium">500</button>
                            <button onclick="quickCash(1000)" class="bg-slate-200 hover:bg-slate-300 py-1.5 rounded font-medium">1000</button>
                        </div>
                    </div>

                    <div class="flex justify-between items-center p-3 bg-emerald-50 rounded-lg text-emerald-900 font-bold border border-emerald-200">
                        <span>เงินทอน</span>
                        <span id="change-amount" class="text-xl text-emerald-600">฿0.00</span>
                    </div>

                    <button onclick="checkout()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3.5 rounded-lg shadow-md transition text-center text-base">
                        <i class="fa-solid fa-check-circle mr-2"></i> จบการขาย & รับเงินทอน
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Receipt Modal Popup -->
    <div id="receipt-modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm hidden flex justify-center items-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6 text-slate-800 space-y-4">
            <div class="text-center">
                <div class="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-2 text-2xl">
                    <i class="fa-solid fa-check"></i>
                </div>
                <h3 class="text-xl font-bold text-slate-900">ชำระเงินสำเร็จ!</h3>
                <p class="text-xs text-slate-500">PoohBanyen Cafe</p>
                <p id="m-date" class="text-[11px] text-slate-400 mt-1"></p>
            </div>

            <div class="border-t border-b border-dashed py-3 my-2 space-y-1 max-h-40 overflow-y-auto text-xs" id="m-items"></div>

            <div class="space-y-1 text-xs">
                <div class="flex justify-between text-slate-600"><span>ราคารวม:</span><span id="m-subtotal"></span></div>
                <div class="flex justify-between text-slate-600"><span>ส่วนลด:</span><span id="m-discount"></span></div>
                <div class="flex justify-between text-slate-600"><span>VAT 7%:</span><span id="m-vat"></span></div>
                <div class="flex justify-between font-bold text-sm text-slate-900 border-t pt-1"><span>ยอดสุทธิ:</span><span id="m-total" class="text-amber-700"></span></div>
                <div class="flex justify-between text-slate-600 pt-1"><span>รับเงินมา:</span><span id="m-cash"></span></div>
                <div class="flex justify-between font-bold text-emerald-700 bg-emerald-50 p-2 rounded"><span>เงินทอน:</span><span id="m-change" class="text-base"></span></div>
            </div>

            <button onclick="closeModal()" class="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-2.5 rounded-xl transition">
                ตกลง / เริ่มรายการใหม่
            </button>
        </div>
    </div>

    <script>
        const presetProducts = [
            { id: 1, name: 'กาแฟอเมริกาโน่', price: 50, icon: 'fa-coffee' },
            { id: 2, name: 'ชาไทยเย็น', price: 45, icon: 'fa-glass-water' },
            { id: 3, name: 'เค้กช็อกโกแลต', price: 85, icon: 'fa-cake-candles' },
            { id: 4, name: 'ครัวซองต์', price: 60, icon: 'fa-bread-slice' },
            { id: 5, name: 'ชาเขียวมัทฉะลาเต้', price: 65, icon: 'fa-leaf' }
        ];

        let cart = [];
        let isTenPercentActive = false;
        let salesHistory = JSON.parse(localStorage.getItem('salesHistory_poohbanyen')) || [];

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('current-date').innerText = new Date().toLocaleDateString('th-TH');
            renderCatalog();
            updateHistorySummary();
        });

        function renderCatalog() {
            document.getElementById('quick-catalog').innerHTML = presetProducts.map(p => `
                <button onclick="addToCart('${p.name}', ${p.price})" class="p-3 border rounded-xl bg-slate-50 hover:bg-amber-50 hover:border-amber-300 transition text-left flex flex-col justify-between h-20 shadow-sm">
                    <div class="font-medium text-xs text-slate-700 truncate"><i class="fa-solid ${p.icon} text-amber-700 mr-1"></i>${p.name}</div>
                    <div class="text-sm font-bold text-amber-800">฿${p.price.toFixed(2)}</div>
                </button>
            `).join('');
        }

        function addToCart(name, price) {
            const item = cart.find(i => i.name === name);
            if (item) { item.qty += 1; } 
            else { cart.push({ name, price: Number(price), qty: 1 }); }
            renderCart();
        }

        function addCustomProduct() {
            const name = document.getElementById('custom-name').value.trim();
            const price = parseFloat(document.getElementById('custom-price').value);
            if (!name || isNaN(price) || price <= 0) return alert('กรุณากรอกชื่อและราคาให้ถูกต้อง');
            addToCart(name, price);
            document.getElementById('custom-name').value = '';
            document.getElementById('custom-price').value = '';
        }

        function renderCart() {
            const container = document.getElementById('cart-items');
            if (cart.length === 0) {
                container.innerHTML = '<p class="text-slate-400 text-center py-8 text-sm">ยังไม่มีสินค้าในตะกร้า</p>';
                calculateTotal();
                return;
            }
            container.innerHTML = cart.map((item, index) => `
                <div class="py-2.5 flex justify-between items-center text-sm">
                    <div class="flex-1 pr-2">
                        <div class="font-medium text-slate-800">${item.name}</div>
                        <div class="text-xs text-slate-500">฿${item.price.toFixed(2)} x ${item.qty}</div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="updateQty(${index}, -1)" class="w-6 h-6 rounded-full bg-slate-100 font-bold text-slate-600 hover:bg-slate-200">-</button>
                        <span class="w-5 text-center font-semibold">${item.qty}</span>
                        <button onclick="updateQty(${index}, 1)" class="w-6 h-6 rounded-full bg-slate-100 font-bold text-slate-600 hover:bg-slate-200">+</button>
                        <span class="font-bold text-slate-800 w-14 text-right">฿${(item.price * item.qty).toFixed(2)}</span>
                    </div>
                </div>
            `).join('');
            calculateTotal();
        }

        function updateQty(index, change) {
            cart[index].qty += change;
            if (cart[index].qty <= 0) cart.splice(index, 1);
            renderCart();
        }

        function clearCart() {
            cart = [];
            isTenPercentActive = false;
            updateTenPercentButtonUI();
            document.getElementById('discount-value').value = 0;
            document.getElementById('cash-received').value = '';
            renderCart();
        }

        function toggleTenPercentDiscount() {
            isTenPercentActive = !isTenPercentActive;
            if (isTenPercentActive) {
                document.getElementById('discount-value').value = 0; // ล้างค่าส่วนลดแบบกรอกมือ
            }
            updateTenPercentButtonUI();
            calculateTotal();
        }

        function updateTenPercentButtonUI() {
            const btn = document.getElementById('btn-discount-10');
            if (isTenPercentActive) {
                btn.className = "w-full py-1.5 px-3 rounded-lg text-xs font-bold border border-amber-600 text-white bg-amber-700 shadow-sm transition";
                btn.innerHTML = '<i class="fa-solid fa-check mr-1"></i> ใช้ส่วนลด 10%';
            } else {
                btn.className = "w-full py-1.5 px-3 rounded-lg text-xs font-bold border border-amber-600 text-amber-800 bg-white hover:bg-amber-100 transition";
                btn.innerHTML = '<i class="fa-solid fa-percent mr-1"></i> ส่วนลด 10%';
            }
        }

        function calculateTotal() {
            const subtotal = cart.reduce((sum, i) => sum + (i.price * i.qty), 0);
            const discountType = document.getElementById('discount-type').value;
            const discountValue = parseFloat(document.getElementById('discount-value').value) || 0;
            const isVat = document.getElementById('vat-toggle').checked;

            let discountAmount = 0;
            if (isTenPercentActive) {
                discountAmount = subtotal * 0.10;
            } else {
                discountAmount = discountType === 'percent' ? subtotal * (discountValue / 100) : discountValue;
            }

            discountAmount = Math.min(discountAmount, subtotal);

            const afterDiscount = subtotal - discountAmount;
            const vatAmount = isVat ? afterDiscount * 0.07 : 0;
            const grandTotal = afterDiscount + vatAmount;

            document.getElementById('subtotal').innerText = `฿${subtotal.toFixed(2)}`;
            document.getElementById('vat-amount').innerText = `฿${vatAmount.toFixed(2)}`;
            document.getElementById('grand-total').innerText = `฿${grandTotal.toFixed(2)}`;

            calculateChange();
            return { subtotal, discountAmount, vatAmount, grandTotal };
        }

        function calculateChange() {
            const { grandTotal } = calculateTotal();
            const cash = parseFloat(document.getElementById('cash-received').value) || 0;
            const changeElem = document.getElementById('change-amount');

            if (cart.length === 0 || cash < grandTotal) {
                changeElem.innerText = '฿0.00';
                changeElem.className = 'text-xl font-bold text-slate-400';
            } else {
                const change = cash - grandTotal;
                changeElem.innerText = `฿${change.toFixed(2)}`;
                changeElem.className = 'text-xl font-bold text-emerald-600';
            }
        }

        function quickCash(amount) {
            const { grandTotal } = calculateTotal();
            document.getElementById('cash-received').value = amount === 'exact' ? grandTotal.toFixed(2) : amount;
            calculateChange();
        }

        function checkout() {
            if (cart.length === 0) return alert('โปรดเลือกสินค้าอย่างน้อย 1 รายการ');
            const { subtotal, discountAmount, vatAmount, grandTotal } = calculateTotal();
            const cash = parseFloat(document.getElementById('cash-received').value) || 0;
            if (cash < grandTotal) return alert('ยอดเงินที่รับมาไม่เพียงพอ');

            const change = cash - grandTotal;
            const transaction = { id: Date.now(), date: new Date().toLocaleString('th-TH'), total: grandTotal };
            salesHistory.push(transaction);
            localStorage.setItem('salesHistory_poohbanyen', JSON.stringify(salesHistory));
            updateHistorySummary();

            // แสดง Modal ใบเสร็จ & สรุปเงินทอน
            document.getElementById('m-date').innerText = transaction.date;
            document.getElementById('m-items').innerHTML = cart.map(i => `
                <div class="flex justify-between text-slate-700">
                    <span>${i.name} x${i.qty}</span>
                    <span>฿${(i.price * i.qty).toFixed(2)}</span>
                </div>
            `).join('');

            document.getElementById('m-subtotal').innerText = `฿${subtotal.toFixed(2)}`;
            document.getElementById('m-discount').innerText = `-฿${discountAmount.toFixed(2)}`;
            document.getElementById('m-vat').innerText = `฿${vatAmount.toFixed(2)}`;
            document.getElementById('m-total').innerText = `฿${grandTotal.toFixed(2)}`;
            document.getElementById('m-cash').innerText = `฿${cash.toFixed(2)}`;
            document.getElementById('m-change').innerText = `฿${change.toFixed(2)}`;

            document.getElementById('receipt-modal').classList.remove('hidden');
        }

        function closeModal() {
            document.getElementById('receipt-modal').classList.add('hidden');
            clearCart();
        }

        function updateHistorySummary() {
            document.getElementById('total-bills').innerText = salesHistory.length;
            const total = salesHistory.reduce((sum, item) => sum + item.total, 0);
            document.getElementById('total-sales-amount').innerText = `฿${total.toFixed(2)}`;
        }

        function clearHistory() {
            if (confirm('ต้องการล้างประวัติการขายทั้งหมดใช่หรือไม่?')) {
                salesHistory = [];
                localStorage.removeItem('salesHistory_poohbanyen');
                updateHistorySummary();
            }
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=True)
