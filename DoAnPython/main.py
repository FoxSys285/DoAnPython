from interfaces.MH_DangNhap import MH_DangNhap
from interfaces.MH_BanHang import MH_BanHang
from interfaces.MH_Loading import MH_Loading
from interfaces.MH_QuanLy import MH_QuanLy

# Thư viện giao diện
from tkinter import *
import tkinter as tk

# Thư viện xử lý hình ảnh
from PIL import Image, ImageTk

# Thư viện lấy ngày, giờ
from datetime import datetime

# ================================================================
# APP CHÍNH
# ================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng quản lý quán cafe mini")
        self.geometry("1280x640")
        self.resizable(False, False)

        self.current_user = None
        self.username = ""
        self.role = ""

        self.iconbitmap("images/icon.ico")

        # Khung chứa toàn bộ màn hình
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Tạo tất cả màn hình
        for F in (MH_DangNhap, MH_BanHang, MH_QuanLy):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(MH_DangNhap)

    def show_frame(self, page):
        """Hiển thị màn hình với hiệu ứng loading đơn giản 1 giây"""
    
        # Tạo màn hình loading tạm
        loading = tk.Frame(self, bg="white")
        loading.place(x=0, y=0, relwidth=1, relheight=1)

        text = tk.Label(loading, text="Đang tải...", font=("Arial", 24, "bold"), bg="white")
        text.place(relx=0.5, rely=0.5, anchor="center")

        # Sau 1 giây chuyển sang trang thật
        self.after(800, lambda: self._show_page(page, loading))

    def fade_in(self, widget, alpha=0.0):
        """Hiệu ứng hiện dần"""
        alpha += 0.1
        if alpha >= 1:
            widget.attributes("-alpha", 1.0)
            return
        widget.attributes("-alpha", alpha)
        self.after(20, lambda: self.fade_in(widget, alpha))


    def fade_out(self, widget, alpha=1.0):
        """Hiệu ứng biến mất dần"""
        alpha -= 0.1
        if alpha <= 0:
            widget.destroy()
            return
        widget.attributes("-alpha", alpha)
        self.after(20, lambda: self.fade_out(widget, alpha))

    def _show_page(self, page, loading_frame):
        """Ẩn loading và hiện trang thật"""
        loading_frame.destroy()
        frame = self.frames[page]
        
        # === THÊM LOGIC NÀY ===
        # Gọi phương thức on_show() của frame nếu nó tồn tại
        if hasattr(frame, 'on_show'):
            frame.on_show()
        # ======================
            
        frame.tkraise()

# ================================================================
# CHẠY APP
# ================================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
