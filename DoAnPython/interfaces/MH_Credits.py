import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from objects.Ban import DanhSachBan

class MH_Credits(tk.Frame):
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


        main_frame = tk.Frame(full_frame, bg = "white")
        main_frame.place(x = 20, y =120, width = 1240, height = 500)
        
        tk.Label(main_frame, text = "THÔNG TIN ĐỒ ÁN", font=("proxima-nova", 26, "bold"),bg="white").place(x = 370, y = 20, width = 500, height = 60)

        boder_frame = tk.Frame(main_frame, bg = "#f9f4ef", bd = 5, relief = "ridge")
        boder_frame.place(x = 100, y = 100, width = 1040, height = 340)

        cross_bar_1_frame = tk.Frame(boder_frame, bg="#eaddcf")
        cross_bar_1_frame.place(x = 520, y = 0 ,width = 10, height = 330)

        tk.Label(boder_frame, text = "Môn: Lập trình Python",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 10)
        tk.Label(boder_frame, text = "Đồ án: Ứng dụng quản lý quán cafe mini",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 50)
        tk.Label(boder_frame, text = "Yêu cầu:",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 90)
        tk.Label(boder_frame, text = "      -  Sử dụng ngôn ngữ lập trình Python và thư viện",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 130)
        tk.Label(boder_frame, text = "          tkinter để tạo giao diện người dùng.",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 170)
        tk.Label(boder_frame, text = "      -  Ứng dụng là một hệ thống quản lý thông tin với",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 210)
        tk.Label(boder_frame, text = "          các chức năng CRUD, sử dụng file JSON để",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 250)
        tk.Label(boder_frame, text = "          lưu trữ dữ liệu thay vì sử dụng CSDL.",font=("proxima-nova", 14, "bold"),bg="#f9f4ef").place(x = 10, y = 290)

        cross_bar_2_frame = tk.Frame(boder_frame, bg="#eaddcf")
        cross_bar_2_frame.place(x = 540, y = 155 ,width = 480, height = 10)
        
        tk.Label(boder_frame, text = "THÀNH VIÊN 1", bg = "#f9f4ef", font=("proxima-nova", 18, "bold")).place(x = 560, y = 20)
        tk.Label(boder_frame, text = "THÀNH VIÊN 2", bg = "#f9f4ef",font=("proxima-nova", 18, "bold")).place(x = 560, y = 185)

        tk.Label(boder_frame, text = "Họ tên: Nguyễn Thành Nam",bg = "#f9f4ef",font=("proxima-nova", 14, "bold")).place(x = 560, y = 70)
        tk.Label(boder_frame, text = "MSSV: 2001240286",bg = "#f9f4ef",font=("proxima-nova", 14, "bold")).place(x = 560, y = 110)

        tk.Label(boder_frame, text = "Họ tên: Trần Nguyên",bg = "#f9f4ef",font=("proxima-nova", 14, "bold")).place(x = 560, y = 235)
        tk.Label(boder_frame, text = "MSSV: 2001240313",bg = "#f9f4ef",font=("proxima-nova", 14, "bold")).place(x = 560, y = 275)


    def on_show(self):
        self.update_user_display() 

    def update_user_display(self):
        """Cập nhật tên QTV và hiển thị/ẩn các nút đặc quyền dựa trên role."""
        
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