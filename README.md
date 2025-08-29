<h1>Site for gambling</h1>

### FastAPI → async backend

- PostgreSQL database  
- Alembic migrations  
- Redis pub/sub with channels to conduct chat messaging along with websocket  
- Celery & Flower are expected in future (probably)  

### React → frontend (Create React App)

- Zustand as storage to store user info  

### Docker

- To run Redis server (more usage in future is expected)

Now 2 games are available: SafeHack and FortuneWheel.


<h3>Here is instruction to the site</h3>

To start a project, first create an environment and download requirements:
`pyhton -m venv venv`
`python venv/Scripts/activate`
`pip install -r reqiurements.txt`

<h5>All commands run from the root of the project</h5>

backend start:
`uvicorn src.main:app --reload`

frontend start (wathc another repo - https://github.com/Youngertss/easy_gem_front):
`npm install`
`npm start`

alembic migrations:
`alembic revision --autogenerate -m "..."`
`alembic upgrade head`

redis start (for chat):
`docker compose up`
