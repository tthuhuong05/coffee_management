from flask import render_template, request, redirect, url_for
from model.attendant_model import AttendantModel

class AttendantController:
    def __init__(self):
        self.model = AttendantModel()

    def list_attendants(self):
        # Lấy danh sách tất cả attendants từ model và render template
        attendants = self.model.get_all_attendants()
        return render_template("list_attend.html", attendants=attendants)

    def create_attendant(self):
        # Hiển thị form để tạo một attendant mới
        return render_template("attend_form.html")

    def store_attendant(self):
        # Lấy thông tin từ form và lưu vào database
        name = request.form.get("name")
        phone = request.form.get("phone")
        role = request.form.get("role")
        work_days = request.form.get("work_days")
        self.model.store_attendant(name, phone, role, work_days)
        return redirect(url_for("show_attendant_list"))

    def edit_attendant(self, attendant_id):
        # Lấy thông tin của một attendant cụ thể để chỉnh sửa
        attendant = self.model.get_attendant_by_id(attendant_id)
        if not attendant:
            return "Attendant not found", 404
        return render_template("edit_attendant.html", attendant=attendant)

    def update_attendant(self, attendant_id):
        # Lấy thông tin từ form và cập nhật vào database
        name = request.form.get("name")
        phone = request.form.get("phone")
        role = request.form.get("role")
        work_days = request.form.get("work_days")
        self.model.update_attendant(attendant_id, name, phone, role, work_days)
        return redirect(url_for("show_attendant_list"))

    def delete_attendant(self, attendant_id):
        # Xóa một attendant dựa trên ID
        self.model.delete_attendant(attendant_id)
        return redirect(url_for("show_attendant_list"))
