from MH_DangNhap import MH_DangNhap
from MH_BanHang import MH_BanHang
from MH_Loading import MH_Loading

class TaiKhoan:
	def __init__(self, username, password):
		self.username = username
		self.password = password

	
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

        # Khung chứa toàn bộ màn hình
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Tạo tất cả màn hình
        for F in (MH_DangNhap, MH_BanHang):
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
        self.after(1000, lambda: self._show_page(page, loading))


    def _show_page(self, page, loading_frame):
        """Ẩn loading và hiện trang thật"""
        loading_frame.destroy()
        frame = self.frames[page]
        frame.tkraise()



# ================================================================
# CHẠY APP
# ================================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
