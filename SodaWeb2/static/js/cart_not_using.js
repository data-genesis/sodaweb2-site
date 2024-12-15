// cart.js (или в блок js вашего шаблона)
function createOrder() {
    fetch(CREATE_ORDER_URL)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                window.location.href = ORDER_THANKS_URL;
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при оформлении заказа');
        });
}

function addToCart(event, item_slug) {
    event.preventDefault(); // Предотвращаем стандартное поведение

    const url = `/cart/add/${item_slug}/`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message); // Временное уведомление
                // Обновление интерфейса, например, счетчика корзины
                const cartCountElement = document.querySelector('#cart-count');
                if (cartCountElement) {
                    cartCountElement.textContent = data.cart_items_count;
                }
            } else {
                alert('Что-то пошло не так');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при добавлении товара в корзину');
        });
}

function decreaseCartItem(item_id) {
     fetch(`${BASE_URL}${item_id}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const cartItem = document.querySelector(`.cart-item[data-item-id="${item_id}"]`);
                if (cartItem) {
                    cartItem.querySelector('.item-quantity').textContent = `Количество: ${data.new_quantity}`;
                }

                updateCartCount(data.cart_items_count);
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

function removeCartItem(item_id) {
    fetch(`${BASE_URL}${item_id}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const cartItem = document.querySelector(`.cart-item[data-item-id="${item_id}"]`);
                if (cartItem) {
                    cartItem.remove();
                }

                updateCartCount(data.cart_items_count);

                if (data.cart_items_count === 0) {
                    document.querySelector('.cart-list').innerHTML = '<p>Ваша корзина пуста.</p>';
                }
            }
        })
        .catch(error => console.error('Ошибка:', error));
}