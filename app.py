from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config["SECRET_KEY"] = "elitedrive-secret-key"

# ============================================================
# DATABASE CONFIGURATION
# ============================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:Gaurav%403512@localhost:5432/elitedrive"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ============================================================
# 1. USER MODEL
# ============================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    phone = db.Column(db.String(15), nullable=False)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship with bookings
    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )


# ============================================================
# 2. CAR MODEL
# ============================================================

class Car(db.Model):
    __tablename__ = "cars"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    type = db.Column(db.String(50), nullable=False)

    price = db.Column(db.Integer, nullable=False)

    city = db.Column(db.String(50), nullable=False)

    seats = db.Column(db.Integer, nullable=False)

    transmission = db.Column(
        db.String(30),
        nullable=False
    )

    fuel = db.Column(
        db.String(30),
        nullable=False
    )

    rating = db.Column(
        db.Float,
        default=0
    )

    image = db.Column(
        db.String(500),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Available"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship with bookings
    bookings = db.relationship(
        "Booking",
        backref="car",
        lazy=True
    )


# ============================================================
# 3. BOOKING MODEL
# ============================================================

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    car_id = db.Column(
        db.Integer,
        db.ForeignKey("cars.id"),
        nullable=False
    )

    pickup_location = db.Column(
        db.String(150),
        nullable=False
    )

    dropoff_location = db.Column(
        db.String(150),
        nullable=False
    )

    pickup_date = db.Column(
        db.Date,
        nullable=False
    )

    return_date = db.Column(
        db.Date,
        nullable=False
    )

    pickup_time = db.Column(
        db.Time,
        nullable=False
    )

    driver_age = db.Column(
        db.Integer,
        nullable=False
    )

    total_amount = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ============================================================
# TEMPORARY CAR DATA
# ============================================================

CARS = [
    {
        "id": 1,
        "name": "Lamborghini Huracán",
        "type": "Supercar",
        "price": 28000,
        "city": "Mumbai",
        "seats": 2,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&w=1200&q=85"
    },

    {
        "id": 2,
        "name": "Ferrari 296 GTB",
        "type": "Supercar",
        "price": 32000,
        "city": "Delhi",
        "seats": 2,
        "transmission": "Automatic",
        "fuel": "Hybrid",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&w=1200&q=85"
    },

    {
        "id": 3,
        "name": "Rolls-Royce Ghost",
        "type": "Luxury Sedan",
        "price": 45000,
        "city": "Mumbai",
        "seats": 5,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "rating": 5.0,
        "image": "https://assets.bwbx.io/images/users/iqjWHBFdfxIU/iTeZ8fQK4hhI/v1/-1x-1.jpg"
    },

    {
        "id": 4,
        "name": "Mercedes-Benz S-Class",
        "type": "Luxury Sedan",
        "price": 18000,
        "city": "Bengaluru",
        "seats": 5,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=85"
    },

    {
        "id": 5,
        "name": "Porsche 911 Turbo S",
        "type": "Sports Car",
        "price": 26000,
        "city": "Pune",
        "seats": 4,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "rating": 4.9,
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=85"
    },

    {
        "id": 6,
        "name": "BMW M8 Competition",
        "type": "Sports Car",
        "price": 22000,
        "city": "Hyderabad",
        "seats": 4,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=85"
    },

    {
        "id": 7,
        "name": "Range Rover Autobiography",
        "type": "SUV",
        "price": 24000,
        "city": "Delhi",
        "seats": 5,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1200&q=85"
    },

    {
        "id": 8,
        "name": "Tesla Model S",
        "type": "Electric",
        "price": 15000,
        "city": "Bengaluru",
        "seats": 5,
        "transmission": "Automatic",
        "fuel": "Electric",
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=1200&q=85"
    }
]


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_car(car_id):
    return Car.query.get(car_id)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    featured_cars = Car.query.limit(6).all()

    total_cars = Car.query.count()

    return render_template(
        "index.html",
        featured_cars=featured_cars,
        total_cars=total_cars
    )


# ============================================================
# FLEET
# ============================================================

@app.route("/fleet")
def fleet():

    cars = Car.query.all()

    return render_template(
        "fleet.html",
        cars=cars
    )


# ============================================================
# CAR DETAILS
# ============================================================

@app.route("/car-details/<int:car_id>")
def car_details(car_id):

    car = get_car(car_id)

    if not car:

        flash(
            "Car not found.",
            "danger"
        )

        return redirect(
            url_for("fleet")
        )

    return render_template(
        "car-details.html",
        car=car
    )


# ============================================================
# BOOKING
# ============================================================

@app.route("/booking", methods=["GET", "POST"])
def booking():

    if "user_id" not in session:

        flash(
            "Please login before making a booking.",
            "danger"
        )

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        car_id = request.form.get(
            "car_id",
            type=int
        )

        pickup_location = request.form.get(
            "pickup_location"
        )

        dropoff_location = request.form.get(
            "dropoff_location"
        )

        pickup_date = request.form.get(
            "pickup_date"
        )

        return_date = request.form.get(
            "return_date"
        )

        pickup_time = request.form.get(
            "pickup_time"
        )

        driver_age = request.form.get(
            "driver_age",
            type=int
        )

        if not all([
            car_id,
            pickup_location,
            dropoff_location,
            pickup_date,
            return_date,
            pickup_time,
            driver_age
        ]):

            flash(
                "Please fill in all required booking fields.",
                "danger"
            )

            return redirect(
                url_for(
                    "booking",
                    car_id=car_id
                )
            )

        car = Car.query.get(car_id)

        if not car:

            flash(
                "Selected car is not available.",
                "danger"
            )

            return redirect(
                url_for("fleet")
            )

        # Calculate number of rental days
        from datetime import date

        start_date = date.fromisoformat(
            pickup_date
        )

        end_date = date.fromisoformat(
            return_date
        )

        days = (
            end_date - start_date
        ).days

        if days <= 0:
            days = 1

        total_amount = car.price * days

        new_booking = Booking(

            user_id=session["user_id"],

            car_id=car.id,

            pickup_location=pickup_location,

            dropoff_location=dropoff_location,

            pickup_date=start_date,

            return_date=end_date,

            pickup_time=datetime.strptime(
                pickup_time,
                "%H:%M"
            ).time(),

            driver_age=driver_age,

            total_amount=total_amount,

            status="Pending"
        )

        db.session.add(new_booking)

        db.session.commit()

        flash(
            "Booking request submitted successfully!",
            "success"
        )

        return redirect(
            url_for(
                "booking",
                car_id=car.id
            )
        )

    selected_car_id = request.args.get(
        "car_id",
        type=int
    )

    cars = Car.query.all()

    return render_template(
        "booking.html",
        cars=cars,
        selected_car_id=selected_car_id
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.password == password:

            session["user_id"] = user.id

            session["user_email"] = user.email

            session["user_name"] = user.name

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                url_for("home")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not all([
            name,
            email,
            phone,
            password,
            confirm_password
        ]):

            flash(
                "Please fill in all fields.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "An account with this email already exists.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        new_user = User(

            name=name,

            email=email,

            phone=phone,

            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )



#DASHBOARD-------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please login to access your dashboard.", "danger")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        flash("Please login again.", "danger")
        return redirect(url_for("login"))

    bookings = Booking.query.filter_by(
        user_id=user.id
    ).order_by(
        Booking.created_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        user=user,
        bookings=bookings
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# CREATE DATABASE TABLES + INSERT CARS
# ============================================================

def seed_cars():

    if Car.query.count() > 0:
        return

    for car_data in CARS:

        car = Car(
            name=car_data["name"],
            type=car_data["type"],
            price=car_data["price"],
            city=car_data["city"],
            seats=car_data["seats"],
            transmission=car_data["transmission"],
            fuel=car_data["fuel"],
            rating=car_data["rating"],
            image=car_data["image"],
            status="Available"
        )

        db.session.add(car)

    db.session.commit()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        seed_cars()

    app.run(host="0.0.0.0", port=5081, debug=True)