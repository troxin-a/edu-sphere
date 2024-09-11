# 📚️ Edu Sphere (Платформа для онлайн-обучения)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-4.2-brightgreen)
![DRF](https://img.shields.io/badge/DRF-red)



## Полное заполнение базы: курсы, уроки, пользователи и платежи:
```
python3 manage.py fill
```

## 📦 О проекте

### Список курсов:
```
http://localhost:8000/courses/
```

### Информация о курсе:
```
http://localhost:8000/courses/:id/
```

### Информация о пользователе:
```
http://localhost:8000/users/:id/
```

### Список платежей:
```
http://localhost:8000/users/payments/
```

 - Сортировка платежей по дате оплаты:
```
?ordering=date - Сначала старые
?ordering=-date - Сначала новые
```

 - Фильтрация платежей по уроку, курсу и методу оплаты:
```
?course=:id - курс
?lesson=:id - урок
?method=:id - метод оплаты
```
Фильтрации и сортировку можно объединять через знак &