import json
from objects.Mon import Mon, DanhSachMon
class HoaDon:
    def __init__(self, maHD, gioLap, dsMon = DanhSachMon(), tongTien = 0, maBan = None, gioRa = None, nguoi_lap = None):
        self.maHD=maHD
        self.gioLap=gioLap
        self.dsMon=dsMon
        self.tongTien=tongTien
        self.maBan = maBan
        self.gioRa = gioRa
        self.nguoi_lap = nguoi_lap

    def to_dict(self):
        return {"maHD":self.maHD,"gioLap":self.gioLap,"dsMon":self.dsMon.to_dict(),"tongTien":self.tongTien,"maBan":self.maBan,"gioRa":self.gioRa,"nguoi_lap":self.nguoi_lap}
    def xuat(self):
        return f"Mã hóa đơn: {self.maHD}\n\tGiờ lập: {self.gioLap}\n\tTổng tiền: {self.tongTien}\n\tDanh sách món: {self.dsMon.xuat_ds()}\n\tGiờ ra: {self.gioRa}"
    def TinhThanhTien(self):
        return self.tongTien
    def check_mon(self, mon):
        for i in self.dsMon:
            if mon.ma_mon == i.ma_mon:
                return True
        return False


class DanhSachHoaDon:
    def __init__(self):
        self.dsHD=[]
    def doc_file(self,file):
        try:
            with open(file,'r',encoding='utf-8') as f:
                du_lieu=json.load(f)
                temp_dsHD = []
                for i in du_lieu:

                    ds_mon_obj = DanhSachMon()

                    for mon_dict in i["dsMon"]:
                        ds_mon_obj.ds.append(Mon(
                            mon_dict["ma_mon"],
                            mon_dict["ten_mon"],
                            mon_dict["don_gia"],
                            mon_dict["so_luong"],
                            mon_dict["loai"],
                            mon_dict["dvt"]
                        ))

                    temp_dsHD.append(HoaDon(
                        i["maHD"],
                        i["gioLap"],
                        ds_mon_obj,
                        i["tongTien"],
                        i["maBan"],
                        i["gioRa"],
                        i["nguoi_lap"]
                    ))
                self.dsHD = temp_dsHD
                print("Doc file thanh cong!")
        except FileNotFoundError:
            print("Doc file ko thanh cong")
        except Exception as loi:
            print(f"Loi khi doc file ",loi)
    def ghi_file(self,file):
       try:
           with open(file,'w',encoding='utf-8') as f:
               list_to_dump = [i.to_dict() for i in self.dsHD if i is not None] 
               json.dump(list_to_dump, f, ensure_ascii=False, indent=4)
               print("Ghi file mon thanh cong!")
       except Exception as loi:
           print("Ghi file bi loi hóa đơn:",loi)

    def xoa_hoa_don(self, maHD):
        for i in self.dsHD:
            if i.maHD == maHD:
                self.dsHD.remove(i)
                print(f"Xóa hóa đơn {i.maHD} thành công")
                return
