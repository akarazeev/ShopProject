## Примеры запросов

### Аутентификация
- username:password
```bash
curl -u test:test -i localhost:5000/api/v1/all_items
```
- token:unused_password
```bash
curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i localhost:5000/api/v1/all_items 
```

### Регистрация
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"username": "test", "password": "test", "birth_date": "test", "register_date": "test", "email": "test", "phone_number": "test"}' localhost:5000/api/v1/register
```

---

Создание нового товара:
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"title": "cd"}' http://localhost:5000/api/v1/new_item
```

Изменение параметров товара (0 - `id` товара):
```bash
curl -i -H "Content-Type: application/json" -X PUT -d '{"description":"new description"}' http://localhost:5000/api/v1/update_item/0
```

Список всех товаров:
```bash
curl -i localhost:5000/api/v1/all_items
```

Запрос всей информации о товаре:
```bash
curl -i localhost:5000/api/v1/get_item/0
```

Добавление товара в корзину:
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"user_id": "1", "item_id": "0"}' http://localhost:5000/api/v1/add_cart
```

Запрос содержимого корзины пользователя:
```bash
curl -i localhost:5000/api/v1/cart/0
```
