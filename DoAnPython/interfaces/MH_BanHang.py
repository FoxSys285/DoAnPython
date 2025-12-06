import tkinter as tk
from tkinter import *
from tkinter import ttk  

import math
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime

from objects.Mon import Mon, DanhSachMon
from objects.Ban import Ban, DanhSachBan 
from objects.HoaDon import HoaDon, DanhSachHoaDon

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
        self.button_mons = []

        self.ds_mon_an = DanhSachMon()
        self.ds_mon_an.doc_file("data/du_lieu_mon.json")

        self.ds_hoa_don = DanhSachHoaDon()
        self.ds_hoa_don.doc_file("data/du_lieu_hoa_don.json")

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
            font=("proxima-nova", 12, "bold"),
            bg="#8c7851", fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command=lambda: self.logout()
        ).place(x=0, y=30, width=160, height=30)

        # TẠO VÀ LƯU CÁC NÚT ĐẶC QUYỀN
        self.manager_buttons = []
        manager_buttons_info = [
            ("QUẢN LÝ", 360,  lambda: self.controller.show_frame("MH_QuanLy")), 
            ("THỐNG KÊ", 520, lambda: self.controller.show_frame("MH_ThongKe")), 
            ("CREDITS", 680, lambda: self.controller.show_frame("MH_Credits"))
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
    def xu_ly_click_mon(self, mon, ban, hoa_don_listbox):
        popup = tk.Toplevel(self, bg = "#FEF9E6")
        popup.title("Nhập số lượng món")
        popup_width = 350
        popup_height = 300

        # Lấy kích thước màn hình
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Tính vị trí giữa màn hình
        x = (screen_width - popup_width) // 2
        y = (screen_height - popup_height) // 2

        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)

        popup_img_logo = Image.open("images/logo.png").resize((150,100), Image.Resampling.LANCZOS) 
        popup_photo_logo = ImageTk.PhotoImage(popup_img_logo)
        popup_photo_logo_label = tk.Label(popup, bd = 0, image = popup_photo_logo)
        popup_photo_logo_label.place(x = 20, y = 0)
        popup_photo_logo_label.image = popup_photo_logo

        popup_ten_ban_label = tk.Label(popup, text = f"{ban.ten_ban}", font=("proxima-nova", 24, "bold"), bg = "#FEF9E6")
        popup_ten_ban_label.place(x = 200, y = 30)

        popup_ten_mon_label = tk.Label(popup, text = f"Món: {mon.ten_mon}", font=("proxima-nova", 16, "bold"), fg = "#716040", bg = "#FEF9E6")
        popup_ten_mon_label.place(x = 22, y = 120)

        cnt = 0
        so_luong_text = StringVar(value = f"{cnt}")
        popup_so_luong_label = tk.Label(popup, textvariable = so_luong_text, font=("proxima-nova", 16, "bold"), bg = "#FEF9E6")
        popup_so_luong_label.place(x = 135, y = 165)


        def giam():
            current_cnt = int(so_luong_text.get())
            if current_cnt > 0:
                new_cnt = current_cnt - 1
                so_luong_text.set(new_cnt)

        def tang():
            current_cnt = int(so_luong_text.get())
            new_cnt = current_cnt + 1
            so_luong_text.set(new_cnt) 

        giam_button = tk.Button(popup, text = "-", font=("proxima-nova", 18, "bold"), fg = "white", bg = "#CC0033", command = giam, cursor = "hand2")
        giam_button.place(x = 22, y = 160, width = 90, height = 40)

        tang_button = tk.Button(popup,  text = "+", font=("proxima-nova", 18, "bold"), fg = "white", bg = "#009900", command = tang, cursor = "hand2")
        tang_button.place(x = 180, y = 160, width = 90, height = 40)

        def xac_nhan():
            try:
                sl = int(so_luong_text.get())
            except ValueError:
                sl = 0
            
            if sl <= 0:
                popup.destroy()
                return

            # Kiểm tra xem bàn đã có hóa đơn chưa
            if not hasattr(ban, "hoa_don") or ban.hoa_don is None:
                print("Lỗi: Bàn chưa được mở (Chưa bấm 'Gọi món')")
                popup.destroy()
                return

            hd = ban.hoa_don

            # Đảm bảo dsMon là một list (nếu mới khởi tạo nó có thể là object DanhSachMon rỗng)
            if not isinstance(hd.dsMon, DanhSachMon):
                hd.dsMon = DanhSachMon()

            # Kiểm tra món đã tồn tại trong hóa đơn chưa
            found = False
            for m in hd.dsMon.ds:
                if m.ma_mon == mon.ma_mon:
                    m.so_luong += sl
                    found = True
                    break
            
            if not found:
                mon_moi = Mon(
                    mon.ma_mon, 
                    mon.ten_mon, 
                    mon.don_gia, 
                    sl, 
                    mon.loai, 
                    mon.dvt
                )
                hd.dsMon.ds.append(mon_moi)

            # --- TÍNH LẠI TỔNG TIỀN ---
            tong_tien_moi = 0
            for m in hd.dsMon.ds:
                tong_tien_moi += m.so_luong * m.don_gia
            
            hd.tongTien = tong_tien_moi # Cập nhật thuộc tính tổng tiền của Object HoaDon

            self.ds_ban.ghi_file("data/du_lieu_ban.json")

            # Cập nhật giao diện
            popup.destroy()
            self.cap_nhat_listbox_hoa_don(ban, hoa_don_listbox)


        xac_nhan_button = tk.Button(popup, text = "Xác nhận", font=("proxima-nova", 11, "bold"), bg= "#8c7851", fg="#fffffe", cursor = "hand2", command = xac_nhan)
        xac_nhan_button.place(x = 30, y = 220, width = 110, height = 30)

        def huy():
            popup.destroy()

        huy_button = tk.Button(popup, text = "Hủy", font=("proxima-nova", 11, "bold"), bg= "#8c7851", fg="#fffffe", cursor = "hand2", command = huy)
        huy_button.place(x = 150, y = 220, width = 110, height = 30)
    #==========================================================================================#
    def xu_ly_click_ban(self, ban):

        current = self.controller.current_user
        if current:
            username = current.username
            user_role = current.role
        else:
            username = "ADMIN"
            user_role = "Manager"

        ban.nguoi_lap = username
        ds_loai = DanhSachNhomMon()
        ds_loai.doc_file("data/du_lieu_nhom_mon.json")

        print(f"{ban}")

        # self.ds_hoa_don.doc_file("data/du_lieu_hoa_don.json")
        if ban.trang_thai == "Serve":
            # Tìm hóa đơn đang hoạt động của bàn này
            for hd in reversed(self.ds_hoa_don.dsHD):
                if hd.maBan == ban.ten_ban:
                    ban.hoa_don = hd
                    break
        # ===================================================
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


        hoa_don_frame = tk.Frame(info_table_frame, bg="#FEF9E6", bd = 0)
        
        scroll_bar = Scrollbar(hoa_don_frame, bd = 0)
        hoa_don_listbox = tk.Listbox(hoa_don_frame, bg="#FEF9E6", bd = 0,yscrollcommand=scroll_bar.set,font=("proxima-nova", 11, "bold"))
        scroll_bar.pack(side = RIGHT, fill = Y)
        hoa_don_listbox.pack(side = LEFT, fill = BOTH, expand=True)

        # === KHU VỰC HIỂN THỊ TỔNG TIỀN ===
        tong_tien_frame = tk.Frame(info_table_frame, bg="#FEF9E6")
        tong_tien_frame.place(x=10, y=450, width=330, height=40) # Đặt ở dưới cùng danh sách món

        lbl_tong_tien_text = tk.Label(tong_tien_frame, text="Tổng cộng:", font=("proxima-nova", 12, "bold"), bg="#FEF9E6", fg="#716040")
        lbl_tong_tien_text.pack(side=LEFT)

        self.lbl_tong_tien_value = tk.Label(tong_tien_frame, text="0 VNĐ", font=("proxima-nova", 14, "bold"), bg="#FEF9E6", fg="#CC0033")
        self.lbl_tong_tien_value.pack(side=RIGHT)

        if ban.trang_thai == "Serve":
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

        chon_mon_label = tk.Label(info_order_frame, text = "Chọn món", font=("proxima-nova", 14, "bold"), fg="#F9F4EF", bg = "#C58747")

        mon_an_frame = tk.Frame(info_order_frame, bg="#FEF9E6")


        
        #===========================================================#
        def dat_ban():
            if ban.trang_thai == "Free":
                ban.trang_thai = "Booked"
                dat_ban_var.set("Huỷ đặt")
                status_var.set("Đã đặt trước")
                print("Đã đặt bàn")
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
            type_frame.place(x = 820, y = 10, width = 90, height = 500)
            temp_frame.place_forget()
            chon_mon_label.place(x = 10, y = 10, width = 330, height = 40)
            hoa_don_frame.place(x = 10, y = 220, width = 330, height = 170)
            chinh_sua_button.place(x = 120, y = 400, width = 100, height = 40)

            
            # ======= TẠO HÓA ĐƠN MỚI =======
            ma_hd = f"HD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            gio_lap = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            hoa_don_moi = HoaDon(ma_hd, gio_lap, DanhSachMon(), 0, ban.ten_ban)

            quay_lai_button.place_forget()
            ban.hoa_don = hoa_don_moi
            self.ds_hoa_don.dsHD.append(hoa_don_moi)
            
            huy_ban_button.place(x = 10, y = 400, width = 100, height = 40)
            thanh_toan_button.place(x = 230, y = 400, width = 100, height = 40)

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
            ban.hoa_don = None
            self.ds_ban.ghi_file("data/du_lieu_ban.json")
            goi_mon_frame.place_forget()
            photo_menu_label.place(x = 0, y = 0) 
            photo_menu_label.image = photo_menu
            temp_frame.place(x = 820, y = 10, width = 90, height = 500)
            chon_mon_label.place_forget()
            mon_an_frame.place_forget()
            quay_lai_button.place(x = 120, y = 300, width = 100, height = 40)
            hoa_don_frame.place_forget()
            thanh_toan_button.place_forget()
            chinh_sua_button.place_forget()
            self.lbl_tong_tien_value.config(text="0 VNĐ")
            ban.hoa_don = None
            self.cap_nhat_listbox_hoa_don(ban, hoa_don_listbox)

        def thanh_toan(ban):
            if not ban.hoa_don.dsMon.ds:
                print("Bàn chưa đặt món")
                return
            ban.hoa_don.gioRa = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            popup = tk.Toplevel(self, bg = "#FEF9E6")
            popup.title("Thanh toán")
            popup_width = 350
            popup_height = 300
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            x = (screen_width - popup_width) // 2
            y = (screen_height - popup_height) // 2
            popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
            popup.resizable(False, False)

            text_label = tk.Label(popup, text = f"{ban.ten_ban} - Thanh toán",font=("proxima-nova", 20, "bold"), bg="#FEF9E6")
            text_label.place(x = 10, y = 10)
            
            # Tính tổng tiền từ thuộc tính hoa_don
            tong_tien_phai_tra = 0
            if ban.hoa_don and isinstance(ban.hoa_don.dsMon, DanhSachMon):
                for mon in ban.hoa_don.dsMon.ds:
                    tong_tien_phai_tra += mon.so_luong * mon.don_gia 

            # Hiển thị Tổng tiền
            tk.Label(popup, text=f"Tổng tiền:", font=("proxima-nova", 14, "bold"), bg="#FEF9E6", fg="#716040").place(x=10, y=80)
            lbl_tong_tien = tk.Label(popup, text=f"{tong_tien_phai_tra:,} VNĐ".replace(",", "."), font=("proxima-nova", 16, "bold"), bg="#FEF9E6", fg="#CC0033")
            lbl_tong_tien.place(x=150, y=80)

            khach_dua_var = tk.StringVar(value="0")
            tien_thua_var = tk.StringVar(value="0 VNĐ")

            def format_number_string(text):
                return "".join(filter(str.isdigit, text))

            def tinh_tien_thua(*args):
                try:
                    khach_dua_str = format_number_string(khach_dua_var.get())
                    khach_dua = int(khach_dua_str)
                    
                    tien_thua = khach_dua - tong_tien_phai_tra
                    
                    tien_thua_var.set(f"{tien_thua:,} VNĐ".replace(",", "."))
                    
                    khach_dua_var.set(f"{khach_dua:,}".replace(",", "."))
                    return tien_thua
                    
                except ValueError:
                    # Xử lý nếu ô nhập rỗng hoặc không phải số
                    tien_thua_var.set("Lỗi nhập liệu")
                    khach_dua_var.set("0")
                
                entry_khach_dua.icursor(tk.END)
                
                
            khach_dua_var.trace_add("write", tinh_tien_thua)
            
            tk.Label(popup, text =f"Số tiền khách đưa:", font=("proxima-nova", 14, "bold"), bg="#FEF9E6", fg="#716040").place(x=10, y=120)
            
            entry_khach_dua = tk.Entry(popup, textvariable=khach_dua_var, font=("proxima-nova", 14), justify="right", bd=1, relief="solid")
            entry_khach_dua.place(x=200, y=120, width=120, height=30)
            entry_khach_dua.focus_set()

            # 3. Label Tiền thừa
            tk.Label(popup, text =f"Tiền thừa:", font=("proxima-nova", 14, "bold"), bg="#FEF9E6", fg="#716040").place(x=10, y=160)
            lbl_tien_thua = tk.Label(popup, textvariable=tien_thua_var, font=("proxima-nova", 16, "bold"), bg="#FEF9E6", fg="#009900")
            lbl_tien_thua.place(x=180, y=160)
            # Hàm xác nhận thanh toán cuối cùng
            def xac_nhan_thanh_toan():
                if tinh_tien_thua() < 0:
                    print("Giá trị ko hợp lệ")
                    return
                if ban.hoa_don:

                    ban.hoa_don.tongTien = tong_tien_phai_tra 
                    ban.hoa_don.thoiGianKetThuc = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    # 3. Lưu danh sách hóa đơn vào file
                    self.ds_hoa_don.ghi_file("data/du_lieu_hoa_don.json")

                # Lưu số lượng món để thống kê
                for i in ban.hoa_don.dsMon.ds:
                    for mon in self.ds_mon_an.ds:
                        if mon.ma_mon == i.ma_mon:
                            mon.so_luong += i.so_luong
                            break
                            
                self.ds_mon_an.ghi_file("data/du_lieu_mon.json")
                
                huy_ban() 
                # Đóng popup
                ban.trang_thai = "Free"
                status_var.set("Còn trống")
                popup.destroy()

            # Nút Xác nhận Thanh toán
            btn_xac_nhan = tk.Button(popup, text="Xác nhận", font=("proxima-nova", 11, "bold"), bg= "#8c7851", fg="#fffffe", cursor = "hand2", command = xac_nhan_thanh_toan)
            btn_xac_nhan.place(x = 30, y = 240, width = 110, height = 30)

            # Nút Hủy
            btn_huy = tk.Button(popup, text = "Hủy", font=("proxima-nova", 11, "bold"), bg= "#8c7851", fg="#fffffe", cursor = "hand2", command = popup.destroy)
            btn_huy.place(x = 150, y = 240, width = 110, height = 30)

            
            
        def chinh_sua(ban):
            popup = tk.Toplevel(self, bg = "#FEF9E6")
            popup.title("Điều chỉnh số lượng")
            popup_width = 350
            popup_height = 300

            # Lấy kích thước màn hình
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()

            # Tính vị trí giữa màn hình
            x = (screen_width - popup_width) // 2
            y = (screen_height - popup_height) // 2

            popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
            popup.resizable(False, False)

            tree = ttk.Treeview(popup, column = ("ten_mon", "so_luong"), show = "headings")
            tree.heading("ten_mon", text = "Tên món")
            tree.heading("so_luong", text = "Số lượng")

            tree.place(x = 10, y = 120, width = 330, height = 130)
            
            tk.Label(popup, text = "Tên món:",bg = "#FEF9E6").place(x = 30, y = 30)
            tk.Label(popup, text = "Số lượng:",bg = "#FEF9E6").place(x = 30, y = 60)
            
            text = tk.StringVar(value = "")
            tk.Label(popup, textvariable = text,bg = "#FEF9E6", fg = "red").place(x = 30, y = 90)

            ten_entry = tk.Entry(popup)
            so_luong_entry = tk.Entry(popup)

            ten_entry.place(x = 90, y = 30, width = 100, height = 20)
            so_luong_entry.place(x = 90, y = 60, width = 100, height = 20)
            
            def on_tree_select(event):
                selected_item = tree.focus()
                if not selected_item:
                    return

                values = tree.item(selected_item, 'values')
                
                ten_entry.delete(0, tk.END)
                ten_entry.insert(0, values[0])

                so_luong_entry.delete(0, tk.END)
                so_luong_entry.insert(0, values[1])

            for mon in ban.hoa_don.dsMon.ds:
                tree.insert("","end",values=(mon.ten_mon, mon.so_luong))

            def xac_nhan():
                ten_mon = ten_entry.get()
                so_luong = int(so_luong_entry.get())
                
                if ban.kiem_tra_co_mon(ten_mon) == False:
                    text.set("Không có món này trong hóa đơn")
                    return

                if so_luong <= 0:
                    ban.hoa_don.dsMon.xoa_mon(ten_mon)
                    print("Đã xóa món")
                    self.ds_ban.ghi_file("data/du_lieu_ban.json")
                    self.cap_nhat_listbox_hoa_don(ban, hoa_don_listbox)
                    huy()
                else:
                    ban.cap_nhat_so_luong(ten_mon, so_luong)
                    print("Cập nhật số lượng thành công")
                    self.ds_ban.ghi_file("data/du_lieu_ban.json")
                    self.cap_nhat_listbox_hoa_don(ban, hoa_don_listbox)
                    huy()

            xac_nhan_button = tk.Button(popup, text = "Xác nhận",
                font=("proxima-nova", 12, "bold"), 
                bg="#8c7851", 
                fg="#fffffe",
                cursor="hand2",
                bd=3, relief="ridge",
                command = xac_nhan)

            def huy():
                popup.destroy()

            huy_button = tk.Button(popup,text = "Hủy",
                font=("proxima-nova", 12, "bold"), 
                bg="#8c7851", 
                fg="#fffffe",
                cursor="hand2",
                bd=3, relief="ridge",
                command = huy)

            xac_nhan_button.place(x = 10, y = 260, width = 100, height = 30)
            huy_button.place(x = 240, y = 260, width = 100, height = 30)

            tree.bind("<<TreeviewSelect>>", on_tree_select)

        def raise_bh_bg():
            self.photo_bh_bg_label.tkraise()

        def xu_ly_click_loai_mon(loai):
            ds_mon = DanhSachMon()
            ds_mon.doc_file("data/du_lieu_mon.json")

            ds_mon_theo_loai = ds_mon.tim_mon_theo_loai(loai)
            so_luong = len(ds_mon_theo_loai)

            #=========== TẠO CÁC NÚT CHỌN MÓN ============#
            cot_mon_an = 3
            hang_mon_an = math.ceil(so_luong / cot_mon_an)

            button_mon_an_width = 100
            button_mon_an_height = 60
            spacing = 15

            for widget in mon_an_frame.winfo_children():
                widget.destroy()

            for r in range(hang_mon_an):
                for c in range(cot_mon_an):
                    index = r * cot_mon_an + c
                    if index >= so_luong:
                        break 

                    mon = ds_mon_theo_loai[index]
                    btn_mon = tk.Button(mon_an_frame, 
                        text=f"{mon.ten_mon}\n {mon.don_gia:,} VND".replace(",", "."),
                        command=lambda mon_obj=mon: self.xu_ly_click_mon(mon_obj, ban, hoa_don_listbox))

                    btn_mon.place(
                        x = c*(button_mon_an_width + spacing),
                        y = r*(button_mon_an_height + spacing),
                        width = button_mon_an_width, height = button_mon_an_height
                    )
                    self.button_mons.append(btn_mon) 
            #============================================#
            mon_an_frame.place(x = 10, y = 60, width = 330, height = 430)

        
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
            command = dat_ban)

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

        thanh_toan_button = tk.Button(info_table_frame, 
            text = "Thanh toán", 
            width = 11, 
            height = 1,
            font=("proxima-nova", 12, "bold"), 
            bg="#8c7851", 
            fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command=lambda b_obj=ban: thanh_toan(b_obj))

        chinh_sua_button = tk.Button(info_table_frame,
            text = "Chỉnh sửa", 
            width = 11, 
            height = 1,
            font=("proxima-nova", 12, "bold"), 
            bg="#8c7851", 
            fg="#fffffe",
            cursor="hand2",
            bd=3, relief="ridge",
            command=lambda b_obj=ban: chinh_sua(b_obj))
        #===========================================================#
        if ban.trang_thai == "Serve":
            # Gọi hàm cập nhật sau khi tất cả GUI đã sẵn sàng
            self.cap_nhat_listbox_hoa_don(ban, hoa_don_listbox)
        cross_bar_1_frame.place(x = 910, y = 10 ,width = 10, height = 500)
        cross_bar_2_frame.place(x = 810, y = 10 ,width = 10, height = 500)

        info_table_frame.place(x = 470, y = 10, width = 340, height = 500)        
        info_order_frame.place(x = 920, y = 10, width = 350, height = 500)

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
            quay_lai_button.place(x = 120, y = 300, width = 100, height = 40)
            temp_frame.place(x = 820, y = 10, width = 90, height = 500)
            type_frame.place_forget()
        else:
            temp_frame.place_forget()
            type_frame.place(x = 820, y = 10, width = 90, height = 500)
            chon_mon_label.place(x = 10, y = 10, width = 330, height = 40)
            hoa_don_frame.place(x = 10, y = 220, width = 330, height = 170)
            huy_ban_button.place(x = 10, y = 400, width = 100, height = 40)
            thanh_toan_button.place(x = 230, y = 400, width = 100, height = 40)
            chinh_sua_button.place(x = 120, y = 400, width = 100, height = 40)


        #======================================================#
        y_position = 50
        padding = 5 

        for nhom_mon in ds_loai.ds:
            loai_button = tk.Button(type_frame, 
                text = nhom_mon,
                width = 10, 
                height = 1,
                font=("proxima-nova", 9, "bold"), 
                bg= "#C58745", 
                fg= "#F9F4EF",
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
            username = "ADMIN"
            user_role = "Manager"
            
        # 1. Cập nhật tên QTV
        self.label_qtv.config(text=f"QTV: {username.upper()}")
        
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
        self.update_user_display()
        self.show_page(self.bh_frame)

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

    def cap_nhat_listbox_hoa_don(self, ban, listbox):
        listbox.delete(0, tk.END) # Xóa dữ liệu cũ

        if not hasattr(ban, "hoa_don") or ban.hoa_don is None:
            return

        hd = ban.hoa_don
        tong_tien_hien_tai = 0

        # Duyệt qua danh sách món (đang là list các dict)
        if isinstance(hd.dsMon, DanhSachMon):
            for mon in hd.dsMon.ds:
                ten = mon.ten_mon 
                sl = mon.so_luong  
                dg = mon.don_gia
                thanh_tien = sl * dg
                tong_tien_hien_tai += thanh_tien
                
                dong_hien_thi = f"{ten} (x{sl}) - {thanh_tien:,} VNĐ".replace(",", ".")
                print("Đã thêm thành công")
                listbox.insert(tk.END, dong_hien_thi)
        else:
            print("Thêm ko thành công")
        if hasattr(self, 'lbl_tong_tien_value'):
             self.lbl_tong_tien_value.config(text=f"{tong_tien_hien_tai:,} VNĐ".replace(",", "."))