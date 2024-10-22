from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase

class PDF_TEXT_STRU() :
    def __init__(self, detect) :
        # pass in soup' forms
        self.detect = detect
        # {textID : {Attribute : {value}}}
        self.maga_info = dict()
       # # attributes of each text
       # self.text_string = dict()
    # attributes : 
    def normal_attributes(self, text_id, tag, dice) :
       # if text.has_attr('style') :
        if dice == 0 :
            self.maga_info[text_id][tag].update({'bgc' : 1})
        if dice == 1 :
            self.maga_info[text_id][tag].update({'color' : 1})
        if dice == 2 :
            self.maga_info[text_id][tag].update({'font-family':1})
        if dice == 3 :
            self.maga_info[text_id][tag].update({'font-size':1})
        if dice == 4 :
            self.maga_info[text_id][tag].update({'text-align':1})
        if dice == 5 :
            self.maga_info[text_id][tag].update({'font-weight':1})
        if dice == 6 :
            self.maga_info[text_id][tag].update({'text-indent':1})
        if dice == 7 :
            self.maga_info[text_id][tag].update({'text-transform':1})
        if dice == 8 :
            self.maga_info[text_id][tag].update({'display':1})
        if dice == 9 :
            self.maga_info[text_id][tag].update({'margin-top':1})
        if dice == 10 :
            self.maga_info[text_id][tag].update({'margin-bottom':1})
        if dice == 11 :
            self.maga_info[text_id][tag].update({'margin-left':1})
        if dice == 12 :
            self.maga_info[text_id][tag].update({'margin-right':1})
        if dice == 13 :
            self.maga_info[text_id][tag].update({'font-style':1})
        if dice == 14 :
            self.maga_info[text_id][tag].update({'padding':1})
        if dice == 15 :
            self.maga_info[text_id][tag].update({'padding-left':1})
        if dice == 16 :
            self.maga_info[text_id][tag].update({'padding-right':1})
        if dice == 17 :
            self.maga_info[text_id][tag].update({'padding-top':1})
        if dice == 18 :
            self.maga_info[text_id][tag].update({'padding-bottom':1})
        if dice == 19 :
            self.maga_info[text_id][tag].update({'line-height':1})
        if dice == 20 :
            self.maga_info[text_id][tag].update({'text-decoration':1})
        if dice == 21 :
            self.maga_info[text_id][tag].update({'vertical-align':1})
        if dice ==22 :
            self.maga_info[text_id][tag].update({'horizontal-align':1})
        if dice == 23 :
            self.maga_info[text_id][tag].update({'list-style-type':1})

    # TAG 0 : <p>   
    def p_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<p>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<p>', dice)
    # TAG 1 : <span>
    def span_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<span>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<span>', dice)
    # TAG 2 : <h?>
    def h_text(self, text, text_id, dice, h_rand) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<h'+str(h_rand)+'>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<h'+str(h_rand)+'>', dice)
    # TAG 3 : <strong>
    def strong_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<strong>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<strong>', dice)
    # TAG 4 : <em>
    def em_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<em>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<em>', dice)
    # TAG 5 : <blockquote>
    def blockquote_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<blockquote>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<blockquote>', dice)
    # TAG 6 : <code>
    def code_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<code>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<code>', dice)
    # TAG 7 : <mark>
    def mark_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<mark>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<mark>', dice)
    # TAG 8 : <ins>
    def ins_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<ins>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<ins>', dice)
    # TAG 9 : <del>
    def del_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<del>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<del>', dice)
    # TAG 10 : <sup>
    def sup_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<sup>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<sup>', dice)
    # TAG 11 : <sub>
    def sub_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<sub>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<sub>', dice)
    # TAG 12 : <i>
    def i_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<i>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<i>', dice)
    # TAG 13 : <b>
    def b_text(self, text, text_id, dice) :
        text_len = len(text.encode('utf-8'))
        self.maga_info[text_id] = {'<b>':{'text_len':text_len}}
        self.normal_attributes(text_id, '<b>', dice)
    # TAG 14 : <ul>
    def ul_text(self, text, text_id, dice) :
        self.maga_info[text_id] = {'<ul>':{}}
        for i in range(0, len(text)) :
            text_len = len(text[i].encode('utf-8'))
            self.maga_info[text_id]['<ul>'].update({'<li>'+str(i):{'text_len':text_len}})
        self.normal_attributes(text_id, '<ul>', dice)
    # TAG 15 : <ol>
    def ol_text(self, text, text_id, dice) :
        self.maga_info[text_id] = {'<ol>':{}}
        for i in range(0, len(text)) :
            text_len = len(text[i].encode('utf-8'))
            self.maga_info[text_id]['<ol>'].update({'<li>'+str(i):{'text_len':text_len}})
        self.normal_attributes(text_id, '<ol>', dice)
    # TAG 16 : <dl>
    def dl_text(self, text, text_id, dice) :
        self.maga_info[text_id] = {'<dl>':{}}
        for i in range(0, len(text), 2) :
            text_len = len(text[i].encode('utf-8'))
            self.maga_info[text_id]['<dl>'].update({'<dt>'+str(i):{'text_len':text_len}})
        for j in range(1, len(text), 2) :
            text_len = len(text[j].encode('utf-8'))
            self.maga_info[text_id]['<dl>'].update({'<dd>'+str(j):{'text_len':text_len}})
        self.normal_attributes(text_id, '<dl>', dice)

    def rand_dice(self, lo, up) : 
        dice_rs = random.randint(lo,up)
        return dice_rs

    def text_parse(self) :
        self.maga_info[0] = dict()
        style_rand = self.rand_dice(0, 23)
        tag_rand = self.rand_dice(0, 13)
        outline_rand = self.rand_dice(14, 16)
        h_rand = self.rand_dice(1,6)
        if isinstance(self.detect, list) :
            if outline_rand == 14 :
                self.ul_text(self.detect, 0, style_rand)
            elif outline_rand == 15 :
                self.ol_text(self.detect, 0, style_rand)
            elif outline_rand == 16 :
                self.dl_text(self.detect, 0, style_rand)
        else :
            if tag_rand == 0 :
                self.p_text(self.detect, 0, style_rand)
            elif tag_rand == 1 :
                self.span_text(self.detect, 0, style_rand)
            elif tag_rand == 2 :
                self.h_text(self.detect, 0, style_rand, h_rand)
            elif tag_rand == 3 :
                self.strong_text(self.detect, 0, style_rand)
            elif tag_rand == 4 :
                self.em_text(self.detect, 0, style_rand)
            elif tag_rand == 5 : 
                self.blockquote_text(self.detect, 0, style_rand)
            elif tag_rand == 6 : 
                self.code_text(self.detect, 0, style_rand)
            elif tag_rand == 10 : 
                self.mark_text(self.detect, 0, style_rand) 
            elif tag_rand == 11 :
                self.ins_text(self.detect, 0, style_rand)
            elif tag_rand == 12 :
                self.del_text(self.detect, 0, style_rand)
            elif tag_rand == 13 :
                self.sup_text(self.detect, 0, style_rand)
            elif tag_rand == 14 :
                self.sub_text(self.detect, 0, style_rand)
            elif tag_rand == 15 :
                self.i_text(self.detect, 0, style_rand)
            elif tag_rand == 16 : 
                self.b_text(self.detect, 0, style_rand)
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
            self.adding_all_fonts(text_id)
            self.set_text_mode(text_id)
            for tag in self.maga_info[text_id] :
                if tag == '<p>' :
                    self.set_text_size(text_id,"0")
                    self.style_checking(text_id, '<p>', self.maga_info[text_id]['<p>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<p>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<span>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<span>',self.maga_info[text_id]['<span>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<span>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<h1>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<h1>', self.maga_info[text_id]['<h1>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<h1>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<h2>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<h2>', self.maga_info[text_id]['<h2>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<h2>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<h3>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<h3>', self.maga_info[text_id]['<h3>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<h3>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<h4>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<h4>', self.maga_info[text_id]['<h4>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<h4>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<h5>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<h5>', self.maga_info[text_id]['<h5>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<h5>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<h6>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<h6>', self.maga_info[text_id]['<h6>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<h6>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<strong>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<strong>', self.maga_info[text_id]['<strong>']['text_len'], "0")
                    self.draw_html_text(self.maga_info[text_id]['<strong>']['text_len'],text_id,"0")
                    self.set_html_bold_font(text_id,"0")
                    self.append_space(text_id,"0")
                    self.set_text_char_spacing(text_id,"0")
                elif tag == '<em>' :
                    self.set_text_size(text_id,"0")
                    self.style_checking(text_id, '<em>', self.maga_info[text_id]['<em>']['text_len'], "0")
                    self.draw_html_text(self.maga_info[text_id]['<em>']['text_len'], text_id,"0")
                    self.set_html_italic_font(text_id,"0")
                    self.append_space(text_id,"0")
                    self.set_text_char_spacing(text_id,"0")
                elif tag == '<blockquote>' :
                    self.set_text_size(text_id,"0")
                    self.style_checking(text_id, '<blockquote>', self.maga_info[text_id]['<blockquote>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<blockquote>']['text_len'], text_id,"0")
                    self.append_space(text_id,"0")
                    self.set_text_char_spacing(text_id,"0")
                elif tag == '<code>' :
                    self.set_text_size(text_id,"0")
                    self.style_checking(text_id, '<code>', self.maga_info[text_id]['<code>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<code>']['text_len'], text_id, "0")
                    self.append_space(text_id,"0")
                    self.set_text_char_spacing(text_id,"0")
                elif tag == '<ul>' :
                    self.set_text_size(text_id,"0")
                    for li_tag in self.maga_info[text_id]['<ul>'] :
                        if li_tag[0:4] == '<li>' :
                            self.style_checking(text_id, '<ul>', self.maga_info[text_id]['<ul>'][li_tag]['text_len'], li_tag)
                            self.draw_text(self.maga_info[text_id]['<ul>'][li_tag]['text_len'], str(text_id), li_tag)
                            self.append_space(str(text_id), li_tag)
                            self.set_text_char_spacing(str(text_id), li_tag)
                elif tag == '<ol>' :
                    self.set_text_size(text_id, "0")
                    for li_tag in self.maga_info[text_id]['<ol>'] :
                        if li_tag[0:4] == '<li>' :
                            self.style_checking(text_id, '<ol>', self.maga_info[text_id]['<ol>'][li_tag]['text_len'], li_tag)
                            self.draw_text(self.maga_info[text_id]['<ol>'][li_tag]['text_len'], str(text_id), li_tag)
                            self.append_space(str(text_id), li_tag)
                            self.set_text_char_spacing(str(text_id), li_tag)
                elif tag == '<dl>' :
                    self.set_text_size(text_id, "0")
                    for li_tag in self.maga_info[text_id]['<dl>'] :
                        if li_tag[0:4] == '<dt>' :
                            self.style_checking(text_id, '<dl>', self.maga_info[text_id]['<dl>'][li_tag]['text_len'], li_tag)
                            self.draw_text(self.maga_info[text_id]['<dl>'][li_tag]['text_len'], str(text_id),li_tag)
                            self.append_space(str(text_id), li_tag)
                            self.set_text_char_spacing(str(text_id), li_tag)
                        if li_tag[0:4] == '<dd>' :
                            self.style_checking(text_id, '<dl>', self.maga_info[text_id]['<dl>'][li_tag]['text_len'], li_tag)
                            self.draw_text(self.maga_info[text_id]['<dl>'][li_tag]['text_len'], str(text_id), li_tag)
                            self.append_space(str(text_id), li_tag)
                            self.set_text_char_spacing(str(text_id), li_tag)
                elif tag == '<mark>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<mark>', self.maga_info[text_id]['<mark>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<mark>']['text_len'], text_id, "0")
                    self.append_space(text_id,"0" )
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<ins>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<ins>', self.maga_info[text_id]['<ins>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<ins>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<del>' :
                    self.set_text_size(text_id, "0")
                    self.set_text_underline(text_id, "0")
                    self.style_checking(text_id, '<del>', self.maga_info[text_id]['<del>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<del>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<sup>' :
                    self.set_text_size(text_id, "0")
                    self.set_text_rise_sup(text_id, "0")
                    self.style_checking(text_id, '<sup>', self.maga_info[text_id]['<sup>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<sup>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<sub>' :
                    self.set_text_size(text_id, "0")
                    self.set_text_rise_sub(text_id, "0")
                    self.style_checking(text_id, '<sub>', self.maga_info[text_id]['<sub>']['text_len'], "0")
                    self.draw_text(self.maga_info[text_id]['<sub>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<i>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<i>', self.maga_info[text_id]['<i>']['text_len'], "0")
                    self.set_html_italic_font(text_id, "0")
                    self.draw_text(self.maga_info[text_id]['<i>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")
                elif tag == '<b>' :
                    self.set_text_size(text_id, "0")
                    self.style_checking(text_id, '<b>', self.maga_info[text_id]['<b>']['text_len'], "0")
                    self.set_html_bold_font(text_id, "0")
                    self.draw_html_text(self.maga_info[text_id]['<b>']['text_len'], text_id, "0")
                    self.append_space(text_id, "0")
                    self.set_text_char_spacing(text_id, "0")

               
