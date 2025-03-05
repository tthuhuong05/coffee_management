
import sqlite3

class MenuModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def store_menu(self, name, price, description, image_filename=None):
        """
        Insert a new menu item into the 'menus' table.
        `image_filename` is the name of the uploaded file (or None if not provided).
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO menus (name, price, description, image)
            VALUES (?, ?, ?, ?)
        """, (name, price, description, image_filename))

        connection.commit()
        connection.close()

    def get_menu(self):
        """
        Fetch all menu items.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, price, description, image FROM menus")
        results = cursor.fetchall()

        connection.close()

        menu_items = []
        for row in results:
            item_id, name, price, description, image = row
            menu_items.append({
                "id": item_id,
                "name": name,
                "price": price,
                "description": description,
                "image": image
            })
        return menu_items
    
    def edit_menu(self, item_id, name, price, description):
        """
        Update an existing menu item in the 'menus' table.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Cập nhật mục menu theo ID
        cursor.execute("""
            UPDATE menus
            SET name = ?, price = ?, description = ?
            WHERE id = ?
        """, (name, price, description, item_id))

        connection.commit()
        connection.close()
    
    def update_menu_item(self, item_id, name, price, description):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Kiểm tra xem mục có tồn tại không trước khi cập nhật
            cursor.execute("SELECT id FROM menus WHERE id = ?", (item_id,))
            if not cursor.fetchone():
                raise ValueError(f"Menu item with ID {item_id} does not exist.")

            # Cập nhật mục menu
            cursor.execute("""
                UPDATE menus
                SET name = ?, price = ?, description = ?
                WHERE id = ?
            """, (name, price, description, item_id))

            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            connection.close()
            return False
        except Exception as e:
            print(f"Error: {e}")
            connection.close()
            return False

    
    def delete_menu(self, item_id):
        """
        Xóa một món ăn khỏi cơ sở dữ liệu dựa trên ID.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM menus WHERE id = ?", (item_id,))
        connection.commit()
        connection.close()

    def get_menu_item_by_id(self, item_id):
        """
        Fetch a single menu item based on its ID.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, price, description FROM menus WHERE id = ?", (item_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            item_id, name, price, description = result
            return {
                "id": item_id,
                "name": name,
                "price": price,
                "description": description
            }
        return None
        
    def search_menu(self, keyword):
        """
        Tìm kiếm món ăn trong cơ sở dữ liệu theo từ khóa.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        keyword = f"%{keyword}%"  # Sử dụng ký tự % để tìm kiếm với wildcard
        print(f"Searching for: {keyword}")  # In ra từ khóa tìm kiếm để kiểm tra
        
        cursor.execute("""
            SELECT id, name, price, description, image
            FROM menus
            WHERE name LIKE ?
        """, (keyword,))

        results = cursor.fetchall()

        connection.close()

        menu_items = []
        for row in results:
            item_id, name, price, description, image = row
            menu_items.append({
                "id": item_id,
                "name": name,
                "price": price,
                "description": description,
                "image": image
            })
        
        return menu_items
