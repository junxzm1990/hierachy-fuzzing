from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
import random
from random import seed
#from random import random
from random import choice
from string import ascii_uppercase

class PDF_VGs_STRU() : 
    def __init__(self, vgID) : 
        # pass in soup's forms
        self.vgID = vgID
        #{vgID:{shape:{attributes:value}}}
        self.maga_info = dict()

    def rand_dice(self, lo, up) :
        dice_rs = random.randint(lo,up)
        return dice_rs       
 
    def VG_type(self, vgID, shape_rand) : 
        self.maga_info[vgID] = dict()
        # attributes of each shape
        shape_attributes = dict()
        # counts of shapes
        cnt_circle = 0 
        cnt_rect = 0 
        cnt_ellipse = 0
        cnt_polygon = 0 
        # parse circle
        if shape_rand == 0 :
            shape_attributes["cx"] = self.rand_dice(0, 500) 
            shape_attributes["cy"] = self.rand_dice(0, 500) 
            shape_attributes["r"] = self.rand_dice(0, 500) 
            self.maga_info[vgID]["circle"+ str(vgID) + str(cnt_circle)] = shape_attributes
            shape_attributes = dict()
        # parse rectangular
        if shape_rand == 1 :
            shape_attributes["x"] = self.rand_dice(0, 500)
            shape_attributes["y"] = self.rand_dice(0, 500)
            shape_attributes["rx"] = self.rand_dice(0, 500)
            shape_attributes["ry"] = self.rand_dice(0, 500)
            shape_attributes["width"] = self.rand_dice(0, 500)
            shape_attributes["height"] = self.rand_dice(0, 500)
            self.maga_info[vgID]["rect" + str(vgID) + str(cnt_rect)] = shape_attributes
            shape_attributes = dict()
        # parse ellipse
        if shape_rand == 2 :
            shape_attributes["e_height"] = self.rand_dice(0, 500)
            shape_attributes["e_width"] = self.rand_dice(0, 500)
            self.maga_info[vgID]["ellipse" + str(vgID) + str(cnt_ellipse)] = shape_attributes
            shape_attributes = dict()
        # parse polygon
        if shape_rand == 3 : 
            point_num_rand = self.rand_dice(2, 50)
            for i in range(0, point_num_rand) :
                if i == 0:
                    shape_attributes[i] = (self.rand_dice(0, 500), self.rand_dice(0, 500))
                elif i == point_num_rand : 
                    shape_attributes[point_num_rand] = (shape_attributes[i-1][1], shape_attributes[0][0])
                else :
                    shape_attributes[i] = (shape_attributes[i-1][1], self.rand_dice(0,500))
                
            self.maga_info[vgID]["polygon"+str(vgID) + str(cnt_polygon)] = shape_attributes
            shape_attributes = dict()
    def VG_parse(self) : 
        shape_rand = self.rand_dice(0, 3)
        self.VG_type(self.vgID, shape_rand)
        return self.maga_info

class PDF_IMGs_STRU() :
    def __init__(self, IMGs) :
        # pass in soup's imgs
        self.IMGs = IMGs
        #{imgID:{type:{attributes:value}}}
        self.maga_info = dict()
    def rand_dice(self, lo, up) :
        dice_rs = random.randint(lo,up)
        return dice_rs
    def rand_str(self, text_len) :
        lower_case = string.ascii_lowercase
        upper_case = string.ascii_uppercase
        digits = string.digits
        punc = string.punctuation

        rand_str = ''.join(random.choice(lower_case + upper_case + digits) for i in range(text_len))
        rand_str_amend = rand_str
        for i in rand_str :
            if i in punc :
                rand_str_amend = rand_str_amend.replace(i, "\\" + i)
        return rand_str_amend       
    def IMG_type(self, img_id) :
        size_rand = self.rand_dice(0, 500) 
        self.maga_info[img_id] = {"QR":str(size_rand)}
    def STYLE_type(self, style_id) : 
        self.maga_info[style_id] = "BC"
    def IMG_parse(self) :
        QR_or_Bar = self.rand_dice(0,1)
        str_gen = self.rand_str(4)
        if QR_or_Bar == 0 :
            self.IMG_type(str(self.IMGs)+str_gen)
        else :
            self.STYLE_type(str(self.IMGs)+str_gen)
        return self.maga_info 

#class HTML_STYLEs_STRU() :
#    def __init__(self, STYLEs) :
#        # pass in soup's styles
#        self.STYLEs = STYLEs
#        # {style ID : obj}
#        self.maga_info = dict()
#    def STYLE_type(self, style, style_id) :
#        try :
#            str(style)
#            if ("barcode" in str(style)) or ("Barcode" in str(style)) :
#                self.maga_info[style_id] = "BC"
#        except :
#            style = style.encode("utf-8")
#            if ("barcode" in str(style)) or ("Barcode" in str(style)) :
#                self.maga_info[style_id] = "BC"
#
##        if ("barcode" in str(style)) or ("Barcode" in str(style)) : 
##            self.maga_info[style_id] = "BC"
#    def STYLE_parse(self) : 
#        styleID = 0 
#        for style in self.STYLEs:
#            self.STYLE_type(style, styleID)
#            styleID += 1
#        return self.maga_info
        
       

class PDF_VGs_API_MAP() :
    def __init__(self, maga_info, template, tag_cnt) :
        self.maga_info = maga_info
        self.template = template
        self.tag_cnt = tag_cnt

    def arg_val(self, arg_name, arg_type, constrain, upper, lower):
        self.template.write(arg_type + " "+ arg_name + "=(" + arg_type + ")0; \n")
        self.template.write("if (bytes_read - index >= sizeof(" + arg_type + ")) { \n")
        self.template.write(arg_name + " = *("+arg_type+"*)(buffer+index); \n")
        self.template.write(constrain)
        if arg_type == "int" :
            self.template.write(arg_name+" = random_int((int)"+upper+", (int)"+lower+"); \n")
        elif arg_type == "double" :
            self.template.write(arg_name+" = random_double((double)"+upper+", (double)"+lower+"); \n")
        elif arg_type == "string" :
            self.template.write(arg_name+" = random_string(uppper); \n") ## Here, upper == name_len
       # self.template.write("exit(0); \n")
        self.template.write("}else{ \n")
        self.template.write("index += sizeof(" + arg_type + ");\n")
        self.template.write("} \n")
        self.template.write("}else{ \n")
        self.template.write("exit(0); \n")
        self.template.write("} \n")


    
    def draw_circle(self, vgID, cnt) : 
        # API : DrawCircle(XPos, YPos, Radius, DrawOptions)
        DrawCircle_arg_1 = "DrawCircle_XPos" + str(vgID)+str(cnt)+str(self.tag_cnt)
        DrawCircle_arg_2 = "DrawCircle_YPos" + str(vgID)+str(cnt)+str(self.tag_cnt)
        DrawCircle_arg_3 = "DrawCircle_Radius" + str(vgID)+str(cnt)+str(self.tag_cnt)
        DrawCircle_arg_4 = "DrawCircle_DrawOptions" + str(vgID)+str(cnt)+str(self.tag_cnt)
        DrawCircle_constrain_1 = "if (" + DrawCircle_arg_1 + " <0.001 || " + DrawCircle_arg_1 + " > 800.001) { \n"
        DrawCircle_constrain_2 = "if (" + DrawCircle_arg_2 + " <0.001 || " + DrawCircle_arg_2 + " > 800.001) { \n"
        DrawCircle_constrain_3 = "if (" + DrawCircle_arg_3 + " <0.001 || " + DrawCircle_arg_3 + " > 800.001) { \n"
        DrawCircle_constrain_4 = "if (" + DrawCircle_arg_4 + " <0 || " + DrawCircle_arg_4 + " > 2) { \n"
        self.arg_val(DrawCircle_arg_1, "double", DrawCircle_constrain_1, "800.001", "0.001")
        self.arg_val(DrawCircle_arg_2, "double", DrawCircle_constrain_2, "800.001", "0.001")
        self.arg_val(DrawCircle_arg_3, "double", DrawCircle_constrain_3, "800.001", "0.001")
        self.arg_val(DrawCircle_arg_4, "int", DrawCircle_constrain_4, "2", "0")
        self.template.write("int circle"+str(vgID)+str(cnt)+str(self.tag_cnt)+" = FQL->DrawCircle("+DrawCircle_arg_1+", "+DrawCircle_arg_2+","+DrawCircle_arg_3+", " +DrawCircle_arg_4 + " ); \n")    
    def draw_box(self, vgID, cnt) :
        # API : DrawBox(Left, Top, Width, Height, DrawOption)
        DrawBox_arg_1 = "DrawBox_Left" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawBox_arg_2 = "DrawBox_Top" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawBox_arg_3 = "DrawBox_Width" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawBox_arg_4 = "DrawBox_Height" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawBox_arg_5 = "DrawBox_DrawOptions" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawBox_constrain_1 = "if (" + DrawBox_arg_1 + " < 0.001 || " + DrawBox_arg_1 + " > 800.001) {\n"
        DrawBox_constrain_2 = "if (" + DrawBox_arg_2 + " < 0.001 || " + DrawBox_arg_2 + " > 800.001) {\n"
        DrawBox_constrain_3 = "if (" + DrawBox_arg_3 + " < 0.001 || " + DrawBox_arg_3 + " > 800.001) {\n"
        DrawBox_constrain_4 = "if (" + DrawBox_arg_4 + " < 0.001 || " + DrawBox_arg_4 + " > 800.001) {\n"
        DrawBox_constrain_5 = "if (" + DrawBox_arg_5 + " < 0 || " + DrawBox_arg_5 + " > 2) {\n"
        self.arg_val(DrawBox_arg_1, "double", DrawBox_constrain_1, "800.001", "0.001")
        self.arg_val(DrawBox_arg_2, "double", DrawBox_constrain_2, "800.001", "0.001")
        self.arg_val(DrawBox_arg_3, "double", DrawBox_constrain_3, "800.001", "0.001")
        self.arg_val(DrawBox_arg_4, "double", DrawBox_constrain_4, "800.001", "0.001")
        self.arg_val(DrawBox_arg_5, "int", DrawBox_constrain_5, "2", "0")
        self.template.write("int rect" +str(vgID) +str(cnt) + str(self.tag_cnt) + " = FQL->DrawBox(" + DrawBox_arg_1  + ", " + DrawBox_arg_2 + ", "+DrawBox_arg_3+", "+DrawBox_arg_4+", "+DrawBox_arg_5+");\n")
    def draw_round_box(self, vgID, cnt) :
        # API : DrawRoundedBox(Left, Top, Width, Height, Radius, DrawOptions)
        DrawRoundedBox_arg_1 = "DrawRoundedBox_Left" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawRoundedBox_arg_2 = "DrawRoundedBox_Top" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawRoundedBox_arg_3 = "DrawRoundedBox_Width" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawRoundedBox_arg_4 = "DrawRoundedBox_Height" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawRoundedBox_arg_5 = "DrawRoundedBox_Radius" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawRoundedBox_arg_6 = "DrawRoundedBox_DrawOptions" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawRoundedBox_constrain_1 = "if ("+DrawRoundedBox_arg_1+" < 0.001 || " + DrawRoundedBox_arg_1 + " > 800.001 ){ \n"
        DrawRoundedBox_constrain_2 = "if ("+DrawRoundedBox_arg_2+" < 0.001 || " + DrawRoundedBox_arg_2 + " > 800.001 ){ \n"
        DrawRoundedBox_constrain_3 = "if ("+DrawRoundedBox_arg_3+" < 0.001 || " + DrawRoundedBox_arg_3 + " > 800.001 ){ \n"
        DrawRoundedBox_constrain_4 = "if ("+DrawRoundedBox_arg_4+" < 0.001 || " + DrawRoundedBox_arg_4 + " > 800.001 ){ \n"
        DrawRoundedBox_constrain_5 = "if ("+DrawRoundedBox_arg_5+" < 0.001 || " + DrawRoundedBox_arg_5 + " > 800.001 ){ \n"
        DrawRoundedBox_constrain_6 = "if ("+DrawRoundedBox_arg_6+" < 0 || " + DrawRoundedBox_arg_6 + " > 2 ){ \n"
        self.arg_val(DrawRoundedBox_arg_1, "double", DrawRoundedBox_constrain_1, "800.001", "0.001")
        self.arg_val(DrawRoundedBox_arg_2, "double", DrawRoundedBox_constrain_2, "800.001", "0.001")
        self.arg_val(DrawRoundedBox_arg_3, "double", DrawRoundedBox_constrain_3, "800.001", "0.001")
        self.arg_val(DrawRoundedBox_arg_4, "double", DrawRoundedBox_constrain_4, "800.001", "0.001")
        self.arg_val(DrawRoundedBox_arg_5, "double", DrawRoundedBox_constrain_5, "800.001", "0.001")
        self.arg_val(DrawRoundedBox_arg_6, "int", DrawRoundedBox_constrain_6, "2", "0")
        self.template.write("int rect_round" +str(vgID) + str(cnt)+str(self.tag_cnt)+ " = FQL->DrawRoundedBox("+DrawRoundedBox_arg_1+", "+DrawRoundedBox_arg_2+", "+DrawRoundedBox_arg_3+","+DrawRoundedBox_arg_4+", "+DrawRoundedBox_arg_5+","+DrawRoundedBox_arg_6+" ); \n ")
    def draw_polygon(self, vgID, cnt) :
       # for i in self.maga_info[vgID][cnt].values():
        StartPath_arg_1 = "StartPath_StartX"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        StartPath_arg_2 = "StartPath_StartY"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        StartPath_constrain_1 = "if ("+StartPath_arg_1+" < 0.001 || " + StartPath_arg_1 + " > 800.001 ){ \n"
        StartPath_constrain_2 = "if ("+StartPath_arg_2+" < 0.001 || " + StartPath_arg_2 + " > 800.001 ){ \n"
        self.arg_val(StartPath_arg_1, "double", StartPath_constrain_1, "800.001", "0.001")
        self.arg_val(StartPath_arg_2, "double", StartPath_constrain_2, "800.001", "0.001")
        self.template.write("FQL->StartPath("+StartPath_arg_1+", " + StartPath_arg_1+"); \n")

        AddLineToPath_arg_1 = "AddLineToPath_EndX"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        AddLineToPath_arg_2 = "AddLineToPath_EndY"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        AddLineToPath_constrain_1 = "if ("+AddLineToPath_arg_1+" < 0.001 || " + AddLineToPath_arg_1 + " > 800.001 ){ \n"
        AddLineToPath_constrain_2 = "if ("+AddLineToPath_arg_2+" < 0.001 || " + AddLineToPath_arg_2 + " > 800.001 ){ \n"
        self.arg_val(AddLineToPath_arg_1, "double", AddLineToPath_constrain_1, "800.001", "0.001")
        self.arg_val(AddLineToPath_arg_2, "double", AddLineToPath_constrain_2, "800.001", "0.001")
        self.template.write("FQL->AddLineToPath("+AddLineToPath_arg_1+", "+AddLineToPath_arg_2+"); \n")


        DrawLine_arg_1 = "DrawLine_StartX"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        DrawLine_arg_2 = "DrawLine_StartY"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        DrawLine_arg_3 = "PathDrawLine_EndX"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        DrawLine_arg_4 = "PathDrawLine_EndY"+ str(vgID) + str(cnt) + str(self.tag_cnt)
        DrawLine_constrain_1 = "if ("+DrawLine_arg_1+" < 0.001 || " + DrawLine_arg_1 + " > 800.001 ){ \n"
        DrawLine_constrain_2 = "if ("+DrawLine_arg_2+" < 0.001 || " + DrawLine_arg_2 + " > 800.001 ){ \n"
        DrawLine_constrain_3 = "if ("+DrawLine_arg_3+" < 0.001 || " + DrawLine_arg_3 + " > 800.001 ){ \n"
        DrawLine_constrain_4 = "if ("+DrawLine_arg_4+" < 0.001 || " + DrawLine_arg_4 + " > 800.001 ){ \n"
        self.arg_val(DrawLine_arg_1, "double", DrawLine_constrain_1, "800.001", "0.001")
        self.arg_val(DrawLine_arg_2, "double", DrawLine_constrain_2, "800.001", "0.001")
        self.arg_val(DrawLine_arg_3, "double", DrawLine_constrain_3, "800.001", "0.001")
        self.arg_val(DrawLine_arg_4, "double", DrawLine_constrain_4, "800.001", "0.001")

        self.template.write("FQL->DrawLine("+DrawLine_arg_1+", "+DrawLine_arg_2+","+DrawLine_arg_3+", "+DrawLine_arg_4+"); \n")
    def draw_ellipse(self, vgID, cnt) :
        # API : DrawEllipse(XPos, YPos, Width, Height, DrawOptions)
        DrawEllipse_arg_1 = "DrawEllipse_XPos" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawEllipse_arg_2 = "DrawEllipse_YPos" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawEllipse_arg_3 = "DrawEllipse_Width" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawEllipse_arg_4 = "DrawEllipse_Height" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawEllipse_arg_5 = "DrawEllipse_DrawOptions" + str(vgID) + str(cnt)+str(self.tag_cnt)
        DrawEllipse_constrain_1 = "if (" + DrawEllipse_arg_1 + " < 0.001 || " + DrawEllipse_arg_1 + " > 800.001) {\n"
        DrawEllipse_constrain_2 = "if (" + DrawEllipse_arg_2 + " < 0.001 || " + DrawEllipse_arg_2 + " > 800.001) {\n"
        DrawEllipse_constrain_3 = "if (" + DrawEllipse_arg_3 + " < 0.001 || " + DrawEllipse_arg_3 + " > 800.001) {\n"
        DrawEllipse_constrain_4 = "if (" + DrawEllipse_arg_4 + " < 0.001 || " + DrawEllipse_arg_4 + " > 800.001) {\n"
        DrawEllipse_constrain_5 = "if (" + DrawEllipse_arg_5 + " < 0 || " + DrawEllipse_arg_5 + " > 2) {\n"
        self.arg_val(DrawEllipse_arg_1, "double", DrawEllipse_constrain_1, "800.001", "0.001")
        self.arg_val(DrawEllipse_arg_2, "double", DrawEllipse_constrain_2, "800.001", "0.001")
        self.arg_val(DrawEllipse_arg_3, "double", DrawEllipse_constrain_3, "800.001", "0.001")
        self.arg_val(DrawEllipse_arg_4, "double", DrawEllipse_constrain_4, "800.001", "0.001")
        self.arg_val(DrawEllipse_arg_5, "int", DrawEllipse_constrain_5, "2", "0")
        self.template.write("int ellipse" +str(vgID) +str(cnt) +str(self.tag_cnt)+ " = FQL->DrawEllipse("+DrawEllipse_arg_1+", "+DrawEllipse_arg_2+", "+DrawEllipse_arg_3+", "+DrawEllipse_arg_4+", "+DrawEllipse_arg_5+"); \n")    
    def color_setting(self, Red, Green, Blue) :
        self.template.write("FQL->SetFillColor("+str(Red)+","+str(Green)+","+str(Blue)+"); \n")
 
    def api_order(self) : 
        for svg in self.maga_info : 
            for shape in self.maga_info[svg] :
                red = random.random()
                green = random.random()
                blue = random.random()
                self.color_setting(red, green, blue)
                if shape[0:6] == "circle" :
                    self.draw_circle(svg, shape)
                elif shape[0:4] == "rect" :
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
    def arg_val(self, arg_name, arg_type, constrain, upper, lower):
        self.template.write(arg_type + " "+ arg_name + "=(" + arg_type + ")0; \n")
        self.template.write("if (bytes_read - index >= sizeof(" + arg_type + ")) { \n")
        self.template.write(arg_name + " = *("+arg_type+"*)(buffer+index); \n")
        self.template.write(constrain)
        if arg_type == "int" :
            self.template.write(arg_name+" = random_int((int)"+upper+", (int)"+lower+"); \n")
        elif arg_type == "double" :
            self.template.write(arg_name+" = random_double((double)"+upper+", (double)"+lower+"); \n")
        elif arg_type == "string" :
            self.template.write(arg_name+" = random_string(uppper); \n") ## Here, upper == name_len
       # self.template.write("exit(0); \n")
        self.template.write("}else{ \n")
        self.template.write("index += sizeof(" + arg_type + ");\n")
        self.template.write("} \n")
        self.template.write("}else{ \n")
        self.template.write("exit(0); \n")
        self.template.write("} \n")
    def draw_qrcode (self, img_id) :
        # API : DrawQRCode(Left, Top, SymbolSize, Text, EncodeOptions, DrawOptions)
        letters = string.ascii_lowercase
        text_rand = ''.join(choice(letters) for i in range(35))

        DrawQRCode_arg_1 = "DrawQRCode_Left" + str(img_id) + str(self.tag_cnt)
        DrawQRCode_arg_2 = "DrawQRCode_Top" + str(img_id) + str(self.tag_cnt)
        DrawQRCode_arg_3 = "DrawQRCode_SymbolSize" + str(img_id) + str(self.tag_cnt)
        DrawQRCode_arg_4 = "DrawQRCode_EncodeOptions" + str(img_id) + str(self.tag_cnt)
        DrawQRCode_arg_5 = "DrawQRCode_DrawOptions" + str(img_id) + str(self.tag_cnt)
        DrawQRCode_constrain_1 = "if("+DrawQRCode_arg_1+" < 0.001 || "+DrawQRCode_arg_1+" > 800.001) { \n"
        DrawQRCode_constrain_2 = "if("+DrawQRCode_arg_2+" < 0.001 || "+DrawQRCode_arg_2+" > 800.001) { \n"
        DrawQRCode_constrain_3 = "if("+DrawQRCode_arg_3+" < 0.001 || "+DrawQRCode_arg_3+" > 800.001) { \n"
        DrawQRCode_constrain_4 = "if("+DrawQRCode_arg_4+" < 0 || "+DrawQRCode_arg_4+" > 5) { \n"
        DrawQRCode_constrain_5 = "if("+DrawQRCode_arg_5+" < 0 || "+DrawQRCode_arg_5+" > 3) { \n"
        self.arg_val(DrawQRCode_arg_1, "double", DrawQRCode_constrain_1, "800.001", "0.001")
        self.arg_val(DrawQRCode_arg_2, "double", DrawQRCode_constrain_2, "800.001", "0.001")
        self.arg_val(DrawQRCode_arg_3, "double", DrawQRCode_constrain_3, "800.001", "0.001")
        self.arg_val(DrawQRCode_arg_4, "int", DrawQRCode_constrain_4, "5", "0")
        self.arg_val(DrawQRCode_arg_5, "int", DrawQRCode_constrain_5, "3", "0")
 
        self.template.write("FQL->DrawQRCode("+DrawQRCode_arg_1+", "+DrawQRCode_arg_2+", "+DrawQRCode_arg_3+", L\""+text_rand+"\", "+DrawQRCode_arg_4+", "+DrawQRCode_arg_5+"); \n")

    def api_order(self) : 
        for img_id in self.maga_info :
            #print("***** : ", self.maga_info[img_id])
            if self.maga_info[img_id].keys() == ["QR"] :
                self.draw_qrcode(img_id)

class PDF_STYLEs_API_MAP() :
    def __init__(self, maga_info, template, tag_cnt) :
        self.maga_info = maga_info
        self.template = template
        self.tag_cnt = tag_cnt
    def arg_val(self, arg_name, arg_type, constrain, upper, lower):
        self.template.write(arg_type + " "+ arg_name + "=(" + arg_type + ")0; \n")
        self.template.write("if (bytes_read - index >= sizeof(" + arg_type + ")) { \n")
        self.template.write(arg_name + " = *("+arg_type+"*)(buffer+index); \n")
        self.template.write(constrain)
        if arg_type == "int" :
            self.template.write(arg_name+" = random_int((int)"+upper+", (int)"+lower+"); \n")
        elif arg_type == "double" :
            self.template.write(arg_name+" = random_double((double)"+upper+", (double)"+lower+"); \n")
        elif arg_type == "string" :
            self.template.write(arg_name+" = random_string(uppper); \n") ## Here, upper == name_len
       # self.template.write("exit(0); \n")
        self.template.write("}else{ \n")
        self.template.write("index += sizeof(" + arg_type + ");\n")
        self.template.write("} \n")
        self.template.write("}else{ \n")
        self.template.write("exit(0); \n")
        self.template.write("} \n")
    def draw_barcode (self, style_id) :
        # DrawBarcode(Left, Top, Width, Height, Text, Barcode, Options)
        letters = string.ascii_lowercase
        text_rand = ''.join(choice(letters) for i in range(35))
        DrawBarcode_arg_1 = "DrawBarcode_Left" + str(style_id) + str(self.tag_cnt)
        DrawBarcode_arg_2 = "DrawBarcode_Top" + str(style_id)+ str(self.tag_cnt)
        DrawBarcode_arg_3 = "DrawBarcode_Width" + str(style_id)+ str(self.tag_cnt)
        DrawBarcode_arg_4 = "DrawBarcode_Height" + str(style_id)+ str(self.tag_cnt)
        DrawBarcode_arg_5 = "DrawBarcode_Barcode" + str(style_id)+ str(self.tag_cnt)
        DrawBarcode_arg_6 = "DrawBarcode_Option" + str(style_id)+ str(self.tag_cnt)
        DrawBarcode_constrain_1 = "if("+DrawBarcode_arg_1+" < 0.001 || "+DrawBarcode_arg_1+" > 800.001) { \n"
        DrawBarcode_constrain_2 = "if("+DrawBarcode_arg_2+" < 0.001 || "+DrawBarcode_arg_2+" > 800.001) { \n"
        DrawBarcode_constrain_3 = "if("+DrawBarcode_arg_3+" < 0.001 || "+DrawBarcode_arg_3+" > 800.001) { \n"
        DrawBarcode_constrain_4 = "if("+DrawBarcode_arg_4+" < 0.001 || "+DrawBarcode_arg_4+" > 800.001) { \n"
        DrawBarcode_constrain_5 = "if("+DrawBarcode_arg_5+" < 1 || "+DrawBarcode_arg_5+" > 5) { \n"
        DrawBarcode_constrain_6 = "if("+DrawBarcode_arg_6+" < 0 || "+DrawBarcode_arg_6+" > 4) { \n"
        self.arg_val(DrawBarcode_arg_1, "double", DrawBarcode_constrain_1, "800.001", "0.001")
        self.arg_val(DrawBarcode_arg_2, "double", DrawBarcode_constrain_2, "800.001", "0.001")
        self.arg_val(DrawBarcode_arg_3, "double", DrawBarcode_constrain_3, "800.001", "0.001")
        self.arg_val(DrawBarcode_arg_4, "double", DrawBarcode_constrain_4, "800.001", "0.001")
        self.arg_val(DrawBarcode_arg_5, "int", DrawBarcode_constrain_5, "5", "1")
        self.arg_val(DrawBarcode_arg_6, "int", DrawBarcode_constrain_6, "4", "0")

        self.template.write ("FQL -> DrawBarcode("+DrawBarcode_arg_1+", "+DrawBarcode_arg_2+", "+DrawBarcode_arg_3+", "+DrawBarcode_arg_4+", L\"" + text_rand +"\", "+DrawBarcode_arg_5+", "+DrawBarcode_arg_6+"); \n ")
    def api_order(self) :
        for style_id in self.maga_info :
            if self.maga_info[style_id] == "BC" : 
                self.draw_barcode(style_id) 
