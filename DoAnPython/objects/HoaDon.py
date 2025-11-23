import json

class HoaDon:
    def __init__(self, maHD, gioLap, dsMon, tongTien, giamGia, maBan):
        self.maHD=maHD
        self.gioLap=gioLap
        self.dsMon=dsMon
        self.tongTien=tongTien
        self.giamGia=giamGia
        self.maBan = maBan

    def to_dict(self):
        return {"maHD":self.maHD,"gioLap":self.gioLap,"dsMon":self.dsMon,"tongTien":self.tongTien,"giamGia":self.giamGia,"maBan":self.maBan}
    def __str__(self):
        return f"{self.maHD:<8}{self.gioLap:<15}{self.dsMon:<8}{self.tongTien:>8}{self.giamGia:>5}"
    def TinhThanhTien(self):
        return self.tongTien - self.giamGia * self.tongTien

class DanhSachHoaDon:
    def __init__(self):
        self.dsHD=[]
    def doc_file(self,file):
        try:
            with open(file,'r',encoding='utf-8') as f:
                du_lieu=json.load(f)
                self.dsHD=[HoaDon(i["maHD"],i["gioLap"],i["dsMon"],i["tongTien"],i["giamGia"],i["maBan"]) for i in du_lieu]
                print("Doc file thanh cong!")
        except FileNotFoundError:
            print("Doc file ko thanh cong")
        except Exception as loi:
            print(f"Loi khi doc file ",loi)
    def ghi_file(self,file):
       try:
           with open(file,'w',encoding='utf-8') as f:
               json.dump([i.to_dict() for i in self.dsHD],f,ensure_ascii=False,indent=4)
               print("Ghi file mon thanh cong!")
       except Exception as loi:
           print("Ghi file bi loi ",loi)
