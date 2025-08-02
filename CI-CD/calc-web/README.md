# Calculator Web App (Flask)

This is a basic web-based calculator app using Flask, designed to demonstrate Jenkins CI/CD and Docker multi-stage builds.

## Endpoints

- `GET /add?a=5&b=2` → `{ "result": 7 }`
- `GET /subtract?a=5&b=2` → `{ "result": 3 }`

## Running Locally

```bash
docker build -t calculator-webapp .
docker run -p 5000:5000 calculator-webapp
```

Visit [http://localhost:5000](http://localhost:5000)

Adding random stuf