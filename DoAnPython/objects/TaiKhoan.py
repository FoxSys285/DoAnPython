import json
from objects.NhanVien import NhanVien, DanhSachNhanVien
from tkinter import messagebox

class TaiKhoan:
	def __init__(self, username, password, role = "Employee"):
		self.username = username
		self.password = password
		self.role = role

	def to_dict(self):
		return {
			"username": self.username,
			"password": self.password,
			"role": self.role
		}
	def __str__(self):
		return f"{username}"

class DanhSachTaiKhoan:
	def __init__(self):
		self.ds = {}

	def Add(self, username, password, role="Employee"): 
		if username not in self.ds:
			# Lưu đối tượng TaiKhoan vào dictionary
			new_account = TaiKhoan(username, password, role)
			self.ds[username] = new_account 
			return True
		return False

	def Find(self, username):
		return self.ds.get(username, None) # Trả về đối tượng TaiKhoan hoặc None

	def doc_file(self, filename):
		try:
			with open(filename, "r", encoding = "utf-8") as file:
				data = json.load(file)
				
				# Duyệt qua các dictionary trong file và chuyển thành đối tượng TaiKhoan
				self.ds = {}
				for user_data in data:
					# Tạo đối tượng TaiKhoan từ dữ liệu đã đọc
					account = TaiKhoan(
						user_data["username"], 
						user_data["password"], 
						user_data["role"]
					)
					self.ds[account.username] = account
				
				print("Đọc file thành công")
		except FileNotFoundError:
			print(f"Lỗi đọc file: Không tìm thấy tệp {filename}")
		except Exception as loi:
			print("Lỗi đọc file du_lieu_tk.json:", loi)

	def ghi_file(self, filename):
		try:
			list_to_dump = [account.to_dict() for account in self.ds.values()]
			
			with open(filename, "w", encoding = "utf-8") as file:
				json.dump(list_to_dump, file, ensure_ascii = False, indent = 4)
				print("Ghi file thành công")
		except Exception as loi:
			print("Lỗi ghi file:", loi)

	def check_login(self, username_input, password_input):
		ds_nv = DanhSachNhanVien()
		ds_nv.doc_file("data/du_lieu_nv.json")
		account = self.ds.get(username_input)
		if account:
			if account.password == password_input:
				nv = ds_nv.find_by_username(username_input)
				print(nv)
				return True, account
			else:
				return False, "Sai mật khẩu."
		else:
			return False, "Tài khoản không tồn tại."

	def kiem_tra_ton_tai(self, user):
		return user in self.ds

	def xoa_nhan_vien(self):
	    selected = self.tree_nhan_vien.selection()
	    if not selected:
	        messagebox.showwarning("Cảnh báo", "Bạn chưa chọn nhân viên cần xóa")
	        return

	    item = self.tree_nhan_vien.item(selected[0])
	    ma_nv = item["values"][1]
	    ten_nv = item["values"][2]
	    username_xoa = item["values"][5] # Lấy username từ bảng

	    confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa nhân viên '{ten_nv}' không?")
	    if not confirm: return

	    if ma_nv in self.ds_nhan_vien.ds:
	        # 1. Xóa nhân viên
	        self.ds_nhan_vien.remove_nv(ma_nv)
	        self.ds_nhan_vien.ghi_file("data/du_lieu_nv.json")

	        # 2. XÓA TÀI KHOẢN TƯƠNG ỨNG (Thêm đoạn này)
	        from objects.TaiKhoan import DanhSachTaiKhoan
	        ds_tk = DanhSachTaiKhoan()
	        ds_tk.doc_file("data/du_lieu_tk.json")
	        if username_xoa in ds_tk.ds:
	            del ds_tk.ds[username_xoa]
	            ds_tk.ghi_file("data/du_lieu_tk.json")
	            print(f"Đã xóa tài khoản: {username_xoa}")

	        self.load_nhan_vien()
	        messagebox.showinfo("Thông báo", "Đã xóa nhân viên và tài khoản liên quan")