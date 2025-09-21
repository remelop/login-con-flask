from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from conexion.conexion import get_db_connection
from models import Usuario

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

# Página principal protegida
@app.route("/")
@login_required
def home():
    return render_template("home.html", nombre=current_user.nombre)

# Registro de usuario
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                       (nombre, email, password))
        conn.commit()
        conn.close()
        
        flash("Usuario registrado con éxito. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

# Login de usuario
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = Usuario.obtener_por_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template("login.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
