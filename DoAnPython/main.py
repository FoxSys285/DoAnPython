from interfaces.MH_DangNhap import MH_DangNhap
from interfaces.MH_BanHang import MH_BanHang
from interfaces.MH_QuanLy import MH_QuanLy
from interfaces.MH_TrangChu import MH_TrangChu
from interfaces.MH_Credits import MH_Credits
from interfaces.MH_ThongKe import MH_ThongKe

import threading
# Import ứng dụng Flask, đổi tên biến để tránh xung đột với tk.App
from bestselling_api import app as flask_app

# Thư viện giao diện
from tkinter import *
import tkinter as tk

# Thư viện xử lý hình ảnh
from PIL import Image, ImageTk

# Thư viện lấy ngày, giờ
from datetime import datetime


def run_flask_api():
    # Chạy Flask app. Đảm bảo debug=False trong thread để tránh lỗi
    # Mặc định chạy trên http://127.0.0.1:5000/
    flask_app.run(host='127.0.0.1', port=5000, debug=False)
# ================================================================
# APP CHÍNH
# ================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng quản lý quán cafe mini")
        self.resizable(False, False)

        # Kích thước cửa sổ
        window_width = 1280
        window_height = 640

        # Lấy kích thước màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Tính tọa độ để cửa sổ nằm giữa màn hình
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Đặt geometry kèm tọa độ
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")


        self.current_user = None
        self.current_page = None
        self.username = ""
        self.role = ""

        self.iconbitmap("images/icon.ico")

        # Khung chứa toàn bộ màn hình
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Tạo tất cả màn hình
        for F in (MH_TrangChu, MH_BanHang, MH_QuanLy, MH_DangNhap, MH_ThongKe, MH_Credits):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("MH_QuanLy")

        # ================================================================
        # BẮT ĐẦU FLASK API TRÊN MỘT THREAD RIÊNG
        # ================================================================
        self.flask_thread = threading.Thread(target=run_flask_api, daemon=True)
        self.flask_thread.start()
        print("Flask API đã được khởi động trên thread riêng: http://127.0.0.1:5000/")
        
        # Đảm bảo Flask server dừng khi Tkinter app đóng (sử dụng daemon=True là đủ, 
        # nhưng thêm hàm protocol để kiểm soát tốt hơn)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        print("http://127.0.0.1:5000/api/v1/best-selling/top5")
    
    def on_closing(self):
        """Hàm xử lý khi đóng cửa sổ Tkinter"""
        print("Đang đóng ứng dụng Tkinter.")
        self.destroy()

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

    def show_frame(self, page):
        """Hiển thị màn hình với hiệu ứng loading đơn giản 1 giây"""
        
        if page == self.current_page:
            print(f"Trang '{page}' đã là trang hiện tại. Bỏ qua chuyển đổi.")
            return

        self.current_page = page

        # # Tạo màn hình loading tạm
        loading = tk.Frame(self, bg="white")
        loading.place(x=0, y=0, relwidth=1, relheight=1)

        
        if page == "MH_QuanLy" or page == "MH_ThongKe":
            text = tk.Label(loading, text="Đang tải...", font=("Arial", 24, "bold"), bg="white")
            text.place(relx=0.5, rely=0.5, anchor="center")
            self.after(300, lambda: self._show_page(page, loading))
        else:
            self.after(0, lambda: self._show_page(page, loading))

    
    def _show_page(self, page_name, loading_frame):
        """Ẩn loading và hiện trang thật"""
        loading_frame.destroy()
        frame = self.frames[page_name]
        
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

