# menu_controller.py
import os
from flask import request, redirect, url_for, current_app, render_template, session
from model.menu_model import MenuModel

class MenuController:
    def __init__(self):
        self.model = MenuModel()

    def request_menu(self):
        menu_items = self.model.get_menu()
        if "username" in session:
            username = session['username']
            role = session["role"]
            return render_template("menu.html", items=menu_items, username=username, role=role)
        else:
            return render_template("menu.html", items=menu_items)
          
    def create_menu(self):
        return render_template("menu_form.html")

    def store_menu(self):
        # Retrieve form data
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        # Convert price to float
        if price:
            price = float(price)

        # Handle file upload
        image_file = request.files.get("image")
        image_filename = None

        if image_file and image_file.filename != "":
            # Optional: Validate file extension
            # e.g., only allow .jpg, .png, etc.
            allowed_extensions = {"jpg", "jpeg", "png", "gif"}
            ext = image_file.filename.rsplit(".", 1)[-1].lower()
            if ext in allowed_extensions:
                # Create a secure filename, store in static folder
                # Note: In production, consider using a unique name or timestamps
                image_filename = image_file.filename
                upload_path = os.path.join(
                    current_app.root_path, "static", "uploads", image_filename
                )
                image_file.save(upload_path)

        # Call model to store in DB
        self.model.store_menu(name, price, description, image_filename)

        # Redirect to the menu page
        return redirect(url_for("show_menu_list"))

    def list_menu(self):
        menu = self.model.get_menu()
        if "username" in session:
            username = session['username']
            role = session["role"]
            return render_template("list_menu.html", items=menu, username=username, role=role)
    
    def edit_menu(self, item_id):
     menu_item = self.model.get_menu_item_by_id(item_id)
     if menu_item:
        if request.method == 'POST':
            name = request.form['name']
            price = float(request.form['price'])  # Chuyển đổi giá trị thành float
            description = request.form['description']

            # Gọi phương thức update_menu để cập nhật thông tin
            return self.update_menu(item_id, name, price, description)

        return render_template('edit_menu.html', item=menu_item)
     return "Item not found", 404


    def update_menu(self, item_id, name, price, description):
     if self.model.update_menu_item(item_id, name, price, description):
        return redirect(url_for('show_menu_list'))  # Chuyển hướng về danh sách menu sau khi cập nhật
     else:
        return "Error updating menu item", 500

    
    def delete_menu(self, item_id):
        """
        Xóa món ăn từ cơ sở dữ liệu và chuyển hướng về danh sách món ăn.
        """
        self.model.delete_menu(item_id)
        return redirect(url_for("show_menu_list"))
    
    def buy_now(self, item_id):
        """
        Xử lý đơn hàng, bao gồm việc nhận thông tin từ form mua hàng và tính toán tổng giá tiền.
        """
        if request.method == 'POST':
            # Lấy thông tin từ form
            name = request.form.get("name")
            quantity = int(request.form.get("quantity"))
            price = float(request.form.get("price"))
            
            # Tính tổng giá tiền
            total_price = quantity * price
            
            # Lưu thông tin đơn hàng hoặc thực hiện các thao tác khác (ví dụ: lưu vào cơ sở dữ liệu)
            # Ví dụ có thể lưu vào một bảng đơn hàng hoặc gửi email
            self.model.store_order(name, quantity, price, total_price)

            # Trả về trang xác nhận đơn hàng
            return render_template("order_confirmation.html", name=name, quantity=quantity, total_price=total_price)
        
        else:
            # Lấy thông tin món ăn từ cơ sở dữ liệu (dùng ID)
            menu_item = self.model.get_menu_item_by_id(item_id)
            
            # Hiển thị form mua hàng
            return render_template("buy_now.html", item=menu_item)
        
    def request_menu(self):
     menu_items = self.model.get_menu()
    # Render 'menu.html' và pass menu_items dưới dạng 'items'
     return render_template("menu.html", items=menu_items)
    
    def search(self):
        keyword = request.args.get("search")
        print(keyword)
        menu_items = self.model.search_menu(keyword)
        print(menu_items)
        if "username" in session:
            username = session['username']
            role = session["role"]
            return render_template("search_menu.html", items=menu_items, username=username, role=role)
        else:
            return render_template("search_menu.html", items=menu_items)
    
   

    