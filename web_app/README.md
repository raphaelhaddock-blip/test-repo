# Calculator Web App

A beautiful web-based calculator built with Flask.

## Features
- Addition, Subtraction, Multiplication, Division
- Power (exponentiation)
- Modern, responsive UI
- Real-time calculations
- Error handling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open your browser to:
```
http://localhost:5000
```

## Project Structure
```
web_app/
├── app.py              # Flask application
├── templates/
│   └── index.html      # HTML template
├── static/
│   └── style.css       # CSS styles
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## How It Works

1. **Backend (app.py)**: Flask server that imports our calculator functions
2. **Frontend (index.html)**: User interface with form inputs
3. **Styling (style.css)**: Modern gradient design
4. **API**: POST endpoint `/calculate` that processes operations

## Technologies
- Python 3.x
- Flask (web framework)
- HTML5
- CSS3
- JavaScript (Fetch API)