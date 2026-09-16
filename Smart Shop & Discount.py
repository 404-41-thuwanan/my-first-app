<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Shop & Discount - แอปคิดเงินและคำนวณประจำร้าน</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Kanit', sans-serif; }
        @media print {
            .no-print { display: none !important; }
            .print-only { display: block !important; }
        }
    </style>
</head>
<body class="bg-slate-100 min-h-screen text-slate-800">

    <!-- Navbar -->
    <nav class="bg-indigo-600 text-white shadow-md no-print">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid fa-store text-2xl"></i>
                <h1 class="text-xl font-bold">Smart Shop & Discount</h1>
            </div>
            <div class="text-sm">
                <span id="current-date" class="bg-indigo-700 px-3 py-1 rounded-full"></span>
            </div>
        </div>
    </nav>

    <!-- Main Container -->
    <div class="max-w-7xl mx-auto p-4 grid grid-cols-1 lg:grid-cols-12 gap-6 no-print">
        
        <!-- Left Column: Products & Custom Input (7 Cols) -->
        <div class="lg:col-span-7 space-y-6">
            
            <!-- Custom Add Product -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <h2 class="text-lg font-semibold mb-4 text-indigo-900"><i class="fa-solid fa-cart-plus mr-2"></i>เพิ่มรายการสินค้าด่วน</h2>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <input type="text" id="custom-name" placeholder="ชื่อสินค้า (เช่น กาแฟเย็น)" class="p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
                    <input type="number" id="custom-price" placeholder="ราคา (บาท)" class="p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
                    <button onclick="addCustomProduct()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 px-4 rounded-lg transition duration-200">
                        <i class="fa-solid fa-plus mr-1"></i> เพิ่มลงตะกร้า
                    </button>
                </div>
            </div>

            <!-- Quick Catalog -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <h2 class="text-lg font-semibold mb-4 text-indigo-900"><i class="fa-solid fa-boxes-stacked mr-2"></i>เมนูลัดประจำร้าน</h2>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-3" id="quick-catalog">
                    <!-- Dynamic Buttons -->
                </div>
            </div>

            <!-- Sales History / Summary -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-semibold text-indigo-900"><i class="fa-solid fa-chart-line mr-2"></i>สรุปยอดขายวันนี้</h2>
                    <button onclick="clearHistory()" class="text-xs text-red-500 hover:underline">ล้างประวัติ</button>
                </div>
                <div class="grid grid-cols-2 gap-4 text-center">
                    <div class="bg-indigo-50 p-3 rounded-lg">
                        <div class="text-xs text-indigo-600 font-medium">จำนวนบิลวันนี้</div>
                        <div id="total-bills" class="text-2xl font-bold text-indigo-900">0</div>
                    </div>
                    <div class="bg-emerald-50 p-3 rounded-lg">
                        <div class="text-xs text-emerald-600 font-medium">ยอดขายรวมสุทธิ</div>
                        <div id="total-sales-amount" class="text-2xl font-bold text-emerald-900">฿0.00</div>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Column: Cart, Discount & Checkout (5 Cols) -->
        <div class="lg:col-span-5 space-y-6">
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 sticky top-4">
                <div class="flex justify-between items-center mb-4 border-b pb-3">
                    <h2 class="text-lg font-bold text-slate-800"><i class="fa-solid fa-receipt mr-2 text-indigo-600"></i>ตะกร้าสินค้า</h2>
                    <button onclick="clearCart()" class="text-xs text-red-500 hover:text-red-700">ล้างตะกร้า</button>
                </div>

                <!-- Cart Items List -->
                <div id="cart-items" class="max-h-56 overflow-y-auto divide-y mb-4">
                    <p class="text-slate-400 text-center py-8 text-sm">ยังไม่มีสินค้าในตะกร้า</p>
                </div>

                <!-- Calculation Section -->
                <div class="space-y-3 border-t pt-4 text-sm">
                    <!-- Subtotal -->
                    <div class="flex justify-between text-slate-600">
                        <span>ราคารวม (Subtotal)</span>
                        <span id="subtotal">฿0.00</span>
                    </div>

                    <!-- Discount Section -->
                    <div class="bg-amber-50 p-3 rounded-lg space-y-2">
                        <div class="font-medium text-amber-900 text-xs">คำนวณส่วนลด (Discount)</div>
                        <div class="flex gap-2">
                            <select id="discount-type" onchange="calculateTotal()" class="p-2 text-xs border rounded-lg bg-white outline-none">
                                <option value="percent">ส่วนลด (%)</option>
                                <option value="flat">ส่วนลด (บาท)</option>
                            </select>
                            <input type="number" id="discount-value" value="0" min="0" oninput="calculateTotal()" placeholder="0" class="p-2 text-xs border rounded-lg bg-white w-full outline-none">
                        </div>
                    </div>

                    <!-- VAT Toggle -->
                    <div class="flex justify-between items-center text-slate-600">
                        <label class="flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="vat-toggle" onchange="calculateTotal()" class="rounded text-indigo-600">
                            <span>คิดภาษี VAT 7%</span>
                        </label>
                        <span id="vat-amount">฿0.00</span>
                    </div>

                    <!-- Grand Total -->
                    <div class="flex justify-between items-center text-lg font-bold text-slate-900 border-t pt-2">
                        <span>ยอดชำระสุทธิ</span>
                        <span id="grand-total" class="text-2xl text-indigo-600">฿0.00</span>
                    </div>

                    <!-- Payment Section -->
                    <div class="pt-3 border-t space-y-2">
                        <label class="block text-xs font-medium text-slate-600">รับเงินมา (บาท)</label>
                        <div class="flex gap-2">
                            <input type="number" id="cash-received" oninput="calculateChange()" placeholder="0.00" class="p-2.5 border rounded-lg w-full text-lg font-semibold focus:ring-2 focus:ring-indigo-500 outline-none">
                        </div>
                        <div class="grid grid-cols-4 gap-1 text-xs">
                            <button onclick="quickCash('exact')" class="bg-slate-200 hover:bg-slate-300 py-1 rounded">พอดี</button>
                            <button onclick="quickCash(100)" class="bg-slate-200 hover:bg-slate-300 py-1 rounded">100</button>
                            <button onclick="quickCash(500)" class="bg-slate-200 hover:bg-slate-300 py-1 rounded">500</button>
                            <button onclick="quickCash(1000)" class="bg-slate-200 hover:bg-slate-300 py-1 rounded">1000</button>
                        </div>
                    </div>

                    <!-- Change Result -->
                    <div class="flex justify-between items-center p-3 bg-emerald-50 rounded-lg text-emerald-900 font-bold">
                        <span>เงินทอน</span>
                        <span id="change-amount" class="text-xl">฿0.00</span>
                    </div>

                    <!-- Submit Button -->
                    <button onclick="checkout()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-lg shadow-md transition duration-200 text-center">
                        <i class="fa-solid fa-check-circle mr-2"></i> จบการขาย / พิมพ์ใบเสร็จ
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Printable Receipt Area (Hidden on Web View) -->
    <div id="receipt-print" class="hidden print-only p-6 max-w-xs mx-auto bg-white text-black text-xs font-mono">
        <div class="text-center mb-4">
            <h2 class="text-base font-bold">Smart Shop</h2>
            <p>ใบเสร็จรับเงินอย่างย่อ</p>
            <p id="receipt-date"></p>
        </div>
        <div class="border-b border-dashed mb-2"></div>
        <div id="receipt-items" class="space-y-1 mb-2"></div>
        <div class="border-b border-dashed mb-2"></div>
        <div class="space-y-1">
            <div class="flex justify-between"><span>รวม:</span><span id="r-subtotal"></span></div>
            <div class="flex justify-between"><span>ส่วนลด:</span><span id="r-discount"></span></div>
            <div class="flex justify-between"><span>VAT 7%:</span><span id="r-vat"></span></div>
            <div class="flex justify-between font-bold text-sm"><span>สุทธิ:</span><span id="r-total"></span></div>
            <div class="flex justify-between"><span>รับเงิน:</span><span id="r-cash"></span></div>
            <div class="flex justify-between"><span>เงินทอน:</span><span id="r-change"></span></div>
        </div>
        <div class="border-b border-dashed my-3"></div>
        <div class="text-center text-slate-500">ขอบคุณที่อุดหนุนครับ!</div>
    </div>

    <script>
        // Preset Products
        const presetProducts = [
            { id: 1, name: 'กาแฟอเมริกาโน่', price: 50, icon: 'fa-coffee' },
            { id: 2, name: 'ชาไทยเย็น', price: 45, icon: 'fa-glass-water' },
            { id: 3, name: 'เค้กช็อกโกแลต', price: 85, icon: 'fa-cake-candles' },
            { id: 4, name: 'ครัวซองต์', price: 60, icon: 'fa-bread-slice' },
            { id: 5, name: 'น้ำเปล่า', price: 10, icon: 'fa-bottle-water' }
        ];

        let cart = [];
        let salesHistory = JSON.parse(localStorage.getItem('salesHistory')) || [];

        // Initialize App
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('current-date').innerText = new Date().toLocaleDateString('th-TH');
            renderCatalog();
            updateHistorySummary();
        });

        // Render Quick Catalog
        function renderCatalog() {
            const container = document.getElementById('quick-catalog');
            container.innerHTML = presetProducts.map(p => `
                <button onclick="addToCart('${p.name}', ${p.price})" class="p-3 border rounded-xl bg-slate-50 hover:bg-indigo-50 hover:border-indigo-300 transition text-left flex flex-col justify-between h-20">
                    <div class="font-medium text-xs text-slate-700 truncate"><i class="fa-solid ${p.icon} text-indigo-500 mr-1"></i>${p.name}</div>
                    <div class="text-sm font-bold text-indigo-600">฿${p.price.toFixed(2)}</div>
                </button>
            `).join('');
        }

        // Add Product to Cart
        function addToCart(name, price) {
            const existing = cart.find(item => item.name === name);
            if (existing) {
                existing.qty += 1;
            } else {
                cart.push({ name, price: Number(price), qty: 1 });
            }
            renderCart();
        }

        function addCustomProduct() {
            const nameInput = document.getElementById('custom-name');
            const priceInput = document.getElementById('custom-price');
            const name = nameInput.value.trim();
            const price = parseFloat(priceInput.value);

            if (!name || isNaN(price) || price <= 0) {
                alert('กรุณากรอกชื่อและราคาให้ถูกต้อง');
                return;
            }

            addToCart(name, price);
            nameInput.value = '';
            priceInput.value = '';
        }

        // Render Cart
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
                        <button onclick="updateQty(${index}, -1)" class="w-6 h-6 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center font-bold text-slate-600">-</button>
                        <span class="w-5 text-center font-semibold">${item.qty}</span>
                        <button onclick="updateQty(${index}, 1)" class="w-6 h-6 rounded-full bg-slate-100 hover:bg-slate-200 flex items-center justify-center font-bold text-slate-600">+</button>
                        <span class="font-bold text-slate-800 w-14 text-right">฿${(item.price * item.qty).toFixed(2)}</span>
                    </div>
                </div>
            `).join('');

            calculateTotal();
        }

        function updateQty(index, change) {
            cart[index].qty += change;
            if (cart[index].qty <= 0) {
                cart.splice(index, 1);
            }
            renderCart();
        }

        function clearCart() {
            cart = [];
            document.getElementById('discount-value').value = 0;
            document.getElementById('cash-received').value = '';
            renderCart();
        }

        // Calculation Logic
        function calculateTotal() {
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
            const discountType = document.getElementById('discount-type').value;
            const discountValue = parseFloat(document.getElementById('discount-value').value) || 0;
            const isVat = document.getElementById('vat-toggle').checked;

            let discountAmount = 0;
            if (discountType === 'percent') {
                discountAmount = subtotal * (discountValue / 100);
            } else {
                discountAmount = discountValue;
            }
            discountAmount = Math.min(discountAmount, subtotal); // Prevent negative

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
            const change = cash - grandTotal;
            const changeElem = document.getElementById('change-amount');

            if (cart.length === 0 || cash < grandTotal) {
                changeElem.innerText = '฿0.00';
                changeElem.className = 'text-xl text-slate-400';
            } else {
                changeElem.innerText = `฿${change.toFixed(2)}`;
                changeElem.className = 'text-xl text-emerald-600';
            }
        }

        function quickCash(amount) {
            const { grandTotal } = calculateTotal();
            if (amount === 'exact') {
                document.getElementById('cash-received').value = grandTotal.toFixed(2);
            } else {
                document.getElementById('cash-received').value = amount;
            }
            calculateChange();
        }

        // Checkout & Print Receipt
        function checkout() {
            if (cart.length === 0) {
                alert('โปรดเลือกสินค้าอย่างน้อย 1 รายการ');
                return;
            }

            const { subtotal, discountAmount, vatAmount, grandTotal } = calculateTotal();
            const cash = parseFloat(document.getElementById('cash-received').value) || 0;

            if (cash < grandTotal) {
                alert('ยอดเงินที่รับมาไม่เพียงพอ');
                return;
            }

            // Save transaction to history
            const transaction = {
                id: Date.now(),
                date: new Date().toLocaleString('th-TH'),
                total: grandTotal
            };
            salesHistory.push(transaction);
            localStorage.setItem('salesHistory', JSON.stringify(salesHistory));
            updateHistorySummary();

            // Prepare Receipt Print
            document.getElementById('receipt-date').innerText = transaction.date;
            document.getElementById('receipt-items').innerHTML = cart.map(item => `
                <div class="flex justify-between">
                    <span>${item.name} x${item.qty}</span>
                    <span>${(item.price * item.qty).toFixed(2)}</span>
                </div>
            `).join('');
            document.getElementById('r-subtotal').innerText = subtotal.toFixed(2);
            document.getElementById('r-discount').innerText = discountAmount.toFixed(2);
            document.getElementById('r-vat').innerText = vatAmount.toFixed(2);
            document.getElementById('r-total').innerText = grandTotal.toFixed(2);
            document.getElementById('r-cash').innerText = cash.toFixed(2);
            document.getElementById('r-change').innerText = (cash - grandTotal).toFixed(2);

            // Print
            window.print();

            // Reset after sale
            clearCart();
            alert('บันทึกการขายสำเร็จ!');
        }

        // History Summary
        function updateHistorySummary() {
            document.getElementById('total-bills').innerText = salesHistory.length;
            const totalAmount = salesHistory.reduce((sum, item) => sum + item.total, 0);
            document.getElementById('total-sales-amount').innerText = `฿${totalAmount.toFixed(2)}`;
        }

        function clearHistory() {
            if (confirm('คุณต้องการล้างประวัติการขายทั้งหมดใช่หรือไม่?')) {
                salesHistory = [];
                localStorage.removeItem('salesHistory');
                updateHistorySummary();
            }
        }
    </script>
</body>
</html>
