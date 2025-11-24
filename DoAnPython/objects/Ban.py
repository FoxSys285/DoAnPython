import json
from objects.Mon import Mon, DanhSachMon

class Ban:
    def __init__(self, ma_ban, ten_ban, trang_thai, thoi_gian, ds_mon, giam_gia=0):
        self.ma_ban = ma_ban
        self.ten_ban = ten_ban
        self.trang_thai = trang_thai
        self.thoi_gian = thoi_gian
        # Khi đọc file, ds_mon có thể chỉ là danh sách dict,
        # cần đảm bảo chuyển đổi nó thành đối tượng Mon nếu cần thiết
        if all(isinstance(m, dict) for m in ds_mon):
            self.ds_mon = [Mon(m['ma_mon'], m['ten_mon'], m['don_gia'], m['so_luong']) for m in ds_mon]
        else:
            self.ds_mon = ds_mon

        self.giam_gia = giam_gia

    def to_dict(self):
        return {
            "ma_ban": self.ma_ban,
            "ten_ban": self.ten_ban,
            "trang_thai": self.trang_thai,
            "thoi_gian": self.thoi_gian,
            "ds_mon": [mon.to_dict() for mon in self.ds_mon],
            "giam_gia": self.giam_gia
        }

    def thanh_tien(self):
        tong = 0
        for mon in self.ds_mon:
            tong += mon.don_gia * mon.so_luong
        return tong - self.giam_gia


class DanhSachBan:
    def __init__(self):
        self.ds = []

    def doc_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                du_lieu = json.load(f)
                # Dữ liệu đọc từ JSON là list of dicts, cần chuyển về list of Ban objects
                self.ds = [Ban(
                    i["ma_ban"],
                    i["ten_ban"],
                    i["trang_thai"],
                    i["thoi_gian"],
                    i["ds_mon"], # Danh sách món ở đây đang là list of dicts, class Ban sẽ xử lý
                    i["giam_gia"]
                ) for i in du_lieu]
        except Exception as loi:
            print("Lỗi đọc file: ", loi)

    def ghi_file(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([i.to_dict() for i in self.ds], f, ensure_ascii=False, indent=4)
        except Exception as loi:
            print("Lỗi ghi file: ", loi)


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
