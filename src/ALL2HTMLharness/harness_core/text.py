from bs4 import BeautifulSoup, NavigableString, Tag
import re
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase

class HTML_TEXT_STRU() :
    def __init__(self, texts) :
        # pass in soup' forms
        self.texts = texts
        # {textID : {Attribute : {value}}}
        self.maga_info = dict()
        # attributes of each text
        self.text_string = dict()
    # attributes : 
    def normal_attributes(self, text, text_id, tag) :
        if text.has_attr('style') :
            if 'background-color' in text['style'] or text.has_attr('background-color') :
                self.maga_info[text_id][tag].update({'bgc' : 1})
            if 'color' in text['style'] or text.has_attr('color') :
                self.maga_info[text_id][tag].update({'color' : 1})
            if 'font-family' in text['style'] or text.has_attr('font-family') :
                self.maga_info[text_id][tag].update({'font-family':1})
            if 'font-size' in text['style'] or text.has_attr('font-size') :
                self.maga_info[text_id][tag].update({'font-size':1})
            if 'text-align' in text['style'] or text.has_attr('text-align') :
                self.maga_info[text_id][tag].update({'text-align':1})
            if 'font-weight' in text['style'] or text.has_attr('font-weight') :
                self.maga_info[text_id][tag].update({'font-weight':1})
            if 'text-indent' in text['style'] or text.has_attr('text-indent') :
                self.maga_info[text_id][tag].update({'text-indent':1})
            if 'text-transform' in text['style'] or text.has_attr('text-transform') :
                self.maga_info[text_id][tag].update({'text-transform':1})
            if 'display' in text['style'] or text.has_attr('display') :
                self.maga_info[text_id][tag].update({'display':1})
            if 'margin-top' in text['style'] or text.has_attr('margin-top') :
                self.maga_info[text_id][tag].update({'margin-top':1})
            if 'margin-bottom' in text['style'] or text.has_attr('margin-bottom') :
                self.maga_info[text_id][tag].update({'margin-bottom':1})
            if 'margin-left' in text['style'] or text.has_attr('margin-left') :
                self.maga_info[text_id][tag].update({'margin-left':1})
            if 'margin-right' in text['style'] or text.has_attr('margin-right') :
                self.maga_info[text_id][tag].update({'margin-right':1})
            if 'font-style' in text['style'] or text.has_attr('font-style') :
                self.maga_info[text_id][tag].update({'font-style':1})
            if 'padding' in text['style'] or text.has_attr('padding') :
                self.maga_info[text_id][tag].update({'padding':1})
            if 'padding-left' in text['style'] or text.has_attr('padding-left') :
                self.maga_info[text_id][tag].update({'padding-left':1})
            if 'padding-right' in text['style'] or text.has_attr('padding-right') :
                self.maga_info[text_id][tag].update({'padding-right':1})
            if 'padding-top' in text['style'] or text.has_attr('padding-top') :
                self.maga_info[text_id][tag].update({'padding-top':1})
            if 'padding-bottom' in text['style'] or text.has_attr('padding-bottom') :
                self.maga_info[text_id][tag].update({'padding-bottom':1})
            if 'line-height' in text['style'] or text.has_attr('line-height') :
                self.maga_info[text_id][tag].update({'line-height':1})
            if 'text-decoration' in text['style'] or text.has_attr('text-decoration') :
                self.maga_info[text_id][tag].update({'text-decoration':1})
            if 'vertical-align' in text['style'] or text.has_attr('vertical-align') :
                self.maga_info[text_id][tag].update({'vertical-align':1})
            if 'horizontal-align' in text['style'] or text.has_attr('horizontal-align') :
                self.maga_info[text_id][tag].update({'horizontal-align':1})
            if 'list-style-type' in text['style'] or text.has_attr('list-style-type') :
                self.maga_info[text_id][tag].update({'list-style-type':1})

    # TAG : <p>   
    def p_text(self, text, text_id) :
        text_len = len(str(text)[4:])
        self.maga_info[text_id] = {'<p>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<p>')
    # TAG : <span>
    def span_text(self, text, text_id) :
        text_len = len(str(text)[6:])
        self.maga_info[text_id] = {'<span>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<span>')
    # TAG : <h?>
    def h_text(self, text, text_id) :
        text_len = len(str(text)[4:])
        self.maga_info[text_id] = {str(text)[0:4]:{'text_len':text_len}}
        self.normal_attributes(text, text_id, str(text)[0:4])
    # TAG : <strong>
    def strong_text(self, text, text_id) :
        text_len = len(str(text)[9:])
        self.maga_info[text_id] = {'<strong>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<strong>')
    # TAG : <em>
    def em_text(self, text, text_id) :
        text_len = len(str(text)[5:])
        self.maga_info[text_id] = {'<em>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<em>')
    # TAG : <blockquote>
    def blockquote_text(self, text, text_id) :
        text_len = len(str(text)[12:])
        self.maga_info[text_id] = {'<blockquote>':{'text_len':text_len}}
        if text.has_attr('cite') :
            self.maga_info[text_id]['<blockquote>'].update({'cite':text['cite']})
        self.normal_attributes(text, text_id, '<blockquote>')
    # TAG : <code>
    def code_text(self, text, text_id) :
        text_len = len(str(text)[12:])
        self.maga_info[text_id] = {'<code>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<code>')
    # TAG : <ul>
    def ul_text(self, text, text_id) :
        self.maga_info[text_id] = {'<ul>':{}}
        for i in range(0, len(text.find_all('li'))) :
            text_len = len(str(text.find_all('li')[i])[4:])
            self.maga_info[text_id]['<ul>'].update({'<li>'+str(i):{'text_len':text_len}})
        self.normal_attributes(text, text_id, '<ul>')
    # TAG : <ol>
    def ol_text(self, text, text_id) :
        self.maga_info[text_id] = {'<ol>':{}}
        for i in range(0, len(text.find_all('li'))) :
            text_len = len(str(text.find_all('li')[i])[4:])
            self.maga_info[text_id]['<ol>'].update({'<li>'+str(i):{'text_len':text_len}})
        self.normal_attributes(text, text_id, '<ol>')
    # TAG : <dl>
    def dl_text(self, text, text_id) :
        self.maga_info[text_id] = {'<dl>':{}}
        for i in range(0, len(text.find_all('dt'))) :
            text_len = len(str(text.find_all('dt')[i]))
            self.maga_info[text_id]['<dl>'].update({'<dt>'+str(i):{'text_len':text_len}})
        for j in range(0, len(text.find_all('dd'))) :
            text_len = len(str(text.find_all('dd')[j]))
            self.maga_info[text_id]['<dl>'].update({'<dd>'+str(j):{'text_len':text_len}})
        self.normal_attributes(text, text_id, '<dl>')
    # TAG : <mark>
    def mark_text(self, text, text_id) :
        text_len = len(str(text)[6:])
        self.maga_info[text_id] = {'<mark>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<mark>')
    # TAG : <ins>
    def ins_text(self, text, text_id) :
        text_len = len(str(text)[5:])
        self.maga_info[text_id] = {'<ins>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<ins>')
    # TAG : <del>
    def del_text(self, text, text_id) :
        text_len = len(str(text)[5:])
        self.maga_info[text_id] = {'<del>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<del>')
    # TAG : <sup>
    def sup_text(self, text, text_id) :
        text_len = len(str(text)[5:])
        self.maga_info[text_id] = {'<sup>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<sup>')
    # TAG : <sub>
    def sub_text(self, text, text_id) :
        text_len = len(str(text)[5:])
        self.maga_info[text_id] = {'<sub>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<sub>')
    # TAG : <i>
    def i_text(self, text, text_id) :
        text_len = len(str(text)[3:])
        self.maga_info[text_id] = {'<i>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<i>')
    # TAG : <b>
    def b_text(self, text, text_id) :
        text_len = len(str(text)[3:])
        self.maga_info[text_id] = {'<b>':{'text_len':text_len}}
        self.normal_attributes(text, text_id, '<b>')

    def text_parse(self) :
       # how many texts in file
       num_text = len(self.texts)
       if isinstance(self.texts, Tag) :
           # update maga_info with textID
            self.maga_info[0] = dict()
            # update maga_info with text type and text content
            if str(self.texts)[0:2] == '<p' :
                self.p_text(self.texts, 0)
            elif str(self.texts)[0:5] == '<span' :
                self.span_text(self.texts, 0)
            elif str(self.texts)[0:2] == '<h' and str(self.texts)[3] == ">" :
                self.h_text(self.texts, 0)
            elif str(self.texts)[0:7] == '<strong' :
                self.strong_text(self.texts, 0)
            elif str(self.texts)[0:3] == '<em' :
                self.em_text(self.texts, 0)
            elif str(self.texts)[0:11] == '<blockquote' :
                self.blockquote_text(self.texts, 0)
            elif str(self.texts)[0:5] == '<code' :
                self.code_text(self.texts, 0)
            elif str(self.texts)[0:3] == '<ul' :
                self.ul_text(self.texts, 0)
            elif str(self.texts)[0:3] == '<ol' :
                self.ol_text(self.texts, 0)
            elif str(self.texts)[0:3] == '<dl' :
                self.dl_text(self.texts, 0)
            elif str(self.texts)[0:5] == '<mark' :
                self.mark_text(self.texts, 0)
            elif str(self.texts)[0:4] == '<ins' :
                self.ins_text(self.texts, 0)
            elif str(self.texts)[0:4] == '<del' :
                self.del_text(self.texts, 0)
            elif str(self.texts)[0:4] == '<sup' :
                self.sup_text(self.texts, 0)
            elif str(self.texts)[0:4] == '<sub' :
                self.sub_text(self.texts, 0)
            elif str(self.texts)[0:2] == '<i' :
                self.i_text(self.texts, 0)
            elif str(self.texts)[0:2] == '<b' :
                self.b_text(self.texts, 0)
       else :
           for i in range(0, num_text) :
               # update maga_info with textID
               self.maga_info[i] = dict()
               # update maga_info with text type and text content
               if str(self.texts[i])[0:2] == '<p' :
                   self.p_text(self.texts[i], i)
               elif str(self.texts[i])[0:5] == '<span' :
                   self.span_text(self.texts[i], i)
               elif str(self.texts[i])[0:2] == '<h' and str(self.texts[i])[3] == ">" :
                   self.h_text(self.texts[i], i)
               elif str(self.texts[i])[0:7] == '<strong' :
                   self.strong_text(self.texts[i], i)
               elif str(self.texts[i])[0:3] == '<em' :
                   self.em_text(self.texts[i], i)
               elif str(self.texts[i])[0:11] == '<blockquote' :
                   self.blockquote_text(self.texts[i], i)
               elif str(self.texts[i])[0:5] == '<code' :
                   self.code_text(self.texts[i], i)
               elif str(self.texts[i])[0:3] == '<ul' :
                   self.ul_text(self.texts[i], i)
               elif str(self.texts[i])[0:3] == '<ol' :
                   self.ol_text(self.texts[i], i)
               elif str(self.texts[i])[0:3] == '<dl' :
                   self.dl_text(self.texts[i], i)
               elif str(self.texts[i])[0:5] == '<mark' :
                   self.mark_text(self.texts[i], i)
               elif str(self.texts[i])[0:4] == '<ins' :
                   self.ins_text(self.texts[i], i)
               elif str(self.texts[i])[0:4] == '<del' :
                   self.del_text(self.texts[i], i)
               elif str(self.texts[i])[0:4] == '<sup' :
                   self.sup_text(self.texts[i], i)
               elif str(self.texts[i])[0:4] == '<sub' :
                   self.sub_text(self.texts[i], i)
               elif str(self.texts[i])[0:2] == '<i' :
                   self.i_text(self.texts[i], i)
               elif str(self.texts[i])[0:2] == '<b' :
                   self.b_text(self.texts[i], i)
       return self.maga_info


class PDF_TEXT_API_MAP() :
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

    def rand_str_gen(self,text_len) :
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

    def draw_text(self, text_len, text_id, li_tag) :
        # API : DrawText(XPos, YPos, Text)
        DrawText_arg_1 = "DrawText_XPos" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        DrawText_arg_2 = "DrawText_YPos" + str(text_id) + str(self.tag_cnt) +  li_tag.replace('<','').replace('>','')
        DrawText_constrain_1 = "if (" + DrawText_arg_1  + " <0.001 || " + DrawText_arg_1  + " > 800.001 ){ \n"
        DrawText_constrain_2 = "if (" + DrawText_arg_2  + " <0.001 || " + DrawText_arg_2  + " > 800.001 ){ \n"
        self.arg_val(DrawText_arg_1, "double", DrawText_constrain_1, "800.001", "0.001")
        self.arg_val(DrawText_arg_2, "double", DrawText_constrain_2, "800.001", "0.001")
        content = self.rand_str_gen(text_len)
        self.template.write("FQL->DrawText(" + DrawText_arg_1  + ", " + DrawText_arg_2  +  ", L\""+content+"\"); \n")

    def draw_html_text(self, text_len, text_id, li_tag) :
        # API : DrawHTMLText(DrawHTMLTextBox(Left, Top, Width, Height, HTMLText))
        DrawHTMLText_arg_1 = "DrawHTMLText_Left" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        DrawHTMLText_arg_2 = "DrawHTMLText_Top" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        DrawHTMLText_arg_3 = "DrawHTMLText_Width" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        DrawHTMLText_arg_4 = "DrawHTMLText_Height" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        DrawHTMLText_constrain_1 = "if (" + DrawHTMLText_arg_1 + " < 0.001 || " + DrawHTMLText_arg_1 + " > 800.001 ) { \n"
        DrawHTMLText_constrain_2 = "if (" + DrawHTMLText_arg_1 + " < 0.001 || " + DrawHTMLText_arg_2 + " > 800.001 ) { \n"
        DrawHTMLText_constrain_3 = "if (" + DrawHTMLText_arg_1 + " < 0.001 || " + DrawHTMLText_arg_3 + " > 200.001 ) { \n"
        DrawHTMLText_constrain_4 = "if (" + DrawHTMLText_arg_1 + " < 0.001 || " + DrawHTMLText_arg_4 + " > 200.001 ) { \n"
        self.arg_val(DrawHTMLText_arg_1, "double", DrawHTMLText_constrain_1, "800.001", "0.001")
        self.arg_val(DrawHTMLText_arg_2, "double", DrawHTMLText_constrain_2, "800.001", "0.001")
        self.arg_val(DrawHTMLText_arg_3, "double", DrawHTMLText_constrain_3, "200.001", "0.001")
        self.arg_val(DrawHTMLText_arg_4, "double", DrawHTMLText_constrain_4, "200.001", "0.001")

        content = self.rand_str_gen(text_len)
        self.template.write("int textID"+str(text_id)+str(self.tag_cnt) + "= FQL->DrawHTMLText(150, 150, 150, L\""+content+"\"); \n")
    def set_html_bold_font(self, text_id, li_tag) :
        # API SetHTMLBoldFont(FontSet, FontID) -> fontID returned by AddXXXFont
        self.template.write("FQL->SetHTMLBoldFont(L\"Default\", FontID_CJK" +str(text_id) + str(self.tag_cnt) + "); \n")
        self.template.write("FQL->SetHTMLBoldFont(L\"Default\", FontID_Standard" +str(text_id) + str(self.tag_cnt) + "); \n")
    def set_html_italic_font(self, text_id, li_tag) :
        # API SetHTMLItalicFont(FontSet, FontID) -> fontID returned by AddXXXFont
        self.template.write("FQL->SetHTMLItalicFont(L\"Default\", FontID_CJK"+str(text_id)+str(self.tag_cnt) + "); \n")
        self.template.write("FQL->SetHTMLItalicFont(L\"Default\", FontID_Standard"+str(text_id)+str(self.tag_cnt) + "); \n")
    def set_text_size(self, text_id, li_tag) :
        # API SetTextSize(TextSize)
        SetTextSize_arg_1 = "SetTextSize_TextSize" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextSize_constrain_1 = "if(" + SetTextSize_arg_1 + " < 0.001 || " + SetTextSize_arg_1  + " > 200.001 ) { \n"
        self.arg_val(SetTextSize_arg_1, "double", SetTextSize_constrain_1, "200.001", "0.001")
        self.template.write("FQL->SetTextSize(" + SetTextSize_arg_1 + "); \n")
    def set_text_rise_sup(self, text_id, li_tag) :
        # API SetTextRise(Rise0-)
        SetTextRise_arg_1 = "SetTextRise_Rise" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextRise_constrain_1 = "if(" + SetTextRise_arg_1 + " < 0.001 || " + SetTextRise_arg_1  + " > 200.001 ){ \n"
        self.arg_val(SetTextRise_arg_1, "double", SetTextRise_constrain_1, "200.001", "0.001")
        self.template.write("FQL->SetTextRise(" + SetTextRise_arg_1  + "); \n")
    def set_text_rise_sub(self, text_id, li_tag) :
        # API SetTExtRise(Rise0+)
        SetTextRise_arg_1 = "SetTextRise_Rise" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextRise_constrain_1 = "if(" + SetTextRise_arg_1  + " > 0.001 || " + SetTextRise_arg_1 + " < -200.001 ){ \n"
        self.arg_val(SetTextRise_arg_1, "double", SetTextRise_constrain_1, "0.001", "-200.001")
        self.template.write("FQL->SetTextRise(" + SetTextRise_arg_1 + "); \n")
    def set_text_underline(self,text_id, li_tag) :
        # API SetTextUnderline(Underline(0-4))
        SetTextUnderline_arg_1 = "SetTextUnderline_Underline" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderline_constrain_1 = "if(" + SetTextUnderline_arg_1 + " < 0 || " + SetTextUnderline_arg_1 + " > 4) { \n"
        self.arg_val(SetTextUnderline_arg_1, "int", SetTextUnderline_constrain_1, "4", "0")
        self.template.write("FQL->SetTextUnderline(" + SetTextUnderline_arg_1 + "); \n")
        # API SetTextUnderlineDash(DashOn(double), DashOff(double))
        SetTextUnderlineDash_arg_1 = "SetTextUnderlineDash_DashOn" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineDash_arg_2 = "SetTextUnderlineDash_DashOff" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineDash_constrain_1 = "if(" + SetTextUnderlineDash_arg_1  + " < 0.001 || " + SetTextUnderlineDash_arg_1  + " > 200.001) { \n"
        SetTextUnderlineDash_constrain_2 = "if(" + SetTextUnderlineDash_arg_2  + " < 0.001 || " + SetTextUnderlineDash_arg_2  + " > 200.001) { \n"
        self.arg_val(SetTextUnderlineDash_arg_1, "double", SetTextUnderlineDash_constrain_1, "200.001", "0.001")
        self.arg_val(SetTextUnderlineDash_arg_2, "double", SetTextUnderlineDash_constrain_2, "200.001", "0.001")
        self.template.write("FQL->SetTextUnderlineDash(" + SetTextUnderlineDash_arg_1 + ", " + SetTextUnderlineDash_arg_2 + "); \n")
        # API SetTextUnderlineDistance(UnderlineDistance(double))
        SetTextUnderlineDistance_arg_1 = "SetTextUnderlineDistance_UnderlineDistance" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineDistance_constrain_1 = "if(" + SetTextUnderlineDistance_arg_1 + " < 0.001 || " + SetTextUnderlineDistance_arg_1  + " > 200.001) { \n"
        self.arg_val(SetTextUnderlineDistance_arg_1, "double", SetTextUnderlineDistance_constrain_1, "200.001", "0.001")
        self.template.write("FQL->SetTextUnderlineDistance("+SetTextUnderlineDistance_arg_1+"); \n")
        # API SetTextUnderlineWidth(UnderlineWidth(double))
        SetTextUnderlineWidth_arg_1 = "SetTextUnderlineWidth_UnderlineWidth" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineWidth_constrain_1 = "if("+SetTextUnderlineWidth_arg_1+" < 0.001 || " + SetTextUnderlineWidth_arg_1  + " > 200.001) { \n"
        self.arg_val(SetTextUnderlineWidth_arg_1, "double", SetTextUnderlineWidth_constrain_1, "200.001", "0.001")
        self.template.write("FQL->SetTextUnderlineWidth("+SetTextUnderlineWidth_arg_1+"); \n")
        # API SetTextUnderlineColor(Red(double), Green(double), Blue(double))
        SetTextUnderlineColor_arg_1 = "SetTextUnderlineColor_Red" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineColor_arg_2 = "SetTextUnderlineColor_Green" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineColor_arg_3 = "SetTextUnderlineColor_Blue" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextUnderlineColor_constrain_1 = "if(" + SetTextUnderlineColor_arg_1 + " < 0.001 || " + SetTextUnderlineColor_arg_1 + " > 0.999) { \n"
        SetTextUnderlineColor_constrain_2 = "if(" + SetTextUnderlineColor_arg_2 + " < 0.001 || " + SetTextUnderlineColor_arg_2 + " > 0.999) { \n"
        SetTextUnderlineColor_constrain_3 = "if(" + SetTextUnderlineColor_arg_3 + " < 0.001 || " + SetTextUnderlineColor_arg_3 + " > 0.999) { \n"
        self.arg_val(SetTextUnderlineColor_arg_1, "double", SetTextUnderlineColor_constrain_1, "0.999", "0.001")
        self.arg_val(SetTextUnderlineColor_arg_2, "double", SetTextUnderlineColor_constrain_2, "0.999", "0.001")
        self.arg_val(SetTextUnderlineColor_arg_3, "double", SetTextUnderlineColor_constrain_3, "0.999", "0.001")
        self.template.write("FQL->SetTextUnderlineColor(" + SetTextUnderlineColor_arg_1  + ", " + SetTextUnderlineColor_arg_2 + ", " + SetTextUnderlineColor_arg_3 + "); \n")
    def style_checking(self, text_id, tag, text_len, li_tag):
        text_content = self.rand_str_gen(text_len)
        if 'bgc' in self.maga_info[text_id][tag].keys() :
            # API SetTextHighlight(Highlight(0-2))
            SetTextHighlight_arg_1 = "SetTextHighlight_Highlight" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextHighlight_constrain_1 = "if(" + SetTextHighlight_arg_1  + " < 0 || " + SetTextHighlight_arg_1  + " > 2) { \n"
            self.arg_val(SetTextHighlight_arg_1, "int", SetTextHighlight_constrain_1, "2", "0")
            self.template.write("FQL->SetTextHighlight(" + SetTextHighlight_arg_1 + "); \n")
            # API SetTextHighlightColor(Red, Green, Blue)
            SetTextHighlightColor_arg_1 = "SetTextHighlight_Red" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextHighlightColor_arg_2 = "SetTextHighlight_Green" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextHighlightColor_arg_3 = "SetTextHighlight_Blue" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextHighlightColor_constrain_1 = "if(" + SetTextHighlightColor_arg_1  + "< 0.001 || " + SetTextHighlightColor_arg_1 + " > 0.999){ \n"
            SetTextHighlightColor_constrain_2 = "if(" + SetTextHighlightColor_arg_2  + "< 0.001 || " + SetTextHighlightColor_arg_2 + " > 0.999){ \n"
            SetTextHighlightColor_constrain_3 = "if(" + SetTextHighlightColor_arg_3  + "< 0.001 || " + SetTextHighlightColor_arg_3 + " > 0.999){ \n"
            self.arg_val(SetTextHighlightColor_arg_1, "double", SetTextHighlightColor_constrain_1, "0.999", "0.001")
            self.arg_val(SetTextHighlightColor_arg_2, "double", SetTextHighlightColor_constrain_2, "0.999", "0.001")
            self.arg_val(SetTextHighlightColor_arg_3, "double", SetTextHighlightColor_constrain_3, "0.999", "0.001")
            self.template.write("FQL->SetTextHighlightColor("+SetTextHighlightColor_arg_1+","+SetTextHighlightColor_arg_2+","+SetTextHighlightColor_arg_3+"); \n")
        if 'color' in self.maga_info[text_id][tag].keys() :
            # API SetTextColor(Red, Green, Blue)
            SetTextColor_arg_1 = "SetTextColor_Red" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextColor_arg_2 = "SetTextColor_Green" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextColor_arg_3 = "SetTextColor_Blue" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextColor_constrain_1 = "if(" + SetTextColor_arg_1 + "< 0.001 || " + SetTextColor_arg_1 + " > 0.999 ){ \n"
            SetTextColor_constrain_2 = "if(" + SetTextColor_arg_2 + "< 0.001 || " + SetTextColor_arg_2 + " > 0.999 ){ \n"
            SetTextColor_constrain_3 = "if(" + SetTextColor_arg_3 + "< 0.001 || " + SetTextColor_arg_3 + " > 0.999 ){ \n"
            self.arg_val(SetTextColor_arg_1, "double", SetTextColor_constrain_1,"0.999", "0.001")
            self.arg_val(SetTextColor_arg_2, "double", SetTextColor_constrain_2,"0.999", "0.001")
            self.arg_val(SetTextColor_arg_3, "double", SetTextColor_constrain_3,"0.999", "0.001")
            self.template.write("FQL->SetTextColor("+SetTextColor_arg_1+","+SetTextColor_arg_2+","+SetTextColor_arg_3+"); \n")
        if 'text-align' in self.maga_info[text_id][tag].keys() :
            # API SetTextAlign(TextAlign(0-5))
            # (0 - 5)
            SetTextAlign_arg_1 = "SetTextAlign_TextAligh" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            SetTextAlign_constrain_1 = "if(" + SetTextAlign_arg_1 + " < 0 || " + SetTextAlign_arg_1 + ">5 ) { \n"
            self.arg_val(SetTextAlign_arg_1, "int", SetTextAlign_constrain_1, "5", "0")
            self.template.write("FQL->SetTextAlign(" + SetTextAlign_arg_1 + "); \n")
        if 'display' in self.maga_info[text_id][tag].keys() :
            # API DrawTextBox(Left, Top, Width, Height, Text, Options)
            DrawTextBox_arg_1 = "DrawTextBox_Left" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBox_arg_2 = "DrawTextBox_Top" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBox_arg_3 = "DrawTextBox_Width" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBox_arg_4 = "DrawTextBox_Height" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBox_arg_5 = "DrawTextBox_Options" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBox_constrain_1 = "if(" + DrawTextBox_arg_1 + " < 0.001 || " +  DrawTextBox_arg_1 + " > 800.001) { \n"
            DrawTextBox_constrain_2 = "if(" + DrawTextBox_arg_2 + " < 0.001 || " +  DrawTextBox_arg_1 + " > 800.001) { \n"
            DrawTextBox_constrain_3 = "if(" + DrawTextBox_arg_3 + " < 0.001 || " +  DrawTextBox_arg_1 + " > 200.001) { \n"
            DrawTextBox_constrain_4 = "if(" + DrawTextBox_arg_4 + " < 0.001 || " +  DrawTextBox_arg_1 + " > 200.001) { \n"
            DrawTextBox_constrain_5 = "if(" + DrawTextBox_arg_5 + " < 0 || " +  DrawTextBox_arg_5 + " > 5) { \n"
            self.arg_val(DrawTextBox_arg_1, "double", DrawTextBox_constrain_1, "800.001", "0.001")
            self.arg_val(DrawTextBox_arg_2, "double", DrawTextBox_constrain_2, "800.001", "0.001")
            self.arg_val(DrawTextBox_arg_3, "double", DrawTextBox_constrain_3, "200.001", "0.001")
            self.arg_val(DrawTextBox_arg_4, "double", DrawTextBox_constrain_4, "200.001", "0.001")
            self.arg_val(DrawTextBox_arg_5, "int", DrawTextBox_constrain_5, "5", "0")
            self.template.write("FQL->DrawTextBox(" + DrawTextBox_arg_1 + ", " + DrawTextBox_arg_2 + ", " + DrawTextBox_arg_3 + ", " + DrawTextBox_arg_4 + ", L\""+text_content+"\", " + DrawTextBox_arg_5 + "); \n")
        if 'text-transform' in self.maga_info[text_id][tag].keys() :
            # API DrawTextBoxMatrix(Width, Height, Text, Options, M11, M12, M21, M22, MDX, MDY)
            DrawTextBoxMatrix_arg_1 = "DrawTextBoxMatrix_Width" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_2 = "DrawTextBoxMatrix_Height" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_3 = "DrawTextBoxMatrix_Options" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_4 = "DrawTextBoxMatrix_M11" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_5 = "DrawTextBoxMatrix_M12" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_6 = "DrawTextBoxMatrix_M21" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_7 = "DrawTextBoxMatrix_M22" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_8 = "DrawTextBoxMatrix_MDX" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_arg_9 = "DrawTextBoxMatrix_MDY" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawTextBoxMatrix_constrain_1 = "if(" + DrawTextBoxMatrix_arg_1 + " < 0.001 || " + DrawTextBoxMatrix_arg_1 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_2 = "if(" + DrawTextBoxMatrix_arg_2 + " < 0.001 || " + DrawTextBoxMatrix_arg_2 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_3 = "if(" + DrawTextBoxMatrix_arg_3 + " < 0 || " + DrawTextBoxMatrix_arg_3 + "> 5 ) { \n"
            DrawTextBoxMatrix_constrain_4 = "if(" + DrawTextBoxMatrix_arg_4 + " < 0.001 || " + DrawTextBoxMatrix_arg_4 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_5 = "if(" + DrawTextBoxMatrix_arg_5 + " < 0.001 || " + DrawTextBoxMatrix_arg_5 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_6 = "if(" + DrawTextBoxMatrix_arg_6 + " < 0.001 || " + DrawTextBoxMatrix_arg_6 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_7 = "if(" + DrawTextBoxMatrix_arg_7 + " < 0.001 || " + DrawTextBoxMatrix_arg_7 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_8 = "if(" + DrawTextBoxMatrix_arg_8 + " < 0.001 || " + DrawTextBoxMatrix_arg_8 + ">200.001 ) { \n"
            DrawTextBoxMatrix_constrain_9 = "if(" + DrawTextBoxMatrix_arg_9 + " < 0.001 || " + DrawTextBoxMatrix_arg_9 + ">200.001 ) { \n"
            self.arg_val(DrawTextBoxMatrix_arg_1, "double", DrawTextBoxMatrix_constrain_1, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_2, "double", DrawTextBoxMatrix_constrain_2, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_3, "int", DrawTextBoxMatrix_constrain_3, "0", "5")
            self.arg_val(DrawTextBoxMatrix_arg_4, "double", DrawTextBoxMatrix_constrain_4, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_5, "double", DrawTextBoxMatrix_constrain_5, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_6, "double", DrawTextBoxMatrix_constrain_6, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_7, "double", DrawTextBoxMatrix_constrain_7, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_8, "double", DrawTextBoxMatrix_constrain_8, "200.001", "0.001")
            self.arg_val(DrawTextBoxMatrix_arg_9, "double", DrawTextBoxMatrix_constrain_9, "200.001", "0.001")
            self.template.write("FQL->DrawTextBoxMatrix(" + DrawTextBoxMatrix_arg_1 + ", " + DrawTextBoxMatrix_arg_2 + " , L\""+text_content+"\", " + DrawTextBoxMatrix_arg_3 + ", " + DrawTextBoxMatrix_arg_4 + "," + DrawTextBoxMatrix_arg_5 + "," + DrawTextBoxMatrix_arg_6 + "," + DrawTextBoxMatrix_arg_7 + "," + DrawTextBoxMatrix_arg_8 + ", "+DrawTextBoxMatrix_arg_9+"); \n")
        if 'padding' in self.maga_info[text_id][tag].keys() :
            # API DrawSpacedText(XPos, YPos, Spacing, Text)
            DrawSpacedText_arg_1 = "DrawSpacedText_XPos" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawSpacedText_arg_2 = "DrawSpacedText_YPos" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawSpacedText_arg_3 = "DrawSpacedText_Spacing" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawSpacedText_constrain_1 = "if(" + DrawSpacedText_arg_1 + " < 0.001 || " + DrawSpacedText_arg_1 + ">800.001 ) { \n"
            DrawSpacedText_constrain_2 = "if(" + DrawSpacedText_arg_2 + " < 0.001 || " + DrawSpacedText_arg_2 + ">800.001 ) { \n"
            DrawSpacedText_constrain_3 = "if(" + DrawSpacedText_arg_3 + " < 0.001 || " + DrawSpacedText_arg_3 + ">200.001 ) { \n"
            self.arg_val(DrawSpacedText_arg_1, "double", DrawSpacedText_constrain_1, "800.001", "0.001")
            self.arg_val(DrawSpacedText_arg_2, "double", DrawSpacedText_constrain_2, "800.001", "0.001")
            self.arg_val(DrawSpacedText_arg_3, "double", DrawSpacedText_constrain_3, "200.001", "0.001")
            self.template.write("FQL->DrawSpacedText(" + DrawSpacedText_arg_1 + ", " + DrawSpacedText_arg_2 + "," + DrawSpacedText_arg_3 + ", L\""+text_content+"\"); \n")
        if 'align-' in self.maga_info[text_id][tag].keys() :
            # API DrawWrappedText(XPos, YPos, Width, Text)
            DrawWrappedText_arg_1 = "DrawWwrappedText_XPos" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawWrappedText_arg_2 = "DrawWwrappedText_YPos" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawWrappedText_arg_3 = "DrawWwrappedText_Width" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
            DrawWrappedText_constrain_1 = "if(" + DrawWrappedText_arg_1 + "< 0.001 || " + DrawWrappedText_arg_1 + " > 800.001 ) { \n"
            DrawWrappedText_constrain_2 = "if(" + DrawWrappedText_arg_2 + "< 0.001 || " + DrawWrappedText_arg_2 + " > 800.001 ) { \n"
            DrawWrappedText_constrain_1 = "if(" + DrawWrappedText_arg_1 + "< 0.001 || " + DrawWrappedText_arg_3 + " > 200.001 ) { \n"
            self.arg_val(DrawWrappedText_arg_1, "double", DrawWrappedText_constrains_1, "800.001", "0.001")
            self.arg_val(DrawWrappedText_arg_2, "double", DrawWrappedText_constrains_2, "800.001", "0.001")
            self.arg_val(DrawWrappedText_arg_3, "double", DrawWrappedText_constrains_3, "200.001", "0.001")
            self.template.write("FQL->DrawWrappedText(" + DrawWrappedText_arg_1 + "," + DrawWrappedText_arg_2 + ", " + DrawWrappedText_arg_3 + " , L\""+text_content+"\"); \n")
    def set_text_mode(self, text_id) :
        # API SetTextMode(TextMode(0-7))
        SetTextMode_arg_1 = "SetTextMode_TextMode" + str(text_id) + str(self.tag_cnt)
        SetTextMode_constrain_1 = "if(" + SetTextMode_arg_1 + " < 0 || " + SetTextMode_arg_1 + " > 7) { \n"
        self.arg_val(SetTextMode_arg_1, "int", SetTextMode_constrain_1, "7", "0")
        self.template.write("FQL->SetTextMode(" + SetTextMode_arg_1 + "); \n")
    def append_space(self, text_id, li_tag) :
        # API AppendSpace(RelativeSpace(double))
        AppendSpace_arg_1 = "AppendSpace_RelativeSpace" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        AppendSpace_constrain_1 = "if(" + AppendSpace_arg_1 + " < 0.001 || " + AppendSpace_arg_1 + " > 200.001) { \n"
        self.arg_val(AppendSpace_arg_1, "double", AppendSpace_constrain_1, "200.001", "0.001")
        self.template.write("FQL->AppendSpace(" + AppendSpace_arg_1 + "); \n")
    def set_text_char_spacing(self, text_id, li_tag) :
        # API SetTextCharSpacing(CharSpacing)
        SetTextCharSpacing_arg_1 = "SetTextCharSpacing_CharSpacing" + str(text_id)+ str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextCharSpacing_constrain_1 = "if( " + SetTextCharSpacing_arg_1 + "< 0.001 || " + SetTextCharSpacing_arg_1 + " > 200.001 ) { \n"
        self.arg_val(SetTextCharSpacing_arg_1, "double", SetTextCharSpacing_constrain_1, "200.001", "0.001")
        self.template.write("FQL->SetTextCharSpacing(" + SetTextCharSpacing_arg_1 + "); \n")
    # Adding Fonts 
    def adding_all_fonts(self,text_id) :
        # API AddCJKFont(CJKFontID)
        AddCJKFont_arg_1 = "AddCJKFont_CJKFontID" + str(text_id) + str(self.tag_cnt)
        AddCJKFont_constrain_1 = "if(" + AddCJKFont_arg_1 + " < 1 || " + AddCJKFont_arg_1 + " > 8 ) { \n"
        self.arg_val(AddCJKFont_arg_1, "int", AddCJKFont_constrain_1, "8", "1")
        # (1 - 8)
        self.template.write("int FontID_CJK"+str(text_id)+str(self.tag_cnt) + "= FQL->AddCJKFont(" + AddCJKFont_arg_1 + "); \n")
        # API AddStandardFont(StardardFontID)
        AddStandardFont_arg_1 = "AddStandardFont_StandardFont" + str(text_id) + str(self.tag_cnt) 
        AddStandardFont_constrain_1 = "if(" + AddStandardFont_arg_1 + " < 0 || " + AddStandardFont_arg_1 + " > 13 ) { \n"
        self.arg_val(AddStandardFont_arg_1, "int", AddStandardFont_constrain_1, "13", "0")
        # (0 - 13)
        self.template.write("int FontID_Standard"+str(text_id)+str(self.tag_cnt) + " = FQL->AddStandardFont(" + AddStandardFont_arg_1 + "); \n")
    # Set Text Size
    def set_text_size(self, text_id, li_tag) :
        # API SetTextSize(TextSize)
        SetTextSize_arg_1 = "SetTextSize_TextSize" + str(text_id) + str(self.tag_cnt) + li_tag.replace('<','').replace('>','')
        SetTextSize_constrain_1 = "if(" + SetTextSize_arg_1 + "< 0.001 || " + SetTextSize_arg_1 + " > 200.001){\n"
        self.arg_val(SetTextSize_arg_1, "double", SetTextSize_constrain_1, "200.001", "0.001")
        self.template.write("FQL->SetTextSize(" + SetTextSize_arg_1 + "); \n")
    def api_order(self) :
        for text_id in self.maga_info :
            #self.adding_all_fonts(text_id)
           ## self.set_text_size(text_id
            #self.set_text_mode(text_id)
            for tag in self.maga_info[text_id] :
                self.template.write("auto container_ta" + str(text_id) + str(tag[1]) + " = root()->addWidget(std::make_unique<Wt::WContainerWidget>()); \n")
                self.template.write("Wt::WTextArea *ta" + str(text_id) + str(tag[1]) + " = \n")
                self.template.write("container_ta" + str(text_id) + str(tag[1]) + "->addNew<Wt::WTextArea>(); \n")
                self.template.write("ta" + str(text_id) + str(tag[1]) + "->setColumns(random_int(0, 10000)); \n")
                self.template.write("ta" + str(text_id) + str(tag[1]) + "->setRows(random_int(0, 10000)); \n")
                self.template.write("ta" + str(text_id) + str(tag[1]) + "->setText(random_string(500)); \n")
                self.template.write("Wt::WText *out_ta" + str(text_id) + str(tag[1]) + " = container_ta" + str(text_id) + str(tag[1]) + "->addNew<Wt::WText>(\"<p></p>\"); \n")
                self.template.write("out_ta" + str(text_id) + str(tag[1]) + "->addStyleClass(random_string(30)); \n")
                self.template.write("ta" + str(text_id) + str(tag[1]) + "->changed().connect([=] { \n")
                self.template.write("out_ta" + str(text_id) + str(tag[1]) + "->setText(\"<p>Text area changed at \" + \n")
                self.template.write("Wt::WDateTime::currentDateTime().toString() + \".</p>\"); \n")
                self.template.write("}); \n")
                self.template.write("std::move(container_ta" + str(text_id) + str(tag)[1] + "); \n")
                self.template.write("auto *container_edit"+str(text_id)+str(tag[1])+" = root()->addWidget(std::make_unique<Wt::WContainerWidget>());\n")
                self.template.write("Wt::WTextEdit *edit_edit"+str(text_id)+str(tag[1])+" = container_edit"+str(text_id)+str(tag[1])+"->addNew<Wt::WTextEdit>();\n")
                self.template.write("edit_edit"+str(text_id)+str(tag[1])+"->setHeight(random_double(-1000, 1000));\n")
                self.template.write("edit_edit"+str(text_id)+str(tag[1])+"->setText(\"<p>\"\n")
                self.template.write("\"<span style=\\\"font-family: \'courier new\', courier; font-size: medium;\\\">\"\n")
                self.template.write("\"<strong>WTextEdit</strong></span></p>\"\n")
                self.template.write("\"<p>Hey, I'm a <strong>WTextEdit</strong> and you can make me\"\n")
                self.template.write("\" <span style=\\\"text-decoration: underline;\\\"><em>rich</em></span>\"\n")
                self.template.write("\" by adding your <span style=\\\"color: #ff0000;\\\"><em>style</em>\"\n")
                self.template.write("\"</span>!</p>\"\n")
                self.template.write("\"<p>Other widgets like...</p>\"\n")
                self.template.write("\"<ul style=\\\"padding: 0px; margin: 0px 0px 10px 25px;\\\">\"\n")
                self.template.write("\"<li>WLineEdit</li>\"\n")
                self.template.write("\"<li>WTextArea</li>\"\n")
                self.template.write("\"<li>WSpinBox</li>\"\n")
                self.template.write("\"</ul>\"\n")
                self.template.write("\"<p>don't have style.</p>\");\n")
                self.template.write("Wt::WPushButton *button_edit"+str(text_id)+str(tag[1])+" = container_edit"+str(text_id)+str(tag[1])+"->addNew<Wt::WPushButton>(random_string(50));\n")
                self.template.write("button_edit"+str(text_id)+str(tag[1])+"->setMargin(random_int(-1000, 1000), static_cast<Wt::Side>(rand()%6) |static_cast<Wt::Side>(rand()%6));\n")
                self.template.write("Wt::WText *out_edit"+str(text_id)+str(tag[1])+" = container_edit"+str(text_id)+str(tag[1])+"->addNew<Wt::WText>();\n")
                self.template.write("out_edit"+str(text_id)+str(tag[1])+"->setStyleClass(\"xhtml-output\");\n")
                self.template.write("button_edit"+str(text_id)+str(tag[1])+"->clicked().connect([=] {\n")
                self.template.write("out_edit"+str(text_id)+str(tag[1])+"->setText(\"<pre>\" + Wt::Utils::htmlEncode(edit_edit"+str(text_id)+str(tag[1])+"->text()) + \"</pre>\");\n")
                self.template.write("});\n")
                self.template.write("std::move(container_edit"+str(text_id)+str(tag[1])+");\n")
###########------------------ OLD ----------------------##########
                #if tag == '<p>' :
                #    self.set_text_size(text_id,"0")
                #    self.style_checking(text_id, '<p>', self.maga_info[text_id]['<p>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<p>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<span>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<span>',self.maga_info[text_id]['<span>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<span>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<h1>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<h1>', self.maga_info[text_id]['<h1>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<h1>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<h2>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<h2>', self.maga_info[text_id]['<h2>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<h2>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<h3>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<h3>', self.maga_info[text_id]['<h3>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<h3>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<h4>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<h4>', self.maga_info[text_id]['<h4>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<h4>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<h5>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<h5>', self.maga_info[text_id]['<h5>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<h5>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<h6>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<h6>', self.maga_info[text_id]['<h6>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<h6>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<strong>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<strong>', self.maga_info[text_id]['<strong>']['text_len'], "0")
                #    self.draw_html_text(self.maga_info[text_id]['<strong>']['text_len'],text_id,"0")
                #    self.set_html_bold_font(text_id,"0")
                #    self.append_space(text_id,"0")
                #    self.set_text_char_spacing(text_id,"0")
                #elif tag == '<em>' :
                #    self.set_text_size(text_id,"0")
                #    self.style_checking(text_id, '<em>', self.maga_info[text_id]['<em>']['text_len'], "0")
                #    self.draw_html_text(self.maga_info[text_id]['<em>']['text_len'], text_id,"0")
                #    self.set_html_italic_font(text_id,"0")
                #    self.append_space(text_id,"0")
                #    self.set_text_char_spacing(text_id,"0")
                #elif tag == '<blockquote>' :
                #    self.set_text_size(text_id,"0")
                #    self.style_checking(text_id, '<blockquote>', self.maga_info[text_id]['<blockquote>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<blockquote>']['text_len'], text_id,"0")
                #    self.append_space(text_id,"0")
                #    self.set_text_char_spacing(text_id,"0")
                #elif tag == '<code>' :
                #    self.set_text_size(text_id,"0")
                #    self.style_checking(text_id, '<code>', self.maga_info[text_id]['<code>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<code>']['text_len'], text_id, "0")
                #    self.append_space(text_id,"0")
                #    self.set_text_char_spacing(text_id,"0")
                #elif tag == '<ul>' :
                #    self.set_text_size(text_id,"0")
                #    for li_tag in self.maga_info[text_id]['<ul>'] :
                #        if li_tag[0:4] == '<li>' :
                #            self.style_checking(text_id, '<ul>', self.maga_info[text_id]['<ul>'][li_tag]['text_len'], li_tag)
                #            self.draw_text(self.maga_info[text_id]['<ul>'][li_tag]['text_len'], str(text_id), li_tag)
                #            self.append_space(str(text_id), li_tag)
                #            self.set_text_char_spacing(str(text_id), li_tag)
                #elif tag == '<ol>' :
                #    self.set_text_size(text_id, "0")
                #    for li_tag in self.maga_info[text_id]['<ol>'] :
                #        if li_tag[0:4] == '<li>' :
                #            self.style_checking(text_id, '<ol>', self.maga_info[text_id]['<ol>'][li_tag]['text_len'], li_tag)
                #            self.draw_text(self.maga_info[text_id]['<ol>'][li_tag]['text_len'], str(text_id), li_tag)
                #            self.append_space(str(text_id), li_tag)
                #            self.set_text_char_spacing(str(text_id), li_tag)
                #elif tag == '<dl>' :
                #    self.set_text_size(text_id, "0")
                #    for li_tag in self.maga_info[text_id]['<dl>'] :
                #        if li_tag[0:4] == '<dt>' :
                #            self.style_checking(text_id, '<dl>', self.maga_info[text_id]['<dl>'][li_tag]['text_len'], li_tag)
                #            self.draw_text(self.maga_info[text_id]['<dl>'][li_tag]['text_len'], str(text_id),li_tag)
                #            self.append_space(str(text_id), li_tag)
                #            self.set_text_char_spacing(str(text_id), li_tag)
                #        if li_tag[0:4] == '<dd>' :
                #            self.style_checking(text_id, '<dl>', self.maga_info[text_id]['<dl>'][li_tag]['text_len'], li_tag)
                #            self.draw_text(self.maga_info[text_id]['<dl>'][li_tag]['text_len'], str(text_id), li_tag)
                #            self.append_space(str(text_id), li_tag)
                #            self.set_text_char_spacing(str(text_id), li_tag)
                #elif tag == '<mark>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<mark>', self.maga_info[text_id]['<mark>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<mark>']['text_len'], text_id, "0")
                #    self.append_space(text_id,"0" )
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<ins>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<ins>', self.maga_info[text_id]['<ins>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<ins>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<del>' :
                #    self.set_text_size(text_id, "0")
                #    self.set_text_underline(text_id, "0")
                #    self.style_checking(text_id, '<del>', self.maga_info[text_id]['<del>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<del>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<sup>' :
                #    self.set_text_size(text_id, "0")
                #    self.set_text_rise_sup(text_id, "0")
                #    self.style_checking(text_id, '<sup>', self.maga_info[text_id]['<sup>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<sup>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<sub>' :
                #    self.set_text_size(text_id, "0")
                #    self.set_text_rise_sub(text_id, "0")
                #    self.style_checking(text_id, '<sub>', self.maga_info[text_id]['<sub>']['text_len'], "0")
                #    self.draw_text(self.maga_info[text_id]['<sub>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<i>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<i>', self.maga_info[text_id]['<i>']['text_len'], "0")
                #    self.set_html_italic_font(text_id, "0")
                #    self.draw_text(self.maga_info[text_id]['<i>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")
                #elif tag == '<b>' :
                #    self.set_text_size(text_id, "0")
                #    self.style_checking(text_id, '<b>', self.maga_info[text_id]['<b>']['text_len'], "0")
                #    self.set_html_bold_font(text_id, "0")
                #    self.draw_html_text(self.maga_info[text_id]['<b>']['text_len'], text_id, "0")
                #    self.append_space(text_id, "0")
                #    self.set_text_char_spacing(text_id, "0")

               
