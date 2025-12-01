from objects.TaiKhoan import TaiKhoan, DanhSachTaiKhoan

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime


# MÀN HÌNH ĐĂNG NHẬP
class MH_DangNhap(tk.Frame):
    def __init__(self, parent, controller):

        dulieu_path = "data/du_lieu_tk.json"

        self.tb_text = tk.StringVar(value = "") # Thông báo đăng nhập

        list_user = DanhSachTaiKhoan()
        list_user.doc_file(dulieu_path) 

        super().__init__(parent, bg="#FCFAE5")
        self.controller = controller

        full_frame = tk.Frame(self, bg="#FCFAE5")
        full_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # ===================== TIÊU ĐỀ =====================
        hien_thi = tk.Frame(self, bg="#FCFAE5")
        hien_thi.place(x=470, y=340)

        tk.Label(
            hien_thi, text="Đăng nhập - Giao ca",
            fg="#990000", bg="#FCFAE5",
            font=("proxima-nova", 25, "bold")
        ).pack(fill="both", expand=True)

        # ===================== KHUNG ĐĂNG NHẬP =====================
        dang_nhap_frame = tk.Frame(self, bg="#FCFAE5")
        dang_nhap_frame.place(x=470, y= 400, width=300, height=60)

        tk.Label(dang_nhap_frame, text="Username",
                 bg="#FCFAE5", fg="#003300",
                 font=("proxima-nova", 12, "bold")).place(x=0, y=0, width=100)
        username_entry = tk.Entry(dang_nhap_frame, width=30,
                                  font=("proxima-nova", 13))
        username_entry.place(x=100, y=0)

        tk.Label(dang_nhap_frame, text="Password",
                 bg="#FCFAE5", fg="#003300",
                 font=("proxima-nova", 12, "bold")).place(x=0, y=30, width=100)
        password_entry = tk.Entry(dang_nhap_frame, width=30,
                                  font=("proxima-nova", 13), show="*")
        password_entry.place(x=100, y=30)

        def reset(username_entry, password_entry):
            self.tb_text.set("") 
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

        # Xử lí dữ liệu đăng nhập

        def login():
            tb_frame = tk.Frame(self, bg="#FCFAE5", height=30, width=350)
            tb_label = tk.Label(tb_frame, textvariable=self.tb_text,font=("proxima-nova", 12), fg="red", bg="#FCFAE5")
            tb_label.pack(side=LEFT)
            tb_frame.place(x=470, y=300)
            username = username_entry.get()
            password = password_entry.get()
            if not username:
                self.tb_text.set("Bạn chưa nhập tài khoản.")
                return
            if username and not password:
                self.tb_text.set("Bạn chưa nhập mật khẩu.")
                return


            is_successful, result_data = list_user.check_login(username, password)
    
            if is_successful:
                self.tb_text.set("")
                
                # result_data ở đây là đối tượng TaiKhoan (bao gồm cả role)
                controller.current_user = result_data
                controller.username = username
                controller.role = result_data.role
                print(f"Đăng nhập thành công! Quyền: {result_data.role}") 
                # Chuyển màn hình  
                self.current_page = "MH_TrangChu"
                controller.show_frame("MH_TrangChu")
                reset(username_entry, password_entry)
            else:
                # Nếu đăng nhập thất bại, result_data là thông báo lỗi (chuỗi)
                self.tb_text.set(result_data)

        # ===================== HÌNH ẢNH =====================
        path_img = "images/name_cafe.png"
        img = Image.open(path_img)
        img = img.resize((700, 200), Image.Resampling.LANCZOS)
        name_img = ImageTk.PhotoImage(img)
        label_img = tk.Label(self, image=name_img, bd=0)
        label_img.image = name_img
        label_img.place(x=290, y=100)

        # ===================== NÚT ĐĂNG NHẬP =====================
        tk.Button(
            self, text="Đăng nhập",
            bg="#fffffe", fg="#e45858",
            font=("proxima-nova", 10, "bold"),
            default='active',
            command=login
        ).place(x=570, y=460, width=90, height=25)

        # ===================== NÚT THOÁT =====================
        tk.Button(
            self, text="Thoát",
            bg="#fffffe", fg="#e45858",
            font=("proxima-nova", 10, "bold"),
            default='active',
            command=controller.destroy
        ).place(x=680, y=460, width=90, height=25)

