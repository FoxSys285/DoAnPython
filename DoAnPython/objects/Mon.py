import json

class Mon:
    def __init__(self, ma_mon, ten_mon, don_gia, so_luong, loai, dvt):
        self.ma_mon = ma_mon
        self.ten_mon = ten_mon
        self.don_gia = don_gia
        self.so_luong = so_luong
        self.loai = loai
        self.dvt = dvt

    def to_dict(self):
        return {
            "ma_mon": self.ma_mon,
            "ten_mon": self.ten_mon,
            "don_gia": self.don_gia,
            "so_luong": self.so_luong,
            "loai": self.loai,
            "dvt": self.dvt
        }

    def __str__(self):
        return f"{self.ma_mon} | {self.ten_mon} | {self.don_gia} | {self.so_luong} | {self.loai} | {self.dvt}"

class DanhSachMon:
    def __init__(self):
        self.ds = []

    def doc_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                du_lieu = json.load(f)
                self.ds = [
                    Mon(
                        m["ma_mon"],
                        m["ten_mon"],
                        m["don_gia"],
                        m["so_luong"],
                        m["loai"],
                        m["dvt"]
                    )
                    for m in du_lieu
                ]
        except Exception as loi:
            print("Lỗi đọc file:", loi)

    def ghi_file(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([m.to_dict() for m in self.ds], f, ensure_ascii=False, indent=4)
        except Exception as loi:
            print("Lỗi ghi file:", loi)

    def to_dict(self):
        return [m.to_dict() for m in self.ds]

    def tim_mon_theo_loai(self, loai):
        ds = []
        for mon in self.ds:
            if mon.loai == loai:
                ds.append(mon)
        return ds
