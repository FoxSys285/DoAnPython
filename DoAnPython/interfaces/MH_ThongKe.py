import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from objects.Ban import DanhSachBan
from objects.HoaDon import DanhSachHoaDon
from tkinter import ttk
from tkcalendar import DateEntry

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

    ########  Tạo Khung và Danh Sách hóa đơn ##############
        self.ds_hoa_don = DanhSachHoaDon()
        self.ds_hoa_don.doc_file("data/du_lieu_hoa_don.json")

        # 1) Khung hóa đơn
        self.frame_hoa_don = tk.Frame(full_frame, bg="#fffffe", bd=2, relief="groove")
        self.label_tieu_de_hd = tk.Label(
            full_frame,
            text="Thống kê theo hóa đơn",
            font=("Arial", 14, "bold"),
            fg="#b00020",        # màu đỏ đậm
            bg="#f9f4ef",
            anchor="center"
        )
        self.label_tieu_de_hd.place(x=240, y=160, width=250)
        self.frame_hoa_don.place(x=40, y=190, width=600, height=250)
    
        # 2) Frame nội + scrollbars + treeview (grid)
        self.tree_frame_hd = tk.Frame(self.frame_hoa_don, bg="#fffffe")
        self.tree_frame_hd.pack(fill="both", expand=True)

        columns_hd = ("ma_hd", "thoi_gian", "tien_mon", "giam_gia", "thanh_tien", "diem_ban", "cac_mon")

        self.scroll_y = ttk.Scrollbar(self.tree_frame_hd, orient="vertical")
        self.scroll_x = ttk.Scrollbar(self.tree_frame_hd, orient="horizontal")

        self.tree_hoa_don = ttk.Treeview(
            self.tree_frame_hd,
            columns=columns_hd,
            show="headings",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )
        self.scroll_y.config(command=self.tree_hoa_don.yview)
        self.scroll_x.config(command=self.tree_hoa_don.xview)

        self.tree_hoa_don.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.tree_frame_hd.rowconfigure(0, weight=1)
        self.tree_frame_hd.columnconfigure(0, weight=1)

        # 3) Cấu hình cột
        col_widths = {
            "ma_hd": 130, "thoi_gian": 140, "tien_mon": 90,
            "giam_gia": 90, "thanh_tien": 110, "diem_ban": 80, "cac_mon": 300
        }
        for col in columns_hd:
            self.tree_hoa_don.heading(col, text=col.upper())
            self.tree_hoa_don.column(col, width=col_widths[col], anchor="center", stretch=False)

        # 4) Label tổng kết (tạo TRƯỚC khi on_show có thể chạy)
        self.label_tong_ket = tk.Label(
            full_frame,
            text="",  # để trống ban đầu
            font=("Arial", 14, "bold"),
            bg="#f9f4ef",        
            fg="#00214d",         
            justify="left",      
            anchor="nw",         
            bd=2, relief="groove" 
        )
        self.label_tong_ket.place(x=40, y=460, width=600, height=120)

        # ======= Tiêu đề bảng thống kê theo món =======
        self.label_tieu_de_mon = tk.Label(
            full_frame,
            text="Thống kê theo món",
            font=("Arial", 14, "bold"),
            fg="#b00020",
            bg="#f9f4ef",
            anchor="center"
        )
        self.label_tieu_de_mon.place(x=860, y=160, width=200)

        # ======= Khung bảng thống kê theo món =======
        self.frame_thong_ke_mon = tk.Frame(full_frame, bg="#fffffe", bd=2, relief="groove")
        self.frame_thong_ke_mon.place(x=660, y=190, width=600, height=250)

        self.label_tong_mon = tk.Label(
            full_frame,
            text="",  # để trống ban đầu
            font=("Arial", 12, "bold"),
            bg="#f9f4ef",
            fg="#00214d",
            anchor="w",
            justify="left",
            bd=2, relief="groove"
        )
        self.label_tong_mon.place(x=660, y=460, width=600, height=40)

        self.tree_frame_mon = tk.Frame(self.frame_thong_ke_mon, bg="#fffffe")
        self.tree_frame_mon.pack(fill="both", expand=True)

        columns_mon = ("ten_mon", "dvt", "so_luong", "doanh_thu")

        self.scroll_y_mon = ttk.Scrollbar(self.tree_frame_mon, orient="vertical")
        self.scroll_x_mon = ttk.Scrollbar(self.tree_frame_mon, orient="horizontal")

        self.tree_thong_ke_mon = ttk.Treeview(
            self.tree_frame_mon,
            columns=columns_mon,
            show="headings",
            yscrollcommand=self.scroll_y_mon.set,
            xscrollcommand=self.scroll_x_mon.set
        )
        self.scroll_y_mon.config(command=self.tree_thong_ke_mon.yview)
        self.scroll_x_mon.config(command=self.tree_thong_ke_mon.xview)

        self.tree_thong_ke_mon.grid(row=0, column=0, sticky="nsew")
        self.scroll_y_mon.grid(row=0, column=1, sticky="ns")
        self.scroll_x_mon.grid(row=1, column=0, sticky="ew")

        self.tree_frame_mon.rowconfigure(0, weight=1)
        self.tree_frame_mon.columnconfigure(0, weight=1)

        # Cấu hình cột
        col_widths_mon = {
            "ten_mon": 200,
            "dvt": 80,
            "so_luong": 80,
            "doanh_thu": 150
        }
        for col in columns_mon:
            self.tree_thong_ke_mon.heading(col, text=col.upper())
            self.tree_thong_ke_mon.column(col, width=col_widths_mon[col], anchor="center", stretch=False)

        # ======= Khung chọn ngày nằm ngang =======
        self.frame_chon_ngay = tk.Frame(full_frame, bg="#f9f4ef")
        self.frame_chon_ngay.place(x=360, y=120, width=520, height=40)

        # ======= Label "Từ ngày" =======
        self.label_tu_ngay = tk.Label(self.frame_chon_ngay, text="Từ ngày", font=("Arial", 11, "bold"), bg="#f9f4ef", fg="#00214d")
        self.label_tu_ngay.place(x=0, y=5)

        # ======= DateEntry chọn từ ngày =======
        self.entry_tu_ngay = DateEntry(self.frame_chon_ngay, font=("Arial", 11), date_pattern="dd/MM/yyyy")
        self.entry_tu_ngay.place(x=70, y=5, width=120)

        # ======= Label "Đến ngày" =======
        self.label_den_ngay = tk.Label(self.frame_chon_ngay, text="Đến ngày", font=("Arial", 11, "bold"), bg="#f9f4ef", fg="#00214d")
        self.label_den_ngay.place(x=210, y=5)

        # ======= DateEntry chọn đến ngày =======
        self.entry_den_ngay = DateEntry(self.frame_chon_ngay, font=("Arial", 11), date_pattern="dd/MM/yyyy")
        self.entry_den_ngay.place(x=290, y=5, width=120)

        # ======= Nút "Thống kê" =======
        self.btn_thong_ke = tk.Button(
            self.frame_chon_ngay,
            text="Thống kê",
            font=("Arial", 11, "bold"),
            bg="#8c7851", fg="#fffffe", cursor="hand2",
            bd=2, relief="ridge",
            command=self.thong_ke_theo_ngay
        )
        self.btn_thong_ke.place(x=420, y=3, width=90, height=30)




    def on_show(self):
        self.update_user_display()
        self.load_hoa_don()

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

    def load_hoa_don(self):
        # Lấy ngày từ DateEntry
        tu_ngay_str = self.entry_tu_ngay.get()
        den_ngay_str = self.entry_den_ngay.get()

        # Chuyển thành datetime để so sánh
        tu_ngay = datetime.strptime(tu_ngay_str, "%d/%m/%Y")
        den_ngay = datetime.strptime(den_ngay_str, "%d/%m/%Y")

        self.tree_hoa_don.delete(*self.tree_hoa_don.get_children())
        tong_tien_mon = tong_giam_gia = tong_thanh_tien = 0
        so_hd = 0

        for hd in self.ds_hoa_don.dsHD:
            try:
                ngay_lap = datetime.strptime(hd.gioLap.split()[0], "%d/%m/%Y")
            except:
                continue  # bỏ qua nếu lỗi định dạng

            if tu_ngay <= ngay_lap <= den_ngay:
                cac_mon = ", ".join([f"{mon.ten_mon}({mon.so_luong})" for mon in hd.dsMon.ds])
                self.tree_hoa_don.insert("", "end", values=(
                    hd.maHD, hd.gioLap, hd.tongTien, 0, hd.TinhThanhTien(), hd.maBan, cac_mon
                ))
                tong_tien_mon += hd.tongTien
                tong_thanh_tien += hd.TinhThanhTien()
                so_hd += 1

        self.label_tong_ket.config(
            text=f"Tổng số hóa đơn thanh toán: {so_hd} hóa đơn\n"
                f"Tiền món: {tong_tien_mon:,} VNĐ\n"
                f"Tiền giảm giá: {tong_giam_gia:,} VNĐ\n"
                f"----------------------------------------------------------------------\n"
                f"Tiền thu về: {tong_thanh_tien:,} VNĐ"
        )


    def load_thong_ke_mon(self):
        tu_ngay_str = self.entry_tu_ngay.get()
        den_ngay_str = self.entry_den_ngay.get()

        tu_ngay = datetime.strptime(tu_ngay_str, "%d/%m/%Y")
        den_ngay = datetime.strptime(den_ngay_str, "%d/%m/%Y")

        self.tree_thong_ke_mon.delete(*self.tree_thong_ke_mon.get_children())

        thong_ke = {}  # key: ma_mon, value: dict chứa tên, dvt, sl, doanh thu

        for hd in self.ds_hoa_don.dsHD:
            try:
                ngay_lap = datetime.strptime(hd.gioLap.split()[0], "%d/%m/%Y")
            except:
                continue

            if tu_ngay <= ngay_lap <= den_ngay:
                for mon in hd.dsMon.ds:
                    key = mon.ma_mon
                    if key not in thong_ke:
                        thong_ke[key] = {
                            "ten_mon": mon.ten_mon,
                            "dvt": mon.dvt,
                            "so_luong": 0,
                            "doanh_thu": 0
                        }
                    thong_ke[key]["so_luong"] += mon.so_luong
                    thong_ke[key]["doanh_thu"] += mon.so_luong * mon.don_gia

        for item in thong_ke.values():
            self.tree_thong_ke_mon.insert("", "end", values=(
                item["ten_mon"],
                item["dvt"],
                item["so_luong"],
                f"{item['doanh_thu']:,} VNĐ"
            ))

        self.label_tong_mon.config(
            text=f"Tổng số món đã bán: {sum(item['so_luong'] for item in thong_ke.values())} món"
        )

    def thong_ke_theo_ngay(self):
        tu_ngay = self.entry_tu_ngay.get()
        den_ngay = self.entry_den_ngay.get()
        print(f"Thống kê từ {tu_ngay} đến {den_ngay}")
        # Sau này bạn lọc hóa đơn theo khoảng ngày ở đây
        self.load_hoa_don()
        self.load_thong_ke_mon()




