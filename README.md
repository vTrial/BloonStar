# datachipper
 Battles 2 stats website

## What is used for each section:
Database: sqlite3 (python)
Backend: Flask (python)
Frontend: Svelte

## How to operate
1. Set up backend + database
    - pip install -r requirements.txt
    - cd backend
    - python3 backend.py
The backend should be hosted at http://localhost:5000/

2. Set up frontend
    - cd frontend
    - npm install
    - npm run dev
The backend should be hosted at http://localhost:5173/

## Things to keep in mind
- nk api only has max 120 requests/minute. Refrain from opening b2.lol when using this program.