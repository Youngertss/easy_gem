<h1>Site for gambling</h1>

This project combine in itself such technologies as:

- <h6>FastAPI</h6> ➝ async backend:
    •Postgresql database;
    •Alembic migrations;
    •Redis pub/sub with channels to conduct chat messaging;
    ◦Cerely & flower are expected in future.

- <h6>React</h6> ➝ frontent (react create app):
    •Zustand as storage to store user info.

- <h6>Docker</h6> ➝ to run Redis server. (more usage in future are expexted)

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
