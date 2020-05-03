# API

Address: `http://d07d7b94.ngrok.io`

Prefix: `/api/v1`

| Type   | Endpoint                      | Admin | Description                                              |
| :---   | :-------------                | :---  | :-------------                                           |
| `POST` |  `/register`                  | `0`   | Регистрация нового пользователя                          |
| `GET`  |  `/token`                     | `0`   | Запрос токена                                            |
| `POST` |  `/new_item`                  | `1`   | Добавление нового товара в магазин                       |
| `POST` |  `/set_admin`                 | `1`   | Дать пользователю права админа                           |
| `POST` |  `/unset_admin`               | `1`   | Забрать у пользователя права админа                      |
| `PUT`  |  `/update_item/<int:item_id>` | `1`   | Обновить параметры товара                                |
| `GET`  |  `/all_items`                 | `1`   | Список всех товаров магазина                             |
| `GET`  |  `/get_item/<int:item_id>`    | `0`   | Запрос параметров товара                                 |
| `POST` |  `/add_cart`                  | `0`   | Добавить товар в корзину                                 |
| `POST` |  `/remove_cart`               | `0`   | Убрать товар из корзины (полностью или несколько единиц) |
| `GET`  |  `/cart`                      | `0`   | Список всех товаров в корзине                            |
| `GET`  |  `/orders`                    | `0`   | Список оформленных заказов                               |
| `GET`  |  `/order/<int:order_id>`      | `0`   | Список всех товаров в оформленном заказе                 |
| `POST` |  `/confirm_cart`              | `0`   | Оформить заказ с товарами в корзине                      |
| `GET`  |  `/categories`                | `0`   | ?                                                        |
| `GET`  |  `/search`                    | `0`   | ?                                                        |

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
* Admin: `0`
* Регистрация нового пользователя
* Пример: `curl -i -H "Content-Type: application/json" -X POST -d '{"username": "test", "password": "test", "birth_date": "test", "register_date": "test", "email": "test", "phone_number": "test"}' http://d07d7b94.ngrok.io/api/v1/register`

### `/token`
* `GET`
* Admin: `0`
* Запрос токена
* Пример:

### `/new_item`
* `POST`
* Admin: `1`
* Добавление нового товара в магазин
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i -H "Content-Type: application/json" -X POST -d '{"title": "cd"}' http://d07d7b94.ngrok.io/api/v1/new_item`

### `/set_admin`
* `POST`
* Admin: `1`
* Дать пользователю права админа
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"username": "test2"}' http://d07d7b94.ngrok.io/api/v1/set_admin`

### `/unset_admin`              
* `POST`
* Admin: `1`
* Забрать у пользователя права админа
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"username": "test2"}' http://d07d7b94.ngrok.io/api/v1/unset_admin`

### `/update_item/<int:item_id>`
* `PUT`
* Admin: `1`
* Обновить параметры товара
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i -H "Content-Type: application/json" -X PUT -d '{"description":"new description"}' http://d07d7b94.ngrok.io/api/v1/update_item/0`

### `/all_items`                
* `GET`
* Admin: `1`
* Список всех товаров магазина
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i http://d07d7b94.ngrok.io/api/v1/all_items`

### `/get_item/<int:item_id>`   
* `GET`
* Admin: `0`
* Запрос параметров товара
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i http://d07d7b94.ngrok.io/api/v1/get_item/0`

### `/add_cart`                 
* `POST`
* Admin: `0`
* Добавить товар в корзину
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i -H "Content-Type: application/json" -X POST -d '{"amount": "1", "item_id": "2"}' http://d07d7b94.ngrok.io/api/v1/add_cart`

### `/remove_cart`              
* `POST`
* Admin: `0`
* Убрать товар из корзины (полностью или несколько единиц)
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i -H "Content-Type: application/json" -X POST -d '{"amount": "1", "item_id": "2"}' http://d07d7b94.ngrok.io/api/v1/remove_cart`

### `/cart`                     
* `GET`
* Admin: `0`
* Список всех товаров в корзине
* Пример: `curl -u WpqKaw2J0gHNKdhyRXsVQ5QjiOtB1zTM:unused -i http://d07d7b94.ngrok.io/api/v1/cart`

### `/orders`                   
* `GET`
* Admin: `0`
* Список оформленных заказов
* Пример:

### `/order/<int:order_id>`     
* `GET`
* Admin: `0`
* Список всех товаров в оформленном заказе
* Пример:

### `/confirm_cart`             
* `POST`
* Admin: `0`
* Оформить заказ с товарами в корзине
* Пример:

### `/categories`               
* `GET`
* Admin: `0`
* ?
* Пример: ?

### `/search`                   
* `GET`
* Admin: `0`
* ?
* Пример: ?
