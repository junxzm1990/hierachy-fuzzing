from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase

import vector_graphic as VG
import form as FM
import table as TAB
import text as TX

class HTML_PAGE_STRU() :
    def __init__(self, div,template, cnt) :
        # pass in stru (eg{body:div})
        self.div = div
        self.template = template
        self.tag_cnt = cnt

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

    # parsing and mapping
    def div_parse(self) :
        # MAPPING DIV API :
        # API : NewPage 
        self.template.write("FQL->NewPage(); \n")

        # API : SetPageBox
        SetPageBox_arg_1 = "SetPageBox_BoxType" + str(self.tag_cnt) 
        SetPageBox_arg_2 = "SetPageBox_Left" + str(self.tag_cnt) 
        SetPageBox_arg_3 = "SetPageBox_Top" + str(self.tag_cnt) 
        SetPageBox_arg_4 = "SetPageBox_Width" + str(self.tag_cnt) 
        SetPageBox_arg_5 = "SetPageBox_Height" + str(self.tag_cnt) 
        SetPageBox_constrain_1 = "if("+SetPageBox_arg_1+" < 1 || "+SetPageBox_arg_1+" > 5 ) { \n"

        SetPageBox_constrain_2 = "if("+SetPageBox_arg_2+" < 0.001 || "+SetPageBox_arg_2+" > 800.001 ) { \n"
        SetPageBox_constrain_3 = "if("+SetPageBox_arg_3+" < 0.001 || "+SetPageBox_arg_3+" > 800.001 ) { \n"
        SetPageBox_constrain_4 = "if("+SetPageBox_arg_4+" < 0.001 || "+SetPageBox_arg_4+" > 800.001 ) { \n"
        SetPageBox_constrain_5 = "if("+SetPageBox_arg_5+" < 0.001 || "+SetPageBox_arg_5+" > 800.001 ) { \n"
 
        self.arg_val(SetPageBox_arg_1, "int", SetPageBox_constrain_1, "5", "1")
        self.arg_val(SetPageBox_arg_2, "double", SetPageBox_constrain_2, "800.001", "0.001")
        self.arg_val(SetPageBox_arg_3, "double", SetPageBox_constrain_3, "800.001", "0.001")
        self.arg_val(SetPageBox_arg_4, "double", SetPageBox_constrain_4, "800.001", "0.001")
        self.arg_val(SetPageBox_arg_5, "double", SetPageBox_constrain_5, "800.001", "0.001")

        self.template.write("FQL->SetPageBox("+SetPageBox_arg_1+", "+SetPageBox_arg_2+", "+SetPageBox_arg_3+", "+SetPageBox_arg_4+", "+SetPageBox_arg_5+"); \n")

        # TEXT
        texts = self.div.find_all(['p', 'span', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'blockquote', 'code', 'ul', 'ol', 'dl', 'mark', 'ins', 'del', 'sup', 'sub', 'i', 'b'])
        # VGs
        VGs = self.div.find_all('svg')
        # IMGs
        IMGs = self.div.find_all('img')
        # STYLEs
        STYLEs = self.div.find_all('style')
        # FORM
        forms = self.div.find_all('form')
        # TABLE
        tables = self.div.find_all('table')
        styles = self.div.find_all('style')

        if len(VGs) != 0 or len(IMGs) != 0 or len(STYLEs) != 0 or len(texts) != 0 or len(forms) != 0 or len(tables) != 0 or len(styles) != 0 :

            # TEXT 
            if len(texts) != 0 :
                maga_info = TX.HTML_TEXT_STRU(texts).text_parse()
                if len(maga_info) > 0 :
                    TX.PDF_TEXT_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
            # VG  
            if len(VGs) != 0 :
                maga_info_vg = VG.HTML_VGs_STRU(VGs).VG_parse()
                if len(maga_info_vg) > 0 :
                    VG.PDF_VGs_API_MAP(maga_info_vg, self.template, self.tag_cnt).api_order()
            # IMG 
            if len(IMGs) != 0:
                maga_info_img = VG.HTML_IMGs_STRU(IMGs).IMG_parse()
                if len(maga_info_img) > 0 :
                    VG.PDF_IMGs_API_MAP(maga_info_img, self.template, self.tag_cnt).api_order()
            # STYLE
            if len(STYLEs) != 0:
                maga_info_style = VG.HTML_STYLEs_STRU(STYLEs).STYLE_parse()
                if len(maga_info_style) > 0 :
                     VG.PDF_STYLEs_API_MAP(maga_info_style, self.template, self.tag_cnt).api_order()
            # FORM
            if len(forms) != 0 :
                maga_info = FM.HTML_FORM_STRU(forms).form_parse()
                if len(maga_info) > 0 :
                    FM.PDF_FORM_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
            # TABLE
            if len(tables) > 0 :
                maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
                if len(maga_info) > 0 and len(maga_info) < 20:
                    tableID = 0
                    for tab in maga_info:

                        # if file contains table, map its structure to PDF API
                        TAB.PDF_TAB_API_MAP(maga_info, self.template, tableID, self.tag_cnt).api_order()
                        tableID += 1


               # maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
               # if len(maga_info) > 0 and len(maga_info) < 10:
               #     # if file contains table, map its structure to PDF API
               #     TAB.PDF_TAB_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
