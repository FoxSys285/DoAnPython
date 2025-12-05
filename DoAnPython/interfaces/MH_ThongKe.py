import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from objects.Ban import DanhSachBan

class MH_ThongKe(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f4ef")
        self.controller = controller


        # Khung toàn trang
        full_frame = tk.Frame(self, bg="#f9f4ef")
        full_frame.place(x=0, y=0, width=1280, height=640)

        # ========== MENU TRÊN CÙNG (giống BH) ==========
        self.menu_frame = tk.Frame(full_frame, bg="#f9f4ef")
        self.menu_frame.place(x=0, y=0, width=820, height=120)

        # Danh sách các nút chung
        common_buttons = [
            ("TRANG CHỦ", 40, lambda: controller.show_frame("MH_TrangChu")),
            ("BÁN HÀNG",  200, lambda: controller.show_frame("MH_BanHang")),

        ]
        
        # Tạo và đặt các nút chung
        for text, xpos, cmd in common_buttons:
            tk.Button(
                self.menu_frame, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe", cursor="hand2",
                bd=3, relief="ridge",
                command=cmd
            ).place(x=xpos, y=40, width=125, height=60)

        self.manager_buttons = []
        manager_buttons_info = [
            ("QUẢN LÝ", 360,  lambda: controller.show_frame("MH_QuanLy")), 
            ("THỐNG KÊ", 520,  lambda: controller.show_frame("MH_QuanLy")),
            ("CREDITS", 680,  lambda: controller.show_frame("MH_Credits"))
        ]
        
        for text, xpos, cmd in manager_buttons_info:
            btn = tk.Button(
                self.menu_frame, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe", cursor="hand2",
                bd=3, relief="ridge",
                command=cmd
            )
            
            self.manager_buttons.append(btn)

        # ========== NGÀY GIỜ bên phải ==========
        date_time_frame = tk.Frame(full_frame, bg="#f9f4ef")
        date_time_frame.place(x=1000, y=0, width=220, height=40)

        self.label_time = tk.Label(
            date_time_frame,
            fg="#00214d",
            bg="#f9f4ef",
            font=("proxima-nova", 14, "bold")
        )
        self.label_time.pack(expand=True, anchor="nw")

        def update_time():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            self.label_time.config(text=now)
            self.label_time.after(1000, update_time)
        update_time()

        # ========== QTV bên phải ==========
        qtv_frame = tk.Frame(full_frame, bg="#f9f4ef")
        qtv_frame.place(x=1020, y=40, width=160, height=60)

        self.label_qtv = tk.Label(
            qtv_frame,
            text="",
            fg="#716040", font=("proxima-nova", 12, "bold"),
            bg="#f9f4ef"
        )
        self.label_qtv.place(x=0, y=0, width=160, height=30)

        tk.Button(
            qtv_frame, text="Đăng xuất",
            font=("proxima-nova", 12, "bold"),
            bg="#8c7851", fg="#fffffe", cursor="hand2",
            bd=3, relief="ridge",
            command=lambda: controller.show_frame("MH_DangNhap")
        ).place(x=0, y=30, width=160, height=30)


        

    def on_show(self):
        self.update_user_display() 

    def update_user_display(self):
        
        current = self.controller.current_user
        if current:
            username = current.username
            user_role = current.role
        else:
            # Trường hợp lỗi/đăng xuất (fallback)
            username = "ADMIN"
            user_role = "Manager"
            
        # 1. Cập nhật tên QTV
        self.label_qtv.config(text=f"QTV: {username.upper()}")
        
        # 2. Xử lý nút đặc quyền (Manager)
        is_manager = user_role.lower() == "manager"
        
        # Danh sách tọa độ cho các nút đặc quyền
        manager_xpos = [360, 520, 680]
        
        for i, btn in enumerate(self.manager_buttons):
            if is_manager:
                # Hiện nút nếu là Manager
                btn.place(x=manager_xpos[i], y=40, width=125, height=60)
            else:
                # Ẩn nút nếu không phải Manager
                btn.place_forget()