import json
class Mon:
    def __init__(self,maMon,tenMon,gia,soLuong,loai):
        self.maMon=maMon
        self.tenMon=tenMon
        self.gia=gia
        self.soLuong=soLuong
        self.loai=loai
    def to_dict(self):
        return {"maMon":self.maMon,"tenMon":self.tenMon,"gia":self.gia,"soLuong":self.soLuong,"loai":self.loai }
    def __str__(self):
        return f"{self.maMon:<8}{self.tenMon:<15}{self.gia:<8}{self.soLuong:>4}{self.loai:>15}"
class DS_Mon:
   def __init__(self):
       self.dsMon=[]
   def docFileJson(self,file):
       try:
           with open(file,'r',encoding='utf-8') as f:
               du_lieu=json.load(f)
               self.dsMon=[Mon(i["maMon"],i["tenMon"],i["gia"],i["soLuong"],i["loai"]) for i in du_lieu]
               print("Doc file thanh cong!")
       except FileNotFoundError:
           print("Doc file ko thanh cong")
       except Exception as loi:
           print(f"Loi khi doc file ",loi)
   def ghiFileJson(self,file):
       try:
           with open(file,'w',encoding='utf-8') as f:
               json.dump([i.to_dict() for i in self.dsMon],f,ensure_ascii=False,indent=4)
               print("Ghi file mon thanh cong!")
       except Exception as loi:
           print("Ghi file bi loi ",loi)
   def xuatDS(self):
       if not self.dsMon:
           print("Danh sach bi rong")
       else:
           print(f"{'Ma Mon':<8}{'Ten Mon':<15}{'Gia':<8}{'So Luong':>4}{'Loai':>15}")
           for i in self.dsMon:
               print(i)
class HoaDon:
    def __init__(self,maHD,gioLap,dsMon,tongTien,giamGia):
        self.maHD=maHD
        self.gioLap=gioLap
        self.dsMon=dsMon
        self.tongTien=tongTien
        self.giamGia=giamGia

    def to_dict(self):
        return {"maHD":self.maHD,"gioLap":self.gioLap,"dsMon":self.dsMon,"tongTien":self.tongTien,"giamGia":self.giamGia}
    def __str__(self):
        return f"{self.maHD:<8}{self.gioLap:<15}{self.dsMon:<8}{self.tongTien:>8}{self.giamGia:>5}"
    def TinhThanhTien(self):
        return self.tongTien-self.giamGia

class DS_HoaDon:
    def __init__(self):
        self.dsHD=[]
    def docFileJson(self,file):
        try:
            with open(file,'r',encoding='utf-8') as f:
                du_lieu=json.load(f)
                self.dsHD=[HoaDon(i["maHD"],i["gioLap"],i["dsMon"],i["tongTien"],i["giamGia"]) for i in du_lieu]
                print("Doc file thanh cong!")
        except FileNotFoundError:
            print("Doc file ko thanh cong")
        except Exception as loi:
            print(f"Loi khi doc file ",loi)
    def ghiFileJson(self,file):
       try:
           with open(file,'w',encoding='utf-8') as f:
               json.dump([i.to_dict() for i in self.dsHD],f,ensure_ascii=False,indent=4)
               print("Ghi file mon thanh cong!")
       except Exception as loi:
           print("Ghi file bi loi ",loi)
    def xuatDS(self):
        if not self.dsHD:
            print("Danh sach bi rong")
        else:
            print(f"{'Ma HD':<8}{'Gio Lap':<15}{'DS Mon':<8}{'Tong Tien':>8}{'Giam Gia':>5}")
            for i in self.dsHD:
                print(i)

class Ban:
    def __init__(self,maBan,tenBan,gioVao,dsMon,tongTien,giamGia):
        self.maBan=maBan
        self.tenBan=tenBan
        self.gioVao=gioVao
        self.dsMon=dsMon
        self.tongTien=tongTien
        self.giamGia=giamGia
        self.HoaDon=None
    def to_dict(self):
        return {"maBan":self.maBan,"tenBan":self.tenBan,"gioVao":self.gioVao,"dsMon":self.dsMon,"tongTien":self.tongTien,"giamGia":self.giamGia}
    def __str__(self):
        return f"{self.maBan:<8}{self.tenBan:<8}{self.gioVao:<15}{self.dsMon:<8}{self.tongTien:>8}{self.giamGia:>5}"
    def tongTien(self):
        if self.HoaDon is None:
            return 0
        return self.HoaDon.tongTien 
    

class DS_Ban:
    def __init__(self):
        self.dsBan=[]
    def docFileJson(self,file):
        try:
            with open(file,'r',encoding='utf-8') as f:
                du_lieu=json.load(f)
                self.dsBan=[Ban(i["maBan"],i["tenBan"],i["gioVao"],i["dsMon"],i["tongTien"],i["giamGia"]) for i in du_lieu]
                print("Doc file ban thanh cong!")
        except FileNotFoundError:
            print("Doc file ko thanh cong")
        except Exception as loi:
            print("Doc file bi loi ",loi)
    def ghiFileJson(self,file):
        try:
            with open(file,'w',encoding='utf-8') as f:
                json.dump([i.to_dict() for i in self.dsBan],f,ensure_ascii=False,indent=4)
                print("Ghi file ban thanh cong ")
        except Exception as loi:
            print("Ghi file ban bi loi ",loi)

    def xuatFile(self):
        if not self.dsBan:
            print("Danh sach ban bi rong")
        else:
            print(f"{'Ma Ban':<8}{'Ten Ban':<8}{'Gio Vao':<15}{'DS Mon':<8}{'Tong Tien':>8}{'Giam Gia':>5}")
            for i in self.dsBan:
                print(i)

