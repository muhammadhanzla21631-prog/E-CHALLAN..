# E-Challan System - New Functions Documentation

## 🎉 Successfully Added Functions

This document lists all the new functions added to enhance the E-Challan system.

---

## 📡 Backend API Functions (main.py)

### 1. **User Profile Management**

#### `GET /api/user/{user_id}`
- **Description**: Get detailed user profile information
- **Returns**: User details, total challans, total fines, unpaid challans count
- **Example**: 
  ```
  GET http://localhost:8000/api/user/1
  ```

#### `PUT /api/user/{user_id}`
- **Description**: Update user profile information
- **Parameters**: `full_name`, `phone`, `cnic`
- **Example**:
  ```
  PUT http://localhost:8000/api/user/1
  Body: { "full_name": "Ahmed Ali", "phone": "03001234567", "cnic": "12345-1234567-1" }
  ```

---

### 2. **Challan Management & Search**

#### `GET /api/challans`
- **Description**: Get all challans with advanced filtering
- **Filters**: `status`, `vehicle`, `camera_id`, `user_id`, `limit`
- **Example**:
  ```
  GET http://localhost:8000/api/challans?status=unpaid&limit=50
  ```

#### `GET /api/challan/{challan_id}`
- **Description**: Get detailed challan information including camera, payment, and appeal details
- **Returns**: Complete challan data with related information
- **Example**:
  ```
  GET http://localhost:8000/api/challan/123
  ```

---

### 3. **Payment Processing System**

#### `POST /api/payment`
- **Description**: Create a new payment for a challan
- **Parameters**: `challan_id`, `user_id`, `payment_method`, `transaction_id`
- **Payment Methods**: `card`, `bank_transfer`, `easypay`, `jazzcash`
- **Example**:
  ```
  POST http://localhost:8000/api/payment
  Body: {
    "challan_id": 123,
    "user_id": 1,
    "payment_method": "jazzcash",
    "transaction_id": "TXN123456"
  }
  ```

#### `PUT /api/payment/{payment_id}/confirm`
- **Description**: Confirm a payment (admin or payment gateway callback)
- **Updates**: Payment status to "completed", challan status to "paid"
- **Example**:
  ```
  PUT http://localhost:8000/api/payment/45/confirm
  ```

#### `GET /api/payments`
- **Description**: Get payment history with filters
- **Filters**: `user_id`, `status`
- **Example**:
  ```
  GET http://localhost:8000/api/payments?user_id=1&status=completed
  ```

---

### 4. **Appeals System**

#### `POST /api/appeal`
- **Description**: Submit an appeal for a challan
- **Parameters**: `challan_id`, `user_id`, `reason`
- **Example**:
  ```
  POST http://localhost:8000/api/appeal
  Body: {
    "challan_id": 123,
    "user_id": 1,
    "reason": "I was not driving the vehicle at the time"
  }
  ```

#### `GET /api/appeals`
- **Description**: Get list of appeals
- **Filters**: `status`, `user_id`
- **Example**:
  ```
  GET http://localhost:8000/api/appeals?status=pending
  ```

#### `PUT /api/appeal/{appeal_id}/review`
- **Description**: Review an appeal (admin only)
- **Parameters**: `approved` (boolean), `reviewer_notes`
- **Example**:
  ```
  PUT http://localhost:8000/api/appeal/10/review
  Body: { "approved": true, "reviewer_notes": "Valid reason provided" }
  ```

---

### 5. **Enhanced Analytics**

#### `GET /api/analytics/dashboard`
- **Description**: Get comprehensive dashboard statistics
- **Returns**: 
  - Total violations, revenue (total/paid/pending)
  - Camera counts (total/active)
  - Payment statistics
  - Appeals statistics
  - Violation types breakdown
- **Example**:
  ```
  GET http://localhost:8000/api/analytics/dashboard
  ```

---

### 6. **Universal Search**

#### `GET /api/search`
- **Description**: Search across vehicles, challans, and cameras
- **Parameters**: `query` (search term)
- **Searches**: Vehicle numbers, challan IDs, camera addresses
- **Example**:
  ```
  GET http://localhost:8000/api/search?query=ABC-123
  ```

---

### 7. **Camera Health Monitoring**

#### `GET /api/cameras/health`
- **Description**: Get health status of all cameras
- **Returns**: Health scores, maintenance status, violation counts
- **Health Levels**: Healthy (80-100), Warning (50-79), Critical (<50)
- **Example**:
  ```
  GET http://localhost:8000/api/cameras/health
  ```

#### `PUT /api/camera/{camera_id}/maintenance`
- **Description**: Record maintenance for a camera
- **Updates**: Last maintenance date, resets health score to 100
- **Example**:
  ```
  PUT http://localhost:8000/api/camera/5/maintenance
  ```

---

### 8. **Export Functionality**

#### `GET /api/export/challans-csv`
- **Description**: Export all challans as CSV data
- **Returns**: CSV formatted data with filename
- **Example**:
  ```
  GET http://localhost:8000/api/export/challans-csv
  ```

---

## 🎨 Frontend Utility Functions (utils.js)

### 1. **API Utilities**

All API endpoints wrapped in easy-to-use functions:

```javascript
// User Management
API.getUser(userId)
API.updateUser(userId, data)
API.login(username, password)
API.register(userData)

// Challans
API.getChallans(filters)
API.getChallanDetails(challanId)

// Payments
API.createPayment(challanId, userId, paymentMethod, transactionId)
API.confirmPayment(paymentId)
API.getPayments(filters)

// Appeals
API.createAppeal(challanId, userId, reason)
API.getAppeals(filters)
API.reviewAppeal(appealId, approved, notes)

// Search & Analytics
API.search(query)
API.getDashboard()
API.getCameraHealth()

// Export
API.exportChallansCSV()
```

---

### 2. **Form Validation**

```javascript
// Validators
Validators.email(email)
Validators.phone(phone)
Validators.cnic(cnic)
Validators.vehicleNumber(number)
Validators.required(value)
Validators.minLength(value, length)
Validators.numeric(value)

// Form Validation
const validation = validateForm(formData, {
    email: [
        { validator: 'required', message: 'Email is required' },
        { validator: 'email', message: 'Invalid email' }
    ],
    phone: [
        { validator: 'required' },
        { validator: 'phone' }
    ]
});

if (validation.isValid) {
    // Proceed
} else {
    console.log(validation.errors);
}
```

---

### 3. **Session Management**

```javascript
// Set/Get data
Session.set('key', value)
Session.get('key')
Session.remove('key')
Session.clear()

// User session
Session.setUser(user)
Session.getUser()
Session.isLoggedIn()
Session.logout()
Session.requireAuth() // Redirect to login if not authenticated
```

---

### 4. **Data Formatting**

```javascript
// Currency
Format.currency(2000) // "PKR 2,000"

// Dates
Format.date("2025-12-10T23:00:00") // "Dec 10, 2025"
Format.datetime("2025-12-10T23:00:00") // "Dec 10, 2025, 11:00 PM"
Format.timeAgo("2025-12-10T22:00:00") // "1 hour ago"

// Phone & CNIC
Format.phone("03001234567") // "+92 300 1234567"
Format.cnic("12345-1234567-1") // "12345-1234567-1"

// Status badges
Format.statusBadge("paid") // Colored badge HTML
Format.capitalize("hello") // "Hello"
```

---

### 5. **UI Utilities**

```javascript
// Loading states
UI.showLoading('elementId')
UI.hideLoading('elementId')

// Notifications
UI.toast('Payment successful!', 'success', 3000)
UI.toast('Error occurred', 'error')
UI.toast('Warning message', 'warning')

// Dialogs
UI.confirm('Delete this challan?', onConfirm, onCancel)

// Error handling
UI.showError('errorDiv', 'Invalid input')
UI.clearError('errorDiv')

// Button states
UI.setButtonLoading('submitBtn', true) // Show loading
UI.setButtonLoading('submitBtn', false) // Hide loading
```

---

### 6. **File Upload Utilities**

```javascript
// Validate image
const validation = FileUpload.validateImage(file, 5) // Max 5MB
if (!validation.valid) {
    alert(validation.error);
}

// Preview image
FileUpload.previewImage(file, 'previewImg')
```

---

### 7. **Download Utilities**

```javascript
// Download CSV
Download.csv(csvData, 'challans.csv')

// Download JSON
Download.json(data, 'export.json')
```

---

### 8. **Other Utilities**

```javascript
// Debounce function (useful for search)
const debouncedSearch = debounce((query) => {
    API.search(query);
}, 500);

// Use in input event
searchInput.addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
});
```

---

## 📊 Enhanced Database Models

### New Fields in Existing Models:

**Camera Model:**
- `last_maintenance` - Last maintenance date
- `total_violations` - Total violations recorded
- `health_score` - Camera health (0-100)

**User Model:**
- `phone` - Phone number
- `cnic` - National ID (CNIC)
- `last_login` - Last login timestamp

**Challan Model:**
- `violation_type` - Type of violation (overspeed, red_light, no_helmet, etc.)
- `status` - Challan status (unpaid, paid, appealed, dismissed)
- `user_id` - Associated user ID
- `issued_at` - Issue timestamp
- `paid_at` - Payment timestamp
- `image_url` - Violation image URL
- `description` - Additional description

### New Models:

**Payment Model:**
- Complete payment tracking with transaction IDs
- Payment methods: card, bank_transfer, easypay, jazzcash
- Payment status tracking

**Appeal Model:**
- Appeal submission and tracking
- Review system with notes
- Status: pending, approved, rejected

---

## 🚀 Usage Examples

### Example 1: User Login & Session
```javascript
// Login
const result = await API.login('username', 'password');
if (result.success) {
    Session.setUser(result.user);
    UI.toast('Login successful!', 'success');
    window.location.href = 'index.html';
}
```

### Example 2: Pay a Challan
```javascript
const paymentBtn = document.getElementById('payBtn');

paymentBtn.addEventListener('click', async () => {
    UI.setButtonLoading(paymentBtn, true);
    
    try {
        const payment = await API.createPayment(
            challanId, 
            userId, 
            'jazzcash', 
            transactionId
        );
        
        await API.confirmPayment(payment.payment_id);
        
        UI.toast('Payment successful!', 'success');
        UI.setButtonLoading(paymentBtn, false);
    } catch (error) {
        UI.toast('Payment failed: ' + error.message, 'error');
        UI.setButtonLoading(paymentBtn, false);
    }
});
```

### Example 3: Submit an Appeal
```javascript
const appealForm = document.getElementById('appealForm');

appealForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const reason = formData.get('reason');
    
    // Validate
    const validation = validateForm({ reason }, {
        reason: [
            { validator: 'required', message: 'Reason is required' },
            { validator: 'minLength', length: 20, message: 'Reason must be at least 20 characters' }
        ]
    });
    
    if (!validation.isValid) {
        UI.showError('appealError', validation.errors.reason);
        return;
    }
    
    try {
        await API.createAppeal(challanId, userId, reason);
        UI.toast('Appeal submitted successfully!', 'success');
        appealForm.reset();
    } catch (error) {
        UI.toast('Failed to submit appeal', 'error');
    }
});
```

### Example 4: Search Functionality
```javascript
const searchInput = document.getElementById('search');
const resultsDiv = document.getElementById('results');

const performSearch = debounce(async (query) => {
    if (query.length < 2) return;
    
    UI.showLoading(resultsDiv);
    
    try {
        const results = await API.search(query);
        
        let html = '';
        
        if (results.vehicles.length > 0) {
            html += '<h3>Vehicles</h3>';
            results.vehicles.forEach(v => {
                html += `<div>${v.vehicle} - ${v.total_challans} challans</div>`;
            });
        }
        
        if (results.cameras.length > 0) {
            html += '<h3>Cameras</h3>';
            results.cameras.forEach(c => {
                html += `<div>${c.address} - ${c.status}</div>`;
            });
        }
        
        resultsDiv.innerHTML = html || 'No results found';
    } catch (error) {
        UI.showError(resultsDiv, 'Search failed');
    }
}, 300);

searchInput.addEventListener('input', (e) => {
    performSearch(e.target.value);
});
```

---

## ✅ Summary

### Backend Functions Added: **15+**
1. User profile GET/PUT
2. Challan filtering & details
3. Payment creation/confirmation/history
4. Appeal submission/review/listing
5. Enhanced dashboard analytics
6. Universal search
7. Camera health monitoring
8. Maintenance recording
9. CSV export

### Frontend Utilities Added: **40+**
1. Complete API wrapper functions
2. Form validators (email, phone, CNIC, vehicle, etc.)
3. Session management
4. Data formatters (currency, date, time, phone, etc.)
5. UI helpers (toast, loading, errors, etc.)
6. File upload utilities
7. Download helpers (CSV, JSON)
8. Debounce utility

### Enhanced Models: **3**
1. Enhanced Camera, User, and Challan models
2. New Payment model
3. New Appeal model

---

## 🎯 Next Steps

To use these functions:

1. **Include utils.js** in your HTML files:
   ```html
   <script src="utils.js"></script>
   ```

2. **Restart the backend** to apply new models:
   ```bash
   cd backend
   python main.py
   ```

3. **Use the utilities** in your frontend code as shown in examples above

---

## 📞 Support

All functions are designed to work seamlessly with your existing E-Challan system. Each function includes error handling and returns consistent data structures.

**Happy Coding! 🚀**
