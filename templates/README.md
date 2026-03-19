# NexRate — Currency & Finance Intelligence Dashboard

A full-stack web application built with Python and Flask that provides live currency exchange rates, interactive trend charts, a currency converter, and a personal watchlist.

🌐 **Live Demo:** [nexrate.onrender.com](https://nexrate.onrender.com)

---

## Features

- User registration and login with secure hashed passwords
- Protected dashboard that requires authentication to access
- Live currency exchange rates fetched from ExchangeRate API
- Currency converter supporting all major currencies
- Interactive 7-day trend chart built with Chart.js
- Personal watchlist to save favourite currency pairs
- Profile page showing account details and saved pairs
- Fully responsive layout for mobile and desktop
- Clean professional UI with dark theme

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite with SQLAlchemy ORM |
| Authentication | Flask-Login, Werkzeug |
| Frontend | HTML5, CSS3, Jinja2 |
| Charts | Chart.js |
| API | ExchangeRate API |
| Deployment | Render |

---

## Project Structure
```
NexRate/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   └── profile.html
├── static/
│   └── style.css
├── app.py
├── models.py
├── requirements.txt
├── Procfile
└── .env
```

---

## Local Setup
```bash
# Clone the repository
git clone https://github.com/shayanali1/NexRate.git
cd NexRate

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "SECRET_KEY=your_secret_key" > .env
echo "EXCHANGE_API_KEY=your_api_key" >> .env

# Run the application
python app.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session secret key |
| `EXCHANGE_API_KEY` | API key from exchangerate-api.com |

---

## Screenshots

### Landing Page
![Landing Page](screenshots/landing.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Profile
![Profile](screenshots/profile.png)

---

## Author

**Syed Muhammad Shayan Ali**
- GitHub: [@shayanali1](https://github.com/shayanali1)
- Previous Project: [Ethical Link](https://ethical-link.onrender.com)

---

## License

This project is open source and available under the [MIT License](LICENSE).