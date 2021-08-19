from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
from random import seed
from random import random
from random import choice
from string import ascii_uppercase

class HTML_VGs_STRU() : 
    def __init__(self, VGs) : 
        # pass in soup's forms
        self.VGs = VGs
        #{vgID:{shape:{attributes:value}}}
        self.maga_info = dict()
        
    def VG_type(self, svg, vgID) : 
        self.maga_info[vgID] = dict()
        # attributes of each shape
        shape_attributes = dict()
        # counts of shapes
        cnt_circle = 0 
        cnt_rect = 0 
        cnt_ellipse = 0
        cnt_polygon = 0

        for c in svg.find_all("circle") :
            if c.has_attr("cx") :
                shape_attributes["cx"] = c["cx"]
            else :
                shape_attributes["cx"] = 0

            if c.has_attr("cy") :
                shape_attributes["cy"] = c["cy"]
            else :
                shape_attributes["cy"] = 0
                
            if c.has_attr("r") :
                shape_attributes["r"] = c["r"]
            else :
                shape_attributes["r"] = 0
                
            self.maga_info[vgID]["circle"+ str(vgID) + str(cnt_circle)] = shape_attributes
            cnt_circle += 1
            shape_attributes = dict()

        # parse rectangular
        for r in svg.find_all("rect") :
            if r.has_attr("x") :
                shape_attributes["x"] = r["x"]
            else :
                shape_attributes["x"] = 0
            if r.has_attr("y") :
                shape_attributes["y"] = r["y"]
            else :
                shape_attributes["y"] = 0
            if r.has_attr("rx") :
                shape_attributes["rx"] = r["rx"]
            else :
                shape_attributes["rx"] = 0
            if r.has_attr("ry") :
                shape_attributes["ry"] = r["ry"]
            else :
                shape_attributes["ry"] = 0 
            if r.has_attr("width") :
                shape_attributes["width"] = r["width"]
            else :
                shape_attributes["width"] = 1
            if r.has_attr("height") :
                shape_attributes["height"] = r["height"]
            else :
                shape_attributes["height"] = 1
            self.maga_info[vgID]["rect" + str(vgID) + str(cnt_rect)] = shape_attributes
            cnt_rect += 1
            shape_attributes = dict()
        # parse ellipse
        for e in svg.find_all("ellipse") :
            if e.has_attr("cx") :
                shape_attributes["e_height"] = e["cy"]
            else :
                shape_attributes["e_height"] = 0
                
            if e.has_attr("cy") :
                shape_attributes["e_width"] = e["cx"]
            else :
                shape_attributes["e_width"] = 0

            self.maga_info[vgID]["ellipse" + str(vgID) + str(cnt_ellipse)] = shape_attributes
            cnt_ellipse += 1
            shape_attributes = dict()
        # parse polygon
        for p in svg.find_all("polygon") :
            if p.has_attr("points") :
                for i in range(0, len(p["points"].split(" "))-1):
                    shape_attributes[i] = (p["points"].split(" ")[i], p["points"].split(" ")[i+1])
                    if i+1 == len(p["points"].split(" "))-1 :
                        shape_attributes[i+1] = (p["points"].split(" ")[i+1], p["points"].split(" ")[0])
            self.maga_info[vgID]["polygon"+str(vgID) + str(cnt_polygon)] = shape_attributes
            cnt_polygon += 1
            shape_attributes = dict()


    def VG_parse(self) : 
        vgID = 0
        print ("THIS IS VG : !!!!!!!!!!!!!!!", self.VGs)
        if isinstance(self.VGs, Tag) :
            self.VG_type(self.VGs, vgID) 
        else :
            for svg in self.VGs:
                self.VG_type(svg, vgID)
                vgID += 1
        print(self.maga_info)
        return self.maga_info

class HTML_IMGs_STRU() :
    def __init__(self, IMGs) :
        # pass in soup's imgs
        self.IMGs = IMGs
        #{imgID:{type:{attributes:value}}}
        self.maga_info = dict()
    def IMG_type(self, img, img_id) :
        if ("qr" in str(img)) or ("QR" in str(img)) :
            if img.has_attr("height") :
                self.maga_info[img_id]={"QR":img["height"]}
                print ("THIS IS TYPE : ", type(img["height"]))
            else :
                self.maga_info[img_id]={"QR":"16"}
    def IMG_parse(self) :
        imgID = 0
        if isinstance(self.IMGs, Tag) :
            self.IMG_type(img, imgID)
        else :
            for img in self.IMGs:
                self.IMG_type(img, imgID)
                imgID += 1
        return self.maga_info 

class HTML_STYLEs_STRU() :
    def __init__(self, STYLEs) :
        # pass in soup's styles
        self.STYLEs = STYLEs
        # {style ID : obj}
        self.maga_info = dict()
    def STYLE_type(self, style, style_id) :
        try :
            str(style)
            if ("barcode" in str(style)) or ("Barcode" in str(style)) : 
                self.maga_info[style_id] = "BC"
        except :
            style = style.encode("utf-8")
            if ("barcode" in str(style)) or ("Barcode" in str(style)) :
                self.maga_info[style_id] = "BC"
    def STYLE_parse(self) : 
        styleID = 0 
        for style in self.STYLEs:
            self.STYLE_type(style, styleID)
            styleID += 1
        print (self.maga_info)
        return self.maga_info
        
       

class PDF_VGs_API_MAP() :
    def __init__(self, maga_info, template, tag_cnt) :
        self.maga_info = maga_info
        self.template = template
        self.tag_cnt = tag_cnt
    
    def draw_circle(self, vgID, cnt) : 
        XPos = self.maga_info[vgID][cnt]["cx"]
        try :
            float(XPos)
        except :
            XPos = 10 
        YPos = self.maga_info[vgID][cnt]["cy"]
        try :
            float(YPos)
        except :
            YPos = 10 
        Radius = self.maga_info[vgID][cnt]["r"]
        self.template.write("int circle"+str(vgID)+str(cnt)+str(self.tag_cnt) + " = FQL->DrawCircle("+str(XPos)+", "+str(YPos)+","+str(Radius)+", 2 ); \n")    
    def draw_box(self, vgID, cnt) :
        Left = self.maga_info[vgID][cnt]["x"]
        Top = self.maga_info[vgID][cnt]["y"]
        Width = self.maga_info[vgID][cnt]["width"]
        Height = self.maga_info[vgID][cnt]["height"]
        self.template.write("int rect" +str(vgID) +str(cnt) +str(self.tag_cnt) +  " = FQL->DrawBox("+str(Left)+", "+str(Top)+", "+str(Width)+", "+str(Height)+", 2);\n")
    def draw_round_box(self, vgID, cnt) :
        Left = self.maga_info[vgID][cnt]["x"]
        Top = self.maga_info[vgID][cnt]["y"]
        Width =  self.maga_info[vgID][cnt]["width"]
        try :
            float(Width)
        except :
            Width = 10 
        Height =  self.maga_info[vgID][cnt]["height"]
        try :
            float(Height)
        except :
            Height = 10
        Radius = (int(float(self.maga_info[vgID][cnt]["rx"])) + int(float(self.maga_info[vgID][cnt]["ry"])))/2
        self.template.write("int rect_round" +str(vgID) + str(cnt)+str(self.tag_cnt) +  " = FQL->DrawRoundedBox("+str(Left)+", "+str(Top)+", "+str(Width)+", "+str(Height)+", "+ str(Radius)+", 2); \n ")
    def draw_polygon(self, vgID, cnt) :
        for i in self.maga_info[vgID][cnt].values():
            StartX = str()
            StartY = str()
            EndX = str()
            EndY = str()
            if "," in i[0] : 
                StartX = i[0].split(",")[0].strip()
                StartY = i[0].split(",")[1].strip()
            else :
                StartX = "0"
                StartY = "0"
            if "," in i[1] :
                EndX = i[1].split(",")[0].strip()
                EndY = i[1].split(",")[1].strip()
            else :
                EndX = "0"
                EndY = "0"
            self.template.write("FQL->StartPath("+str(StartX)+", " + str(StartY)+"); \n")
            self.template.write("FQL->AddLineToPath("+str(EndX)+", "+str(EndY)+"); \n")
            self.template.write("FQL->DrawLine("+str(StartX)+", "+str(StartY)+","+str(EndX)+", "+str(EndY)+"); \n")
    def draw_ellipse(self, vgID, cnt) :
        Width = self.maga_info[vgID][cnt]["e_width"]
        Height = self.maga_info[vgID][cnt]["e_height"]
        self.template.write("int ellipse" +str(vgID) +str(cnt) +str(self.tag_cnt) +  " = FQL->DrawEllipse(50, 500, "+str(Width)+", "+str(Height)+", 2); \n")    
    def color_setting(self, Red, Green, Blue) :
        self.template.write("FQL->SetFillColor("+str(Red)+","+str(Green)+","+str(Blue)+"); \n")
 
    def api_order(self) : 
        for svg in self.maga_info : 
            for shape in self.maga_info[svg] :
                red = random()
                green = random()
                blue = random()
                print(red, green, blue)
                self.color_setting(red, green, blue)
                if shape[0:6] == "circle" :
                    self.draw_circle(svg, shape)
                elif shape[0:4] == "rect" :
                    print("this is shape : ", shape)
                    if "rx" in self.maga_info[svg][shape] or "ry" in self.maga_info[svg][shape] : 
                        self.draw_round_box(svg,shape)
                    else : 
                        self.draw_box(svg, shape)
                elif shape[0:7] == "ellipse" :
                    self.draw_ellipse(svg,shape)
                elif shape[0:7] == "polygon" :
                    self.draw_polygon(svg, shape)

class PDF_IMGs_API_MAP() : 
    def __init__(self, maga_info, template, tag_cnt) :
        self.maga_info = maga_info
        self.template = template
        self.tag_cnt = tag_cnt
    def draw_qrcode (self, img_id) : 
        code_height = self.maga_info[img_id].values()
        self.template.write("FQL->DrawQRCode(10, 10, "+str(code_height[0])+", L\"aaaa\", 0, 0); \n")

    def api_order(self) : 
        for img_id in self.maga_info :
            if self.maga_info[img_id].keys() == ["QR"] :
                self.draw_qrcode(img_id)

class PDF_STYLEs_API_MAP() :
    def __init__(self, maga_info, tempalte, tag_cnt) :
        self.maga_info = maga_info
        self.tempalte = tempalte
        self.tag_cnt = tag_cnt
    def draw_barcode (self, style_id) :
        self.tempalte.write ("FQL -> DrawBarcode(50, 50, 30, 50, L\"happyhappybar12345\", 1, 0); \n ")
    def api_order(self) :
        for style_id in self.maga_info :
            if self.maga_info[style_id] == "BC" : 
                self.draw_barcode(style_id) 

#class GENERAL_API():
#    def __init__(self, template):
#        self.template = template
#
#    def begin_line(self) :
#        self.template.write("#include \"/home/yifan/foxit_quick_pdf_library_1811_linux/Import/CPlusPlus/FoxitQPLLinuxCPP1811.h\" \n")
#        self.template.write("#include \"/home/yifan/foxit_quick_pdf_library_1811_linux/Import/CPlusPlus/FoxitQPLLinuxCPP1811.cpp\" \n")
#        self.template.write("#include <iostream> \n")
#        self.template.write("using namespace std; \n")
#        self.template.write("int main(int argc, char** argv) { \n")
#        self.template.write("std::wstring const wide(L\"/home/yifan/foxit_quick_pdf_library_1811_linux/Libs/libFoxitQPL1811-linux-x64.so\"); \n")
#        self.template.write("FoxitQPLLinuxCPP1811 * FQL = new FoxitQPLLinuxCPP1811(wide); \n")
#        self.template.write("cout << FQL->UnlockKey(L\"jf33n75u9oj3nb9pn7mf5rt8y\") << endl; \n")
#        self.template.write("FQL->SetGlobalOrigin(5); \n")
#
#    def end_line(self) :
#        self.template.write("FQL->SaveToFile(L\"pdf.pdf\"); \n")
#        self.template.write("return 0;\n")
#        self.template.write("} \n")
#
#
