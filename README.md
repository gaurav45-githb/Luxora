# EliteDrive — Simple Luxury Car Rental

A simple Flask luxury car booking project.

## Pages
- Home
- Luxury Fleet
- Car Details
- Booking
- Login
- Register

## Current version
This version does **not** connect to PostgreSQL yet. Cars are stored in `CARS` inside `app.py` and users are temporarily stored in memory.

## Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Next database step
When the UI and Flask flow are finished, replace the temporary data with three SQLAlchemy/PostgreSQL tables:
`users`, `cars`, and `bookings`.
