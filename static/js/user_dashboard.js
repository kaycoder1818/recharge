import { API_BASE_URL } from './config.js';

const stationCard = document.getElementById('stationCard');
const modal = document.getElementById('stationModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const currentStation = document.getElementById('current-station');
const stationMessage = document.getElementById('station-message');

// Get all station buttons
const stationButtons = document.querySelectorAll('.station-button');

async function fetchBottleSummary() {
    try {
        const userEmail = localStorage.getItem('userEmail');
        if (!userEmail || localStorage.getItem('isAuthenticated') !== 'true') {
            console.error('Not authenticated');
            window.location.replace('index.html');
            return;
        }

        const response = await fetch(`${API_BASE_URL}/user/bottle-history`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: userEmail })
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        const history = data.bottleHistory || [];

        // Sum up all bottleCount values (ensure they are numbers)
        const totalBottles = history.reduce((sum, entry) => sum + parseInt(entry.bottleCount), 0);

        // Assuming 1 point per bottle
        const totalPoints = totalBottles * 1;

        // Update DOM elements
        document.getElementById('total-bottles').textContent = totalBottles.toLocaleString();
        document.getElementById('total-points').textContent = totalPoints.toLocaleString();

        // Update user name in dashboard
        const userName = localStorage.getItem('userName');
        if (userName) {
            document.getElementById('user-name').textContent = userName;
        }

    } catch (error) {
        console.error('Failed to fetch bottle summary:', error);
        document.getElementById('total-bottles').textContent = '0';
        document.getElementById('total-points').textContent = '0';
    }
}

// Function to update selected state
function updateSelectedState(selectedStation) {
    stationButtons.forEach(btn => {
        if (btn.dataset.station === selectedStation) {
            btn.classList.add('selected');
        } else {
            btn.classList.remove('selected');
        }
    });
}

// Function to save station to localStorage
function saveStationToStorage(station) {
    localStorage.setItem('selectedStation', station);
}

// Function to get station from localStorage
function getStationFromStorage() {
    return localStorage.getItem('selectedStation');
}

// Add click handlers to all station buttons
stationButtons.forEach(button => {
    button.addEventListener('click', () => {
        const station = button.dataset.station;
        selectStation(station);
    });
});

function openModal() {
    modal.style.display = 'flex';
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.classList.remove('active');
    setTimeout(() => {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }, 300);
}

// Add click event to station card for both mobile and desktop
stationCard.addEventListener('click', openModal);
closeModalBtn.addEventListener('click', closeModal);

// Close modal when clicking outside
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Handle touch events for mobile
let touchStartY = 0;
let touchEndY = 0;
const modalContent = modal.querySelector('.modal-content');

modal.addEventListener('touchstart', (e) => {
    if (e.target === modal || e.target.closest('.modal-drag-indicator')) {
        touchStartY = e.touches[0].clientY;
        modalContent.style.transition = 'none';
    }
});

modal.addEventListener('touchmove', (e) => {
    if (touchStartY > 0) {
        touchEndY = e.touches[0].clientY;
        const swipeDistance = touchEndY - touchStartY;
        
        if (swipeDistance > 0) {
            modalContent.style.transform = `translateY(${swipeDistance}px)`;
            e.preventDefault();
        }
    }
});

modal.addEventListener('touchend', (e) => {
    if (touchStartY > 0) {
        const swipeDistance = touchEndY - touchStartY;
        modalContent.style.transition = 'transform 0.3s ease-out';
        
        if (swipeDistance > 100) {
            closeModal();
        } else {
            modalContent.style.transform = '';
        }
        
        touchStartY = 0;
        touchEndY = 0;
    }
});

function selectStation(station) {
    currentStation.textContent = station;
    stationMessage.textContent = `You have selected: ${station}`;
    
    // Save to localStorage
    saveStationToStorage(station);
    
    // Update selected state
    updateSelectedState(station);
    
    // Show insert bottle button
    document.getElementById('insert-bottle-container').style.display = 'block';
    
    closeModal();
}

// Add insert bottle functionality
document.getElementById('insert-bottle-btn').addEventListener('click', async () => {
    try {
        const userEmail = localStorage.getItem('userEmail');
        const selectedStation = localStorage.getItem('selectedStation');
        
        if (!userEmail || !selectedStation) {
            alert('Please select a station first');
            return;
        }

        const response = await fetch(`${API_BASE_URL}/user/insert-bottle`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: userEmail,
                station: selectedStation,
                bottleCount: 1
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        // Refresh the bottle summary to update counts
        await fetchBottleSummary();
        
        // Show success message
        alert('Bottle inserted successfully!');
        
    } catch (error) {
        console.error('Failed to insert bottle:', error);
        alert('Failed to insert bottle. Please try again.');
    }
});

// Initialize data when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const token = localStorage.getItem('isAuthenticated');
    if (!token) {
        window.location.replace('index.html');
        return;
    }

    // Initialize selected station
    const savedStation = getStationFromStorage();
    if (savedStation) {
        currentStation.textContent = savedStation;
        updateSelectedState(savedStation);
        stationMessage.textContent = `You have selected: ${savedStation}`;
        // Show insert bottle button if station is selected
        document.getElementById('insert-bottle-container').style.display = 'block';
    }
    
    // Add click event to current-station span for mobile
    const currentStationSpan = document.getElementById('current-station');
    if (currentStationSpan) {
        currentStationSpan.addEventListener('click', openModal);
    }

    // Fetch initial bottle summary
    fetchBottleSummary();

    // Refresh bottle summary every 5 minutes
    setInterval(fetchBottleSummary, 5 * 60 * 1000);

    // Points calculation and display
    function updatePoints(bottleCount) {
        // Calculate points (1 bottle = 10 points)
        const points = bottleCount * 10;
        document.getElementById('total-points').textContent = points;
    }

    // Update points when bottle count changes
    const totalBottles = document.getElementById('total-bottles');
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'characterData' || mutation.type === 'childList') {
                const bottleCount = parseInt(totalBottles.textContent) || 0;
                updatePoints(bottleCount);
            }
        });
    });

    observer.observe(totalBottles, {
        characterData: true,
        childList: true,
        subtree: true
    });

    // Initialize points
    updatePoints(parseInt(totalBottles.textContent) || 0);
});

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
    }
});
