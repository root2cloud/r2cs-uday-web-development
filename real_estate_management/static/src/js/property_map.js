/** @odoo-module */
console.log("Property Map JS loaded ✅");

document.addEventListener('DOMContentLoaded', function() {
    const propertyDataEl = document.getElementById('property-data');
    if (!propertyDataEl) return;

    const jsonStr = propertyDataEl.getAttribute('data-properties');
    let propertyData = [];

    try {
        propertyData = JSON.parse(jsonStr);
    } catch (e) {
        console.error('Failed to parse property JSON:', e);
        return;
    }

    function initializeMap() {
        if (typeof L === 'undefined') {
            setTimeout(initializeMap, 200);
            return;
        }

        const mapContainer = document.getElementById('propertyMap');
        if (!mapContainer || propertyData.length === 0) return;

        const map = L.map('propertyMap').setView([17.6868, 83.218], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
        }).addTo(map);

        const markers = [];
        propertyData.forEach(prop => {
            if (prop.latitude && prop.longitude) {
                const marker = L.marker([prop.latitude, prop.longitude]).addTo(map);
                const popup = `
                    <div style="min-width:200px;">
                        <h6><strong>${prop.name}</strong></h6>
                        <p>${prop.street}</p>
                        ${prop.price > 0 ? `<p>Price: ₹${prop.price.toLocaleString()}</p>` : ''}
                        ${prop.contact_phone ? `<p>Phone: ${prop.contact_phone}</p>` : ''}
                    </div>
                `;
                marker.bindPopup(popup);
                markers.push(marker);
            }
        });

        if (markers.length > 0) {
            const group = L.featureGroup(markers);
            map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    initializeMap();
});
