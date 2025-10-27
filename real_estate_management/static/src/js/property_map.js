/** @odoo-module **/
console.log("Enhanced Property Map with Auto-Hide and Category Colors loaded ✅");

document.addEventListener('DOMContentLoaded', () => {
    const dataEl = document.getElementById('property-data');
    const legendEl = document.getElementById('category-legend');
    if (!dataEl || !legendEl) return;

    let properties = [];
    try {
        properties = JSON.parse(dataEl.dataset.properties);
    } catch (e) {
        return console.error('Invalid property JSON', e);
    }

    // Parse category colors from template
    const categoryColors = JSON.parse(legendEl.dataset.colors);

    function initMap() {
        if (typeof L === 'undefined') {
            return setTimeout(initMap, 200);
        }
        const el = document.getElementById('propertyMap');
        if (!el || !properties.length) return;

        const map = L.map(el);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
        }).addTo(map);

        let openPopupMarker = null;
        let pointerInsidePopup = false;

        function createIcon(color) {
            return L.divIcon({
                className: 'custom-marker',
                html: `<div style="
                    width:32px;height:32px;border-radius:50%;
                    background:${color};border:3px solid white;
                    box-shadow:0 3px 12px rgba(0,0,0,0.3);
                    display:flex;align-items:center;justify-content:center;
                    font-size:14px;color:white;cursor:pointer;
                ">📍</div>`,
                iconSize: [32,32],
                iconAnchor: [16,16],
                popupAnchor: [0,-16]
            });
        }

        function popupHtml(p) {
            const img = p.image_url || '/web/static/img/placeholder.png';
            const price = p.price > 0
                ? `₹${p.price.toLocaleString('en-IN')}`
                : 'Price on Request';
            return `
                <div class="property-hover-card">
                  <img src="${img}" class="property-image" onerror="this.src='/web/static/img/placeholder.png'"/>
                  <div class="property-content">
                    <h4 class="property-title">${p.name}</h4>
                    <div class="property-category">${p.property_type}</div>
                    <div class="property-location">📍 ${p.full_address}</div>
                    <div class="property-price">${price}</div>
                    <div class="property-details">
                      ${p.area?`<div class="detail-item">📐 ${p.plot_area} sqft</div>`:''}
                    </div>
                    <div class="action-buttons">
                      <a href="/property/${p.id}" class="btn-sm btn-primary">View Details</a>
                      ${p.contact_phone?`<a href="tel:${p.contact_phone}" class="btn-sm btn-outline">📞 Call</a>`:''}
                    </div>
                  </div>
                </div>`;
        }

        // Add markers
        properties.forEach(p => {
            if (!p.latitude || !p.longitude) return;
            const color = categoryColors[p.property_type] || '#4f46e5';
            const marker = L.marker([p.latitude, p.longitude], { icon: createIcon(color) }).addTo(map);

            marker.bindPopup(popupHtml(p), {
                closeButton: false, autoClose: false, closeOnClick: false,
                className: 'custom-popup', minWidth: 280, maxWidth: 320
            });

            // Hover open/close logic
            marker.on('mouseover', function() {
                if (openPopupMarker && openPopupMarker !== marker) {
                    openPopupMarker.closePopup();
                }
                marker.openPopup();
                openPopupMarker = marker;
            });
            marker.on('mouseout', function() {
                setTimeout(() => {
                    if (openPopupMarker === marker && !pointerInsidePopup) {
                        marker.closePopup();
                        openPopupMarker = null;
                    }
                }, 100);
            });
            marker.on('popupopen', function() {
                const popupEl = marker.getPopup().getElement();
                popupEl.addEventListener('mouseenter', () => pointerInsidePopup = true);
                popupEl.addEventListener('mouseleave', () => {
                    pointerInsidePopup = false;
                    setTimeout(() => {
                        if (openPopupMarker === marker && !pointerInsidePopup) {
                            marker.closePopup();
                            openPopupMarker = null;
                        }
                    }, 100);
                });
            });
        });

        map.on('click', () => {
            if (openPopupMarker) {
                openPopupMarker.closePopup();
                openPopupMarker = null;
            }
        });

        // Build legend
        legendEl.innerHTML = Object.entries(categoryColors).map(
            ([cat, col]) => `
              <div class="legend-item">
                <div class="legend-color" style="background:${col}"></div>
                <span>${cat}</span>
              </div>`
        ).join('');

        // Fit map to markers
        const group = L.featureGroup(properties
            .filter(p => p.latitude && p.longitude)
            .map(p => L.marker([p.latitude, p.longitude]))
        );
        if (group.getLayers().length) {
            map.fitBounds(group.getBounds().pad(0.1));
        }
    }

    initMap();
});