import json

class TaiKhoan:
	def __init__(self, username, password):
		self.username = username
		self.password = password


class DanhSachTaiKhoan:
	def __init__(self):
		self.ds = {}

	def Add(self, username, password):
		if username not in self.ds:
			self.ds[username] = password
			return True
		return False

	def doc_file(self, filename):
		try:
			with open(filename, "r", encoding = "utf-8") as file:
				self.ds = json.load(file)
				print("Đọc file thành công")
		except Exception as loi:
			print("Lỗi đọc file: ", loi)

	def ghi_file(self, filename):
		try:
			with open(filename, "w", encoding = "utf-8") as file:
				json.dump(self.ds, file, ensure_ascii = False, indent = 4)
				print("Ghi file thành công")
		except Exception as loi:
			print("Lỗi ghi file")