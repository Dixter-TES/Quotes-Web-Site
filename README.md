# 🚀 Quotes Site Project

Учебный проект для стажировки в **IT-solution**.  
Цель проекта — продемонстрировать навыки работы с **Django**, структурой проекта и базовыми возможностями веб-разработки.

---

## 📂 Стек технологий
- Python 3.12+
- Django 5.x
- SQLite
---

## ⚠️ Внимание
Проект создан с использованием проектного менеджера **uv**!

---

## ⚙️ Установка и запуск

1. Клонируем репозиторий:

   ```bash
   git clone https://github.com/Dixter-TES/Quotes-Web-Site.git
   cd Quotes-Web-Site
   ```

2. Делаем миграции (**uv** сам создаст виртуальное окружение и установит библиотеки при первом запуске):
   ```bash
   uv run manage.py makemigrations
   ```

3. Применяем миграции:
   ```bash
   uv run manage.py migrate
   ```

4. Запускаем сервер:
   ```bash
   uv run manage.py runserver
   ```
---
✨ Сделано для стажировки в IT-solution
