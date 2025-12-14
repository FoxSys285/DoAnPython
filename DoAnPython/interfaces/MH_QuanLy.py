import tkinter as tk
from tkinter import *
from .MyButton import HoverButton 
from datetime import datetime
from tkinter import ttk
from objects.Mon import DanhSachMon
import json

class MH_QuanLy(tk.Frame):

    def load_mon(self):
        self.tree_mon.delete(*self.tree_mon.get_children())
        for i, mon in enumerate(self.ds_mon.ds, start=1):
            self.tree_mon.insert("", "end", values=(
                i, mon.ma_mon, mon.ten_mon, mon.don_gia, mon.loai, mon.dvt
            ))
        self.tree_mon.pack(fill="both", expand=True) 
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f4ef")
        self.controller = controller
        self.trang_hien_tai = None
        # Khung toàn trang
        full_frame = tk.Frame(self, bg="#f9f4ef")
        full_frame.place(x=0, y=0, width=1280, height=640)

        menu_frame = tk.Frame(full_frame, bg="#f9f4ef")
        menu_frame.place(x=0, y=0, width=820, height=120)

        from objects.NhanVien import DanhSachNhanVien
        self.ds_nhan_vien = DanhSachNhanVien()
        self.ds_nhan_vien.doc_file("data/du_lieu_nv.json")

        # Nút chuyển trang
        menu_buttons = [
            ("TRANG CHỦ", lambda: self.controller.show_frame("MH_TrangChu")),
            ("BÁN HÀNG", lambda: self.controller.show_frame("MH_BanHang")),
            ("QUẢN LÝ", lambda: [self.reset_quan_ly(), self.controller.show_frame("MH_QuanLy")]),
            ("THỐNG KÊ", lambda: self.controller.show_frame("MH_ThongKe")),
            ("CREDITS", lambda: self.controller.show_frame("MH_Credits")),
        ]
        x = 40
        for text, cmd in menu_buttons:
            HoverButton(
                menu_frame, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe",
                cursor="hand2", bd=3, relief="ridge",
                command=cmd
            ).place(x=x, y=40, width=125, height=60)
            x += 160

        qtv_frame = tk.Frame(full_frame, bg="#f9f4ef")
        qtv_frame.place(x=1020, y=40, width=160, height=60)


        date_time_frame = tk.Frame(full_frame, bg="#f9f4ef")
        date_time_frame.place(x=1000, y=0, width=220, height=40)
        # Thời gian
        self.label_time = tk.Label(
            date_time_frame,
            fg="#00214d",
            bg="#f9f4ef",
            font=("proxima-nova", 14, "bold")
        )
        self.label_time.pack(expand=True, anchor="nw")

        # Tên QTV
        self.label_qtv = tk.Label(
            qtv_frame,
            text="",  # sẽ cập nhật trong on_show()
            fg="#716040",
            font=("proxima-nova", 12, "bold"),
            bg="#f9f4ef"
        )
        self.label_qtv.place(x=0, y=0, width=160, height=30)

        # Nút đăng xuất
        HoverButton(
            qtv_frame, text="Đăng xuất",
            font=("proxima-nova", 12, "bold"),
            bg="#8c7851", fg="#fffffe", cursor="hand2",
            bd=3, relief="ridge",
            command=lambda: self.controller.show_frame("MH_DangNhap")
        ).place(x=0, y=30, width=160, height=30)

        # Cập nhật thời gian liên tục
        def update_time():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            self.label_time.config(text=now)
            self.label_time.after(1000, update_time)
        update_time()

        # Vùng nội dung bên dưới thanh menu
        content_frame = tk.Frame(full_frame, bg="#f9f4ef")
        content_frame.place(x=0, y=100, width=1260, height=520)

        # Khung trái – 4 nút quản lý
        left_panel = tk.Frame(content_frame, bg="#fffffe", bd=2, relief="groove")
        left_panel.place(x=20, y=20, width=320, height=500)

        left_buttons = [
            ("QUẢN LÝ THỰC ĐƠN", self.show_quan_ly_thuc_don),
            ("QUẢN LÝ NHÓM MÓN", self.show_quan_ly_nhom_mon),
            ("QUẢN LÝ BÀN", self.show_quan_ly_ban),
            ("QUẢN LÝ NHÂN VIÊN", self.show_quan_ly_nhan_vien),
        ]
        y = 30
        for text, cmd in left_buttons:
            HoverButton(
                left_panel, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe",
                cursor="hand2", bd=3, relief="ridge",
                command=cmd
            ).place(x=20, y=y, width=280, height=60)
            y += 90


        self.right_pannel = tk.Frame(content_frame, bg="#fffffe", bd=2, relief="groove")
        self.right_pannel.place(x=940, y=20, width=320, height=500)

        action_buttons = [
            ("Thêm", lambda: self.handle_action("add")),
            ("Sửa", lambda: self.handle_action("edit")),
            ("Xóa", lambda: self.handle_action("delete"))
        ]
        y = 50  # bắt đầu sau khung nhập
        for text, cmd in action_buttons:
            HoverButton(
                self.right_pannel, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe",
                cursor="hand2", bd=3, relief="ridge",
                command=cmd
            ).place(x=20, y=y, width=280, height=80)
            y += 120

        #Xử lý Nhóm Bàn
        self.frame_nhap_ban = tk.Frame(self.right_pannel, bg="#fffffe", bd=2, relief="ridge")
        self.frame_nhap_ban.place(x=20, y=30, width=280, height=280)
        self.frame_nhap_ban.place_forget()

        

        fields_ban = ["Mã bàn", "Tên bàn", "Trạng thái", "Thời gian","Người lập"]
        self.entry_ban = {}
        y = 10
        for field in fields_ban:
            tk.Label(self.frame_nhap_ban, text=field, font=("Arial", 10), bg="#fffffe").place(x=10, y=y)
            entry = tk.Entry(self.frame_nhap_ban, font=("Arial", 10))
            entry.place(x=100, y=y, width=170)
            self.entry_ban[field] = entry
            y += 30

        tk.Button(
            self.frame_nhap_ban, text="Lưu", font=("Arial", 10, "bold"),
            bg="#4CAF50", fg="white", cursor="hand2",
            command=self.luu_ban
        ).place(x=80, y=200, width=120, height=30)

        tk.Button(
            self.frame_nhap_ban, text="Hủy", font=("Arial", 10, "bold"),
            bg="#f44336", fg="white", cursor="hand2",
            command=self.an_khung_ban
        ).place(x=210, y=200, width=60, height=30)

            #################################

        self.frame_nhap_nhom = tk.Frame(self.right_pannel, bg="#fffffe", bd=2, relief="ridge")
        self.frame_nhap_nhom.place(x=20, y=30, width=200, height=80)  # đủ chỗ cho nút Lưu
        self.frame_nhap_nhom.place_forget()

        tk.Label(self.frame_nhap_nhom, text="Tên nhóm", font=("Arial", 10), bg="#fffffe").place(x=10, y=10)
        self.entry_nhom = tk.Entry(self.frame_nhap_nhom, font=("Arial", 10))
        self.entry_nhom.place(x=100, y=10, width=160)

        tk.Button(
            self.frame_nhap_nhom, text="Lưu", font=("Arial", 10, "bold"),
            bg="#4CAF50", fg="white", cursor="hand2",
            command=self.luu_nhom_mon
        ).place(x=80, y=50, width=120, height=30)

        tk.Button(
            self.frame_nhap_nhom, text="Hủy", font=("Arial", 10, "bold"),
            bg="#f44336", fg="white", cursor="hand2",
            command=self.an_khung_nhom
        ).place(x=210, y=50, width=60, height=30)

        # Khung trung tâm – placeholder để sau hiển thị bảng
        self.center_panel = tk.Frame(content_frame, bg="#eaddcf", bd=2, relief="groove")
        self.center_panel.place(x=360, y=20, width=560, height=500)
        #Khung quản lý thực đơn
        self.frame_thuc_don = tk.Frame(self.center_panel, bg="#eaddcf")
        self.frame_thuc_don.place(x=0, y=0, relwidth=1, relheight=1)
        columns = ("stt", "ma_mon", "ten_mon", "don_gia", "loai", "dvt")
        self.tree_mon = ttk.Treeview(self.frame_thuc_don, columns=columns, show="headings")
        self.tree_mon.bind("<<TreeviewSelect>>", self.on_select_mon)

        #Khung quản lý nhóm món
        self.frame_nhom_mon = tk.Frame(self.center_panel, bg="#eaddcf")
        self.frame_nhom_mon.place(x=0, y=0, relwidth=1, relheight=1)
        #Khung quản lý bàn
        self.frame_ban = tk.Frame(self.center_panel, bg="#eaddcf")
        self.frame_ban.place(x=0, y=0, relwidth=1, relheight=1)

        columns_ban = ("stt", "ma_ban", "ten_ban", "trang_thai", "thoi_gian","nguoi_lap")
        self.tree_ban = ttk.Treeview(self.frame_ban, columns=columns_ban, show="headings")

        self.tree_ban.heading("stt", text="STT")
        self.tree_ban.column("stt", width=50, anchor="center")

        self.tree_ban.heading("ma_ban", text="Mã bàn")
        self.tree_ban.column("ma_ban", width=70, anchor="center")

        self.tree_ban.heading("ten_ban", text="Tên bàn")
        self.tree_ban.column("ten_ban", width=100, anchor="center")

        self.tree_ban.heading("trang_thai", text="Trạng thái")
        self.tree_ban.column("trang_thai", width=80, anchor="center")

        self.tree_ban.heading("thoi_gian", text="Thời gian")
        self.tree_ban.column("thoi_gian", width=130, anchor="center")

        self.tree_ban.heading("nguoi_lap", text="Người lập")
        self.tree_ban.column("nguoi_lap", width=90, anchor="center")

        self.tree_ban.pack(fill="both", expand=True)

        self.tree_ban.bind("<<TreeviewSelect>>", self.on_select_ban)

        self.tree_nhom = ttk.Treeview(self.frame_nhom_mon, columns=("ten_nhom",), show="headings")
        self.tree_nhom.heading("ten_nhom", text="Tên nhóm món")
        self.tree_nhom.column("ten_nhom", anchor="center", width=540)
        self.tree_nhom.pack(fill="both", expand=True)
        self.tree_nhom.bind("<<TreeviewSelect>>", self.on_select_nhom)

        #Khung quản lý nhân viên
        self.frame_nhan_vien = tk.Frame(self.center_panel, bg="#eaddcf")
        self.frame_nhan_vien.place(x=0, y=0, relwidth=1, relheight=1)
        columns_nv = ("stt", "ma_nv", "ten_nv", "role", "luong", "username")
        self.tree_nhan_vien = ttk.Treeview(self.frame_nhan_vien, columns=columns_nv, show="headings")

        self.tree_nhan_vien.bind("<<TreeviewSelect>>", self.on_select_nhan_vien)

        self.tree_nhan_vien.heading("stt", text="STT")
        self.tree_nhan_vien.column("stt", width=50, anchor="center")

        self.tree_nhan_vien.heading("ma_nv", text="Mã NV")
        self.tree_nhan_vien.column("ma_nv", width=80, anchor="center")

        self.tree_nhan_vien.heading("ten_nv", text="Tên nhân viên")
        self.tree_nhan_vien.column("ten_nv", width=150, anchor="center")

        self.tree_nhan_vien.heading("role", text="Chức vụ")
        self.tree_nhan_vien.column("role", width=90, anchor="center")

        self.tree_nhan_vien.heading("luong", text="Lương")
        self.tree_nhan_vien.column("luong", width=100, anchor="center")

        self.tree_nhan_vien.heading("username", text="Tài khoản")
        self.tree_nhan_vien.column("username", width=100, anchor="center")

        self.frame_nhap_nv = tk.Frame(self.right_pannel, bg="#fffffe", bd=2, relief="ridge")
        self.frame_nhap_nv.place(x=20, y=120, width=280, height=280)
        self.frame_nhap_nv.place_forget()

        fields_nv = ["Mã NV", "Tên nhân viên", "Chức vụ", "Lương", "Tài khoản"]
        self.entry_nv = {}
        y = 10
        for field in fields_nv:
            tk.Label(self.frame_nhap_nv, text=field, font=("Arial", 10), bg="#fffffe").place(x=10, y=y)
            entry = tk.Entry(self.frame_nhap_nv, font=("Arial", 10))
            entry.place(x=110, y=y, width=160)
            self.entry_nv[field] = entry
            y += 30

        tk.Button(
            self.frame_nhap_nv, text="Lưu", font=("Arial", 10, "bold"),
            bg="#4CAF50", fg="white", cursor="hand2",
            command=self.luu_nhan_vien_moi
        ).place(x=80, y=220, width=120, height=30)

        tk.Button(
            self.frame_nhap_nv, text="Hủy", font=("Arial", 10, "bold"),
            bg="#f44336", fg="white", cursor="hand2",
            command=self.an_khung_nv
        ).place(x=210, y=220, width=60, height=30)

        # Cấu hình từng cột
        self.tree_mon.heading("stt", text="STT")
        self.tree_mon.column("stt", width=50, anchor="center")

        self.tree_mon.heading("ma_mon", text="Mã món")
        self.tree_mon.column("ma_mon", width=80, anchor="center")

        self.tree_mon.heading("ten_mon", text="Tên món")
        self.tree_mon.column("ten_mon", width=160, anchor="center")

        self.tree_mon.heading("don_gia", text="Đơn giá")
        self.tree_mon.column("don_gia", width=80, anchor="center")

        self.tree_mon.heading("loai", text="Loại")
        self.tree_mon.column("loai", width=80, anchor="center")

        self.tree_mon.heading("dvt", text="Đơn vị tính")
        self.tree_mon.column("dvt", width=110, anchor="center")
          
        self.ds_mon = DanhSachMon()
        self.ds_mon.doc_file("data/du_lieu_mon.json")
        
        from objects.DanhSachNhomMon import DanhSachNhomMon
        self.ds_nhom = DanhSachNhomMon()
        self.ds_nhom.doc_file("data/du_lieu_nhom_mon.json")

        from objects.Ban import DanhSachBan
        self.ds_ban = DanhSachBan()
        self.ds_ban.doc_file("data/du_lieu_ban.json")

        tk.Label(
            self.center_panel, text="Khu vực nội dung (bảng danh sách)",
            font=("proxima-nova", 14, "bold"),
            fg="#716040", bg="#eaddcf"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ##################### Thêm món##################################
        self.frame_them_mon = tk.Frame(self.right_pannel, bg="#fffffe", bd=2, relief="ridge")
        self.frame_them_mon.place(x=20, y=250, width=280, height=220)
        self.frame_them_mon.place_forget()

        fields = ["Mã món", "Tên món", "Đơn giá", "Loại", "Đơn vị tính"]
        self.entry_mon = {}
        y = 10
        for field in fields:
            tk.Label(self.frame_them_mon, text=field, font=("Arial", 10), bg="#fffffe").place(x=10, y=y)
            entry = tk.Entry(self.frame_them_mon, font=("Arial", 10))
            entry.place(x=100, y=y, width=200)
            self.entry_mon[field] = entry
            y += 30

        tk.Button(
            self.frame_them_mon, text="Lưu", font=("Arial", 10, "bold"),
            bg="#4CAF50", fg="white", cursor="hand2",
            command=self.luu_mon_moi
        ).place(x=80, y=170, width=120, height=30)

        tk.Button(
            self.frame_them_mon, text="Hủy", font=("Arial", 10, "bold"),
            bg="#f44336", fg="white", cursor="hand2",
            command=self.an_khung_mon
        ).place(x=210, y=170, width=60, height=30)

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
        

    # Handlers trái
    def show_quan_ly_thuc_don(self):
        self.clear_center()
        self.trang_hien_tai = "thuc_don"
        self.load_mon()
        self.frame_thuc_don.place(x=0, y=0, relwidth=1, relheight=1)
        self.tree_mon.pack(fill="both", expand=True)
        self.frame_thuc_don.tkraise()

    def handle_action(self, action):
        print(f"Hành động: {action}")
        if self.trang_hien_tai == "thuc_don":
            if action == "add":
                self.hien_khung_them_mon()
            elif action == "edit":
                self.hien_khung_sua_mon()
            elif action == "delete":
                self.xoa_mon()
        elif self.trang_hien_tai == "nhom_mon":
            if action == "add":
                self.frame_nhap_nhom.place(x=20, y=30, width=280, height=130)
                self.entry_nhom.delete(0, tk.END)
                self.dang_sua_nhom = False
            elif action == "edit":
                selected = self.tree_nhom.selection()
                if not selected:
                    print("Chưa chọn nhóm để sửa")
                    return

                ten_cu = self.tree_nhom.item(selected[0])["values"][0]
                self.nhom_cu = ten_cu
                self.dang_sua_nhom = True

                self.frame_nhap_nhom.place(x=20, y=30, width=280, height=130)
                self.entry_nhom.delete(0, tk.END)
                self.entry_nhom.insert(0, ten_cu)
                self.entry_nhom.config(state="normal")
                print(f"Đang sửa nhóm: {ten_cu}")
            elif action == "delete":
                selected = self.tree_nhom.selection()
                if not selected:
                    print("Chưa chọn nhóm để xóa")
                    return

                ten = self.tree_nhom.item(selected[0])["values"][0]

                from tkinter import messagebox
                confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa nhóm '{ten}' không?")
                if not confirm:
                    print("Hủy xóa nhóm")
                    return

                if self.ds_nhom.xoa_nhom(ten):
                    print(f"Đã xóa nhóm: {ten}")
                    self.ds_nhom.ghi_file("data/du_lieu_nhom_mon.json")
                    self.load_nhom_mon()
                else:
                    print("Không thể xóa nhóm")
        elif self.trang_hien_tai == "ban":
            if action == "add":
                print("Đang thêm bàn mới")
                self.frame_nhap_ban.place(x=20, y=120, width=280, height=250)
                for entry in self.entry_ban.values():
                    entry.delete(0, tk.END)
                self.dang_sua_ban = False
            elif action == "delete":
                selected = self.tree_ban.selection()
                if not selected:
                    print("Chưa chọn bàn để xóa")
                    return

                item = self.tree_ban.item(selected[0])
                stt = item["values"][0]
                ten_ban = item["values"][2]

                from tkinter import messagebox
                confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa bàn '{ten_ban}' không?")
                if not confirm:
                    print("Hủy xóa bàn")
                    return

                index = stt - 1
                if 0 <= index < len(self.ds_ban.ds):
                    del self.ds_ban.ds[index]
                    self.ds_ban.ghi_file("data/du_lieu_ban.json")
                    self.load_ban()
                    print(f"Đã xóa bàn: {ten_ban}")
                else:
                    print("Không tìm thấy bàn để xóa")

                ten_cu = self.tree_nhom.item(selected[0])["values"][0]
                self.nhom_cu = ten_cu
                self.dang_sua_nhom = True
                self.frame_nhap_nhom.place(x=20, y=30, width=280, height=280)
                self.entry_nhom.delete(0, tk.END)
                self.entry_nhom.insert(0, ten_cu)
            elif action == "delete":
                self.xoa_nhom_mon()

            elif action == "edit":
                selected = self.tree_ban.selection()
                if not selected:
                    print("Chưa chọn bàn để sửa")
                    return

                item = self.tree_ban.item(selected[0])
                stt = item["values"][0]
                index = stt - 1

                if 0 <= index < len(self.ds_ban.ds):
                    ban = self.ds_ban.ds[index]
                    self.ban_dang_sua_index = index
                    self.dang_sua_ban = True

                    self.frame_nhap_ban.place(x=20, y=120, width=280, height=290)
                    for entry in self.entry_ban.values():
                        entry.config(state="normal")

                    self.entry_ban["Mã bàn"].delete(0, tk.END)
                    self.entry_ban["Mã bàn"].insert(0, ban.ma_ban)

                    self.entry_ban["Tên bàn"].delete(0, tk.END)
                    self.entry_ban["Tên bàn"].insert(0, ban.ten_ban)

                    self.entry_ban["Trạng thái"].delete(0, tk.END)
                    self.entry_ban["Trạng thái"].insert(0, ban.trang_thai)

                    self.entry_ban["Thời gian"].delete(0, tk.END)
                    self.entry_ban["Thời gian"].insert(0, ban.thoi_gian)

                    self.entry_ban["Người lập"].delete(0, tk.END)
                    self.entry_ban["Người lập"].insert(0, getattr(ban, "nguoi_lap", ""))

                    print(f"Đang sửa bàn: {ban.ten_ban}")
                else:
                    print("Không tìm thấy bàn để sửa")
        elif self.trang_hien_tai == "nhan_vien":
            if action == "add":
                self.hien_khung_them_nv()
            elif action == "delete":
                self.xoa_nhan_vien()
            elif action == "edit":
                self.hien_khung_sua_nv()
            

    def hien_khung_them_mon(self):
        # Xóa nội dung cũ
        print("Đang hiển thị khung thêm món")
        self.frame_them_mon.place(x=20, y=125, width=280, height=220)
        self.set_entry_state("normal")
        for entry in self.entry_mon.values():
            entry.delete(0, tk.END)
    
    def luu_mon_moi(self):
        ma = self.entry_mon["Mã món"].get()
        ten = self.entry_mon["Tên món"].get()
        gia = self.entry_mon["Đơn giá"].get()
        loai = self.entry_mon["Loại"].get()
        dvt = self.entry_mon["Đơn vị tính"].get()

        if not ma or not ten or not gia:
            print("Thiếu thông tin bắt buộc")
            return
        try:
            gia = int(gia)
        except:
            print("Đơn giá phải là số")
            return

        from objects.Mon import Mon
        mon_moi = Mon(ma, ten, gia, 1, loai, dvt)

        if hasattr(self, "dang_sua") and self.dang_sua:
            self.ds_mon.ds[self.mon_dang_sua_index] = mon_moi
            print(f"Đã cập nhật món: {ten}")
            self.dang_sua = False
        else:
            self.ds_mon.ds.append(mon_moi)
            print(f"Đã thêm món mới: {ten}")

        self.ds_mon.ghi_file("data/du_lieu_mon.json")
        self.load_mon()
        self.frame_them_mon.place_forget()

    def on_hide(self):
        self.clear_center()

    def clear_center(self):
        try:
            self.tree_mon.pack_forget()
        except:
            pass
        try:
            self.tree_nhom.pack_forget()
        except:
            pass
        try:
            self.tree_ban.pack_forget()
        except:
            pass
        try:
            self.frame_nhap_nv.place_forget()
        except:
            pass
        # Ẩn khung nhập phụ
        self.frame_them_mon.place_forget()
        self.frame_nhap_nhom.place_forget()
        self.frame_nhap_ban.place_forget()
        # Ẩn khung chính
        self.frame_thuc_don.place_forget()
        self.frame_nhom_mon.place_forget()
        self.frame_ban.place_forget()
        # Reset trạng thái
        self.trang_hien_tai = None
        self.dang_sua = False
        self.dang_sua_nhom = False
        self.dang_sua_ban = False

    # Xóa Món
    def xoa_mon(self):
        selected = self.tree_mon.selection()
        if not selected:
            print("Chưa chọn món để xóa")
            return

        item = self.tree_mon.item(selected[0])
        stt = item["values"][0]  # STT là số thứ tự hiển thị
        ten_mon = item["values"][2]  # Tên món để hiển thị xác nhận

        # Hộp thoại xác nhận
        from tkinter import messagebox
        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa món '{ten_mon}' không?")
        if not confirm:
            print("Hủy xóa món")
            return

        index = stt - 1
        if 0 <= index < len(self.ds_mon.ds):
            del self.ds_mon.ds[index]
            self.ds_mon.ghi_file("data/du_lieu_mon.json")
            self.load_mon()
            print(f"Đã xóa món: {ten_mon}")
        else:
            print("Không tìm thấy món để xóa")

    #Sửa món
    def hien_khung_sua_mon(self):
        selected = self.tree_mon.selection()
        self.set_entry_state("normal")
        if not selected:
            print("Chưa chọn món để sửa")
            return

        item = self.tree_mon.item(selected[0])
        stt = item["values"][0]
        index = stt - 1

        if 0 <= index < len(self.ds_mon.ds):
            mon = self.ds_mon.ds[index]
            self.mon_dang_sua_index = index 

            self.frame_them_mon.place(x=20, y=250, width=280, height=220)
            self.entry_mon["Mã món"].delete(0, tk.END)
            self.entry_mon["Mã món"].insert(0, mon.ma_mon)

            self.entry_mon["Tên món"].delete(0, tk.END)
            self.entry_mon["Tên món"].insert(0, mon.ten_mon)

            self.entry_mon["Đơn giá"].delete(0, tk.END)
            self.entry_mon["Đơn giá"].insert(0, str(mon.don_gia))

            self.entry_mon["Loại"].delete(0, tk.END)
            self.entry_mon["Loại"].insert(0, mon.loai)

            self.entry_mon["Đơn vị tính"].delete(0, tk.END)
            self.entry_mon["Đơn vị tính"].insert(0, mon.dvt)

            self.dang_sua = True 
            print(f"Đang sửa món: {mon.ten_mon}")
        else:
            print("Không tìm thấy món để sửa")


                ########
    
    def load_nhom_mon(self):
        self.tree_nhom.delete(*self.tree_nhom.get_children())
        for ten in self.ds_nhom.lay_danh_sach():
            self.tree_nhom.insert("", "end", values=(ten,))

    def show_quan_ly_nhom_mon(self):
        print("Chọn: Quản lý nhóm món")
        self.clear_center()
        self.trang_hien_tai = "nhom_mon"
        self.load_nhom_mon()
        self.frame_nhom_mon.place(x=0, y=0, relwidth=1, relheight=1)
        self.tree_nhom.pack(fill="both", expand=True)
        self.frame_nhom_mon.tkraise()

    def luu_nhom_mon(self):
        ten = self.entry_nhom.get().strip()
        if not ten:
            print("Tên nhóm không được để trống")
            return

        if hasattr(self, "dang_sua_nhom") and self.dang_sua_nhom:
            # Sửa nhóm
            if self.ds_nhom.sua_nhom(self.nhom_cu, ten):
                print(f"Đã sửa nhóm: {self.nhom_cu} → {ten}")
            else:
                print("Không thể sửa nhóm")
            self.dang_sua_nhom = False
        else:
            # Thêm nhóm
            if self.ds_nhom.them_nhom(ten):
                print(f"Đã thêm nhóm: {ten}")
            else:
                print("Nhóm đã tồn tại hoặc không hợp lệ")

        self.ds_nhom.ghi_file("data/du_lieu_nhom_mon.json")
        self.load_nhom_mon()
        self.frame_nhap_nhom.place_forget()

    def xoa_nhom_mon(self):
        selected = self.tree_nhom.selection()
        if not selected:
            print("Chưa chọn nhóm để xóa")
            return

        ten = self.tree_nhom.item(selected[0])["values"][0]
        from tkinter import messagebox
        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa nhóm '{ten}' không?")
        if not confirm:
            print("Hủy xóa nhóm")
            return

        if self.ds_nhom.xoa_nhom(ten):
            print(f"Đã xóa nhóm: {ten}")
            self.ds_nhom.ghi_file("data/du_lieu_nhom_mon.json")
            self.load_nhom_mon()
        else:
            print("Không thể xóa nhóm")

    def an_khung_nhom(self):
        self.frame_nhap_nhom.place_forget()
        print("Đã ẩn khung nhóm món")

    def an_khung_mon(self):
        self.frame_them_mon.place_forget()
        print("Đã ẩn khung nhập món")

    def on_select_nhom(self, event):
        selected = self.tree_nhom.selection()
        if not selected:
            return

        self.frame_nhap_nhom.place(x=20, y=30, width=280, height=130)

        # Mở khóa trước khi xóa/điền
        self.entry_nhom.config(state="normal")
        self.entry_nhom.delete(0, tk.END)

        ten_nhom = self.tree_nhom.item(selected[0])["values"][0]
        self.entry_nhom.insert(0, ten_nhom)

        # Khóa lại sau khi đổ xong
        self.entry_nhom.config(state="readonly")
                ###########
    
    def show_quan_ly_ban(self):
        self.ds_ban.doc_file("data/du_lieu_ban.json")
        print("Chọn: Quản lý bàn")
        self.clear_center()
        self.trang_hien_tai = "ban"
        self.load_ban()
        self.frame_ban.place(x=0, y=0, relwidth=1, relheight=1)
        self.tree_ban.pack(fill="both", expand=True)
        self.frame_ban.tkraise()

    def load_ban(self):
        self.tree_ban.delete(*self.tree_ban.get_children())
        for i, ban in enumerate(self.ds_ban.ds, start=1):
            self.tree_ban.insert("", "end", values=(
                i, ban.ma_ban, ban.ten_ban, ban.trang_thai, ban.thoi_gian, getattr(ban, "nguoi_lap", "")
            ))

    def luu_ban(self):
        ma = self.entry_ban["Mã bàn"].get()
        ten = self.entry_ban["Tên bàn"].get()
        tt = self.entry_ban["Trạng thái"].get()
        tg = self.entry_ban["Thời gian"].get()
        nl = self.entry_ban["Người lập"].get()

        if not ma or not ten:
            print("Thiếu thông tin bàn")
            return

        from objects.Ban import Ban
        ban_moi = Ban(ma, ten, tt or "Free", tg or "", None, nl or "")

        if getattr(self, "dang_sua_ban", False):
            self.ds_ban.ds[self.ban_dang_sua_index] = ban_moi
            print(f"Đã sửa bàn: {ten}")
            self.dang_sua_ban = False
        else:
            self.ds_ban.ds.append(ban_moi)
            print(f"Đã thêm bàn mới: {ten}")

        self.ds_ban.ghi_file("data/du_lieu_ban.json")
        self.load_ban()
        self.frame_nhap_ban.place_forget()

    def on_select_ban(self, event):
        selected = self.tree_ban.selection()
        if not selected:
            return

        self.frame_nhap_ban.place(x=20, y=120, width=280, height=290)

        item = self.tree_ban.item(selected[0])
        values = item["values"]

        fields = ["Mã bàn", "Tên bàn", "Trạng thái", "Thời gian", "Người lập"]

        # Mở khóa trước khi cập nhật
        for entry in self.entry_ban.values():
            entry.config(state="normal")

        for i, field in enumerate(fields):
            self.entry_ban[field].delete(0, tk.END)
            self.entry_ban[field].insert(0, values[i + 1])

        # Khóa lại sau khi đổ dữ liệu
        for entry in self.entry_ban.values():
            entry.config(state="readonly")

    def an_khung_ban(self):
        self.frame_nhap_ban.place_forget()
        print("Đã ẩn khung nhập bàn")
                ###############
    
    def show_quan_ly_nhan_vien(self):
        print("Chọn: Quản lý nhân viên")
        self.clear_center()
        self.trang_hien_tai = "nhan_vien"
        self.load_nhan_vien()
        self.frame_nhan_vien.place(x=0, y=0, relwidth=1, relheight=1)
        self.tree_nhan_vien.pack(fill="both", expand=True)
        self.frame_nhan_vien.tkraise()

    def load_nhan_vien(self):
        self.tree_nhan_vien.delete(*self.tree_nhan_vien.get_children())
        for i, nv in enumerate(self.ds_nhan_vien.ds.values(), start=1):
            self.tree_nhan_vien.insert("", "end", values=(
                i, nv.ma_nv, nv.ten_nv, nv.role, nv.luong, nv.username
            ))
        print("Số nhân viên:", len(self.ds_nhan_vien.ds))
        for nv in self.ds_nhan_vien.ds.values():
            print(nv)

    def hien_khung_them_nv(self):
        print("Đang hiển thị khung thêm nhân viên")
        self.frame_nhap_nv.place(x=20, y=120, width=280, height=280)
        for entry in self.entry_nv.values():
            entry.delete(0, tk.END)
        self.dang_sua_nv = False

    def luu_nhan_vien_moi(self):
        ma = self.entry_nv["Mã NV"].get().strip()
        ten = self.entry_nv["Tên nhân viên"].get().strip()
        role = self.entry_nv["Chức vụ"].get().strip()
        luong = self.entry_nv["Lương"].get().strip()
        username = self.entry_nv["Tài khoản"].get().strip()

        if not ma or not ten or not role or not luong or not username:
            print("Thiếu thông tin bắt buộc")
            return
        try:
            luong = int(luong)
        except:
            print("Lương phải là số")
            return

        from objects.NhanVien import NhanVien
        nv_moi = NhanVien(ma, ten, role, luong, username)

        if getattr(self, "dang_sua_nv", False):
            self.ds_nhan_vien.ds[self.ma_nv_dang_sua] = nv_moi
            print(f"Đã cập nhật nhân viên: {ten}")
        else:
            if self.ds_nhan_vien.add_nv(nv_moi):
                print(f"Đã thêm nhân viên: {ten}")
            else:
                print("Mã NV đã tồn tại")
                return

    # Ghi file và reload
        self.ds_nhan_vien.ghi_file("data/du_lieu_nv.json")
        self.load_nhan_vien()
        self.frame_nhap_nv.place_forget()
        self.dang_sua_nv = False

    def xoa_nhan_vien(self):
        selected = self.tree_nhan_vien.selection()
        if not selected:
            print("Chưa chọn nhân viên để xóa")
            return

        item = self.tree_nhan_vien.item(selected[0])
        stt = item["values"][0]       # số thứ tự
        ma_nv = item["values"][1]     # mã NV
        ten_nv = item["values"][2]    # tên NV

        from tkinter import messagebox
        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa nhân viên '{ten_nv}' ({ma_nv}) không?")
        if not confirm:
            print("Hủy xóa nhân viên")
            return

        # Xóa trong dict
        if ma_nv in self.ds_nhan_vien.ds:
            self.ds_nhan_vien.remove_nv(ma_nv)
            self.ds_nhan_vien.ghi_file("data/du_lieu_nv.json")
            self.load_nhan_vien()
            print(f"Đã xóa nhân viên: {ten_nv}")
        else:
            print("Không tìm thấy nhân viên để xóa")


    def hien_khung_sua_nv(self):
        selected = self.tree_nhan_vien.selection()
        if not selected:
            print("Chưa chọn nhân viên để sửa")
            return

        item = self.tree_nhan_vien.item(selected[0])
        ma_nv = item["values"][1]

        nv = self.ds_nhan_vien.ds.get(ma_nv)
        if not nv:
            print("Không tìm thấy nhân viên để sửa")
            return

        # Hiện khung nhập
        self.frame_nhap_nv.place(x=20, y=120, width=280, height=280)
        
        for entry in self.entry_nv.values():
            entry.config(state="normal")
        
        # Đổ dữ liệu vào các ô nhập
        self.entry_nv["Mã NV"].delete(0, tk.END)
        self.entry_nv["Mã NV"].insert(0, nv.ma_nv)

        self.entry_nv["Tên nhân viên"].delete(0, tk.END)
        self.entry_nv["Tên nhân viên"].insert(0, nv.ten_nv)

        self.entry_nv["Chức vụ"].delete(0, tk.END)
        self.entry_nv["Chức vụ"].insert(0, nv.role)

        self.entry_nv["Lương"].delete(0, tk.END)
        self.entry_nv["Lương"].insert(0, nv.luong)

        self.entry_nv["Tài khoản"].delete(0, tk.END)
        self.entry_nv["Tài khoản"].insert(0, nv.username)

        # Đánh dấu đang sửa
        self.dang_sua_nv = True
        self.ma_nv_dang_sua = ma_nv

    def reset_quan_ly(self):
        self.clear_center()
        self.trang_hien_tai = None

        # Đọc lại dữ liệu
        from objects.Mon import DanhSachMon
        self.ds_mon = DanhSachMon()
        self.ds_mon.doc_file("data/du_lieu_mon.json")

        from objects.DanhSachNhomMon import DanhSachNhomMon
        self.ds_nhom = DanhSachNhomMon()
        self.ds_nhom.doc_file("data/du_lieu_nhom_mon.json")

        from objects.Ban import DanhSachBan
        self.ds_ban = DanhSachBan()
        self.ds_ban.doc_file("data/du_lieu_ban.json")

        from objects.NhanVien import DanhSachNhanVien
        self.ds_nhan_vien = DanhSachNhanVien()
        self.ds_nhan_vien.doc_file("data/du_lieu_nv.json")

        print("Đã reset và đọc lại toàn bộ dữ liệu")
                
    def on_select_mon(self, event):
        selected = self.tree_mon.selection()
        if not selected:
            return

        self.frame_them_mon.place(x=20, y=125, width=280, height=220)

        item = self.tree_mon.item(selected[0])
        values = item["values"]

        # MỞ KHÓA TRƯỚC KHI XÓA/ĐIỀN
        self.set_entry_state("normal")

        # STT, Mã món, Tên món, Đơn giá, Loại, ĐVT
        self.entry_mon["Mã món"].delete(0, tk.END)
        self.entry_mon["Mã món"].insert(0, values[1])

        self.entry_mon["Tên món"].delete(0, tk.END)
        self.entry_mon["Tên món"].insert(0, values[2])

        self.entry_mon["Đơn giá"].delete(0, tk.END)
        self.entry_mon["Đơn giá"].insert(0, str(values[3]))

        self.entry_mon["Loại"].delete(0, tk.END)
        self.entry_mon["Loại"].insert(0, values[4])

        self.entry_mon["Đơn vị tính"].delete(0, tk.END)
        self.entry_mon["Đơn vị tính"].insert(0, values[5])

        # KHÓA LẠI SAU KHI ĐỔ XONG
        self.set_entry_state("readonly")

    def set_entry_state(self, state="normal"):
        for entry in self.entry_mon.values():
            entry.config(state=state)

    def on_select_nhan_vien(self, event):
        selected = self.tree_nhan_vien.selection()
        if not selected:
            return

        self.frame_nhap_nv.place(x=20, y=120, width=280, height=280)

        item = self.tree_nhan_vien.item(selected[0])
        values = item["values"]

        fields = ["Mã NV", "Tên nhân viên", "Chức vụ", "Lương", "Tài khoản"]

        # Mở khóa trước khi cập nhật
        for entry in self.entry_nv.values():
            entry.config(state="normal")

        for i, field in enumerate(fields):
            self.entry_nv[field].delete(0, tk.END)
            self.entry_nv[field].insert(0, values[i + 1])

        # Khóa lại sau khi đổ dữ liệu
        for entry in self.entry_nv.values():
            entry.config(state="readonly")

    def an_khung_nv(self):
        self.frame_nhap_nv.place_forget()
        print("Đã ẩn khung nhập nhân viên")

