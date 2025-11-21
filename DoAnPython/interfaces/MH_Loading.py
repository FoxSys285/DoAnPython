import tkinter as tk

class MH_Loading(tk.Frame):
    def __init__(self, parent, controller, next_page):
        super().__init__(parent)
        self.controller = controller
        self.next_page = next_page

        self.label = tk.Label(self, text="Đang tải", font=("Arial", 24, "bold"))
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.dots = 0
        self.animate()

    def animate(self):
        """Hiệu ứng chạy dấu chấm"""
        self.dots = (self.dots + 1) % 4
        self.label.config(text="Đang tải" + "." * self.dots)

        # Sau 1 giây, chuyển trang
        if self.dots == 3:
            self.controller.show_frame(self.next_page)
        else:
            self.after(300, self.animate)
