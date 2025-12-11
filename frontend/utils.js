// ==================== API UTILITIES ====================

const API_BASE_URL = 'http://localhost:8000';

// Generic API call wrapper with error handling
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, defaultOptions);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// API Helper Functions
const API = {
    // User Management
    getUser: (userId) => apiCall(`/api/user/${userId}`),
    updateUser: (userId, data) => apiCall(`/api/user/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    }),

    // Authentication
    login: (username, password) => apiCall('/api/login', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    }),
    register: (userData) => apiCall('/api/register', {
        method: 'POST',
        body: JSON.stringify(userData)
    }),

    // Challans
    getChallans: (filters = {}) => {
        const params = new URLSearchParams(filters);
        return apiCall(`/api/challans?${params}`);
    },
    getChallanDetails: (challanId) => apiCall(`/api/challan/${challanId}`),

    // Payments
    createPayment: (challanId, userId, paymentMethod, transactionId) =>
        apiCall('/api/payment', {
            method: 'POST',
            body: JSON.stringify({ challan_id: challanId, user_id: userId, payment_method: paymentMethod, transaction_id: transactionId })
        }),
    confirmPayment: (paymentId) => apiCall(`/api/payment/${paymentId}/confirm`, {
        method: 'PUT'
    }),
    getPayments: (filters = {}) => {
        const params = new URLSearchParams(filters);
        return apiCall(`/api/payments?${params}`);
    },

    // Appeals
    createAppeal: (challanId, userId, reason) =>
        apiCall('/api/appeal', {
            method: 'POST',
            body: JSON.stringify({ challan_id: challanId, user_id: userId, reason })
        }),
    getAppeals: (filters = {}) => {
        const params = new URLSearchParams(filters);
        return apiCall(`/api/appeals?${params}`);
    },
    reviewAppeal: (appealId, approved, notes) =>
        apiCall(`/api/appeal/${appealId}/review`, {
            method: 'PUT',
            body: JSON.stringify({ approved, reviewer_notes: notes })
        }),

    // Search
    search: (query) => apiCall(`/api/search?query=${encodeURIComponent(query)}`),

    // Analytics
    getDashboard: () => apiCall('/api/analytics/dashboard'),
    getCameraHealth: () => apiCall('/api/cameras/health'),

    // Cameras
    getCameras: () => apiCall('/api/cameras'),

    // Export
    exportChallansCSV: () => apiCall('/api/export/challans-csv')
};

// ==================== FORM VALIDATION ====================

const Validators = {
    email: (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },

    phone: (phone) => {
        // Pakistan phone number format
        const regex = /^(\+92|0)?[0-9]{10}$/;
        return regex.test(phone.replace(/[\s-]/g, ''));
    },

    cnic: (cnic) => {
        // Pakistan CNIC format: 12345-1234567-1
        const regex = /^[0-9]{5}-[0-9]{7}-[0-9]$/;
        return regex.test(cnic);
    },

    vehicleNumber: (number) => {
        // Pakistan vehicle number format
        const regex = /^[A-Z]{2,3}-[0-9]{2,4}$/i;
        return regex.test(number);
    },

    required: (value) => {
        return value !== null && value !== undefined && value.trim() !== '';
    },

    minLength: (value, length) => {
        return value.length >= length;
    },

    maxLength: (value, length) => {
        return value.length <= length;
    },

    numeric: (value) => {
        return !isNaN(value) && !isNaN(parseFloat(value));
    }
};

// Form validation helper
function validateForm(formData, rules) {
    const errors = {};

    for (const field in rules) {
        const value = formData[field];
        const fieldRules = rules[field];

        for (const rule of fieldRules) {
            if (rule.validator === 'required' && !Validators.required(value)) {
                errors[field] = rule.message || 'This field is required';
                break;
            }

            if (rule.validator === 'email' && !Validators.email(value)) {
                errors[field] = rule.message || 'Invalid email format';
                break;
            }

            if (rule.validator === 'phone' && !Validators.phone(value)) {
                errors[field] = rule.message || 'Invalid phone number';
                break;
            }

            if (rule.validator === 'cnic' && !Validators.cnic(value)) {
                errors[field] = rule.message || 'Invalid CNIC format (12345-1234567-1)';
                break;
            }

            if (rule.validator === 'vehicleNumber' && !Validators.vehicleNumber(value)) {
                errors[field] = rule.message || 'Invalid vehicle number format';
                break;
            }

            if (rule.validator === 'minLength' && !Validators.minLength(value, rule.length)) {
                errors[field] = rule.message || `Minimum ${rule.length} characters required`;
                break;
            }
        }
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
}

// ==================== SESSION MANAGEMENT ====================

const Session = {
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },

    get: (key) => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    },

    remove: (key) => {
        localStorage.removeItem(key);
    },

    clear: () => {
        localStorage.clear();
    },

    // User session helpers
    setUser: (user) => Session.set('user', user),
    getUser: () => Session.get('user'),
    isLoggedIn: () => Session.get('user') !== null,
    logout: () => {
        Session.remove('user');
        window.location.href = 'login.html';
    },

    requireAuth: () => {
        if (!Session.isLoggedIn()) {
            window.location.href = 'login.html';
        }
    }
};

// ==================== DATA FORMATTING ====================

const Format = {
    // Format currency in PKR
    currency: (amount) => {
        return `PKR ${amount.toLocaleString('en-PK', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    },

    // Format date
    date: (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-PK', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Format datetime
    datetime: (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString('en-PK', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Format time ago
    timeAgo: (dateString) => {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        const now = new Date();
        const seconds = Math.floor((now - date) / 1000);

        if (seconds < 60) return 'Just now';
        if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
        if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
        if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;

        return Format.date(dateString);
    },

    // Format phone number
    phone: (phone) => {
        if (!phone) return 'N/A';
        // Format as: +92 300 1234567
        const cleaned = phone.replace(/\D/g, '');
        if (cleaned.length === 11 && cleaned.startsWith('0')) {
            return `+92 ${cleaned.substring(1, 4)} ${cleaned.substring(4)}`;
        }
        return phone;
    },

    // Format CNIC
    cnic: (cnic) => {
        if (!cnic) return 'N/A';
        return cnic;
    },

    // Capitalize first letter
    capitalize: (str) => {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    },

    // Format status badge
    statusBadge: (status) => {
        const statusColors = {
            'paid': 'success',
            'unpaid': 'warning',
            'appealed': 'info',
            'dismissed': 'secondary',
            'active': 'success',
            'inactive': 'danger',
            'pending': 'warning',
            'completed': 'success',
            'failed': 'danger',
            'approved': 'success',
            'rejected': 'danger'
        };

        const colorClass = statusColors[status] || 'secondary';
        return `<span class="badge badge-${colorClass}">${Format.capitalize(status)}</span>`;
    }
};

// ==================== UI UTILITIES ====================

const UI = {
    // Show loading spinner
    showLoading: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.innerHTML = '<div class="spinner">Loading...</div>';
        }
    },

    // Hide loading spinner
    hideLoading: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.innerHTML = '';
        }
    },

    // Show toast notification
    toast: (message, type = 'info', duration = 3000) => {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
            color: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
            font-size: 0.9rem;
        `;
        toast.innerText = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, duration);
    },

    // Show confirmation dialog
    confirm: (message, onConfirm, onCancel) => {
        if (window.confirm(message)) {
            if (onConfirm) onConfirm();
        } else {
            if (onCancel) onCancel();
        }
    },

    // Show error message
    showError: (element, message) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.innerHTML = `<div class="error-message">${message}</div>`;
            element.style.color = '#ef4444';
        }
    },

    // Clear error message
    clearError: (element) => {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        if (element) {
            element.innerHTML = '';
        }
    },

    // Disable button with loading state
    setButtonLoading: (button, loading = true) => {
        if (typeof button === 'string') {
            button = document.getElementById(button);
        }
        if (button) {
            if (loading) {
                button.disabled = true;
                button.dataset.originalText = button.innerText;
                button.innerText = 'Loading...';
            } else {
                button.disabled = false;
                button.innerText = button.dataset.originalText || button.innerText;
            }
        }
    }
};

// ==================== FILE UPLOAD UTILITIES ====================

const FileUpload = {
    // Validate image file
    validateImage: (file, maxSizeMB = 5) => {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const maxSize = maxSizeMB * 1024 * 1024;

        if (!validTypes.includes(file.type)) {
            return { valid: false, error: 'Please upload a valid image (JPG, PNG)' };
        }

        if (file.size > maxSize) {
            return { valid: false, error: `File size must be less than ${maxSizeMB}MB` };
        }

        return { valid: true };
    },

    // Preview image
    previewImage: (file, imgElement) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (typeof imgElement === 'string') {
                imgElement = document.getElementById(imgElement);
            }
            if (imgElement) {
                imgElement.src = e.target.result;
            }
        };
        reader.readAsDataURL(file);
    }
};

// ==================== DOWNLOAD UTILITIES ====================

const Download = {
    // Download CSV
    csv: (csvData, filename) => {
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    },

    // Download JSON
    json: (data, filename) => {
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
};

// ==================== DEBOUNCE UTILITY ====================

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== EXPORT ====================

// Make utilities available globally
window.API = API;
window.Validators = Validators;
window.validateForm = validateForm;
window.Session = Session;
window.Format = Format;
window.UI = UI;
window.FileUpload = FileUpload;
window.Download = Download;
window.debounce = debounce;
