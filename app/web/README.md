# Chat Application Web Front-End

## Description

This is a simple chat application that allows users to interact through a chat interface. The application is built using Flask for the backend and HTML for the frontend.

## Run container

> [!IMPORTANT]
> **Recommended**  use the [`docker-compose.yml`](../docker-compose.yml) to run the service as `docker compose up web`

```bash
$ docker build -t chat-web .    
$ docker run -p 8888:8888 --env-file .env  chat-web
 * Serving Flask app 'chat_ui.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8888
 * Running on http://172.17.0.3:8888
Press CTRL+C to quit
192.168.65.1 - - [28/Aug/2024 16:09:25] "GET / HTTP/1.1" 200 -
192.168.65.1 - - [28/Aug/2024 16:09:25] "GET /static/css/milligram.css HTTP/1.1" 200 -
```

## Endpoints

- **Home Page** (`/`):
  - Renders the home page.
  - Method: `GET`
  - Returns: Rendered HTML of the home page.

- **Activities** (`/activities`):
  - Handles GET requests for activities.
  - Method: `GET`
  - Returns: Rendered HTML of the activities page.

- **Chat** (`/chat`):
  - Handles the chat functionality.
  - Method: `POST`
  - Returns: None

- **Chat GUID** (`/chat_guid`):
  - Generates a unique identifier for a chat session.
  - Method: `GET`
  - Returns: A unique identifier for the chat session.

## Additional Notes

- Ensure that you have the `newrelic.ini` file configured if you are using New Relic for monitoring.
- The `templates/index.html` file contains the structure and layout for the chat interface.
