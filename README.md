# fastapi_light_server

This is a simple project on FastAPI Framework.

```/src``` - folder which contains the whole for the API service.

```/tests``` - folder with tests for some features. Will be extended later

```/tic_tac_toe``` - folder with another task. 
The main idea - write the game tic-tac-toe where players are 2 computers, 
which play when code runs

# API (1st task)

API calculator service

This API includes 2 endpoints:
1. ```/calc``` - POST request, payload with JSON (e.g. ```{"expression": "* - 5 6 7"}``` )
Each element of expression should be separated with space (' '). Otherwise calculation may not be calculated.
As response you can get an Error with some details or results of calculation


2. ```/history``` - GET request, request can contain query params such as ```limit``` and ```status```.
Response - list of calculation with results.


3. ```/doc``` - simple documentation based on OpenAPI. Could be extended later

All calculations are saved in DB (PostgreSQL).

Start the server ```docker-compose up --build```

# TIC-TAC-TOE (2nd task)
This task uses sockets.
Start the game - ```python socket_server.py```.

```socket_server.py``` accepts some cli arguments:
1. ```--field-width``` - width for game field
2. ```--field-height``` - height for game field
3. ```--symbols-in-row``` - how many same symbols should be in a row for win
4. ```--logging-file-name``` - where to collect games logs
5. ```--log-format``` - format for logging

When server is up, you can run 2 clients:
```python player.py``` (1 command for 1 client)