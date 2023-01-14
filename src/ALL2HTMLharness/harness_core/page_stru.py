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
        # API : create page layout container 
        self.template.write("Wt::WContainerWidget *w" + str(self.tag_cnt) + " = root() -> addWidget(std::make_unique<Wt::WContainerWidget>()); \n")

        # API : Set Page Box
        self.template.write("w" + str(self.tag_cnt) + "->resize(random_int(-1000, 1000), random_int(-1000, 1000)); \n")
        self.template.write("auto layout" + str(self.tag_cnt) + "= std::make_unique<Wt::WBoxLayout>(Wt::LayoutDirection::TopToBottom);\n")
        self.template.write("layout" + str(self.tag_cnt) + "->addSpacing(random_int(-1000, 1000));\n")
        self.template.write("layout" + str(self.tag_cnt) + "->setSpacing(random_int(-1000, 1000));\n") 
        self.template.write("layout" + str(self.tag_cnt) + "->setContentsMargins(random_int(-1000, 1000), random_int(-1000, 1000), random_int(-1000, 1000), random_int(-1000, 1000));\n")                                              
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

            print ("HELLO!!!!!!!!!!!!!!!!!!!!")
#            # TEXT 
#            if len(texts) != 0 :
#                maga_info = TX.HTML_TEXT_STRU(texts).text_parse()
#                if len(maga_info) > 0 :
#                    TX.PDF_TEXT_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
#            # VG  
#            if len(VGs) != 0 :
#                maga_info_vg = VG.HTML_VGs_STRU(VGs).VG_parse()
#                if len(maga_info_vg) > 0 :
#                    VG.PDF_VGs_API_MAP(maga_info_vg, self.template, self.tag_cnt).api_order()
#            # IMG 
#            if len(IMGs) != 0:
#                maga_info_img = VG.HTML_IMGs_STRU(IMGs).IMG_parse()
#                if len(maga_info_img) > 0 :
#                    VG.PDF_IMGs_API_MAP(maga_info_img, self.template, self.tag_cnt).api_order()
#            # STYLE
#            if len(STYLEs) != 0:
#                maga_info_style = VG.HTML_STYLEs_STRU(STYLEs).STYLE_parse()
#                if len(maga_info_style) > 0 :
#                     VG.PDF_STYLEs_API_MAP(maga_info_style, self.template, self.tag_cnt).api_order()
#            # FORM
#            if len(forms) != 0 :
#                maga_info = FM.HTML_FORM_STRU(forms).form_parse()
#                if len(maga_info) > 0 :
#                    FM.PDF_FORM_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
            # TABLE
            if len(tables) > 0 :
                maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
                if len(maga_info) > 0 and len(maga_info) < 20:
                    tableID = 0
                    for tab in maga_info:

                        # if file contains table, map its structure to PDF API
                        TAB.PDF_TAB_API_MAP(maga_info, self.template, tableID, self.tag_cnt).api_order()
                        tableID += 1
        # API : to show the layout arrangement
        self.template.write("w" + str(self.tag_cnt) + "->setLayout(std::move(layout" + str(self.tag_cnt) + "));\n") 


