# Project: Test Repo

Python calculator library with Flask web frontend and comprehensive CI/CD.

## Structure

```
├── calculator.py          # Core math functions (add, subtract, multiply, divide, power)
├── test_calculator.py     # Unit tests for calculator module
├── web_app/               # Flask web application
│   ├── app.py             # Flask routes and API endpoints
│   ├── templates/         # Jinja2 HTML templates
│   └── static/            # CSS/JS assets
├── docs/                  # Project documentation
└── .github/workflows/     # CI/CD pipelines
```

## Commands

```bash
# Run tests
python -m pytest test_calculator.py -v

# Run calculator directly
python calculator.py

# Start web app (runs on port 5000)
cd web_app && python app.py

# Install web app dependencies
pip install -r web_app/requirements.txt
```

## Conventions

- Python 3.x with PEP 8 style
- Docstrings on all public functions
- Unit tests required for new functionality
- Use `ValueError` for input validation errors

## CI/CD Workflows

| Workflow | Purpose |
|----------|---------|
| `test.yml` | Run tests on push/PR |
| `deploy.yml` | Deploy to production |
| `multi-environment.yml` | Deploy to dev/staging/prod |
| `security-scan.yml` | Security vulnerability scanning |
| `codeql-analysis.yml` | Code quality analysis |

## API Endpoints (web_app)

- `GET /` - Calculator homepage
- `POST /calculate` - Perform calculation
  - Body: `{"num1": float, "num2": float, "operation": string}`
  - Operations: `add`, `subtract`, `multiply`, `divide`, `power`

## Security

- See `docs/SECURITY.md` for security policies
- PR checklist at `.github/SECURITY_CHECKLIST.md`
- CodeQL and security scanning enabled
