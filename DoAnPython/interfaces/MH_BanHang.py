import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime

from objects.Ban import Ban, DanhSachBan 
from .MH_QuanLy import MH_QuanLy
from components.HoverButton import HoverButton
from objects.DanhSachNhomMon import DanhSachNhomMon

# MÀN HÌNH BÁN HÀNG

class MH_BanHang(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f4ef")

        self.controller = controller
        self.bg_image_ref = None 
        self.button_bans = [] 

        table_icon_path = "images/ly_cafe.png"
        try:
            img_table = Image.open(table_icon_path)
            img_table = img_table.resize((75, 75), Image.Resampling.LANCZOS)
            self.table_icon_ref = ImageTk.PhotoImage(img_table)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy icon bàn tại {table_icon_path}")
            self.table_icon_ref = None


        def update_time():
            now = datetime.now().strftime("%H:%M:%S  %d/%m/%Y")
            self.label_time.config(text=now)
            self.label_time.after(1000, update_time)


        # FULL FRAME
        full_frame = tk.Frame(self, bg="#f9f4ef")
        full_frame.place(x=0, y=0, width=1280, height=640)
        
        # ===================== KHU VỰC CHỨA CÁC FRAME CON =====================
        self.content_container = tk.Frame(full_frame, bg="#f9f4ef")
        self.content_container.place(x=0, y=120, width=1280, height=520)


        # ===================== TRANG CHỦ (tt_frame) ============================
        bg_path = "images/anh_nen.png"
        try:
            img_bg = Image.open(bg_path)
            img_bg = img_bg.resize((1280, 520), Image.Resampling.LANCZOS)
            self.bg_image_ref = ImageTk.PhotoImage(img_bg)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file ảnh tại đường dẫn {bg_path}")
            self.bg_image_ref = None
        except NameError: # Xử lý nếu ImageTk chưa được định nghĩa (chưa import Pillow)
            self.bg_image_ref = None

        # ===================== KHU VỰC BÁN HÀNG (bh_frame) =====================
        self.bh_frame = tk.Frame(self.content_container, bg="#eaddcf")
        self.bh_frame.grid(row = 0, column = 0, sticky="nsew")
        
        ban_frame = tk.Frame(self.bh_frame, bg = "#FEF9E6")
        ban_frame.place(x = 10, y = 10, width = 450, height = 420)
        
        img_bh_bg = Image.open("images/banhang_bg.png").resize((800, 500), Image.Resampling.LANCZOS)
        photo_bh_bg = ImageTk.PhotoImage(img_bh_bg)
        self.photo_bh_bg_label = tk.Label(self.bh_frame, bd = 0, image = photo_bh_bg) 
        self.photo_bh_bg_label.place(x = 470, y = 10)
        self.photo_bh_bg_ref = photo_bh_bg


        du_lieu_ban_path = "data/du_lieu_ban.json"
        self.ds_ban = DanhSachBan()
        self.ds_ban.doc_file(du_lieu_ban_path)

        self.tao_danh_sach_ban(ban_frame)
        
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # TẠO KHUNG CHỨA CÁC NÚT MENU ĐỂ DỄ DÀNG QUẢN LÝ
        self.menu_frame = tk.Frame(full_frame, bg="#f9f4ef")
        self.menu_frame.place(x=0, y=0, width=860, height=120)

        # Bảng chú thích
        note_frame = tk.Frame(self.bh_frame, bg = "#eaddcf")
        note_frame.place(x = 10, y = 440, width = 450, height = 80)

        note_color_free = tk.Label(note_frame, bg = "#4CAF50", width = 10, height = 1)
        note_color_free.place(x = 10, y = 10)

        note_color_serve = tk.Label(note_frame, bg = "#FFC107", width = 10, height = 1)
        note_color_serve.place(x = 10, y = 45)

        note_color_booked = tk.Label(note_frame, bg = "#F44336", width = 10, height = 1)
        note_color_booked.place(x = 250, y = 10)
        #################################################################################
        note_free_label = tk.Label(note_frame, text = "Bàn còn trống", fg="black", bg = "#eaddcf", font=("proxima-nova", 10, "bold"))
        note_free_label.place(x = 100, y = 10)

        note_serve_label = tk.Label(note_frame, text = "Bàn đang phục vụ", fg="black", bg = "#eaddcf", font=("proxima-nova", 10, "bold"))
        note_serve_label.place(x = 100, y = 45)

        note_booked_label = tk.Label(note_frame, text = "Bàn đã đặt", fg="black", bg = "#eaddcf", font=("proxima-nova", 10, "bold"))
        note_booked_label.place(x = 340, y = 10)
        #################################################################################

        # ============================ QTV =======================================
        qtv_frame = tk.Frame(full_frame, bg="#f9f4ef")
        qtv_frame.place(x=1080, y=40, width=160, height=60)

        # Tạo Label QTV và lưu vào self.
        self.label_qtv = tk.Label(
            qtv_frame,
            text="",
            fg="#716040", font=("proxima-nova", 12, "bold"),
            bg="#f9f4ef"
        )
        self.label_qtv.place(x=0, y=0, width=160, height=30)

        # KHỞI TẠO CÁC NÚT CHUNG (Trang chủ, Bán hàng)
        self.buttons = []
        buttons_info = [
            ("TRANG CHỦ", 40, lambda: self.controller.show_frame("MH_TrangChu")),
            ("BÁN HÀNG", 200, lambda: self.controller.show_frame("MH_BanHang")),
        ]
        
        for text, xpos, cmd in buttons_info:
            btn = HoverButton(
                self.menu_frame,
                text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851",
                fg="#fffffe",
                cursor="hand2",
                bd=3,
                relief="ridge",
                command=cmd
            )
            btn.place(x=xpos, y=40, width=125, height=60)
            self.buttons.append(btn)
        
        # TẠO NÚT ĐĂNG XUẤT
        HoverButton(
            qtv_frame,
            text="Đăng xuất",
            font=("proxima-nova", 14, "bold"),
            bg="#8c7851", fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command=lambda: self.logout()
        ).place(x=0, y=30, width=160, height=30)

        # TẠO VÀ LƯU CÁC NÚT ĐẶC QUYỀN
        self.manager_buttons = []
        manager_buttons_info = [
            ("QUẢN LÝ", 360,  lambda: self.controller.show_frame("MH_QuanLy")), 
            ("THỐNG KÊ", 520, None), 
            ("CREDITS", 680, None)
        ]
        
        for text, xpos, cmd in manager_buttons_info:
            btn = HoverButton(
                self.menu_frame,
                text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851",
                fg="#fffffe",
                cursor="hand2",
                bd=3,
                relief="ridge",
                command=cmd
            )

            self.manager_buttons.append(btn)
            
        # ===================== NGÀY GIỜ =====================
        date_time_frame = tk.Frame(full_frame, bg="#f9f4ef")
        date_time_frame.place(x=860, y=0, width=220, height=40)

        self.label_time = tk.Label(
            date_time_frame,
            fg="#00214d",
            bg="#f9f4ef",
            font=("proxima-nova", 14, "bold")
        )
        self.label_time.pack(expand=True, anchor="nw")

        update_time() 

        # ===================== TRẠNG THÁI BÀN =====================
        table_free = self.ds_ban.free()
        table_reserved = self.ds_ban.serve()
        table_serve = self.ds_ban.booked()

        self.table_free_var = StringVar()
        self.table_reserved_var = StringVar()
        self.table_serve_var = StringVar()
        
        table_frame = tk.Frame(full_frame, bg="#f9f4ef")
        table_frame.place(x=860, y=40, width=220, height=60)

        tk.Label(table_frame, textvariable=self.table_free_var, fg="#716040",
                 font=("proxima-nova", 10, "bold"), bg="#f9f4ef").pack(anchor="w")
        tk.Label(table_frame, textvariable=self.table_reserved_var, fg="#716040",
                 font=("proxima-nova", 10, "bold"), bg="#f9f4ef").pack(anchor="w")
        tk.Label(table_frame, textvariable=self.table_serve_var, fg="#716040",
                 font=("proxima-nova", 10, "bold"), bg="#f9f4ef").pack(anchor="w")
        
        self.cap_nhat_thong_ke_ban()
   #============================ CHỨC NĂNG CHÍNH ==========================#
    def xu_ly_click_ban(self, ban):

        ds_loai = DanhSachNhomMon()
        ds_loai.doc_file("data/du_lieu_nhom_mon.json")

        print(f"{ban} đã được chọn.")
        
        now = "..."
        gio_den_hien_thi = f"Giờ đến: {now}"
        #============ TẠO KHUNG THÔNG TIN BÀN VÀ CHỌN MÓN======#
        info_table_frame = tk.Frame(self.bh_frame, bg = "#FEF9E6")
        info_order_frame = tk.Frame(self.bh_frame, bg = "#FEF9E6")   
        
        type_frame = tk.Frame(self.bh_frame, bg="#FEF9E6")
        temp_frame = tk.Frame(self.bh_frame, bg="#FEF9E6")


        cross_bar_1_frame = tk.Frame(self.bh_frame, bg="#eaddcf")
        cross_bar_2_frame = tk.Frame(self.bh_frame, bg="#eaddcf")


        img_menu = Image.open("images/menu.png").resize((350, 500), Image.Resampling.LANCZOS)
        photo_menu = ImageTk.PhotoImage(img_menu)
        photo_menu_label = tk.Label(info_order_frame, bd = 0, image = photo_menu)

        img_logo = Image.open("images/logo.png").resize((150,100), Image.Resampling.LANCZOS) 
        photo_logo = ImageTk.PhotoImage(img_logo)
        photo_logo_label = tk.Label(info_table_frame, bd = 0, image = photo_logo)

        ten_ban_var = StringVar(value = f"{ban.ten_ban}")
        ten_ban_label = tk.Label(info_table_frame, textvariable = ten_ban_var,font=("proxima-nova", 24, "bold"), bg="#FEF9E6")

        if ban.trang_thai != "Free":
            if ban.thoi_gian == "":
                ban.thoi_gian = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            gio_den_hien_thi = f"Giờ đến: {ban.thoi_gian}"
        else:
            ban.thoi_gian = ""

        gio_den_var = StringVar(value=gio_den_hien_thi)
        gio_den_label = tk.Label(info_table_frame, textvariable = gio_den_var, font=("proxima-nova", 12, "bold"), bg="#FEF9E6")
        
        status = "Còn trống"
        if ban.trang_thai == "Serve":
            status = "Đang phục vụ"
        elif ban.trang_thai == "Booked":
            status = "Đã đặt trước"

        status_var = StringVar(value=f"{status}")
        trang_thai_bh_label = tk.Label(info_table_frame, text = "Trạng thái:", font=("proxima-nova", 12, "bold"), fg = "#880015", bg="#FEF9E6")
        
        status_label = tk.Label(info_table_frame, textvariable = status_var, font=("proxima-nova", 11, "bold"), bg="#FEF9E6")
        
        dat_ban_text = "Huỷ đặt" if ban.trang_thai == "Booked" else "Đặt bàn"
        dat_ban_var = StringVar(value = dat_ban_text)

        goi_mon_frame = tk.Frame(info_order_frame, bg = "#FEF9E6")
        #===========================================================#
        def thay_doi_trang_thai():
            if ban.trang_thai == "Free":
                ban.trang_thai = "Booked"
                dat_ban_var.set("Huỷ đặt")
                status_var.set("Đã đặt trước")
                ban.thoi_gian = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
                print("Đã đặt bàn")
                gio_den_var.set(datetime.now().strftime("Giờ đến: %H:%M:%S %d/%m/%Y"))
            elif ban.trang_thai == "Booked":
                ban.trang_thai = "Free"
                dat_ban_var.set("Đặt bàn")
                status_var.set("Còn trống")
                ban.thoi_gian = ""
                print("Đã huỷ đặt")
                gio_den_var.set("Giờ đến: ...")
            self.cap_nhat_mau_nut_ban(ban)
            self.ds_ban.ghi_file("data/du_lieu_ban.json")

        def goi_mon():
            goi_mon_frame.place(x = 0, y = 0 , width = 500, height = 500)
            ban.trang_thai = "Serve"
            status_var.set("Đang phục vụ")
            ban.thoi_gian = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            print("Đang gọi món")
            gio_den_var.set(datetime.now().strftime("Giờ đến: %H:%M:%S %d/%m/%Y"))
            self.cap_nhat_mau_nut_ban(ban)
            self.ds_ban.ghi_file("data/du_lieu_ban.json")
            dat_ban_button.place_forget()
            goi_mon_button.place_forget()
            huy_ban_button.place(x = 120, y = 230)
            type_frame.place(x = 820, y = 10, width = 90, height = 500)
            temp_frame.place_forget()

        def huy_ban():
            ban.trang_thai = "Free"
            status_var.set("Còn trống")
            dat_ban_button.place(x = 35, y = 230)
            goi_mon_button.place(x = 190, y = 230)
            huy_ban_button.place_forget()
            gio_den_var.set("Giờ đến: ...")
            ban.thoi_gian = ""
            self.ds_ban.ghi_file("data/du_lieu_ban.json")
            type_frame.place_forget()
            self.cap_nhat_mau_nut_ban(ban)
            self.ds_ban.ghi_file("data/du_lieu_ban.json")
            goi_mon_frame.place_forget()
            photo_menu_label.place(x = 0, y = 0) 
            photo_menu_label.image = photo_menu
            temp_frame.place(x = 820, y = 10, width = 90, height = 500)

        def raise_bh_bg():
            self.photo_bh_bg_label.tkraise()

        def xu_ly_click_loai_mon(loai):
            print(f"Đã chọn loại món: {loai}")
        #======================================================#
        dat_ban_button = tk.Button(info_table_frame, 
            textvariable = dat_ban_var,
            width = 11, 
            height = 2,
            font=("proxima-nova", 12, "bold"), 
            bg="#8c7851", 
            fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command = thay_doi_trang_thai)

        goi_mon_button = tk.Button(info_table_frame, 
            text = "Gọi món",
            width = 11, 
            height = 2,
            font=("proxima-nova", 12, "bold"), 
            bg="#8c7851", 
            fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command = goi_mon)
        
        quay_lai_button = tk.Button(info_table_frame,
            text = "<<<",
            width = 11, 
            height = 1,
            font=("proxima-nova", 12, "bold"), 
            bg="#8c7851", 
            fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command = raise_bh_bg)

        huy_ban_button = tk.Button(info_table_frame,
            text = "Huỷ bàn",
            width = 11, 
            height = 2,
            font=("proxima-nova", 12, "bold"), 
            bg="#8c7851", 
            fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command = huy_ban)

        #===========================================================#
        cross_bar_1_frame.place(x = 910, y = 10 ,width = 10, height = 500)
        cross_bar_2_frame.place(x = 810, y = 10 ,width = 10, height = 500)

        info_table_frame.place(x = 470, y = 10, width = 340, height = 500)        
        info_order_frame.place(x = 920, y = 10, width = 350, height = 500)

        temp_frame.place(x = 820, y = 10, width = 90, height = 500)

        photo_logo_label.place(x = 30, y = 30)
        photo_logo_label.image = photo_logo

        ten_ban_label.place(x = 220, y = 30)
        gio_den_label.place(x = 30, y = 150)

        trang_thai_bh_label.place(x = 30, y = 180)
        status_label.place(x = 120, y = 180)

        type_label = tk.Label(info_table_frame, width = 40, bg = "black")
        type_label.place(x = 30, y = 210, height = 1)

        if ban.trang_thai == "Free" or ban.trang_thai == "Booked":
            photo_menu_label.place(x = 0, y = 0)
            photo_menu_label.image = photo_menu
            dat_ban_button.place(x = 35, y = 230)
            goi_mon_button.place(x = 190, y = 230)
            quay_lai_button.place(x = 120, y = 300)
        else:
            huy_ban_button.place(x = 120, y = 230)
            quay_lai_button.place(x = 120, y = 300)

        #======================================================#
        y_position = 20
        padding = 5 
        
        for nhom_mon in ds_loai.ds:
            loai_button = tk.Button(type_frame, 
                text = nhom_mon,
                width = 10, 
                height = 1,
                font=("proxima-nova", 9, "bold"), 
                bg= "#B8860B", 
                fg= "#4B0000",
                cursor="hand2",
                bd=3, relief="raised",
                command = lambda nm=nhom_mon: xu_ly_click_loai_mon(nm)) 
            
            loai_button.place(x = 4, y = y_position)
            
            y_position += 2 * 20 + padding
        #======================================================#
    def tao_danh_sach_ban(self, frame):
        SO_COT = 4  
        SO_HANG = 4  
        frame.pack_propagate(False)
        ds_ban_hien_thi = self.ds_ban.ds[:SO_HANG * SO_COT]
        for hang in range(SO_HANG):
            for cot in range(SO_COT):
                # Tính chỉ mục của bàn trong danh sách 
                index = hang * SO_COT + cot
                if index < len(ds_ban_hien_thi):
                    ban = ds_ban_hien_thi[index]
                    trang_thai_mau = {
                        "Free": "#4CAF50",    # Xanh lá cây
                        "Serve": "#FFC107",   # Vàng (Đang phục vụ)
                        "Booked": "#F44336",  # Đỏ (Đã đặt)
                    }.get(ban.trang_thai, "#9E9E9E")

                    btn_ban = tk.Button(
                        frame,
                        text=f"{ban.ten_ban}",
                        
                        image = self.table_icon_ref,
                        compound = "top",

                        bg=trang_thai_mau, 
                        fg="white",
                        font=("Arial", 10, "bold"),
                        
                        padx = 5, 

                        command=lambda b_obj=ban: self.xu_ly_click_ban(b_obj)
                    )
                    
                    btn_ban.grid(
                        row=hang,  
                        column=cot,  
                        padx=5,  
                        pady=5,  
                        sticky="nsew",
                    )
                    btn_ban.image = self.table_icon_ref
                    # Lưu tham chiếu nút
                    self.button_bans.append(btn_ban) 
                else:
                    # Tạo ô trống hoặc nút bị vô hiệu hóa nếu ít hơn 16 bàn
                    empty_label = tk.Label(frame, text="", bg="#FEF9E6")
                    empty_label.grid(row=hang, column=cot, padx=5, pady=5, sticky="nsew")
        
        for i in range(SO_HANG):
            frame.grid_rowconfigure(i, weight=1) 
        for i in range(SO_COT):
            frame.grid_columnconfigure(i, weight=1) 

    def update_user_display(self):
        """Cập nhật tên QTV và hiển thị/ẩn các nút đặc quyền dựa trên role."""
        
        current = self.controller.current_user
        if current:
            username = current.username
            user_role = current.role
        else:
            # Trường hợp lỗi/đăng xuất (fallback)
            username = "N/A"
            user_role = ""
            
        # 1. Cập nhật tên QTV
        self.label_qtv.config(text=f"QTV: {username}")
        
        # 2. Xử lý nút đặc quyền (Manager)
        is_manager = user_role.lower() == "manager"
        
        # Danh sách tọa độ cho các nút đặc quyền đã lưu trong self.manager_buttons
        manager_xpos = [360, 520, 680]
        
        for i, btn in enumerate(self.manager_buttons):
            if is_manager:
                # Hiện nút nếu là Manager
                btn.place(x=manager_xpos[i], y=40, width=125, height=60)
            else:
                # Ẩn nút nếu không phải Manager
                btn.place_forget()

    # Chức năng thoát
    def logout(self):
        self.controller.show_frame("MH_DangNhap")

    # Đổi tên từ show_frame thành show_page theo mã gốc của bạn
    def show_page(self, frame):
        """Hiện thị các trang bằng cách đưa frame mong muốn lên trên cùng."""
        frame.tkraise()

    def on_show(self):
        """Hàm được gọi khi màn hình được hiển thị."""
        # Gọi hàm cập nhật ngay khi màn hình Bán Hàng chuẩn bị hiện
        self.update_user_display()
        self.show_page(self.bh_frame) # Mặc định hiển thị trang chủ

    def cap_nhat_mau_nut_ban(self, ban_obj):

        trang_thai_mau = {
            "Free": "#4CAF50",    # Xanh lá cây
            "Serve": "#FFC107",   # Vàng (Đang phục vụ)
            "Booked": "#F44336",  # Đỏ (Đã đặt)
        }.get(ban_obj.trang_thai, "#9E9E9E")

        for i, ban_hien_thi in enumerate(self.ds_ban.ds[:len(self.button_bans)]):
            if ban_hien_thi.ten_ban == ban_obj.ten_ban:
                btn = self.button_bans[i]
                btn.config(bg=trang_thai_mau)
                self.cap_nhat_thong_ke_ban()
                break

    def cap_nhat_thong_ke_ban(self):

        table_free = self.ds_ban.free()
        table_serve = self.ds_ban.serve()
        table_booked = self.ds_ban.booked()

        self.table_free_var.set(f"Bàn còn trống: {table_free:02d}")
        self.table_reserved_var.set(f"Bàn đã đặt: {table_booked:02d}")
        self.table_serve_var.set(f"Bàn đang phục vụ: {table_serve:02d}")