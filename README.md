# API

Address: `http://d07d7b94.ngrok.io`

Prefix: `/api/v1`

| Type   | Endpoint                                  | Login required | Admin required | Description                                              |
| :---   | :-------------                            | :---           | :---           | :-------------                                           |
| `POST` |  `/register`                              | `0`            | `0`            | Регистрация нового пользователя                          |
| `GET`  |  `/token`                                 | `1`            | `0`            | Запрос токена                                            |
| `POST` |  `/new_item`                              | `1`            | `1`            | Добавление нового товара в магазин                       |
| `POST` |  `/set_admin`                             | `1`            | `1`            | Дать пользователю права админа                           |
| `POST` |  `/unset_admin`                           | `1`            | `1`            | Забрать у пользователя права админа                      |
| `PUT`  |  `/update_item/<int:item_id>`             | `1`            | `1`            | Обновить параметры товара                                |
| `GET`  |  `/all_items`                             | `1`            | `1`            | Список всех товаров магазина                             |
| `GET`  |  `/get_item/<int:item_id>`                | `0`            | `0`            | Запрос параметров товара                                 |
| `POST` |  `/add_cart`                              | `1`            | `0`            | Добавить товар в корзину                                 |
| `POST` |  `/remove_cart`                           | `1`            | `0`            | Убрать товар из корзины (полностью или несколько единиц) |
| `GET`  |  `/cart`                                  | `1`            | `0`            | Список всех товаров в корзине                            |
| `GET`  |  `/orders`                                | `1`            | `0`            | Список оформленных заказов                               |
| `GET`  |  `/order/<int:order_id>`                  | `1`            | `0`            | Список всех товаров в оформленном заказе                 |
| `POST` |  `/confirm_cart`                          | `1`            | `0`            | Оформить заказ с товарами в корзине                      |
| `GET`  |  `/categories`                            | `0`            | `0`            | Список всех имеющихся категорий в магазине               |
| `GET`  |  `/search`                                | `0`            | `0`            | Поиск по категории                                       |
| `POST` |  `/items/<int:item_id>/add_commentary`    | `1`            | `0`            | Добавление комментария к товару                          |
| `POST` |  `/items/<int:item_id>/remove_commentary` | `1`            | `0`            | Удаление комментария к товару                            |
| `GET`  |  `/items/<int:item_id>/commentaries`      | `0`            | `0`            | Список всех комментариев к товару                        |

## Авторизация

В качестве аутентификации может использоваться как пара `username`:`password`, так и `token`:unused_password
- `username`:`password`
```bash
curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/all_items
```
- `token`:unused_password
```bash
curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i http://d07d7b94.ngrok.io/api/v1/all_items
```

## Подробное описание "ручек"

### `/register`
* `POST`
* Login: `0`, Admin: `0`
* Регистрация нового пользователя
* Пример: `curl -i -H "Content-Type: application/json" -X POST -d '{"username": "test", "password": "test", "birth_date": "test", "register_date": "test", "email": "test", "phone_number": "test"}' http://d07d7b94.ngrok.io/api/v1/register`

### `/token`
* `GET`
* Login: `1`, Admin: `0`
* Запрос токена
* Пример:

### `/new_item`
* `POST`
* Login: `1`, Admin: `1`
* Добавление нового товара в магазин
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"title": "cd"}' http://d07d7b94.ngrok.io/api/v1/new_item`

### `/set_admin`
* `POST`
* Login: `1`, Admin: `1`
* Дать пользователю права админа
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"username": "test2"}' http://d07d7b94.ngrok.io/api/v1/set_admin`

### `/unset_admin`              
* `POST`
* Login: `1`, Admin: `1`
* Забрать у пользователя права админа
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"username": "test2"}' http://d07d7b94.ngrok.io/api/v1/unset_admin`

### `/update_item/<int:item_id>`
* `PUT`
* Login: `1`, Admin: `1`
* Обновить параметры товара
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X PUT -d '{"description":"new description"}' http://d07d7b94.ngrok.io/api/v1/update_item/0`

### `/all_items`                
* `GET`
* Login: `1`, Admin: `1`
* Список всех товаров магазина
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/all_items`

### `/get_item/<int:item_id>`   
* `GET`
* Login: `0`, Admin: `0`
* Запрос параметров товара
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/get_item/0`

### `/add_cart`                 
* `POST`
* Login: `1`, Admin: `0`
* Добавить товар в корзину
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"amount": "1", "item_id": "2"}' http://d07d7b94.ngrok.io/api/v1/add_cart`

### `/remove_cart`              
* `POST`
* Login: `1`, Admin: `0`
* Убрать товар из корзины (полностью или несколько единиц)
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"amount": "1", "item_id": "2"}' http://d07d7b94.ngrok.io/api/v1/remove_cart`

### `/cart`                     
* `GET`
* Login: `1`, Admin: `0`
* Список всех товаров в корзине
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/cart`

### `/orders`                   
* `GET`
* Login: `1`, Admin: `0`
* Список оформленных заказов
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/orders`

### `/order/<int:order_id>`     
* `GET`
* Login: `1`, Admin: `0`
* Список всех товаров в оформленном заказе
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/order/0`

### `/confirm_cart`             
* `POST`
* Login: `1`, Admin: `0`
* Оформить заказ с товарами в корзине
* Пример: `curl -u test:test -i -X POST http://d07d7b94.ngrok.io/api/v1/confirm_cart`

### `/categories`               
* `GET`
* Login: `0`, Admin: `0`
* Список всех имеющихся категорий в магазине
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/categories`

### `/search`                   
* `GET`
* Login: `0`, Admin: `0`
* Поиск по категории
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X GET -d '{"category": "laptops"}' http://d07d7b94.ngrok.io/api/v1/search`

### `/items/<int:item_id>/add_commentary`                   
* `POST`
* Login: `1`, Admin: `0`
* Добавление комментария к товару
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"text": "Test comment"}' http://d07d7b94.ngrok.io/api/v1/items/1/add_commentary`

### `/items/<int:item_id>/remove_commentary`                   
* `POST`
* Login: `1`, Admin: `0`
* Удаление комментария к товару
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"commentary_id": "1"}' http://d07d7b94.ngrok.io/api/v1/items/1/remove_commentary`

### `/items/<int:item_id>/commentaries`                   
* `GET`
* Login: `0`, Admin: `0`
* Список всех комментариев к товару
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/items/1/commentaries`
