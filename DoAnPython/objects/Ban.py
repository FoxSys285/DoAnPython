import json
from objects.Mon import Mon, DanhSachMon
from objects.HoaDon import HoaDon, DanhSachHoaDon

class Ban:
    def __init__(self, ma_ban, ten_ban, trang_thai, thoi_gian, hoa_don: HoaDon | None, nguoi_lap = None):
        self.ma_ban = ma_ban
        self.ten_ban = ten_ban
        self.trang_thai = trang_thai
        self.thoi_gian = thoi_gian
        self.hoa_don = hoa_don
        self.nguoi_lap = nguoi_lap

    def to_dict(self):
        hoa_don_dict = self.hoa_don.to_dict() if self.hoa_don else None
        
        return {
            "ma_ban": self.ma_ban,
            "ten_ban": self.ten_ban,
            "trang_thai": self.trang_thai,
            "thoi_gian": self.thoi_gian,
            "hoa_don": hoa_don_dict,
            "nguoi_lap": self.nguoi_lap
        }

    def check_serve(self):
        if self.hoa_don:
            self.trang_thai = "Serve"
            return True
        return False

    def __str__(self):
        return f"---------------------------------\nMã bàn: {self.ma_ban}\nTên bàn: {self.ten_ban}\nTrạng thái: {self.trang_thai}\nGiờ lập: {self.thoi_gian}\nNgười lập: {self.nguoi_lap}\n---------------------------------"

class DanhSachBan:
    def __init__(self):
        self.ds = []

    def doc_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                du_lieu = json.load(f)
                temp_ds = []
                
                for i in du_lieu:
                    hoa_don_obj = None
                    hoa_don_data = i.get("hoa_don")
                    
                    # 1. Tái tạo đối tượng HoaDon nếu có dữ liệu
                    if hoa_don_data and isinstance(hoa_don_data, dict):
                        
                        # Tái tạo DanhSachMon
                        ds_mon_obj = DanhSachMon()
                        for mon_dict in hoa_don_data.get("dsMon", []):
                            ds_mon_obj.ds.append(Mon(
                                mon_dict["ma_mon"],
                                mon_dict["ten_mon"],
                                mon_dict["don_gia"],
                                mon_dict["so_luong"],
                                mon_dict["loai"],
                                mon_dict["dvt"]
                            ))
                        
                        # Tái tạo HoaDon
                        hoa_don_obj = HoaDon(
                            hoa_don_data["maHD"],
                            hoa_don_data["gioLap"],
                            ds_mon_obj,
                            hoa_don_data.get("tongTien", 0),
                            hoa_don_data.get("maBan")
                        )

                    # 2. Tạo đối tượng Ban
                    temp_ds.append(Ban(
                        i["ma_ban"],
                        i["ten_ban"],
                        i["trang_thai"],
                        i["thoi_gian"],
                        hoa_don_obj,
                        i["nguoi_lap"]
                    ))
                
                self.ds = temp_ds
                
        except Exception as loi:
            print("Lỗi đọc file ban: ", loi)

    def ghi_file(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([i.to_dict() for i in self.ds], f, ensure_ascii=False, indent=4)
        except Exception as loi:
            print("Lỗi ghi file Bàn: ", loi)


    def free(self):
        cnt = 0
        for i in self.ds:
            if i.trang_thai == "Free":
                cnt += 1
        return cnt

    def serve(self):
        cnt = 0
        for i in self.ds:
            if i.trang_thai == "Serve":
                cnt += 1
        return cnt

    def booked(self):
        cnt = 0
        for i in self.ds:
            if i.trang_thai == "Booked":
                cnt += 1
        return cnt

    def tim_ban(self, ma_ban):
        for ban in self.ds:
            if ban.ma_ban == ma_ban:
                return ban
        return None