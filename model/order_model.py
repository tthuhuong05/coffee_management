import sqlite3

class OrderModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_all_orders(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        conn.close()
        return orders

    def create_order(self, customer_name, items, quantity, price):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_name, items, quantity, price)
            VALUES (?, ?, ?, ?)""",
            (customer_name, items, quantity, price))
        conn.commit()
        conn.close()

    def update_order(self, order_id, customer_name, items, quantity, price):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders
            SET customer_name = ?, items = ?, quantity = ?, price = ?
            WHERE id = ?""",
            (customer_name, items, quantity, price, order_id))
        conn.commit()
        conn.close()

    def delete_order(self, order_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
        conn.close()

    def get_order_by_id(self, order_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        conn.close()
        return order
