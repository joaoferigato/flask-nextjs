# Next.js + Flask Security Lab

A small full-stack learning project demonstrating server-side communication between a Next.js frontend and a Flask backend. The project starts locally and is intended to evolve into a hands-on lab for API security and Azure deployment.

## Architecture

The browser requests a page from Next.js. The Next.js server calls Flask directly, attaching a shared service token. Flask validates that token before returning data.

```text
Browser
   |
   | GET /
   v
Next.js Server Component
   |
   | GET http://localhost:5000/api/hello
   | Authorization: Bearer <service-token>
   v
Flask API
   |
   | JSON response
   v
Next.js renders the page
   |
   v
Browser
```

The browser does not call Flask directly and must never receive the service token. Since the browser only communicates with Next.js in this setup, Flask CORS configuration is not required for this server-to-server request.

## Project Structure

```text
next-flask-app/
├── frontend/                 # Next.js application
│   ├── src/
│   │   └── app/
│   │       └── page.tsx      # Server Component fetches Flask data
│   ├── .env.local            # Local frontend environment variables (not committed)
│   └── package.json
├── backend/                  # Flask application
│   ├── app/
│   │   ├── __init__.py       # Application factory
│   │   ├── auth.py           # Service-token validation
│   │   └── routes/
│   │       └── hello.py      # Example API blueprint
│   ├── .env                  # Local backend environment variables (not committed)
│   ├── .venv/                # Python virtual environment (not committed)
│   ├── run.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

> Adjust the tree above to match the files currently present in your checkout. The project is a learning example, not a production-ready security template.

## Prerequisites

- Node.js and npm
- Python 3
- Git (optional, but recommended)

## Local Setup

### 1. Configure the backend

Open a terminal in the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

If you have not generated `requirements.txt` yet, install the packages used by the app (Flask and python-dotenv) and then generate it:

```bash
pip install Flask python-dotenv
pip freeze > requirements.txt
```

Create `backend/.env`:

```dotenv
BACKEND_API_TOKEN=replace-with-a-long-random-secret
```

Generate a strong local token with Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the same generated value for `BACKEND_API_TOKEN` in both the backend and frontend environment files. Do not commit either file.

Start Flask:

```bash
python run.py
```

The backend should listen at `http://localhost:5000` if configured with that port.

### 2. Configure the frontend

Open a second terminal at the repository root:

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```dotenv
BACKEND_URL=http://localhost:5000
BACKEND_API_TOKEN=replace-with-the-same-long-random-secret
```

The token must match the value configured in `backend/.env`. Do not prefix it with `NEXT_PUBLIC_`: it must remain server-side only.

Start Next.js:

```bash
npm run dev
```

Open <http://localhost:3000>.

## Try It

- Visit `http://localhost:3000`. The Next.js Server Component should fetch data from Flask and render the message.
- Visit `http://localhost:5000/api/hello` directly without an `Authorization` header. Flask should return `401 Unauthorized`.
- Test the Next.js server-side request at `http://localhost:3000/api/hello` only if you have implemented the optional Route Handler. In the Server Component approach, a separate Next.js API route is not required.

## Security Notes

- **CORS is not authentication.** CORS governs browser cross-origin access; it does not stop calls made with tools such as `curl` or Postman.
- **Keep secrets server-side.** Never use `NEXT_PUBLIC_` for the service token and never expose it in HTML, client components, browser requests, logs, or source control.
- **The shared token is a learning step, not the ideal production solution.** It is a static credential and needs secure storage, rotation, and careful handling.
- **A `401` response is not a network boundary.** If Flask is reachable from the Internet, other clients can still reach it; they should be rejected by authentication, but the service remains exposed.
- **Do not rely on CORS or an obscure URL to protect the API.** For production, combine authentication and authorization with network restrictions where appropriate.
- **Validate inputs and handle failures.** Add request validation, sensible timeouts, safe error responses, and tests as the API grows.
- **Do not log tokens.** Keep logs useful for troubleshooting without recording credentials or sensitive data.
- **Use HTTPS in deployed environments.** Local development uses HTTP; production service-to-service communication should use TLS.

## Potential Next Steps

This repository can be extended incrementally:

1. Add pytest tests for missing, invalid, and valid service tokens.
2. Add more Flask blueprints and centralize authentication at the appropriate blueprint or application level.
3. Add request validation, timeouts, structured logging, and correlation IDs.
4. Deploy the frontend and backend as separate Azure App Services.
5. Explore App Service Authentication (Easy Auth) with Microsoft Entra ID.
6. Replace the static shared token with service-to-service access tokens and validate issuer, audience, expiry, and permissions in Flask.
7. Consider Managed Identity where supported by the hosting and token-acquisition design.
8. Restrict direct network access to Flask where the Azure architecture supports it.
9. Add CI/CD checks and automated security tests.

## Disclaimer

This is an educational lab for learning frontend/backend communication and security concepts. Review the architecture, identity configuration, network exposure, secret management, and operational controls before using similar patterns in production.
