## Примеры запросов

Создание нового товара:
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"title": "cd"}' http://localhost:5000/api/new_item
```

Изменение параметров товара (0 - `id` товара):
```bash
curl -i -H "Content-Type: application/json" -X PUT -d '{"description":"new description"}' http://localhost:5000/api/update_item/0
```

Список всех товаров:
```bash
curl -i localhost:5000/api/all_items
```