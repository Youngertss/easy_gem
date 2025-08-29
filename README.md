<h1 align="center"><img src="https://placekitten.com/300/150"/>Site for gambling</h1>


To start a project, first create an environment and download requirements:
`pyhton -m venv venv`
`python venv/Scripts/activate`
`pip install -r reqiurements.txt`

All commands run from the root of the project

backend start:
`uvicorn src.main:app`

frontend start (push from another repo):
`npm install`
`npm start`

alembic migrations:
`alembic revision --autogenerate -m "..."`
`alembic upgrade head`

redis start (for chat):
`docker compose up`
