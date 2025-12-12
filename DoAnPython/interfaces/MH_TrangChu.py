import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from objects.Ban import DanhSachBan

class MH_TrangChu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f4ef")
        self.controller = controller

        # Dữ liệu bàn
        self.ds_ban = DanhSachBan()
        self.ds_ban.doc_file("data/du_lieu_ban.json")

        # Khung toàn trang
        full_frame = tk.Frame(self, bg="#f9f4ef")
        full_frame.place(x=0, y=0, width=1280, height=640)

        # ========== MENU TRÊN CÙNG (giống BH) ==========
        self.menu_frame = tk.Frame(full_frame, bg="#f9f4ef")
        self.menu_frame.place(x=0, y=0, width=860, height=120)

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
            ("THỐNG KÊ", 520,  lambda: controller.show_frame("MH_ThongKe")),
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
        date_time_frame.place(x=860, y=0, width=220, height=40)

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
        qtv_frame.place(x=1080, y=40, width=160, height=60)

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

        # ========== TRẠNG THÁI BÀN ngay dưới QTV ==========
        self.table_free_var = StringVar()
        self.table_reserved_var = StringVar()
        self.table_serve_var = StringVar()

        table_frame = tk.Frame(full_frame, bg="#f9f4ef")
        table_frame.place(x=860, y=40, width=220, height=60)

        tk.Label(table_frame, textvariable=self.table_free_var,
                fg="#716040", font=("proxima-nova", 10, "bold"),
                bg="#f9f4ef").pack(anchor="w")
        tk.Label(table_frame, textvariable=self.table_reserved_var,
                fg="#716040", font=("proxima-nova", 10, "bold"),
                bg="#f9f4ef").pack(anchor="w")
        tk.Label(table_frame, textvariable=self.table_serve_var,
                fg="#716040", font=("proxima-nova", 10, "bold"),
                bg="#f9f4ef").pack(anchor="w")

        # ========== VÙNG NỘI DUNG DƯỚI MENU (ảnh nền) ==========
        content_container = tk.Frame(full_frame, bg="#f9f4ef")
        content_container.place(x=0, y=120, width=1280, height=520)

        bg_path = "images/anh_nen.png"
        try:
            img_bg = Image.open(bg_path)
            img_bg = img_bg.resize((1280, 520), Image.Resampling.LANCZOS)
            self.bg_image_ref = ImageTk.PhotoImage(img_bg)
        except Exception as e:
            print("Lỗi ảnh nền:", e)
            self.bg_image_ref = None

        if self.bg_image_ref:
            image_label = tk.Label(content_container, image=self.bg_image_ref, bd=0)
            image_label.place(x=0, y=0, width=1280, height=520)
            image_label.image = self.bg_image_ref

    def update_table_status(self):
        table_free = self.ds_ban.free()
        table_reserved = self.ds_ban.booked()
        table_serve = self.ds_ban.serve()

        self.table_free_var.set(f"Bàn còn trống: {table_free:02d}")
        self.table_reserved_var.set(f"Bàn đã đặt: {table_reserved:02d}")
        self.table_serve_var.set(f"Bàn đang phục vụ: {table_serve:02d}")

    def on_show(self):
        self.ds_ban.doc_file("data/du_lieu_ban.json")
        self.update_user_display() 
        self.update_table_status()

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