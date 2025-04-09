from flask import Blueprint, render_template, request, redirect, url_for

admin_login_bp = Blueprint('admin_login_bp', __name__)

@admin_login_bp.route('/admin_login_page')
def admin_login_page():
    return render_template("admin_login.html")

@admin_login_bp.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == "admin_gah@gmail.com" and password == "Qwert@1234":
        return redirect(url_for('admin_dashboard_bp.admin_dashboard'))
    else:
        return render_template("error.html", message="✗ Invalid credentials! Please try again.")
