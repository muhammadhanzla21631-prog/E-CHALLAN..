# 🚀 E-Challan Quick Reference Card

## Most Useful Functions - Quick Access

---

## 🔐 Authentication & Session
```javascript
// Login
const user = await API.login('username', 'password');
Session.setUser(user.user);

// Check if logged in
if (Session.isLoggedIn()) { /* ... */ }

// Logout
Session.logout();
```

---

## 👤 User Profile
```javascript
// Get profile
const profile = await API.getUser(userId);

// Update profile
await API.updateUser(userId, {
    full_name: "Ahmed Ali",
    phone: "03001234567",
    cnic: "12345-1234567-1"
});
```

---

## 🚗 Challans
```javascript
// Get all challans (with filters)
const challans = await API.getChallans({
    status: 'unpaid',
    vehicle: 'ABC-1234',
    limit: 50
});

// Get detailed challan
const details = await API.getChallanDetails(challanId);
```

---

## 💳 Payments
```javascript
// Create payment
const payment = await API.createPayment(
    challanId,
    userId,
    'jazzcash',  // or 'easypay', 'card', 'bank_transfer'
    'TXN123456'
);

// Confirm payment
await API.confirmPayment(payment.payment_id);

// Get payment history
const payments = await API.getPayments({ user_id: userId });
```

---

## 📝 Appeals
```javascript
// Submit appeal
await API.createAppeal(
    challanId,
    userId,
    "I was not driving the vehicle at that time..."
);

// Get appeals
const appeals = await API.getAppeals({ status: 'pending' });

// Review appeal (admin)
await API.reviewAppeal(appealId, true, "Approved - Valid reason");
```

---

## 🔍 Search
```javascript
// Universal search
const results = await API.search('ABC-1234');
// Returns: { vehicles: [], challans: [], cameras: [] }
```

---

## 📊 Analytics
```javascript
// Get dashboard statistics
const stats = await API.getDashboard();
// Returns: total violations, revenue, cameras, payments, appeals, etc.

// Get camera health
const health = await API.getCameraHealth();
```

---

## ✅ Validation
```javascript
// Email
Validators.email('test@example.com')  // true/false

// Phone (Pakistan)
Validators.phone('03001234567')  // true/false

// CNIC
Validators.cnic('12345-1234567-1')  // true/false

// Vehicle number
Validators.vehicleNumber('ABC-1234')  // true/false

// Form validation
const validation = validateForm(formData, {
    email: [
        { validator: 'required' },
        { validator: 'email' }
    ]
});

if (!validation.isValid) {
    console.log(validation.errors);
}
```

---

## 🎨 Formatting
```javascript
// Currency
Format.currency(2500)  // "PKR 2,500"

// Date & Time
Format.date("2025-12-10T23:00:00")      // "Dec 10, 2025"
Format.datetime("2025-12-10T23:00:00")  // "Dec 10, 2025, 11:00 PM"
Format.timeAgo("2025-12-10T22:00:00")   // "1 hour ago"

// Phone
Format.phone('03001234567')  // "+92 300 1234567"

// Status badge (HTML)
Format.statusBadge('paid')  // <span class="badge badge-success">Paid</span>
```

---

## 🔔 UI Notifications
```javascript
// Success toast
UI.toast('Payment successful!', 'success');

// Error toast
UI.toast('Operation failed', 'error');

// Warning toast
UI.toast('Please check your input', 'warning');

// Info toast
UI.toast('Processing...', 'info');

// Confirmation dialog
UI.confirm('Delete this item?', 
    () => { /* on confirm */ },
    () => { /* on cancel */ }
);
```

---

## ⏳ Loading States
```javascript
// Show loading
UI.showLoading('resultDiv');

// Hide loading
UI.hideLoading('resultDiv');

// Button loading
UI.setButtonLoading('submitBtn', true);   // Show loading
UI.setButtonLoading('submitBtn', false);  // Hide loading
```

---

## 📥 Download/Export
```javascript
// Export challans as CSV
const result = await API.exportChallansCSV();
Download.csv(result.csv, result.filename);

// Export custom data as JSON
Download.json(data, 'export.json');
```

---

## 🎯 Common Patterns

### Pattern 1: Login Flow
```javascript
async function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const result = await API.login(username, password);
        Session.setUser(result.user);
        UI.toast('Login successful!', 'success');
        window.location.href = 'index.html';
    } catch (error) {
        UI.toast('Login failed: ' + error.message, 'error');
    }
}
```

### Pattern 2: Payment Flow
```javascript
async function handlePayment(challanId) {
    const user = Session.getUser();
    
    UI.confirm('Proceed with payment?', async () => {
        try {
            const payment = await API.createPayment(
                challanId,
                user.id,
                'jazzcash',
                'TXN_' + Date.now()
            );
            
            await API.confirmPayment(payment.payment_id);
            
            UI.toast('Payment successful!', 'success');
        } catch (error) {
            UI.toast('Payment failed', 'error');
        }
    });
}
```

### Pattern 3: Search with Debounce
```javascript
const searchInput = document.getElementById('search');

const performSearch = debounce(async (query) => {
    if (query.length < 2) return;
    
    const results = await API.search(query);
    displayResults(results);
}, 300);

searchInput.addEventListener('input', (e) => {
    performSearch(e.target.value);
});
```

### Pattern 4: Form Validation & Submission
```javascript
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        cnic: document.getElementById('cnic').value
    };
    
    const validation = validateForm(formData, {
        email: [
            { validator: 'required', message: 'Email required' },
            { validator: 'email', message: 'Invalid email' }
        ],
        phone: [
            { validator: 'required' },
            { validator: 'phone', message: 'Invalid phone number' }
        ],
        cnic: [
            { validator: 'required' },
            { validator: 'cnic', message: 'Invalid CNIC format' }
        ]
    });
    
    if (!validation.isValid) {
        for (const [field, error] of Object.entries(validation.errors)) {
            UI.showError(field + 'Error', error);
        }
        return;
    }
    
    // Submit form
    try {
        await API.updateUser(userId, formData);
        UI.toast('Profile updated!', 'success');
    } catch (error) {
        UI.toast('Update failed', 'error');
    }
}
```

---

## 📚 File Structure

```
e--challan/
├── backend/
│   ├── main.py           ← 18 new API endpoints
│   └── models.py         ← Enhanced models + Payment + Appeal
│
├── frontend/
│   ├── utils.js          ← 53 utility functions
│   ├── demo.html         ← Interactive demo page
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── NEW_FUNCTIONS_GUIDE.md    ← Complete documentation
└── FUNCTIONS_SUMMARY.md      ← Summary overview
```

---

## 🎓 Learning Resources

1. **Demo Page**: `frontend/demo.html` - Interactive examples
2. **Full Guide**: `NEW_FUNCTIONS_GUIDE.md` - Detailed documentation
3. **Summary**: `FUNCTIONS_SUMMARY.md` - Quick overview
4. **This Card**: `QUICK_REFERENCE.md` - Common usage patterns

---

## 🔥 Pro Tips

1. **Always include utils.js** in your HTML:
   ```html
   <script src="utils.js"></script>
   ```

2. **Use Session.requireAuth()** at the top of protected pages:
   ```javascript
   Session.requireAuth(); // Redirects to login if not authenticated
   ```

3. **Wrap API calls in try-catch** for error handling:
   ```javascript
   try {
       const result = await API.someFunction();
       UI.toast('Success!', 'success');
   } catch (error) {
       UI.toast('Error: ' + error.message, 'error');
   }
   ```

4. **Use debounce for search** to avoid excessive API calls:
   ```javascript
   const debouncedSearch = debounce(searchFunction, 300);
   ```

5. **Show loading states** for better UX:
   ```javascript
   UI.showLoading('resultDiv');
   // ... do work ...
   UI.hideLoading('resultDiv');
   ```

---

**Keep this card handy for quick reference! 📌**
