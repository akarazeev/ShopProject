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
| `GET`  |  `/search`                                | `0`            | `0`            | Список всех товаров в данной категории                   |
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
* Параметры запроса:
    1. username - логин пользователя
    2. password - пароль пользователя
    3. birth_date - дата рождения пользователя
    4. register_date - дата регистрации пользователя
    5. email - почта пользователя
    6. phone_number - телефон пользователя
* Пример: `curl -i -H "Content-Type: application/json" -X POST -d '{"username": "test", "password": "test", "birth_date": "test", "register_date": "test", "email": "test", "phone_number": "test"}' http://d07d7b94.ngrok.io/api/v1/register`

### `/token`
* `GET`
* Login: `1`, Admin: `0`
* Запрос токена
* Параметры запроса: нет
* Результат при успешном выполнении: json с параметром token
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/token`

### `/new_item`
* `POST`
* Login: `1`, Admin: `1`
* Добавление нового товара в магазин
* Параметры запроса: 
    1. title - название нового товара
    2. category - категория нового товара
    3. description? - описание нового товара (если не указано, то description="")
    4. amount? - доступное количество товара (если не указано, то amount=0)
* Результат при успешном выполнении: json с параметром task, где task - описание товара
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"title": "Water bottle", "category": "Bottles"}' http://d07d7b94.ngrok.io/api/v1/new_item`

### `/set_admin`
* `POST`
* Login: `1`, Admin: `1`
* Дать пользователю права админа
* Параметры запроса:
    1. username - логин пользователя, которому надо дать права админа
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"username": "test2"}' http://d07d7b94.ngrok.io/api/v1/set_admin`

### `/unset_admin`              
* `POST`
* Login: `1`, Admin: `1`
* Забрать у пользователя права админа
* Параметры запроса:
    1. username - логин пользователя, у которого надо забрать права админа
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"username": "test2"}' http://d07d7b94.ngrok.io/api/v1/unset_admin`

### `/update_item/<int:item_id>`
* `PUT`
* Login: `1`, Admin: `1`
* Обновить параметры товара с id=item_id
* Параметры запроса:
    1. title? - новый заголовок для товара
    2. description? - новое описание для товара
    3. amount? - новое количество для товара
* Результат при успешном выполнении: json с параметром task, где task - новое описание товара
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X PUT -d '{"description":"new description"}' http://d07d7b94.ngrok.io/api/v1/update_item/0`

### `/all_items`                
* `GET`
* Login: `1`, Admin: `1`
* Список всех товаров магазина
* Параметры запроса: нет
* Результат при успешном выполнении: json с параметром items, где items - массив с описанием товаров
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/all_items`

### `/get_item/<int:item_id>`   
* `GET`
* Login: `0`, Admin: `0`
* Запрос параметров товара с id=item_id
* Параметры запроса: нет
* Результат при успешном выполнении: json с описанием товара
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/get_item/0`

### `/add_cart`                 
* `POST`
* Login: `1`, Admin: `0`
* Добавить товар в корзину
* Параметры запроса:
    1. item_id - id товара, который надо добавить
    2. amount - количества единиц товара, которые надо добавить в корзину
* Результат при успешном выполнении: json с параметром record, где record имеет следующие параметры:
    1. user_id - id пользователя
    2. item_id - id товара
    3. amount - новое количество товара
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"amount": "1", "item_id": "2"}' http://d07d7b94.ngrok.io/api/v1/add_cart`

### `/remove_cart`              
* `POST`
* Login: `1`, Admin: `0`
* Убрать товар из корзины (полностью или несколько единиц)
* Параметры запроса:
    1. item_id - id товара, который надо удалить
    2. amount? - количества единиц товара, который надо удалить из корзины (если параметр не указан, то amount=1)
* Результат при успешном выполнении: json с параметром record, где record имеет следующие параметры:
    1. user_id - id пользователя
    2. item_id - id товара
    3. amount - новое количество товара
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"amount": "1", "item_id": "2"}' http://d07d7b94.ngrok.io/api/v1/remove_cart`

### `/cart`                     
* `GET`
* Login: `1`, Admin: `0`
* Список всех товаров в корзине
* Параметры запроса: нет
* Результат при успешном выполнении: массив из объектов с двумя полями: item (описание товара) и amount (количество товара в корзине)
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/cart`

### `/orders`                   
* `GET`
* Login: `1`, Admin: `0`
* Список оформленных заказов
* Параметры запроса: нет
* Результат при успешном выполнении: json с массивом id заказов
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/orders`

### `/order/<int:order_id>`     
* `GET`
* Login: `1`, Admin: `0`
* Список всех товаров в оформленном заказе с id=order_id
* Параметры запроса: нет
* Результат при успешном выполнении: json со следующими параметрами:
    1. finished - состояние заказа
    2. checkout_date - дата составления заказа
    3. items - массив из объектов с двумя полями: item (описание товара) и amount (количество товара в заказе) 
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/order/0`

### `/confirm_cart`             
* `POST`
* Login: `1`, Admin: `0`
* Оформить заказ с товарами в корзине
* Параметры запроса: нет
* Пример: `curl -u test:test -i -X POST http://d07d7b94.ngrok.io/api/v1/confirm_cart`

### `/categories`               
* `GET`
* Login: `0`, Admin: `0`
* Список всех имеющихся категорий в магазине
* Параметры запроса: нет
* Результат при успешном выполнении: json с массивом названий категорий
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/categories`

### `/search`                   
* `GET`
* Login: `0`, Admin: `0`
* Список всех товаров в данной категории
* Параметры запроса:
    1. category - именование категории, по которой надо сделать поиск
* Результат при успешном выполнении: json с массивом товаров
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X GET -d '{"category": "laptops"}' http://d07d7b94.ngrok.io/api/v1/search`

### `/items/<int:item_id>/add_commentary`                   
* `POST`
* Login: `1`, Admin: `0`
* Добавление комментария к товару с id=item_id
* Параметры запроса:
    1. text - текст комментария
    2. creation_date? - дата создания комментария
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"text": "Test comment"}' http://d07d7b94.ngrok.io/api/v1/items/1/add_commentary`

### `/items/<int:item_id>/remove_commentary`                   
* `POST`
* Login: `1`, Admin: `0`
* Удаление комментария к товару с id=item_id
* Параметры запроса: 
    1. commentary_id - id комментария, который надо удалить
* Пример: `curl -u test:test -i -H "Content-Type: application/json" -X POST -d '{"commentary_id": "1"}' http://d07d7b94.ngrok.io/api/v1/items/1/remove_commentary`

### `/items/<int:item_id>/commentaries`                   
* `GET`
* Login: `0`, Admin: `0`
* Список всех комментариев к товару с id=item_id
* Параметры запроса: нет
* Результат при успешном выполнении: json с массивом комментариев
* Пример: `curl -u test:test -i http://d07d7b94.ngrok.io/api/v1/items/1/commentaries`


## Описание json некоторых возвращаемых элементов

### Товар
* id - id товара
* title - название товара
* description - описание товара
* date_added - дата добавления товара 
* category - категория товара


### Комментарий
* id - id комментария
* user_id - пользователь, который создал данный комментарий
* item_id - товар, к которому написан данный комментарий
* text - текст комментария
* creation_date - дата создания комментария
