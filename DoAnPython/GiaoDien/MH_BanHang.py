

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime


# MÀN HÌNH BÁN HÀNG

class MH_BanHang(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f4ef")
        self.controller = controller

        def update_time():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            label_time.config(text=now)
            label_time.after(1000, update_time)

        # FULL FRAME
        full_frame = tk.Frame(self, bg="#f9f4ef")
        full_frame.place(x=0, y=0, width=1280, height=640)

        # ===================== CÁC NÚT MENU =====================
        buttons_info = [
            ("TRANG CHỦ", 40),
            ("BÁN HÀNG", 200),
            ("QUẢN LÝ", 360),
            ("THỐNG KÊ", 520),
            ("CREDITS", 680)
        ]

        for text, xpos in buttons_info:
            tk.Button(
                self,
                text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851",
                fg="#fffffe",
                cursor="hand2",
                bd=3,
                relief="ridge"
            ).place(x=xpos, y=40, width=125, height=60)

        # ===================== NGÀY GIỜ =====================
        date_time_frame = tk.Frame(full_frame, bg="#f9f4ef")
        date_time_frame.place(x=860, y=0, width=220, height=40)

        global label_time
        label_time = tk.Label(
            date_time_frame,
            fg="#00214d",
            bg="#f9f4ef",
            font=("proxima-nova", 14, "bold")
        )
        label_time.pack(expand=True, anchor="nw")

        update_time()

        # ===================== TRẠNG THÁI BÀN =====================
        table_free = 20
        table_reserved = 0
        table_serve = 0

        table_free_var = StringVar(value=f"Bàn còn trống: {table_free:02d}")
        table_reserved_var = StringVar(value=f"Bàn đã đặt: {table_reserved:02d}")
        table_serve_var = StringVar(value=f"Bàn đang phục vụ: {table_serve:02d}")

        table_frame = tk.Frame(full_frame, bg="#f9f4ef")
        table_frame.place(x=860, y=40, width=220, height=60)

        tk.Label(table_frame, textvariable=table_free_var, fg="#716040",
                 font=("proxima-nova", 10, "bold"), bg="#f9f4ef").pack(anchor="w")
        tk.Label(table_frame, textvariable=table_reserved_var, fg="#716040",
                 font=("proxima-nova", 10, "bold"), bg="#f9f4ef").pack(anchor="w")
        tk.Label(table_frame, textvariable=table_serve_var, fg="#716040",
                 font=("proxima-nova", 10, "bold"), bg="#f9f4ef").pack(anchor="w")

        # ===================== QTV + ĐĂNG XUẤT =====================
        qtv_frame = tk.Frame(full_frame, bg="#f9f4ef")
        qtv_frame.place(x=1080, y=40, width=160, height=60)

        tk.Label(
            qtv_frame, text="QTV: nv001",
            fg="#716040", font=("proxima-nova", 12, "bold"),
            bg="#f9f4ef"
        ).place(x=0, y=0, width=160, height=30)


        # Nút đăng xuất sẽ chuyển về màn hình đăng nhập

        tk.Button(
            qtv_frame,
            text="Đăng xuất",
            font=("proxima-nova", 14, "bold"),
            bg="#8c7851", fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command=lambda: self.logout()
        ).place(x=0, y=30, width=160, height=30)

        # ===================== KHU VỰC BÁN HÀNG =====================
        bh_frame = tk.Frame(full_frame, bg="#eaddcf")
        bh_frame.place(x=0, y=120, width=1280, height=520)

        tk.Label(
            bh_frame,
            text="KHU VỰC BÁN HÀNG (BÀN, MENU,...)",
            fg="#716040", bg="#eaddcf",
            font=("proxima-nova", 22, "bold")
        ).pack(pady=150)

    def logout(self):
            from MH_DangNhap import MH_DangNhap
            self.controller.show_frame(MH_DangNhap)

