// Initialize map centered on Lahore
const map = L.map('map').setView([31.5204, 74.3587], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Custom icon for cameras
// Custom Icons
const activeIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const inactiveIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

async function loadCameras() {
    try {
        const response = await fetch('http://localhost:8000/api/cameras');
        const cameras = await response.json();

        // Update total count
        const totalElement = document.getElementById('totalCameras');
        if (totalElement) {
            totalElement.innerText = cameras.length;
        }

        cameras.forEach(cam => {
            const markerIcon = cam.status === 'active' ? activeIcon : inactiveIcon;

            const marker = L.marker([cam.lat, cam.lng], {
                icon: markerIcon
            }).addTo(map);

            // Add click event to show details
            marker.on('click', () => {
                showCameraDetails(cam);
            });

            marker.bindPopup(`
                <div style="min-width: 150px">
                    <h3 style="margin: 0 0 5px 0; color: #3b82f6">${cam.location || cam.address}</h3>
                    <p style="margin: 0 0 5px 0">Status: <strong style="color: ${cam.status === 'active' ? '#10b981' : '#ef4444'}">${cam.status.toUpperCase()}</strong></p>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <span>Traffic Light:</span>
                        <span style="width: 12px; height: 12px; border-radius: 50%; background-color: ${cam.light_status || 'gray'}; border: 1px solid #fff;"></span>
                        <span style="text-transform: capitalize;">${cam.light_status || 'Unknown'}</span>
                    </div>
                </div>
            `);
        });
    } catch (error) {
        console.error("Error loading cameras:", error);
    }
}

let routingControl = null;

// Simulated user location (e.g., somewhere in Lahore)
const userLocation = [31.5600, 74.3100];

function showCameraDetails(cam) {
    const detailsDiv = document.getElementById('cameraInfo');

    // Mock some data for "working details"
    const uptime = Math.floor(Math.random() * 24) + 1;
    const violations = Math.floor(Math.random() * 50);
    const lastMaint = new Date(Date.now() - Math.floor(Math.random() * 10000000000)).toLocaleDateString();
    const statusClass = cam.status === 'active' ? 'status-active' : 'status-offline';
    const lightColor = cam.light_status || 'gray';

    detailsDiv.innerHTML = `
        <h3 style="margin-bottom: 1rem; color: #3b82f6">${cam.location}</h3>
        
        <div class="info-row">
            <span class="info-label">Camera ID</span>
            <span class="info-value">#${cam.id}</span>
        </div>
        
        <div class="info-row">
            <span class="info-label">Status</span>
            <span class="status-badge ${statusClass}">${cam.status.toUpperCase()}</span>
        </div>

        <div class="info-row">
            <span class="info-label">Traffic Light</span>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="width: 16px; height: 16px; border-radius: 50%; background-color: ${lightColor}; box-shadow: 0 0 10px ${lightColor};"></span>
                <span class="info-value" style="text-transform: capitalize;">${lightColor}</span>
            </div>
        </div>

        <div class="info-row">
            <span class="info-label">Speed Limit</span>
            <span class="info-value" style="color: #f59e0b; font-weight: bold;">${cam.speed_limit || 60} km/h</span>
        </div>
        
        <div class="info-row">
            <span class="info-label">Coordinates</span>
            <span class="info-value">${cam.lat.toFixed(4)}, ${cam.lng.toFixed(4)}</span>
        </div>

        <div class="info-row">
            <span class="info-label">Uptime</span>
            <span class="info-value">${uptime} Hours</span>
        </div>

        <div class="info-row">
            <span class="info-label">Violations Today</span>
            <span class="info-value">${violations}</span>
        </div>

        <div class="info-row">
            <span class="info-label">Last Maintenance</span>
            <span class="info-value">${lastMaint}</span>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 0.5rem; border: 1px solid rgba(59, 130, 246, 0.2);">
            <h4 style="margin-bottom: 0.5rem; font-size: 0.9rem">Live Feed Status</h4>
            <div style="display: flex; align-items: center; gap: 0.5rem; color: #34d399; font-size: 0.9rem">
                <span style="width: 8px; height: 8px; background: #34d399; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #34d399;"></span>
                Signal Strong (1080p)
            </div>
        </div>

        <button onclick="getDirections(${cam.lat}, ${cam.lng})" class="btn-primary" style="width: 100%; margin-top: 1.5rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/>
            </svg>
            Get Directions
        </button>
    `;
}

function getDirections(lat, lng) {
    // Remove existing routing control if any
    if (routingControl) {
        map.removeControl(routingControl);
    }

    // Add user marker if not already there (optional, but good for context)
    L.marker(userLocation).addTo(map).bindPopup("Your Location").openPopup();

    // Create new routing control
    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(userLocation[0], userLocation[1]),
            L.latLng(lat, lng)
        ],
        routeWhileDragging: true,
        lineOptions: {
            styles: [{ color: '#3b82f6', opacity: 0.7, weight: 5 }]
        },
        createMarker: function () { return null; } // Don't create default markers, we have our own
    }).addTo(map);
}

loadCameras();

// Activity Feed Simulation
const activities = [
    { type: 'warning', text: 'Signal Violation Detected', icon: '!' },
    { type: 'info', text: 'Routine Maintenance Check', icon: '✓' },
    { type: 'warning', text: 'Speed Limit Exceeded', icon: '⚡' },
    { type: 'info', text: 'Camera Online', icon: '•' },
    { type: 'warning', text: 'Unregistered Vehicle', icon: '?' }
];

const locations = ['Mall Road', 'Jail Road', 'Ferozepur Road', 'Liberty Market', 'Fort Road'];

function addActivity() {
    const feed = document.getElementById('activityFeed');
    const activity = activities[Math.floor(Math.random() * activities.length)];
    const location = locations[Math.floor(Math.random() * locations.length)];

    const item = document.createElement('div');
    item.className = 'activity-item';
    item.innerHTML = `
        <div class="activity-icon ${activity.type}">${activity.icon}</div>
        <div class="activity-content">
            <p class="activity-text">${activity.text}</p>
            <p class="activity-meta">${location} • Just now</p>
        </div>
    `;

    feed.insertBefore(item, feed.firstChild);

    // Keep only last 10 items
    if (feed.children.length > 10) {
        feed.removeChild(feed.lastChild);
    }
}

// Simulate activity every 3-7 seconds
setInterval(addActivity, 5000);

// Stats Simulation
let stats = {
    violations: 124,
    revenue: 248000
};

function updateStats() {
    document.getElementById('totalViolations').innerText = stats.violations.toLocaleString();
    document.getElementById('totalRevenue').innerText = `PKR ${stats.revenue.toLocaleString()}`;
}

// Simulate random violations
setInterval(() => {
    if (Math.random() > 0.7) {
        stats.violations++;
        stats.revenue += 2000; // 2000 PKR per challan
        updateStats();

        // Add to activity feed
        const feed = document.getElementById('activityFeed');
        const item = document.createElement('div');
        item.className = 'activity-item';
        item.innerHTML = `
            <div class="activity-icon warning">!</div>
            <div class="activity-content">
                <p class="activity-text">New Challan Issued</p>
                <p class="activity-meta">Automated • Just now</p>
            </div>
        `;
        feed.insertBefore(item, feed.firstChild);
        if (feed.children.length > 10) feed.removeChild(feed.lastChild);
    }
}, 3000);

async function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    const resultElement = document.getElementById("result");

    if (!fileInput.files.length) {
        alert("Please select a file first");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    resultElement.innerText = "Processing...";
    resultElement.style.color = "var(--text-muted)";

    try {
        const res = await fetch("http://localhost:8000/predict", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error('Prediction failed');

        const data = await res.json();

        // Simulate a result if the model returns "Unknown" or similar for demo
        let prediction = data.prediction;

        resultElement.innerText = `Result: ${prediction}`;

        if (prediction.toLowerCase().includes("violation") || prediction.toLowerCase().includes("helmet") || prediction.toLowerCase().includes("speed")) {
            resultElement.style.color = "#ef4444";
            stats.violations++;
            stats.revenue += 2000;
            updateStats();

            let msg = `Violation Detected: ${prediction}. Challan of PKR 2000 issued.`;

            if (prediction.toLowerCase().includes("speed")) {
                msg = `Over Speed Detected! Please Slow Speed. Challan Issued.`;
            }

            showNotification(msg, 'warning');
            // speak(msg); // showNotification already handles speaking
        } else {
            resultElement.style.color = "#10b981";
            speak(`No violation detected: ${prediction}`);
        }

    } catch (error) {
        console.error("Error:", error);
        resultElement.innerText = "Error processing image";
        resultElement.style.color = "#ef4444";
    }
}

// Initial stats update
updateStats();

const cityCoordinates = {
    'pakistan': { lat: 30.3753, lng: 69.3451, zoom: 6 },
    'karachi': { lat: 24.8607, lng: 67.0011, zoom: 12 },
    'lahore': { lat: 31.5204, lng: 74.3587, zoom: 12 },
    'islamabad': { lat: 33.6844, lng: 73.0479, zoom: 12 },
    'peshawar': { lat: 34.0151, lng: 71.5249, zoom: 12 },
    'quetta': { lat: 30.1798, lng: 66.9750, zoom: 12 }
};

function jumpToCity(city) {
    const coords = cityCoordinates[city];
    if (coords) {
        map.flyTo([coords.lat, coords.lng], coords.zoom, {
            duration: 1.5
        });
    }
}

// Map Legend
const legend = L.control({ position: 'bottomright' });

legend.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'info legend');
    div.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    div.style.padding = '10px';
    div.style.borderRadius = '8px';
    div.style.color = 'white';
    div.style.border = '1px solid #333';

    div.innerHTML = `
        <h4 style="margin: 0 0 10px 0; font-size: 14px; border-bottom: 1px solid #555; padding-bottom: 5px;">Map Key</h4>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 5px;">
            <img src="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png" width="15" height="25">
            <span style="font-size: 12px;">Active Camera</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <img src="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png" width="15" height="25">
            <span style="font-size: 12px;">Inactive Camera</span>
        </div>
    `;
    return div;
};

legend.addTo(map);

// Theme Toggle Logic
let isLightMode = false;
const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
});

// We need to keep a reference to the tile layer to change it if needed
// Actually, for this demo, we can just use CSS filters or swap the URL if we had a dark tile provider.
// Standard OSM is light. Let's try to use a dark filter for dark mode if possible, or just stick to OSM.
// A simple way to make OSM look "dark" is using CSS filter on the map pane.

function toggleTheme() {
    isLightMode = !isLightMode;
    document.body.classList.toggle('light-mode');

    const btn = document.getElementById('themeToggle');
    if (isLightMode) {
        btn.innerText = '🌙 Dark Mode';
        btn.style.background = 'rgba(0,0,0,0.1)';
        // Optional: Change map tiles to a lighter style if we were using dark tiles
        // For now, OSM is already light, so it fits Light Mode perfectly.
        document.querySelector('.leaflet-tile-pane').style.filter = 'none';
    } else {
        btn.innerText = '☀️ Light Mode';
        btn.style.background = 'transparent';
        // Dark Mode: Invert map colors to simulate dark mode
        document.querySelector('.leaflet-tile-pane').style.filter = 'invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%)';
    }
}

// Initialize Dark Mode Map Style
// Since default is dark mode, apply the filter initially
document.addEventListener('DOMContentLoaded', () => {
    // Wait for map to load
    setTimeout(() => {
        const tilePane = document.querySelector('.leaflet-tile-pane');
        if (tilePane) {
            tilePane.style.filter = 'invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%)';
        }
    }, 1000);
});

// Store all cameras globally for filtering
let allCameras = [];
let allMarkers = [];
let currentFilter = 'all';

// Update loadCameras to store data
const originalLoadCameras = loadCameras;
loadCameras = async function () {
    try {
        const response = await fetch('http://localhost:8000/api/cameras');
        const cameras = await response.json();

        allCameras = cameras; // Store globally
        allMarkers = []; // Reset markers

        // Update total count
        const totalElement = document.getElementById('totalCameras');
        if (totalElement) {
            totalElement.innerText = cameras.length;
        }

        cameras.forEach(cam => {
            const markerIcon = cam.status === 'active' ? activeIcon : inactiveIcon;

            const marker = L.marker([cam.lat, cam.lng], {
                icon: markerIcon
            }).addTo(map);

            marker.cameraData = cam; // Store camera data on marker
            allMarkers.push(marker); // Store marker reference

            marker.on('click', () => {
                showCameraDetails(cam);
            });

            marker.bindPopup(`
                <div style="min-width: 150px">
                    <h3 style="margin: 0 0 5px 0; color: #3b82f6">${cam.location || cam.address}</h3>
                    <p style="margin: 0 0 5px 0">Status: <strong style="color: ${cam.status === 'active' ? '#10b981' : '#ef4444'}">${cam.status.toUpperCase()}</strong></p>
                    <div style="display: flex; align-items: center; gap: 5px;">
                        <span>Traffic Light:</span>
                        <span style="width: 12px; height: 12px; border-radius: 50%; background-color: ${cam.light_status || 'gray'}; border: 1px solid #fff;"></span>
                        <span style="text-transform: capitalize;">${cam.light_status || 'Unknown'}</span>
                    </div>
                </div>
            `);
        });
    } catch (error) {
        console.error("Error loading cameras:", error);
    }
};

// Search Cameras
function searchCameras(query) {
    query = query.toLowerCase();

    allMarkers.forEach(marker => {
        const cam = marker.cameraData;
        const address = (cam.address || cam.location || '').toLowerCase();
        const id = String(cam.id).toLowerCase();

        if (address.includes(query) || id.includes(query)) {
            marker.setOpacity(1);
        } else {
            marker.setOpacity(0.2);
        }
    });
}

// Filter Cameras
function filterCameras(status) {
    currentFilter = status;

    // Update button states
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`filter${status.charAt(0).toUpperCase() + status.slice(1)}`).classList.add('active');

    allMarkers.forEach(marker => {
        const cam = marker.cameraData;

        if (status === 'all' || cam.status === status) {
            marker.setOpacity(1);
            marker.addTo(map);
        } else {
            marker.setOpacity(0);
            map.removeLayer(marker);
        }
    });
}

// Heatmap View
let heatmapLayer = null;
function showHeatmap() {
    alert('📊 Heatmap Feature\n\nThis would show violation density heatmap.\n\nNote: Requires leaflet-heat plugin for full implementation.\n\nCurrent demo shows marker clustering instead.');

    // Simple demo: zoom to show all cameras
    map.setView([30.3753, 69.3451], 6);
}

// Export Report as CSV
function exportReport() {
    let csv = 'Camera ID,Address,Status,Traffic Light,Speed Limit,Latitude,Longitude\n';

    allCameras.forEach(cam => {
        csv += `${cam.id},"${cam.address}",${cam.status},${cam.light_status},${cam.speed_limit},${cam.lat},${cam.lng}\n`;
    });

    // Create download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `e-challan-report-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    alert('📥 Report Downloaded!\n\nCamera data exported to CSV file.');
}

// Real-time Notifications
function showNotification(message, type = 'info') {
    const notif = document.createElement('div');
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'warning' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notif.innerText = message;
    document.body.appendChild(notif);

    // Speak the notification if voice is enabled
    if (type === 'warning') {
        speak(`Alert: ${message}`);
    } else {
        speak(message);
    }

    setTimeout(() => {
        notif.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => document.body.removeChild(notif), 300);
    }, 3000);
}

// Voice Alert Logic
let voiceEnabled = false;
const synth = window.speechSynthesis;

function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    const btn = document.getElementById('voiceToggle');

    if (voiceEnabled) {
        btn.innerText = '🔊 Voice On';
        btn.style.background = 'rgba(16, 185, 129, 0.2)';
        btn.style.borderColor = '#10b981';
        speak("Voice alerts enabled");
    } else {
        btn.innerText = '🔇 Voice Off';
        btn.style.background = 'transparent';
        btn.style.borderColor = 'var(--border-color)';
        synth.cancel(); // Stop speaking immediately
    }
}

function speak(text) {
    if (!voiceEnabled) return;
    if (synth.speaking) {
        // Optional: cancel previous or queue? For alerts, usually we want immediate feedback, 
        // but maybe not cutting off the previous one instantly if it's important.
        // Let's just let it queue naturally or cancel if it's too much.
        // For now, let's just let it play.
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
    synth.speak(utterance);
}

// Simulate random notifications
setInterval(() => {
    if (Math.random() > 0.8) {
        const messages = [
            'New challan issued in Karachi',
            'Over Speed Detected - Mall Road. Slow Speed!',
            'Camera maintenance scheduled',
            'High traffic detected - Jail Road'
        ];
        // Only speak warnings or important updates to avoid annoyance
        const msg = messages[Math.floor(Math.random() * messages.length)];
        const type = msg.includes('maintenance') ? 'info' : 'warning';
        showNotification(msg, type);
    }
}, 15000);