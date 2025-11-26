import json

class DanhSachNhomMon:
    def __init__(self):
        self.ds = []  # Danh sách các nhóm món (chuỗi)

    def doc_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.ds = json.load(f)
        except:
            self.ds = []

    def ghi_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.ds, f, ensure_ascii=False, indent=2)

    def them_nhom(self, ten_nhom):
        if ten_nhom and ten_nhom not in self.ds:
            self.ds.append(ten_nhom)
            return True
        return False

    def xoa_nhom(self, ten_nhom):
        if ten_nhom in self.ds:
            self.ds.remove(ten_nhom)
            return True
        return False

    def sua_nhom(self, ten_cu, ten_moi):
        if ten_cu in self.ds and ten_moi not in self.ds:
            index = self.ds.index(ten_cu)
            self.ds[index] = ten_moi
            return True
        return False

    def lay_danh_sach(self):
        return self.ds