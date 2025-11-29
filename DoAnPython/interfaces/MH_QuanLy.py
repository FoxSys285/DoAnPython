import tkinter as tk
from tkinter import *
from .MyButton import HoverButton  # dùng nút hover đã có
from datetime import datetime
from tkinter import ttk
from objects.Mon import DanhSachMon


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

        # Thanh menu trên cùng (tái sử dụng phong cách)
        menu_frame = tk.Frame(full_frame, bg="#f9f4ef")
        menu_frame.place(x=0, y=0, width=1280, height=80)

        # Nút chuyển trang
        menu_buttons = [
            ("TRANG CHỦ", lambda: self.controller.show_frame("MH_TrangChu")),
            ("BÁN HÀNG", lambda: self.controller.show_frame("MH_BanHang")),
            ("QUẢN LÝ", lambda: self.controller.show_frame("MH_QuanLy")),
            ("THỐNG KÊ", lambda: None),
            ("CREDITS", lambda: None),
        ]
        x = 40
        for text, cmd in menu_buttons:
            HoverButton(
                menu_frame, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe",
                cursor="hand2", bd=3, relief="ridge",
                command=cmd
            ).place(x=x, y=20, width=150, height=60)
            x += 170

        qtv_frame = tk.Frame(menu_frame, bg="#f9f4ef")
        qtv_frame.place(x=1080, y=10, width=180, height=60)

        # Thời gian
        self.label_time = tk.Label(
            qtv_frame,
            fg="#00214d",
            bg="#f9f4ef",
            font=("proxima-nova", 12, "bold")
        )
        self.label_time.place(x=0, y=0, width=180, height=20)

        # Tên QTV
        self.label_qtv = tk.Label(
            qtv_frame,
            text="",  # sẽ cập nhật trong on_show()
            fg="#716040",
            font=("proxima-nova", 12, "bold"),
            bg="#f9f4ef"
        )
        self.label_qtv.place(x=0, y=20, width=180, height=20)

        # Nút đăng xuất
        HoverButton(
            qtv_frame,
            text="Đăng xuất",
            font=("proxima-nova", 10, "bold"),
            bg="#8c7851", fg="#fffffe",
            cursor="hand2", bd=2, relief="ridge",
            command=lambda: self.controller.show_frame("MH_DangNhap")
        ).place(x=0, y=40, width=180, height=25)

        # Cập nhật thời gian liên tục
        def update_time():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            self.label_time.config(text=now)
            self.label_time.after(1000, update_time)
        update_time()

        # Vùng nội dung bên dưới thanh menu
        content_frame = tk.Frame(full_frame, bg="#f9f4ef")
        content_frame.place(x=0, y=80, width=1280, height=560)

        # Khung trái – 4 nút quản lý
        left_panel = tk.Frame(content_frame, bg="#fffffe", bd=2, relief="groove")
        left_panel.place(x=20, y=20, width=320, height=520)

        left_buttons = [
            ("QUẢN LÝ THỰC ĐƠN", self.show_quan_ly_thuc_don),
            ("QUẢN LÝ NHÓM MÓN", self.show_quan_ly_nhom_mon),
            ("QUẢN LÝ BÀN", self.show_quan_ly_ban),
            ("QUẢN LÝ TÀI KHOẢN", self.show_quan_ly_tai_khoan),
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

        right_panel = tk.Frame(content_frame, bg="#fffffe", bd=2, relief="groove")
        right_panel.place(x=940, y=20, width=320, height=520)


        action_buttons = [
            ("Thêm", lambda: self.handle_action("add")),
            ("Sửa", lambda: self.handle_action("edit")),
            ("Xóa", lambda: self.handle_action("delete"))
        ]
        y = 30  # bắt đầu sau khung nhập
        for text, cmd in action_buttons:
            HoverButton(
                right_panel, text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851", fg="#fffffe",
                cursor="hand2", bd=3, relief="ridge",
                command=cmd
            ).place(x=20, y=y, width=280, height=80)
            y += 90

        self.frame_nhap_nhom = tk.Frame(right_panel, bg="#fffffe", bd=2, relief="ridge")
        self.frame_nhap_nhom.place(x=20, y=250, width=200, height=190)  # đủ chỗ cho nút Lưu
        self.frame_nhap_nhom.place_forget()

        tk.Label(self.frame_nhap_nhom, text="Tên nhóm", font=("Arial", 10), bg="#fffffe").place(x=10, y=10)
        self.entry_nhom = tk.Entry(self.frame_nhap_nhom, font=("Arial", 10))
        self.entry_nhom.place(x=100, y=10, width=160)

        tk.Button(
            self.frame_nhap_nhom, text="Lưu", font=("Arial", 10, "bold"),
            bg="#4CAF50", fg="white", cursor="hand2",
            command=self.luu_nhom_mon
        ).place(x=80, y=170, width=120, height=30)

        # Khung trung tâm – placeholder để sau hiển thị bảng
        center_panel = tk.Frame(content_frame, bg="#eaddcf", bd=2, relief="groove")
        center_panel.place(x=360, y=20, width=560, height=520)
        
        self.frame_thuc_don = tk.Frame(center_panel, bg="#eaddcf")
        self.frame_thuc_don.place(x=0, y=0, relwidth=1, relheight=1)
        columns = ("stt", "ma_mon", "ten_mon", "don_gia", "loai", "dvt")
        self.tree_mon = ttk.Treeview(self.frame_thuc_don, columns=columns, show="headings")

        self.frame_nhom_mon = tk.Frame(center_panel, bg="#eaddcf")
        self.frame_nhom_mon.place(x=0, y=0, relwidth=1, relheight=1)

        self.tree_nhom = ttk.Treeview(self.frame_nhom_mon, columns=("ten_nhom",), show="headings")
        self.tree_nhom.heading("ten_nhom", text="Tên nhóm món")
        self.tree_nhom.column("ten_nhom", anchor="center", width=540)
        self.tree_nhom.pack(fill="both", expand=True)

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

        tk.Label(
            center_panel, text="Khu vực nội dung (bảng danh sách)",
            font=("proxima-nova", 14, "bold"),
            fg="#716040", bg="#eaddcf"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ##################### Thêm món##################################
        self.frame_them_mon = tk.Frame(right_panel, bg="#fffffe", bd=2, relief="ridge")
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

    def on_show(self):
        current = self.controller.current_user
        if current:
            self.label_qtv.config(text=f"QTV: {current.username}")

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
                self.frame_nhap_nhom.place(x=20, y=30, width=280, height=280)
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
                self.frame_nhap_nhom.place(x=20, y=30, width=280, height=280)
                self.entry_nhom.delete(0, tk.END)
                self.entry_nhom.insert(0, ten_cu)
            elif action == "delete":
                self.xoa_nhom_mon()

    def hien_khung_them_mon(self):
        # Xóa nội dung cũ
        print("Đang hiển thị khung thêm món")
        self.frame_them_mon.place(x=20, y=250, width=280, height=220)
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

        # Ẩn khung nhập phụ
        self.frame_them_mon.place_forget()
        self.frame_nhap_nhom.place_forget()

        # Ẩn khung chính
        self.frame_thuc_don.place_forget()
        self.frame_nhom_mon.place_forget()

        # Reset trạng thái
        self.trang_hien_tai = None
        self.dang_sua = False
        self.dang_sua_nhom = False

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
        if not selected:
            print("Chưa chọn món để sửa")
            return

        item = self.tree_mon.item(selected[0])
        stt = item["values"][0]
        index = stt - 1

        if 0 <= index < len(self.ds_mon.ds):
            mon = self.ds_mon.ds[index]
            self.mon_dang_sua_index = index  # ✅ lưu lại vị trí để sửa

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

            self.dang_sua = True  # ✅ đánh dấu đang sửa
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
                ###########
    def show_quan_ly_ban(self):
        print("Chọn: Quản lý bàn")

    def show_quan_ly_tai_khoan(self):
        print("Chọn: Quản lý tài khoản")