import json

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

	# Phương thức tìm kiếm (Hữu ích cho đăng nhập)
	def Find(self, username):
		return self.ds.get(username, None) # Trả về đối tượng TaiKhoan hoặc None

	# Đọc file JSON và chuyển đổi dữ liệu thành đối tượng TaiKhoan
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

		account = self.ds.get(username_input)
		if account:
			if account.password == password_input:
				return True, account
			else:
				return False, "Sai mật khẩu."
		else:
			return False, "Tài khoản không tồn tại."