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

    def show_toast(self, message, duration=1500):
        """Hiển thị thông báo nhỏ tự tắt sau duration(ms)"""

        toast = tk.Toplevel(self)
        toast.overrideredirect(True)  # bỏ viền
        toast.attributes("-topmost", True)
        toast.configure(bg="#333333")

        # nội dung
        label = tk.Label(
            toast,
            text=message,
            fg="white",
            bg="#333333",
            font=("Arial", 11, "bold"),
            padx=12, pady=8
        )
        label.pack()

        # đặt vị trí (góc phải dưới của cửa sổ app)
        self.update_idletasks()
        x = self.winfo_x() + self.winfo_width() - toast.winfo_reqwidth() - 20
        y = self.winfo_y() + self.winfo_height() - toast.winfo_reqheight() - 40
        toast.geometry(f"+{x}+{y}")

        # hiệu ứng fade-in
        toast.attributes("-alpha", 0.0)
        self.fade_in(toast)

        # tự tắt sau duration ms
        self.after(duration, lambda: self.fade_out(toast))


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
        frame.tkraise()



# ================================================================
# CHẠY APP
# ================================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
