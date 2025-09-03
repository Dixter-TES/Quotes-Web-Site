# 🚀 Quotes Site Project

Учебный проект для стажировки в **IT-solution**.  
Цель проекта — продемонстрировать навыки работы с **Django**, структурой проекта и базовыми возможностями веб-разработки.

---

## 📂 Стек технологий
- Python 3.12+
- Django 5.x
- SQLite (по умолчанию)
uv run [command]
---

## ⚠️ Внимание
Проект создан с использованием **uv** в качестве аналога pip. Поэтому рекомендуется выполнять все команды используя:

```bash
uv run [command]
```

---

## ⚙️ Установка и запуск

1. Клонируем репозиторий:

   ```bash
   git clone https://github.com/username/django-test-project.git
   cd django-test-project
   ```

2. Создаём виртуальное окружение и активируем его:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / MacOS
   venv\Scripts\activate      # Windows
   ```

3. Устанавливаем зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Применяем миграции:
   ```bash
   python manage.py migrate
   ```

5. Запускаем сервер:
   ```bash
   python manage.py runserver
   ```

---

## 📖 Структура проекта
```
django-test-project/
│── project/        # Настройки проекта
│── app/            # Основное приложение
│── templates/      # HTML-шаблоны
│── static/         # Статические файлы (CSS, JS)
│── manage.py
```

---

## ✅ Возможности проекта
- Регистрация и авторизация пользователей
- CRUD-операции (создание, чтение, редактирование, удаление)
- Работа с шаблонами Django
- Использование моделей и ORM

---
✨ Сделано для стажировки в IT-solution
