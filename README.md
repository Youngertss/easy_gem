<h1>Site for gambling</h1>

Look for frontend on https://github.com/Youngertss/easy_gem_front

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
- To run Postgres DB with alembic migrations and seed data (games and tags)
- To run Redis server (more usage in future is expected)
- To run celery, celery_beat and flower

Now 3 games are available: FortuneWheel, SafeHack, Miner
All database models declared in file src/auth/models.py

<h3>Here is instruction to the site</h3>
The easiest way to start project on your local machine, is to use docker

Run in the root of project (add --build if it's first time)

```bash
docker compose up --build
docker compose up
```

Don't forget to create .env file in the root with your data. You can see example of it in file environment_example.txt

Now you will have fastapi on 127.0.0.1:8000 and Flower on 127.0.0.1:5555
Frontend is in another repo.


<h5>If you don't wan't to use a docker, here is instruction.</h5>

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

frontend start (watch another repo - <https://github.com/Youngertss/easy_gem_front>):

```bash
npm install
npm start
```

alembic migrations:

```bash
alembic revision --autogenerate -m "..."
alembic upgrade head
python -m migrations.seed
```

redis start (for chat - you still need this. Delete all services except redis if you want):

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
