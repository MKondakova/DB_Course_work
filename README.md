# Дерево бота
## Подборки
Приходит номерованный список "№ Заголовок - Описание"
# Ввести номер
# Следующая страница
# Предыдущая страница
# В меню

## Мои плейлисты (в том числе общие)
## Друзья
## Вид автора



# Команда запуска
```
 docker cp russify_drop.sql database:russify_dr.sql && docker exec -u postgres database psql postgres postgres -f russify_dr.sql &&  docker cp russify.sql database:russify.sql && docker exec -u postgres database psql postgres postgres -f russify.sql
./postgrest tutorial.conf


docker cp triggers.sql database:r_triggers.sql && docker exec -u postgres database psql postgres postgres -f r_triggers.sql
docker cp functions.sql database:r_functions.sql && docker exec -u postgres database psql postgres postgres -f r_functions.sql

```