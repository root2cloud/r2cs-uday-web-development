// Wait for DOM and Leaflet to load
document.addEventListener('DOMContentLoaded', function() {
    // Check if Leaflet is loaded
    if (typeof L === 'undefined') {
        console.error('Leaflet library not loaded');
        return;
    }

    // Get property data from hidden div
    var propertyDataElement = document.getElementById('property-data');
    if (!propertyDataElement) {
        console.error('Property data element not found');
        return;
    }

    var propertyData;
    try {
        propertyData = JSON.parse(propertyDataElement.getAttribute('data-properties'));
        console.log('Property data loaded:', propertyData);
    } catch (e) {
        console.error('Error parsing property data:', e);
        return;
    }

    console.log('Initializing map with', propertyData.length, 'properties');

    // Initialize map centered on Vishakapatnam
    var map = L.map('map-container').setView([17.6868, 83.2185], 12);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Add property markers
    propertyData.forEach(function(property) {
        if (property.latitude && property.longitude) {
            // Create marker
            var marker = L.marker([property.latitude, property.longitude]).addTo(map);

            // Create popup content
            var popupContent = '<div style="min-width: 200px;">' +
                '<h6><strong>' + property.name + '</strong></h6>' +
                '<p><i class="fa fa-map-marker"></i> ' + property.street + ', ' + property.locality + '</p>';

            if (property.price > 0) {
                popupContent += '<p><i class="fa fa-money"></i> ₹' + property.price.toLocaleString() + '</p>';
            }

            if (property.contact_phone) {
                popupContent += '<p><i class="fa fa-phone"></i> ' + property.contact_phone + '</p>';
            }

            if (property.contact_email) {
                popupContent += '<p><i class="fa fa-envelope"></i> ' + property.contact_email + '</p>';
            }

            popupContent += '</div>';

            // Bind popup to marker
            marker.bindPopup(popupContent);

            // Add click event for additional info display
            marker.on('click', function() {
                document.getElementById('property-info').innerHTML =
                    '<div class="alert alert-info">' +
                    '<h5>' + property.name + '</h5>' +
                    '<p>' + property.street + ', ' + property.locality + '</p>' +
                    (property.price > 0 ? '<p>Price: ₹' + property.price.toLocaleString() + '</p>' : '') +
                    '</div>';
            });
        }
    });

    // Fit map to show all markers if we have properties
    if (propertyData.length > 0) {
        var group = new L.featureGroup();
        propertyData.forEach(function(property) {
            if (property.latitude && property.longitude) {
                group.addLayer(L.marker([property.latitude, property.longitude]));
            }
        });

        if (group.getLayers().length > 0) {
            map.fitBounds(group.getBounds().pad(0.1));
        }
    }
});
