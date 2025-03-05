from flask import render_template, request, redirect, url_for
from model.order_model import OrderModel

class OrderController:
    def __init__(self):
        self.model = OrderModel()

    def list_orders(self):
        orders = self.model.get_all_orders()
        return render_template("orders.html", orders=orders)

    def create_order_form(self):
        return render_template("order_form.html")

    def store_order(self):
        customer_name = request.form["customer_name"]
        items = request.form["items"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        self.model.create_order(customer_name, items, quantity, price)
        return redirect(url_for("list_orders"))

    def edit_order_form(self, order_id):
        order = self.model.get_order_by_id(order_id)
        return render_template("order_form.html", order=order)

    def update_order(self, order_id):
        customer_name = request.form["customer_name"]
        items = request.form["items"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        self.model.update_order(order_id, customer_name, items, quantity, price)
        return redirect(url_for("list_orders"))

    def delete_order(self, order_id):
        self.model.delete_order(order_id)
        return redirect(url_for("list_orders"))
