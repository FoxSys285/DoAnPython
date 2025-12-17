import json

class NhanVien:
    def __init__(self, ma_nv, ten_nv, role, luong, username): 
        self.ma_nv = ma_nv
        self.ten_nv = ten_nv
        self.role = role        # Dùng cho Phân quyền: Manager (Quản lý), Cashier (Thu ngân), Server (Bồi bàn), Barista (Pha chế)
        self.luong = luong
        self.username = username # Liên kết với TaiKhoan để Đăng nhập

    def to_dict(self):
        return {
            "ma_nv": self.ma_nv,
            "ten_nv": self.ten_nv,
            "role": self.role,
            "luong": self.luong,
            "username": self.username
        }
    
    def __str__(self):
        return f"Mã NV: {self.ma_nv} | Tên: {self.ten_nv} | Vai trò: {self.role} | Lương: {self.luong} | User: {self.username}"


class DanhSachNhanVien:
    def __init__(self):
        self.ds = {}

    def doc_file(self, filename):
        try:
            with open(filename, "r", encoding = "utf-8") as file:
                data = json.load(file)
                
                self.ds = {}
                for nv_data in data:
                    nv = NhanVien(
                        nv_data["ma_nv"],
                        nv_data["ten_nv"],
                        nv_data["role"],
                        nv_data["luong"],
                        nv_data["username"]
                    )
                    self.ds[nv.ma_nv] = nv
            print("Đọc file nhân viên thành công")
        except FileNotFoundError:
            print(f"Lỗi đọc file: Không tìm thấy tệp {filename}")
            self.ds = {}
        except Exception as loi:
            print("Lỗi đọc file nhân viên:", loi)

    def ghi_file(self, filename):
        try:
            list_to_dump = [nv.to_dict() for nv in self.ds.values()]
            
            with open(filename, "w", encoding = "utf-8") as file:
                json.dump(list_to_dump, file, ensure_ascii = False, indent = 4)
                print("Ghi file nhân viên thành công")
        except Exception as loi:
            print("Lỗi ghi file nhân viên:", loi)

    def find_by_username(self, username):
        for nv in self.ds.values():
            if nv.username == username:
                return nv
        return None

    def add_nv(self, nv_obj):
        if nv_obj.ma_nv not in self.ds:
            self.ds[nv_obj.ma_nv] = nv_obj
            return True
        return False

    def remove_nv(self, ma_nv):
        if ma_nv in self.ds:
            del self.ds[ma_nv]
            return True
        return False

    def lay_danh_sach_chuc_vu(self):
        return list({nv.role for nv in self.ds.values()})
