import sqlite3

class AttendantModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def create_table():
     connection = sqlite3.connect("database.db")  # Đảm bảo đường dẫn đến database đúng
     cursor = connection.cursor()
    
    # Câu lệnh SQL để tạo bảng attendants
     cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        role TEXT NOT NULL,
        work_days TEXT NOT NULL
    )
    """)
    
     connection.commit()
     connection.close()

# Gọi hàm này để tạo bảng
    create_table()


    def get_all_attendants(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, phone, role, work_days FROM attendants")
        results = cursor.fetchall()
        connection.close()

        attendants = []
        for row in results:
            attendants.append({
                "id": row[0],
                "name": row[1],
                "phone": row[2],
                "role": row[3],
                "work_days": row[4]
            })
        return attendants

    def store_attendant(self, name, phone, role, work_days):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO attendants (name, phone, role, work_days)
            VALUES (?, ?, ?, ?)
        """, (name, phone, role, work_days))
        connection.commit()
        connection.close()

    def get_attendant_by_id(self, attendant_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, phone, role, work_days FROM attendants WHERE id = ?", (attendant_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            return {
                "id": result[0],
                "name": result[1],
                "phone": result[2],
                "role": result[3],
                "work_days": result[4]
            }
        return None

    def update_attendant(self, attendant_id, name, phone, role, work_days):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE attendants
            SET name = ?, phone = ?, role = ?, work_days = ?
            WHERE id = ?
        """, (name, phone, role, work_days, attendant_id))
        connection.commit()
        connection.close()

    def delete_attendant(self, attendant_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM attendants WHERE id = ?", (attendant_id,))
        connection.commit()
        connection.close()
