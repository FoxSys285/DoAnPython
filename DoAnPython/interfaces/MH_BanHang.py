import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance # Import thêm ImageEnhance để làm mờ ảnh (tùy chọn)
from datetime import datetime

from objects.Ban import Ban, DanhSachBan 
from .MH_QuanLy import MH_QuanLy

# Giả định lớp HoverButton
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.default_bg = kw.get('bg', self['bg'])
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = '#a99c80' # Màu hover
    
    def on_leave(self, e):
        self['bg'] = self.default_bg

# MÀN HÌNH BÁN HÀNG

class MH_BanHang(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f9f4ef")
        self.controller = controller
        
        # Biến tham chiếu ảnh nền Tcl/Tk (Cần thiết cho ảnh TT_frame)
        self.bg_image_ref = None 

        # KHỞI TẠO BIẾN THAM CHIẾU NÚT BÀN NGAY TẠI ĐÂY (Vị trí mới)
        self.button_bans = [] 

        table_icon_path = "images/ly_cafe.png" # Cần đảm bảo đường dẫn này đúng
        try:
            img_table = Image.open(table_icon_path)
            img_table = img_table.resize((75, 75), Image.Resampling.LANCZOS)
            # Lưu đối tượng ImageTk.PhotoImage vào biến của lớp
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
        # Khu vực này sẽ chứa tt_frame và bh_frame (chồng lên nhau)
        self.content_container = tk.Frame(full_frame, bg="#f9f4ef")
        self.content_container.place(x=0, y=120, width=1280, height=520)


        # ===================== TRANG CHỦ (tt_frame) ============================
        # Tải ảnh nền
        bg_path = "images/anh_nen.png" # Cần đảm bảo đường dẫn này đúng
        try:
            img_bg = Image.open(bg_path)
            # Giảm kích thước và làm ảnh nền hơi mờ đi (Tùy chọn)
            img_bg = img_bg.resize((1280, 520), Image.Resampling.LANCZOS)
            # TẠO ĐỐI TƯỢNG PHOTOIMAGE VÀ LƯU VÀO THAM CHIẾU CỦA CLASS
            self.bg_image_ref = ImageTk.PhotoImage(img_bg)
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file ảnh tại đường dẫn {bg_path}")
            self.bg_image_ref = None
        except NameError: # Xử lý nếu ImageTk chưa được định nghĩa (chưa import Pillow)
            self.bg_image_ref = None

        # ===================== KHU VỰC BÁN HÀNG (bh_frame) =====================
        self.bh_frame = tk.Frame(self.content_container, bg="#eaddcf")
        self.bh_frame.grid(row = 0, column = 0, sticky="nsew") # Đặt cùng vị trí với tt_frame
        
        ban_frame = tk.Frame(self.bh_frame, bg = "#f9f4ef")
        ban_frame.place(x = 10, y = 10, width = 500, height = 420) # Tăng height để đủ 16 bàn
        
        du_lieu_ban_path = "data/du_lieu_ban.json"
        self.ds_ban = DanhSachBan()
        self.ds_ban.doc_file(du_lieu_ban_path)

        self.tao_danh_sach_ban(ban_frame)
        
        # Cấu hình container chia đều không gian cho các frame con (nếu cần)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # TẠO KHUNG CHỨA CÁC NÚT MENU ĐỂ DỄ DÀNG QUẢN LÝ
        self.menu_frame = tk.Frame(full_frame, bg="#f9f4ef")
        self.menu_frame.place(x=0, y=0, width=860, height=120)

        # Bảng chú thích
        note_frame = tk.Frame(self.bh_frame, bg = "#eaddcf")
        note_frame.place(x = 10, y = 440, width = 500, height = 80)

        # "Free": "#4CAF50",    # Xanh lá cây
        # "Serve": "#FFC107",   # Vàng (Đang phục vụ)
        # "Booked": "#F44336",  # Đỏ (Đã đặt)

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
            text="", # Để trống ban đầu, sẽ cập nhật sau
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
                self.menu_frame, # Dùng self.menu_frame
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
                self.menu_frame, # Dùng self.menu_frame
                text=text,
                font=("proxima-nova", 14, "bold"),
                bg="#8c7851",
                fg="#fffffe",
                cursor="hand2",
                bd=3,
                relief="ridge",
                command=cmd
            )
            # Không place() ở đây, sẽ place() trong update_user_display()
            self.manager_buttons.append(btn)
            
        # ===================== NGÀY GIỜ =====================
        date_time_frame = tk.Frame(full_frame, bg="#f9f4ef")
        date_time_frame.place(x=860, y=0, width=220, height=40)

        # KHÔNG DÙNG global, GÁN VÀO self.
        self.label_time = tk.Label(
            date_time_frame,
            fg="#00214d",
            bg="#f9f4ef",
            font=("proxima-nova", 14, "bold")
        )
        self.label_time.pack(expand=True, anchor="nw")

        update_time() # Gọi hàm update_time sau khi label đã được tạo

        # ===================== TRẠNG THÁI BÀN =====================

        table_free = self.ds_ban.free()
        table_reserved = self.ds_ban.serve()
        table_serve = self.ds_ban.booked()

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
        
        # Gọi hàm tạo danh sách bàn sau khi self.ds_ban và self.button_bans đã sẵn sàng
        self.tao_danh_sach_ban(ban_frame)

   #============================ CHỨC NĂNG CHÍNH ==========================#
    def xu_ly_click_ban(self, ban):
        print(f"{ban} đã được chọn.")
        
        #============ TẠO KHUNG THÔNG TIN BÀN VÀ CHỌN MÓN======#
        info_table_frame = tk.Frame(self.bh_frame, bg = "#f9f4ef")
        info_order_frame = tk.Frame(self.bh_frame, bg = "white")   
        info_table_frame.place(x = 520, y = 10, width = 340, height = 500)
        info_order_frame.place(x = 870, y = 10, width = 400, height = 500)
        #======================================================#
        img_logo = Image.open("images/logo.png").resize((150,100), Image.Resampling.LANCZOS) 
        photo_logo = ImageTk.PhotoImage(img_logo)
        photo_label = tk.Label(info_table_frame, bd = 0, image = photo_logo)
        photo_label.place(x = 30, y = 30)
        photo_label.image = photo_logo

        ten_ban_label = tk.Label(info_table_frame, text = "Bàn 1",font=("proxima-nova", 24, "bold"), bg="#f9f4ef")
        ten_ban_label.place(x = 220, y = 30)
        #======================================================#
        # self.ds_ban

    def tao_danh_sach_ban(self, frame):
        """Tạo lưới 16 bàn (Button) và đặt vào frame."""
        
        SO_COT = 4  # Số cột của lưới
        SO_HANG = 4  # Số hàng của lưới
        
        frame.pack_propagate(False) # Ngăn không cho frame chứa bàn bị co lại

        ds_ban_hien_thi = self.ds_ban.ds[:SO_HANG * SO_COT]
        
        for hang in range(SO_HANG):
            for cot in range(SO_COT):
                
                # Tính chỉ mục của bàn trong danh sách 
                index = hang * SO_COT + cot
                
                if index < len(ds_ban_hien_thi):
                    ban = ds_ban_hien_thi[index]
                    
                    # 1. Định nghĩa màu nền dựa trên trạng thái
                    trang_thai_mau = {
                        "Free": "#4CAF50",    # Xanh lá cây
                        "Serve": "#FFC107",   # Vàng (Đang phục vụ)
                        "Booked": "#F44336",  # Đỏ (Đã đặt)
                    }.get(ban.trang_thai, "#9E9E9E")

                    btn_ban = tk.Button(
                        frame,
                        text=f"{ban.ten_ban}", # Hiển thị tên bàn và trạng thái
                        
                        image = self.table_icon_ref,
                        compound = "top",

                        bg=trang_thai_mau, 
                        fg="white",
                        font=("Arial", 10, "bold"),
                        
                        padx = 5, 

                        # Truyền chính đối tượng 'ban' vào command
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
                    empty_label = tk.Label(frame, text="", bg="lightgray")
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

