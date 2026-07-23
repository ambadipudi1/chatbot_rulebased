# College Enquiry Chatbot

A full-stack college enquiry chatbot: **React.js** frontend, **Django + Django REST Framework** backend, **MySQL** database. Answers questions about fee structure, hostel/accommodation, courses & departments, admissions, and scholarships.

## Architecture

```
Browser (React)  --axios-->  Django REST API  --ORM-->  MySQL
     |                              |
  ChatBot.js                  chatbot_logic.py  (keyword/rule engine)
```

- **Frontend**: `frontend/` – React app with a chat UI (`ChatBot.js`) and quick-action buttons for common queries.
- **Backend**: `backend/` – Django project `collegebot` with a single app `chatbot` exposing REST endpoints via DRF routers.
- **Database**: MySQL, storing `Department`, `Course`, `Accommodation`, `FAQ`, and `ChatLog` tables.
- **Chatbot logic**: `backend/chatbot/chatbot_logic.py` — a keyword/intent matcher. It first checks admin-curated FAQ rows, then falls back to live queries against the Course/Accommodation tables so fee and hostel answers always reflect current data.

## 1. Database setup (MySQL)

1. Install MySQL Server if you don't have it.
2. Run the setup script:
   ```bash
   mysql -u root -p < database_setup.sql
   ```
   This creates the `college_chatbot_db` database.

## 2. Backend setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # edit DB credentials inside .env
```

Load the `.env` values (either via `python-dotenv` in settings, or export them manually / use `django-environ`). The simplest option on Linux/macOS:

```bash
export $(cat .env | xargs)
```

Then:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser     # for /admin access
python manage.py seed_data           # loads sample courses, hostels, FAQs
python manage.py runserver
```

Backend now runs at `http://127.0.0.1:8000/`.

- Admin panel: `http://127.0.0.1:8000/admin/`
- API root: `http://127.0.0.1:8000/api/`

## 3. Frontend setup (React)

```bash
cd frontend
npm install
cp .env.example .env       # adjust REACT_APP_API_URL if backend runs elsewhere
npm start
```

Frontend runs at `http://localhost:3000/` and talks to the Django API.

## API Endpoints

| Method | Endpoint                     | Description                                   |
|--------|-------------------------------|------------------------------------------------|
| POST   | `/api/chat/`                  | Send a message, get bot response + category    |
| GET/POST | `/api/departments/`         | List / create departments                       |
| GET/POST | `/api/courses/`             | List / create courses (fee fields included)     |
| GET/POST | `/api/accommodations/`      | List / create hostel/accommodation options       |
| GET/POST | `/api/faqs/`                 | List / create FAQ entries used by the bot        |
| GET    | `/api/chatlogs/`              | Read-only chat history / analytics               |

Example chat request:

```bash
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "what is the hostel fee", "session_id": "abc123"}'
```

Response:
```json
{
  "response": "Here are our accommodation options:\n- Sunrise Boys Hostel ...",
  "category": "ACCOMMODATION"
}
```

## Extending the chatbot

- Add more Q&A pairs from the Django admin under **FAQs** — the matcher scores messages by keyword overlap, so add comma-separated synonyms in the `keywords` field.
- Add more courses/hostels from the admin; the bot will automatically include them in fee/accommodation answers.
- For smarter NLU (typo tolerance, intent classification), swap `chatbot_logic.py`'s keyword matcher for a library like `rapidfuzz` or an LLM call — the REST API contract (`/api/chat/`) doesn't need to change.

## Project structure

```
college_chatbot_project/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── collegebot/        # Django project settings/urls
│   └── chatbot/            # Django app: models, views, serializers, chatbot logic
│       └── management/commands/seed_data.py
├── frontend/
│   ├── package.json
│   ├── public/index.html
│   └── src/
│       ├── App.js / App.css
│       ├── components/ChatBot.js / ChatBot.css
│       └── services/api.js
├── database_setup.sql
└── README.md
```
