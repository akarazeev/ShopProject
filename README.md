## Примеры запросов

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
