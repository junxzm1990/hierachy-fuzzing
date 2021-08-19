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
import page_stru as PS

class GENERAL_API():
    def __init__(self, template, pdf_opt_dir):
        self.template = template
        self.pdf_opt_dir = pdf_opt_dir

    def begin_line(self) :
        self.template.write("#include \"/home/yifan/foxit_quick_pdf_library_1811_linux/Import/CPlusPlus/FoxitQPLLinuxCPP1811.h\" \n")
        self.template.write("#include \"/home/yifan/foxit_quick_pdf_library_1811_linux/Import/CPlusPlus/FoxitQPLLinuxCPP1811.cpp\" \n")
        self.template.write("#include <iostream> \n")
        self.template.write("#include <string> \n")
        self.template.write("using namespace std; \n")
        self.template.write("int main(int argc, char** argv) { \n")
        self.template.write("std::wstring const wide(L\"/home/yifan/foxit_quick_pdf_library_1811_linux/Libs/libFoxitQPL1811-linux-x64.so\"); \n")
        self.template.write("FoxitQPLLinuxCPP1811 * FQL = new FoxitQPLLinuxCPP1811(wide); \n")
        self.template.write("cout << FQL->UnlockKey(L\"jf33n75u9oj3nb9pn7mf5rt8y\") << endl; \n")
        self.template.write("FQL->SetGlobalOrigin(5); \n")
    def end_line(self) :
        self.template.write("std::string opt_random = \""+str(self.pdf_opt_dir)+"\" +  std::string(\"PDF.pdf\"); \n")
        self.template.write("const size_t len = opt_random.length() + 1; \n")
        self.template.write("wchar_t opt_name[len]; \n")
        self.template.write("swprintf(opt_name, len, L\"%s\", opt_random.c_str()); \n")
        self.template.write("FQL->SaveToFile(opt_name); \n")
        self.template.write("return 0;\n")
        self.template.write("} \n")

# Building the HTML strucure tree
def traverse(soup) :
    if soup is not None :
        if soup.name is not None:
           stru = [soup.name]
           for child in soup.children :
               if child.name is not None :
                   stru.append(traverse(child))
           print (stru)
           return stru

# iterate the tree strues, call corresponding tag's(or cluster of tags') classes
def iter_tree(soup,stru,cur_root,out_f,cnt) :
    if stru is not None : 
        for i in stru :
            # iteratively walking on the tree
            if isinstance(i, list) : 
                iter_tree(soup, i, cur_root, out_f, cnt)
            # parsing and mapping the node features
            else :
               if cur_root == 'body' :
                   if i == 'div' :
                       print ("%%%%%%%%%%%%%%%%%%%%%%%%%")
                       pages = soup.find(i)
                       PS.HTML_PAGE_STRU(soup.find('div'), out_f, cnt).div_parse()
                       pages.decompose()
                   elif i in ['p', 'span', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'blockquote', 'code', 'ul', 'ol', 'dl', 'mark', 'ins', 'del', 'sup', 'sub', 'i', 'b'] :
                       texts = soup.find(i)
                       if len(texts) != 0 :
                            maga_info = TX.HTML_TEXT_STRU(texts).text_parse()
                            if len(maga_info) > 0 :
                                TX.PDF_TEXT_API_MAP(maga_info, out_f, cnt).api_order()
                       texts.decompose()
                   elif i == 'svg' : 
                       VGs = soup.find(i)
                       if len(VGs) != 0 :
                           maga_info_vg = VG.HTML_VGs_STRU(VGs).VG_parse()
                           if len(maga_info_vg) > 0 :
                               VG.PDF_VGs_API_MAP(maga_info_vg, out_f, cnt).api_order()
                       VGs.decompose()
                   elif i == 'img' :
                       IMGs = soup.find(i)
                       if len(IMGs) != 0 :
                           maga_info_img = VG.HTML_IMGs_STRU(IMGs).IMG_parse()
                           if len(maga_info_img) > 0 :
                               VG.PDF_IMGs_API_MAP(maga_info_img, out_f, cnt).api_order()
                       IMGs.decompose()
                   elif i == 'style' :
                       STYLEs = soup.find(i)
                       if len(STYLEs) != 0 :
                           maga_info_style = VG.HTML_STYLEs_STRU(STYLEs).STYLE_parse()
                           if len(maga_info_style) > 0 :
                                VG.PDF_STYLEs_API_MAP(maga_info_style, out_f, cnt).api_order()
                       STYLEs.decompose()
                   elif i == 'form' :
                       forms = soup.find(i)
                       if len(forms) != 0 :
                           maga_info = FM.HTML_FORM_STRU(forms).form_parse()
                           if len(maga_info) > 0 :
                               FM.PDF_FORM_API_MAP(maga_info, out_f, cnt).api_order()
                       forms.decompose()
                   elif i == 'table' : 
                       tables = soup.find(i)
                       styles = soup.find('style')
                       if len(tables) > 0 :
                           maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
                           if len(maga_info) > 0 and len(maga_info) < 10:
                           # if file contains table, map its structure to PDF API
                               TAB.PDF_TAB_API_MAP(maga_info, out_f, cnt).api_order()
                       tables.decompose()
            cnt += 1
            cur_root = stru[0]

def main(argv) :
    html_file = argv[0]
    output_dir = argv[1]
    pdf_opt_dir =argv[2]
    file_name = str(html_file.split("/")[-1]).replace(" ","").replace(",", "").replace(".", "")
    print ("@@@@@@@", file_name)

    # load in html content to soup
    in_f = open(html_file, 'r').read()
    soup = BeautifulSoup(in_f, 'lxml')

    # build DOC TREE structure
    stru_tree = traverse(soup.find('html'))

    if stru_tree != {} :
        os.makedirs(output_dir + "/" + file_name)
        out_f = open( output_dir + "/" + file_name + "/html_to_PDF_text_template.cpp", "a")
        GENERAL_API(out_f, argv[2]).begin_line()

        # parsing and mapping based on DOC TREE structure
        cnt = 0 
        iter_tree(soup.find('html'), stru_tree, '', out_f, cnt)

        GENERAL_API(out_f, pdf_opt_dir).end_line()
    else :
        print ("NOTHING CAN BE PARSED !")

    

    # divs = soup.find_all('div')
    # for i in bodies :
    #     PS.HTML_PAGE_STRU(i).div_parse() 
    ## TEXT
    #texts = soup.find_all(['p', 'span', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'blockquote', 'code', 'ul', 'ol', 'dl', 'mark', 'ins', 'del', 'sup', 'sub', 'i', 'b'])
    ## VGs
    #VGs = soup.find_all('svg')
    ## IMGs
    #IMGs = soup.find_all('img')
    ## STYLEs
    #STYLEs = soup.find_all('style')  
    ## FORM
    #forms = soup.find_all('form')
    ## TABLE
    #tables = soup.find_all('table')
    #styles = soup.find_all('style')


    #if len(VGs) != 0 or len(IMGs) != 0 or len(STYLEs) != 0 or len(texts) != 0 or len(forms) != 0 or len(tables) != 0 or len(styles) != 0 :
    #    os.makedirs(output_dir + "/" + file_name)
    #    out_f = open( output_dir + "/" + file_name + "/html_to_PDF_text_template.cpp", "a")
    #    # Write General bein API lines in template
    #    GENERAL_API(out_f, argv[2]).begin_line()
    #   
    #    # TEXT 
    #    if len(texts) != 0 :
    #        maga_info = TX.HTML_TEXT_STRU(texts).text_parse()
    #        if len(maga_info) > 0 :
    #            TX.PDF_TEXT_API_MAP(maga_info, out_f).api_order()
    #    else :
    #        print(file_name + " does not contain TEXTs")   
    #    
    #    # VG  
    #    if len(VGs) != 0 :
    #        maga_info_vg = VG.HTML_VGs_STRU(VGs).VG_parse()
    #        if len(maga_info_vg) > 0 :
    #            VG.PDF_VGs_API_MAP(maga_info_vg, out_f).api_order()
    #    else :
    #        print(file_name + " does not contain VG")
    #   
    #    # IMG 
    #    if len(IMGs) != 0:
    #        maga_info_img = VG.HTML_IMGs_STRU(IMGs).IMG_parse()
    #        if len(maga_info_img) > 0 :
    #            VG.PDF_IMGs_API_MAP(maga_info_img, out_f).api_order()
    #    else :
    #        print(file_name + " does not contain IMG")
    #    # STYLE
    #    if len(STYLEs) != 0:
    #        maga_info_style = VG.HTML_STYLEs_STRU(STYLEs).STYLE_parse()
    #        if len(maga_info_style) > 0 :
    #             VG.PDF_STYLEs_API_MAP(maga_info_style, out_f).api_order()
    #    else :
    #        print(file_name + " does not contain STYLEs")   
    #    # FORM
    #    if len(forms) != 0 :
    #        maga_info = FM.HTML_FORM_STRU(forms).form_parse()
    #        if len(maga_info) > 0 :
    #            FM.PDF_FORM_API_MAP(maga_info, out_f).api_order()
    #    else :
    #        print(file_name + " does not contain form")
    #    # TABLE
    #    if len(tables) > 0 :
    #        maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
    #        if len(maga_info) > 0 and len(maga_info) < 10:
    #            # if file contains table, map its structure to PDF API
    #            TAB.PDF_TAB_API_MAP(maga_info, out_f).api_order()
    #        else :
    #            print(file_name + " does not contain table")
    #    # write general end lines in template
    #    GENERAL_API(out_f, pdf_opt_dir).end_line()
       
 
        

if __name__ == "__main__" :
    main(sys.argv[1:])
