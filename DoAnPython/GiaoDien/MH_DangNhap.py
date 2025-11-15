
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime


# MÀN HÌNH ĐĂNG NHẬP




class MH_DangNhap(tk.Frame):
    def __init__(self, parent, controller):
        self.tb_text = tk.StringVar(value = "") # Thông báo đăng nhập

        du_lieu_dang_nhap = {"admin": "123456"}

        super().__init__(parent, bg="#f9f4ef")
        self.controller = controller

        full_frame = tk.Frame(self, bg="#f9f4ef")
        full_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # ===================== TIÊU ĐỀ =====================
        hien_thi = tk.Frame(self, bg="#f9f4ef")
        hien_thi.place(x=470, y=340)

        tk.Label(
            hien_thi, text="Đăng nhập - Giao ca",
            fg="#990000", bg="#f9f4ef",
            font=("proxima-nova", 25, "bold")
        ).pack(fill="both", expand=True)

        # ===================== KHUNG ĐĂNG NHẬP =====================
        dang_nhap_frame = tk.Frame(self, bg="#f9f4ef")
        dang_nhap_frame.place(x=470, y= 400, width=300, height=60)

        tk.Label(dang_nhap_frame, text="Username",
                 bg="#f9f4ef", fg="#003300",
                 font=("proxima-nova", 12, "bold")).place(x=0, y=0, width=100)
        username_entry = tk.Entry(dang_nhap_frame, width=30,
                                  font=("proxima-nova", 13))
        username_entry.place(x=100, y=0)

        tk.Label(dang_nhap_frame, text="Password",
                 bg="#f9f4ef", fg="#003300",
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

            tb_frame = tk.Frame(self, bg = "#f9f4ef", height = 30, width = 350) # Frame xử lí thông báo khi đăng nhập
            tb_label = tk.Label(tb_frame, textvariable = self.tb_text, font=("proxima-nova", 12), fg = "red", bg = "#f9f4ef")
            tb_label.pack(side = LEFT)
            tb_frame.place(x=470, y = 300)


            username = username_entry.get()
            password = password_entry.get()

            if username in du_lieu_dang_nhap:
                if du_lieu_dang_nhap[username] == password:
                    print("Đăng nhập thành công")
                    self.tb_text.set("")
                    from MH_BanHang import MH_BanHang
                    controller.show_frame(MH_BanHang)
                else:
                    print("Sai mật khẩu.")
                    self.tb_text.set("Sai mật khẩu.")
                reset(username_entry, password_entry)
            elif not username:
                print("Bạn chưa nhập tài khoản.")
                self.tb_text.set("Bạn chưa nhập tài khoản.")
            elif username and not password:
                print("Bạn chưa nhập mật khẩu.")
                self.tb_text.set("Bạn chưa nhập mật khẩu.")
            else:
                print("Sai tài khoản hoặc mật khẩu. Hãy kiểm tra lại")
                self.tb_text.set("Sai tài khoản hoặc mật khẩu. Hãy kiểm tra lại.")
                reset(username_entry, password_entry)

            



        # ===================== HÌNH ẢNH =====================
        img = Image.open("name_cafe.png")
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
            command=login
        ).place(x=570, y=460, width=90, height=25)

        # ===================== NÚT THOÁT =====================
        tk.Button(
            self, text="Thoát",
            bg="#fffffe", fg="#e45858",
            font=("proxima-nova", 10, "bold"),
            command=controller.destroy
        ).place(x=680, y=460, width=90, height=25)
