import { API_BASE_URL } from './config.js';

// Function to show notifications
function showNotification(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        document.body.appendChild(notification);
    }

    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';

    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Function to validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Function to validate password
function isValidPassword(password) {
    return password.length >= 6; // Minimum 6 characters
}

// Function to get correct page for role
function getPageForRole(role) {
    switch(role?.toLowerCase()) {
        case 'admin':
            return '/admin-dashboard';
        case 'superadmin':
            return '/superadmin-dashboard';
        case 'user':
        default:
            return '/user-dashboard';
    }
}

// Function to check if current page matches role
function isOnCorrectPage(role) {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const correctPage = getPageForRole(role);
    return currentPage === correctPage;
}

// Function to handle role-based redirection
function redirectBasedOnRole(role) {
    if (isOnCorrectPage(role)) {
        console.log('Already on correct page for role:', role);
        return;
    }

    const targetPage = getPageForRole(role);
    console.log(`Redirecting to ${targetPage} for role ${role}`);
    window.location.replace(targetPage);
}

// Function to handle login
async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    // Validate inputs
    if (!email || !password) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }

    if (!isValidPassword(password)) {
        showNotification('Password must be at least 6 characters long', 'error');
        return;
    }

    try {
        console.log('Attempting login...');

        const loginData = {
            email: email,
            passwordHash: password // Note: Backend will handle password hashing
        };

        const response = await fetch(`${API_BASE_URL}/auth/login/email`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        const data = await response.json();
        console.log('Login response:', data);

        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }

        if (data.message !== 'Successful') {
            throw new Error('Login failed: ' + (data.message || 'Unknown error'));
        }

        // Store user session data
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('userEmail', email);
        localStorage.setItem('userRole', data.role || 'user');
        localStorage.setItem('lastLogin', data.timestamp || new Date().toISOString());

        console.log('Session state:', {
            isAuthenticated: localStorage.getItem('isAuthenticated'),
            email: localStorage.getItem('userEmail'),
            role: localStorage.getItem('userRole'),
            lastLogin: localStorage.getItem('lastLogin')
        });

        showNotification('Login successful! Redirecting...', 'success');

        // Redirect based on user role after a short delay
        setTimeout(() => {
            redirectBasedOnRole(data.role || 'user');
        }, 1500);

    } catch (error) {
        console.error('Login error:', error);
        showNotification(error.message || 'Login failed. Please try again.', 'error');
    }
}

// Function to check if user is already logged in
function checkAuthStatus() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
    const userRole = localStorage.getItem('userRole');

    console.log('Auth check:', { currentPage, isAuthenticated, userRole });

    // Public pages (no auth needed)
    const publicPages = ['index.html', 'register.html', ''];
    
    if (isAuthenticated) {
        // If authenticated and on a public page, redirect to dashboard
        if (publicPages.includes(currentPage)) {
            redirectBasedOnRole(userRole);
            return;
        }
        
        // If authenticated but on wrong dashboard, redirect to correct one
        if (!isOnCorrectPage(userRole)) {
            redirectBasedOnRole(userRole);
            return;
        }
    } else {
        // If not authenticated and not on a public page, redirect to login
        if (!publicPages.includes(currentPage)) {
            console.log('Not authenticated, redirecting to login');
            window.location.replace('index.html');
            return;
        }
    }
}

// Function to handle logout
function handleLogout(e) {
    if (e) e.preventDefault();
    console.log('Logout initiated');
    
    // Clear all authentication data
    localStorage.clear();
    sessionStorage.clear();
    
    console.log('Storage cleared');

    // Redirect to login page
    window.location.replace('index.html');
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded - Setting up auth listeners');
    
    // Check if user is already logged in
    checkAuthStatus();

    // Add login form submit handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Add logout button handler - check for both IDs used in different pages
    const logoutBtns = document.querySelectorAll('#logout_btn, #logout');
    console.log('Found logout buttons:', logoutBtns.length);
    
    logoutBtns.forEach(btn => {
        btn.addEventListener('click', handleLogout);
    });
}); 