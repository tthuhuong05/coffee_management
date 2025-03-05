# app.py

from functools import wraps

from flask import Flask, render_template, request, session, redirect, url_for, abort, jsonify
from controller.menu_controller import MenuController
from controller.auth_controller import AuthController
from controller.user_controller import UserController
from controller.order_controller import OrderController
from manage_sql import add_image_column
from controller.attendant_controller import AttendantController

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_IN_PRODUCTION"
auth_controller = AuthController()
user_controller = UserController()
order_controller = OrderController()
attendant_controller = AttendantController()

@app.context_processor
def inject_user():
    return {
        'username': session.get('username'),
        'role': session.get('role')
    }


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if "username" not in session:
            return redirect(url_for("login"))  # or show an error

        # Check role
        if session.get("role") != "admin":
            return abort(403)  # or show a custom "Access Denied" message

        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
def show_menu():
    controller = MenuController()
    return controller.request_menu()


# as BACK SYSTEM
@app.route("/admin/menu/list")
@admin_required
def show_menu_list():
    controller = MenuController()
    return controller.list_menu()

@app.route("/admin/menu/create")
@admin_required
def create_menu():
    controller = MenuController()
    return controller.create_menu()

@app.route("/admin/menu/store", methods=['POST'])
@admin_required
def store_menu():
    controller = MenuController()
    return controller.store_menu()

@app.route("/search")
def search():
    controller = MenuController()
    return controller.search()

#APPLICATION AUTH
@app.route("/register", methods=["GET", "POST"])
def register():
    return auth_controller.register()

@app.route("/login", methods=["GET", "POST"])
def login():
    return auth_controller.login()

@app.route("/logout")
def logout():
    return auth_controller.logout()

@app.route("/menu/edit/<int:item_id>", methods=['GET', 'POST'])
def edit_menu(item_id):
    controller = MenuController()
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        # Cập nhật thông tin món ăn
        if controller.update_menu(item_id, name, float(price), description):
            return redirect('/admin/menu/list')  # Chuyển hướng về danh sách menu
        else:
            return "Error updating menu item", 500
    return controller.edit_menu(item_id)  # Hiển thị form chỉnh sửa


@app.route("/menu/delete/<int:item_id>", methods=['GET'])
def delete_menu(item_id):
    controller = MenuController()
    return controller.delete_menu(item_id)

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json  # Lấy dữ liệu từ frontend
    item_name = data.get('item_name')
    item_price = data.get('item_price')
    quantity = data.get('quantity')

    # Xử lý logic (lưu database, xác nhận đơn hàng, v.v.)
    total_price = item_price * quantity

    return jsonify({
        "message": "Order placed successfully!",
        "item_name": item_name,
        "quantity": quantity,
        "total_price": total_price
    })
    
@app.route('/category/<category>')
def category(category):
    template_name = f'category_{category}.html'
    return render_template(template_name, category=category)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/admin/users', methods=['GET'])
@admin_required
def user_list():
   return user_controller.list_users()

@app.route('/users/create', methods=['GET'])
def create_user_form():
     return user_controller.create_user_form()

@app.route('/users/create', methods=['POST'])
def store_user():
    return user_controller.store_user()

@app.route('/users/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    return user_controller.delete_user(user_id)

@app.route('/users/edit/<int:user_id>', methods=['GET'])
def edit_user_form(user_id):
    return user_controller.edit_user_form(user_id)

@app.route('/users/edit/<int:user_id>', methods=['POST'])
def update_user(user_id):
    return user_controller.update_user(user_id)

@app.route('/admin/orders', methods=['GET'])
def list_orders():
   return order_controller.list_orders()

@app.route("/admin/orders/create", methods=["GET"])
@admin_required
def create_order_form():
    return order_controller.create_order_form()

@app.route("/admin/orders/store", methods=["POST"])
@admin_required
def store_order():
    return order_controller.store_order()

@app.route("/admin/orders/edit/<int:order_id>", methods=["GET"])
@admin_required
def edit_order_form(order_id):
    return order_controller.edit_order_form(order_id)

@app.route("/admin/orders/update/<int:order_id>", methods=["POST"])
@admin_required
def update_order(order_id):
    return order_controller.update_order(order_id)

@app.route("/admin/orders/delete/<int:order_id>", methods=["GET"])
@admin_required
def delete_order(order_id):
    return order_controller.delete_order(order_id)

@app.route("/admin/attendant/list")
def show_attendant_list():
    return attendant_controller.list_attendants()

@app.route("/admin/attendant/create", methods=["GET"])
def create_attendant():
    return attendant_controller.create_attendant()

@app.route("/admin/attendant/store", methods=["POST"])
def store_attendant():
    return attendant_controller.store_attendant()

@app.route("/admin/attendant/edit/<int:attendant_id>", methods=["GET"])
def edit_attendant(attendant_id):
    return attendant_controller.edit_attendant(attendant_id)

@app.route("/admin/attendant/update/<int:attendant_id>", methods=["POST"])
def update_attendant(attendant_id):
    return attendant_controller.update_attendant(attendant_id)

@app.route("/admin/attendant/delete/<int:attendant_id>")
def delete_attendant(attendant_id):
    return attendant_controller.delete_attendant(attendant_id)
    
@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    customer_name = data.get('customer_name')
    items = data.get('items')
    quantity = data.get('quantity')
    price = data.get('price')
    
    order_controller.model.create_order(customer_name, items, quantity, price)
    
    return jsonify({
        'customer_name': customer_name,
        'items': items,
        'quantity': quantity,
        'price': price
    })

if __name__ == "__main__":
    app.run(debug=True)
