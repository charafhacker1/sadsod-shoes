import os, json, hashlib
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")   # ✅ تم التصحيح هنا

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SADSOD_SECRET", "CHANGE_ME_IN_PROD")

db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url or ("sqlite:///" + os.path.join(BASE_DIR, "sadsod.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =======================
# Helper: Load Wilayas safely
# =======================
def load_wilayas():
    path = os.path.join(DATA_DIR, "wilayas.json")
    if not os.path.exists(path):
        print("⚠ wilayas.json not found, returning empty list")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# =======================
# Models
# =======================

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False, default="نسائي")
    price = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShippingRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wilaya = db.Column(db.String(80), nullable=False)
    daira = db.Column(db.String(120))
    price = db.Column(db.Integer, default=0)
    eta = db.Column(db.String(80))

# =======================
# Routes
# =======================

@app.get("/")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)

@app.get("/checkout")
def checkout():
    wilayas = load_wilayas()   # ✅ آمن
    return render_template("checkout.html", wilayas=wilayas)

@app.get("/api/wilayas")
def api_wilayas():
    return jsonify(load_wilayas())

# =======================
# Seed
# =======================

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def seed():
    if AdminUser.query.count() == 0:
        db.session.add(AdminUser(username="admin", password_hash=hash_password("admin123")))

    if ShippingRate.query.count() == 0:
        for w in load_wilayas():
            db.session.add(ShippingRate(wilaya=w, daira=None, price=600, eta="24-72 ساعة"))

    db.session.commit()

with app.app_context():
    db.create_all()
    seed()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
