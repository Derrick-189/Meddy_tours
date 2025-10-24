// Dynamic accommodation loading
function loadAccommodations(type) {
    fetch(`/api/accommodations/?type=${type}`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('id_accommodation');
            select.innerHTML = '<option value="">Select Accommodation</option>';
            data.forEach(acc => {
                const option = document.createElement('option');
                option.value = acc.id;
                option.textContent = `${acc.name} - $${acc.price_per_night}/night`;
                select.appendChild(option);
            });
        });
}

// Calculate total amount
function calculateTotal() {
    const tourPackage = document.getElementById('id_tour_package').value;
    const accommodation = document.getElementById('id_accommodation').value;
    const persons = document.getElementById('id_number_of_persons').value;
    
    if (tourPackage) {
        fetch(`/api/calculate-total/?tour_package=${tourPackage}&accommodation=${accommodation}&persons=${persons}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-amount').textContent = `$${data.total_amount}`;
            });
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const tourSelect = document.getElementById('id_tour_package');
    const accommodationSelect = document.getElementById('id_accommodation');
    const personsInput = document.getElementById('id_number_of_persons');
    
    if (tourSelect) {
        tourSelect.addEventListener('change', calculateTotal);
    }
    if (accommodationSelect) {
        accommodationSelect.addEventListener('change', calculateTotal);
    }
    if (personsInput) {
        personsInput.addEventListener('input', calculateTotal);
    }
    
    // Newsletter subscription
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch('/subscribe/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.success) {
                    this.reset();
                }
            });
        });
    }
});