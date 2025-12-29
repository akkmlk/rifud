// if conditnion navbar
document.addEventListener('DOMContentLoaded', () => {
    const role = sessionStorage.getItem('role');

    const btnLogout = document.getElementById('btnLogout')
    btnLogout.addEventListener('click', (e) => {
        e.preventDefault()
        sessionStorage.clear()
        window.location.href = '/'
    })

    const btnLogin2 = document.getElementById('btnLogin2')
    const btnProfile1 = document.getElementById('btnProfile1')
    const btnProfile2 = document.getElementById('btnProfile2')

    btnLogin2.classList.remove('hidden')
    btnProfile1.classList.add('hidden')
    // btnProfile2.classList.add('hidden')
    // if (!role) {
    // }

    if (role === 'client') {
        document.getElementById('transaction-menu').classList.remove('hidden')
        document.getElementById('transaction-history-menu').classList.remove('hidden')
        btnProfile1.classList.remove('hidden')
        // btnProfile2.classList.remove('hidden')

        btnLogin2.classList.add('hidden')
    }
    // dropdown profile
    const dropdown = document.getElementById('profile-dropdown-menu')

    btnProfile1.addEventListener('click', () => {
        dropdown.classList.toggle('hidden')
    })

    btnProfile2.addEventListener('click', () => {
        dropdown.classList.toggle('hidden')
    })
})



const filters = {
    lokasi: '',
    tipe: '',
    near_you: false
};

// Ambil data dropdown dari API dan isi dropdown
async function populateDropdowns() {
    try {
        const lokasiResponse = await fetch('/api/lokasi');
        const lokasiData = await lokasiResponse.json();

        const typeResponse = await fetch('/api/type');
        const typeData = await typeResponse.json();

        // Isi dropdown Lokasi
        const lokasiSelect = document.getElementById('lokasi');
        lokasiSelect.innerHTML = '<option value="">Semua Lokasi</option>';
        lokasiData.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id || item.nama;
            option.textContent = item.nama;
            lokasiSelect.appendChild(option);
        });

        // Isi dropdown Tipe
        const typeSelect = document.getElementById('type');
        typeSelect.innerHTML = '<option value="">Semua Tipe</option>';
        typeData.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id || item.nama;
            option.textContent = item.nama;
            typeSelect.appendChild(option);
        });

        // Tambahkan event listener setelah dropdown diisi
        attachEventListeners();

    } catch (err) {
        console.error("Gagal mengambil data dropdown:", err);
    }
}

// Fungsi untuk mengirim filter dan render card
async function applyFilters() {
    const params = new URLSearchParams(filters);
    try {
        const response = await fetch(`/api/foods?${params}`);
        const html = await response.text();  // HTML card-card dari Jinja
        document.getElementById('foodGrid').innerHTML = html;
    } catch (err) {
        console.error('Error:', err);
    }
}

// Fungsi untuk menambahkan event listener ke dropdown
function attachEventListeners() {
    // Event listener untuk select lokasi
    document.getElementById('lokasi').addEventListener('change', (e) => {
        filters.lokasi = e.target.value;
        applyFilters();
    });

    // Event listener untuk select tipe
    document.getElementById('type').addEventListener('change', (e) => {
        filters.tipe = e.target.value;
        applyFilters();
    });

    // Event listener untuk checkbox Near You
    document.getElementById('nearYou').addEventListener('change', (e) => {
        filters.near_you = e.target.checked;
        applyFilters();
    });
}

// Jalankan saat halaman siap
document.addEventListener("DOMContentLoaded", () => {
    populateDropdowns().then(() => {
        applyFilters(); // Load card awal setelah dropdown siap
    });
});




let locations = [];

// Ambil data dari API
async function fetchLocations() {
    try {
        const response = await fetch('/api/locations');
        locations = await response.json();
        renderList(locations);
        addMarkersToMap();
    } catch (error) {
        console.error("Gagal mengambil data lokasi:", error);
    }
}

/* =========================
   Init Leaflet map
   ========================= */
const map = L.map('map').setView([-6.2, 106.85], 11);

// OSM tiles (gratis)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

const markers = {};

// custom icon (optional) — simple colored circle icon
const icon = L.icon({
    iconUrl: 'data:image/svg+xml;utf8,' + encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" fill="#ffcc00" stroke="#d87a00" stroke-width="1.5"/>
        <text x="12" y="15" font-size="10" text-anchor="middle" fill="#a00" font-family="Arial" font-weight="700">S</text>
        </svg>`
    ),
    iconSize: [36, 36],
    iconAnchor: [18, 36],
    popupAnchor: [0, -36]
});

// add markers to map
function addMarkersToMap() {
    locations.forEach(loc => {
        const m = L.marker([loc.lat, loc.lng], { icon }).addTo(map);
        m.bindPopup(`<b>${escapeHtml(loc.name)}</b><br>${escapeHtml(loc.addr)}<br>
        <a target="_blank" href="https://www.google.com/maps/dir/?api=1&destination=${loc.lat},${loc.lng}">Petunjuk Arah</a>
        `);
        markers[loc.id] = m;
    });
}

/* =========================
   Sidebar list
   ========================= */
const listEl = document.getElementById('list');

function renderList(items) {
    listEl.innerHTML = '';
    items.forEach(item => {
        const el = document.createElement('div');
        el.className = 'p-3 border border-gray-100 rounded-lg mb-2 cursor-pointer hover:bg-blue-50 hover:border-blue-100';
        el.innerHTML = `
        <div class="font-bold text-gray-800">${escapeHtml(item.name)}</div>
        <div class="text-sm text-gray-600 mb-2">${escapeHtml(item.addr)}</div>
        <a class="inline-block px-3 py-1 bg-green-500 text-white rounded-md text-sm" data-id="${item.id}">Petunjuk Arah</a>
        `;
        // click whole item -> fly to marker
        el.addEventListener('click', (ev) => {
            // avoid clicking the inner link (petunjuk arah) from firing fly-to
            if (ev.target && ev.target.matches('a')) return;
            const m = markers[item.id];
            if (m) {
                map.flyTo(m.getLatLng(), 15, { duration: 0.6 });
                m.openPopup();
            }
        });

        // petunjuk arah link
        el.querySelector('a').addEventListener('click', (ev) => {
            ev.stopPropagation();
            window.open(`https://www.google.com/maps/dir/?api=1&destination=${item.lat},${item.lng}`, '_blank');
        });

        listEl.appendChild(el);
    });
}

/* =========================
   Simple search
   ========================= */
const q = document.getElementById('q');
const clear = document.getElementById('clear');
q.addEventListener('input', () => {
    const v = q.value.trim().toLowerCase();
    if (!v) {
        renderList(locations);
        for (const id in markers) markers[id].addTo(map);
        return;
    }
    const filtered = locations.filter(l => (l.name + ' ' + l.addr).toLowerCase().includes(v));
    renderList(filtered);
    // only show filtered markers
    for (const id in markers) {
        const show = filtered.some(f => f.id == id);
        if (show) markers[id].addTo(map); else map.removeLayer(markers[id]);
    }
});
clear.addEventListener('click', () => { q.value = ''; q.dispatchEvent(new Event('input')); });

/* =========================
   User location (watchPosition). Browser will prompt for permission.
   NOTE: geolocation requires https (or localhost).
   ========================= */
let userMarker = null;
let userCircle = null;
// Ganti ID ini agar tidak bentrok
const locationStatus = document.getElementById('location-status');

if ('geolocation' in navigator) {
    const opts = { enableHighAccuracy: true, maximumAge: 10000, timeout: 10000 };

    const success = pos => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        const acc = pos.coords.accuracy; // meters

        // Ganti juga di sini
        locationStatus.textContent = `Kamu: ${lat.toFixed(5)}, ${lng.toFixed(5)} (akurat ±${Math.round(acc)} m)`;

        if (!userMarker) {
            userMarker = L.marker([lat, lng], {
                // simple blue circle marker
                icon: L.icon({
                    iconUrl: 'data:image/svg+xml;utf8,' + encodeURIComponent(
                        `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" fill="#2b8cff" stroke="#1a6fe8" stroke-width="1.5"/>
                </svg>`
                    ),
                    iconSize: [28, 28], iconAnchor: [14, 14]
                })
            }).addTo(map).bindPopup('Kamu di sini');
            userCircle = L.circle([lat, lng], { radius: acc, color: '#2b8cff', weight: 1, fillOpacity: 0.08 }).addTo(map);
            map.setView([lat, lng], 14);
            userMarker.openPopup();
        } else {
            userMarker.setLatLng([lat, lng]);
            userCircle.setLatLng([lat, lng]).setRadius(acc);
        }
    };

    const error = err => {
        // Ganti juga di sini
        locationStatus.textContent = `Gagal ambil lokasi: ${err.message}`;
    };

    // start watching position
    navigator.geolocation.watchPosition(success, error, opts);

} else {
    // Ganti juga di sini
    locationStatus.textContent = 'Geolocation tidak tersedia di browser ini.';
}

/* =========================
   Small helper
   ========================= */
function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// Load data saat halaman dimuat
document.addEventListener("DOMContentLoaded", fetchLocations);