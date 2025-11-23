import json
from .Mon import Mon, DanhSachMon

class Ban:
	def __init__(self, ma_ban, ten_ban, trang_thai, thoi_gian, ds_mon, giam_gia = 0):
		self.ma_ban = ma_ban
		self.ten_ban = ten_ban
		self.trang_thai = trang_thai
		self.thoi_gian = thoi_gian
		self.ds_mon = ds_mon
		self.giam_gia = giam_gia

	def to_dict(self):
		return 
		{
			"ma_ban": self.ma_ban,
			"ten_ban": self.ten_ban, 
			"trang_thai": self.trang_thai,
			"thoi_gian": self.thoi_gian,
			"ds_mon": self.ds_mon.to_dict(),
			"giam_gia": self.giam_gia
		}

	def thanh_tien(self):
		tt = 0
		for mon in self.ds_mon:
			tt += mon.don_gia

class DanhSachBan:
	def __init__(self):
		self.ds = []
	