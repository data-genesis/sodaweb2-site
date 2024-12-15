// order.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-order-btn').addEventListener('click', function() {
        document.getElementById('order-form-container').style.display = 'block';
    });

    document.getElementById('order-form').addEventListener('submit', function(e) {
        e.preventDefault();
        let formData = new FormData(this);

        fetch('', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    window.location.href = '{% url "cart:order_thanks" %}';
                } else {
                    alert(data.message);
                }
            });
    });
});