<h1>Site for gambling</h1>

<h3>▶️ Fast overview of my project on youtube (timecods in the description): https://youtu.be/Dh3BF44voCU?si=NhXs9fE4i1gWIBGu</h3>

Look for frontend React App on https://github.com/Youngertss/easy_gem_front

<h2>This project combines in itself such technologies as:</h2>

### FastAPI → async backend

- PostgreSQL database with Alembic migrations  
- Redis pub/sub with channels to conduct chat messaging along with websocket
- Redis as broker and backend for celery
- Celery & Flower for background & schedualed tasks 

### React → frontend (Create React App)

- Zustand as storage to store user info  

### Docker

- To run Fastapi app (now still using uvicorn)
- To run Postgres DB with alembic migrations and seed data (tags & games, users & gameshistory)
- To run Redis server
- To run celery, celery_beat and flower

Now 3 games are available: FortuneWheel, SafeHack, Miner - "the most popular" section.

All database models declared in file src/auth/models.py

<h3>Here is instruction to the site</h3>
The easiest way to start the project on your local machine, is to use docker.

Run in the root of project (add --build if it's first time)

```bash
docker compose up --build
docker compose up
```

Don't forget to create .env file in the root with your data. You can see example of it in file environment_example.txt

Now you will have fastapi on 127.0.0.1:8000 (with builded frontend React app) and Flower on 127.0.0.1:5555



### If you don't wan't to use docker, here is instruction.

To start the project, first create an environment and download requirements:

```bash
pyhton -m venv venv
python venv/Scripts/activate
pip install -r reqiurements.txt
```

<h5>All commands run from the root of the project</h5>

backend start:

```bash
uvicorn src.main:app --reload
```

frontend is stating autmatically with beckend from builded app. If you want to look at not builded front: watch another repo - <https://github.com/Youngertss/easy_gem_front>


alembic migrations:

```bash
alembic revision --autogenerate -m "..."
alembic upgrade head
python -m migrations.seed
```

redis start (you still need this for chat. Delete all services except redis if you want):

```bash
docker compose up
```

celery worker, beat and flower:

```bash
celery -A src.celery_app.celery worker --loglevel=info
celery -A src.celery_app.celery beat --loglevel=info
celery -A src.celery_app.celery flower
```

Don't forget to create .env file in the root with your data. You can see example of it in file environment_example.txt

Thanks for reading! Happy coding!✨
