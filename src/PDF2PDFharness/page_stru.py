from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase

import commands

import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject

import vector_graphic as VG
import form as FM
import table as TAB
import text as TX

class PDF_PAGE_STRU() :
    def __init__(self, pdf, cur_pg_num, template) :
        # pass in stru (eg{body:div})
        self.pdf = pdf
        self.template = template
        self.tag_cnt = cur_pg_num
        self.cur_pg = pdf.getPage(cur_pg_num) 
        # save current page as a seperate pdf doc for futher parsing
        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(self.cur_pg)
        file_name = 'subset.pdf'
        with open(file_name, 'wb') as fw : 
            pdfWriter.write(fw)
            fw.close()
        self.cur_pg_sep_pdf = PdfFileReader(open(file_name, "rb"), strict=False)
        # check if has svg
        commands.getstatusoutput("pdftocairo -f 1 -l 1 -svg subset.pdf check.svg")
        self.svg_bool = 0
        if commands.getstatusoutput('ls ./check.svg')[1] != '' :
            self.svg_bool = 1
        

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

  #  def set_need_appearances_writer(writer):
  #      try:
  #          catalog = writer._root_object
  #          # get the AcroForm tree and add "/NeedAppearances attribute
  #          if "/AcroForm" not in catalog:
  #              writer._root_object.update({
  #                  NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

  #          need_appearances = NameObject("/NeedAppearances")
  #          writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
  #          return writer

  #      except Exception as e:
  #          print('set_need_appearances_writer() catch : ', repr(e))
  #          return writer

  #  def get_form_individual_page(self) : 
            


    def page_api_map(self) :
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

    # parsing and mapping
    def page_parse(self) :
        # PAGE STRUCTURE :
        self.page_api_map()

        # TEXT PARSING & MAPPING
        text_detect = self.cur_pg.extractText()

        outline_detect = self.cur_pg_sep_pdf.getOutlines()
        text_maga_info = dict()
        if text_detect :
           text_maga_info =  TX.PDF_TEXT_STRU(text_detect).text_parse()
        if outline_detect != []:
            text_maga_info = TX.PDF_TEXT_STRU(outline_detect).text_parse()
        if len(text_maga_info) > 0 :
            TX.PDF_TEXT_API_MAP(text_maga_info, self.template, self.tag_cnt).api_order()

        # VECTOR PARSING & MAPPING 
        vg_maga_info = dict()
        if self.svg_bool == 1 :
            vg_maga_info = VG.PDF_VGs_STRU(self.tag_cnt).VG_parse()
        if len(vg_maga_info) > 0 : 
            VG.PDF_VGs_API_MAP(vg_maga_info, self.template, self.tag_cnt).api_order()

        # IMAGE PARSING & MAPPING
        img_maga_info = dict()
        try : 
            xObj = self.cur_pg['/Resources']['/XObject'].getObject()
            for obj in xObj :
                if xObj[obj]['/Subtype'] == '/Image' :
                    img_maga_info = VG.PDF_IMGs_STRU(self.tag_cnt).IMG_parse()
                if len(img_maga_info) > 0 :
                    if type(img_maga_info.values()[0]) == str :
                        #print (img_maga_info.values()[0]) 
                        VG.PDF_STYLEs_API_MAP(img_maga_info, self.template, self.tag_cnt).api_order()
                    else :
                        VG.PDF_IMGs_API_MAP(img_maga_info, self.template, self.tag_cnt).api_order()
        except :
            print ("cannot get IMG")
            pass

        # TABLE PARSING & MAPPING
        tab_maga_info = dict()
        tab_num = 0
        with open ('subset.pdf', 'rb') as fr:
            for i in fr :
                if '/Form' in i :
                   tab_num += 1
        if tab_num != 0 :
            tab_maga_info = TAB.PDF_TAB_STRU(tab_num).tab_parse()
        if len(tab_maga_info) > 0 :
            for tableID in tab_maga_info :
                if tableID <= 5 :
                    TAB.PDF_TAB_API_MAP(tab_maga_info, self.template, tableID, self.tag_cnt).api_order() 
            
            
        os.remove('subset.pdf')
        os.remove('check.svg')

       # if len(VGs) != 0 or len(IMGs) != 0 or len(STYLEs) != 0 or len(texts) != 0 or len(forms) != 0 or len(tables) != 0 or len(styles) != 0 :

       #     # TEXT 
       #     if len(texts) != 0 :
       #         maga_info = TX.HTML_TEXT_STRU(texts).text_parse()
       #         if len(maga_info) > 0 :
       #             TX.PDF_TEXT_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
       #     # VG  
       #     if len(VGs) != 0 :
       #         maga_info_vg = VG.HTML_VGs_STRU(VGs).VG_parse()
       #         if len(maga_info_vg) > 0 :
       #             VG.PDF_VGs_API_MAP(maga_info_vg, self.template, self.tag_cnt).api_order()
       #     # IMG 
       #     if len(IMGs) != 0:
       #         maga_info_img = VG.HTML_IMGs_STRU(IMGs).IMG_parse()
       #         if len(maga_info_img) > 0 :
       #             VG.PDF_IMGs_API_MAP(maga_info_img, self.template, self.tag_cnt).api_order()
       #     # STYLE
       #     if len(STYLEs) != 0:
       #         maga_info_style = VG.HTML_STYLEs_STRU(STYLEs).STYLE_parse()
       #         if len(maga_info_style) > 0 :
       #              VG.PDF_STYLEs_API_MAP(maga_info_style, self.template, self.tag_cnt).api_order()
       #     # FORM
       #     if len(forms) != 0 :
       #         maga_info = FM.HTML_FORM_STRU(forms).form_parse()
       #         if len(maga_info) > 0 :
       #             FM.PDF_FORM_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
       #     # TABLE
       #     if len(tables) > 0 :
       #         maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
       #         if len(maga_info) > 0 and len(maga_info) < 20:
       #             tableID = 0
       #             for tab in maga_info:

       #                 # if file contains table, map its structure to PDF API
       #                 TAB.PDF_TAB_API_MAP(maga_info, self.template, tableID, self.tag_cnt).api_order()
       #                 tableID += 1


       #        # maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
       #        # if len(maga_info) > 0 and len(maga_info) < 10:
       #        #     # if file contains table, map its structure to PDF API
       #        #     TAB.PDF_TAB_API_MAP(maga_info, self.template, self.tag_cnt).api_order()
