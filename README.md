Новостной портал на Django с фильтрацией, пагинацией и CRUD-операциями.

## 🌐 Ссылки (после запуска сервера)

### 📰 Публикации

- **Список всех новостей:** [/news/](http://127.0.0.1:8000/news/)
- **Поиск по публикациям:** [/news/search/](http://127.0.0.1:8000/news/search/)
- **Детальная страница:** `/news/<int:pk>/` (например, `/news/1/`)

### ✏️ CRUD для Новостей

- **Создать:** `/news/create/`
- **Редактировать:** `/news/<int:pk>/edit/`
- **Удалить:** `/news/<int:pk>/delete/`

### ✏️ CRUD для Статей

- **Создать:** `/news/articles/create/`
- **Редактировать:** `/news/articles/<int:pk>/edit/`
- **Удалить:** `/news/articles/<int:pk>/delete/`

### 🔧 Управление

- **Админ-панель:** [/admin/](http://127.0.0.1:8000/admin/) (логин/пароль: `admin` / `admin`)

---

## 🚀 Быстрый старт (Linux / macOS)

**Клонируйте репозиторий:**
`     git clone https://github.com/DS-975/News-Portal-SF.git
    cd News-Portal-SF
    `

---

**Создайте и активируйте виртуальное окружение:**
`     python3 -m venv venv
    source venv/bin/activate
    `

---

**Установите зависимости:**
`     pip install -r requirements.txt
    `

---

**Перейдите в папку проекта и примените миграции:**
`     cd News_Paper
    python3 manage.py migrate
    `

---

**Создайте суперпользователя (если нужно):**
`     python3 manage.py createsuperuser
    `

---

**Запустите сервер:**
`     python3 manage.py runserver
    `

---

**🛠️ Используемые технологии**
Django (5.2.1) — веб-фреймворк.

django-filter — фильтрация списка публикаций.

Bootstrap 5 — стилизация интерфейса.

SQLite — база данных (по умолчанию).
