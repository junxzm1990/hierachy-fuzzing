import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase

from bs4 import BeautifulSoup, NavigableString, Tag


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
        print (type(self.texts), self.texts)
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
                print ("i", i)
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

    def draw_text(self, text_len, text_id) :
        content = self.rand_str_gen(text_len)
        self.template.write("int textID"+str(text_id)+str(self.tag_cnt) + "= FQL->DrawText(100, 100, L\""+content+"\"); \n")
    def draw_html_text(self, text_len, text_id) :
        content = self.rand_str_gen(text_len)
        self.template.write("int textHID"+str(text_id)+str(self.tag_cnt) + "= FQL->DrawHTMLText(150, 150, 150, L\""+content+"\"); \n")
    def set_html_bold_font(self, text_id) :
        self.template.write("FQL->SetHTMLBoldFont(L\"Default\", 2); \n")
    def set_html_italic_font(self, text_id) :
        self.template.write("FQL->SetHTMLItalicFont(L\"Default\", 3); \n")
    def set_text_size(self, text_id) :
        self.template.write("FQL->SetTextSize(5.5); \n")
    def set_text_rise_sup(self, text_id) :
        self.template.write("FQL->SetTextRise(6.6); \n")
    def set_text_rise_sub(self, text_id) :
        self.template.write("FQL->SetTextRise(-6.6); \n")
    def set_text_underline(self,text_id) :
        self.template.write("FQL->SetTextUnderline(3); \n")
        self.template.write("FQL->SetTextUnderlineDash(6, 9); \n")
        self.template.write("FQL->SetTextUnderlineDistance(3.7); \n")
        self.template.write("FQL->SetTextUnderlineWidth(1.9); \n")
        self.template.write("FQL->SetTextUnderlineColor(0.1, 0.5, 0.8); \n")
    def style_checking(self, text_id, tag, text_len):
        text_content = self.rand_str_gen(text_len)
        if 'bgc' in self.maga_info[text_id][tag].keys() :
            self.template.write("FQL->SetTextHighlight(1); \n")
            self.template.write("FQL->SetTextHighlightColor(0.2, 0.5, 0.8); \n")
        if 'color' in self.maga_info[text_id][tag].keys() :
            self.template.write("FQL->SetTextColor(0.2, 0.5, 0.8); \n")
        if 'text-align' in self.maga_info[text_id][tag].keys() :
            # (0 - 5)
            self.template.write("FQL->SetTextAlign(3); \n")
        if 'display' in self.maga_info[text_id][tag].keys() :
            self.template.write("FQL->DrawTextBox(5.5, 2.2, 3.3, 6.6, L\""+text_content+"\",3 ); \n")
        if 'text-transform' in self.maga_info[text_id][tag].keys() :
            self.template.write("FQL->DrawTextBoxMatrix(2.5,3.5, L\""+text_content+"\",1, 0.5,0.7,1.1,1.5,2.8,7.7); \n")
        if 'padding' in self.maga_info[text_id][tag].keys() :
            self.template.write("FQL->DrawSpacedText(3.9, 5.1, 0.8, L\""+text_content+"\"); \n")
        if 'align-' in self.maga_info[text_id][tag].keys() :
            self.template.write("FQL->DrawWrappedText(0.9, 8.4, 7.7, L\""+text_content+"\"); \n")
    def set_text_mode(self) :
        self.template.write("FQL->SetTextMode(3); \n")
    def append_space(self) :
        self.template.write("FQL->AppendSpace(2.68); \n")
    def set_text_char_spacing(self) :
        self.template.write("FQL->SetTextCharSpacing(5.68); \n")
    # Adding Fonts 
    def adding_all_fonts(self) :
        # (1 - 8)
        self.template.write("FQL->AddCJKFont(1); \n")
        # (0 - 13)
        self.template.write("FQL->AddStandardFont(0); \n")
    # Set Text Size
    def set_text_size(self) :
        self.template.write("FQL->SetTextSize(6.88); \n")

    def api_order(self) :
        #print(self.maga_info)
        self.adding_all_fonts()
        self.set_text_size()
        self.set_text_mode()
        for text_id in self.maga_info :
            for tag in self.maga_info[text_id] :
                if tag == '<p>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<p>', self.maga_info[text_id]['<p>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<p>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<span>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<span>',self.maga_info[text_id]['<span>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<span>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<h1>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<h1>', self.maga_info[text_id]['<h1>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<h1>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<h2>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<h2>', self.maga_info[text_id]['<h2>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<h2>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<h3>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<h3>', self.maga_info[text_id]['<h3>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<h3>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<h4>' :
                    self.set_text_size()   
                    self.style_checking(text_id, '<h4>', self.maga_info[text_id]['<h4>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<h4>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<h5>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<h5>', self.maga_info[text_id]['<h5>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<h5>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<h6>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<h6>', self.maga_info[text_id]['<h6>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<h6>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<strong>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<strong>', self.maga_info[text_id]['<strong>']['text_len'])
                    self.draw_html_text(self.maga_info[text_id]['<strong>']['text_len'],text_id)
                    self.set_html_bold_font(text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<em>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<em>', self.maga_info[text_id]['<em>']['text_len'])
                    self.draw_html_text(self.maga_info[text_id]['<em>']['text_len'], text_id)
                    self.set_html_italic_font(text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<blockquote>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<blockquote>', self.maga_info[text_id]['<blockquote>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<blockquote>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<code>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<code>', self.maga_info[text_id]['<code>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<code>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<ul>' :
                    self.set_text_size()
                    for li_tag in self.maga_info[text_id]['<ul>'] :
                        if li_tag[0:4] == '<li>' :
                            rd_str=self.rand_str_gen(5)
                            self.style_checking(text_id, '<ul>', self.maga_info[text_id]['<ul>'][li_tag]['text_len'])
                            self.draw_text(self.maga_info[text_id]['<ul>'][li_tag]['text_len'], str(text_id)+str(self.tag_cnt) + rd_str + li_tag.replace('<','').replace('>',''))
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<ol>' :
                    self.set_text_size()
                    for li_tag in self.maga_info[text_id]['<ol>'] :
                        if li_tag[0:4] == '<li>' :
                            rd_str=self.rand_str_gen(5)
                            self.style_checking(text_id, '<ol>', self.maga_info[text_id]['<ol>'][li_tag]['text_len'])
                            self.draw_text(self.maga_info[text_id]['<ol>'][li_tag]['text_len'], str(text_id)+str(self.tag_cnt) + rd_str +li_tag.replace('<','').replace('>',''))
                            self.append_space()
                            self.set_text_char_spacing()
                elif tag == '<dl>' :
                    self.set_text_size()
                    for li_tag in self.maga_info[text_id]['<dl>'] :
                        if li_tag[0:4] == '<dt>' :
                            rd_str=self.rand_str_gen(5)
                            self.style_checking(text_id, '<dl>', self.maga_info[text_id]['<dl>'][li_tag]['text_len'])
                            self.draw_text(self.maga_info[text_id]['<dl>'][li_tag]['text_len'], str(text_id)+str(self.tag_cnt) +  rd_str +li_tag.replace('<','').replace('>',''))
                            self.append_space()
                            self.set_text_char_spacing()
                        if li_tag[0:4] == '<dd>' :
                            rd_str=self.rand_str_gen(5)
                            self.style_checking(text_id, '<dl>', self.maga_info[text_id]['<dl>'][li_tag]['text_len'])
                            self.draw_text(self.maga_info[text_id]['<dl>'][li_tag]['text_len'], str(text_id)+str(self.tag_cnt) +  rd_str +li_tag.replace('<','').replace('>',''))
                            self.append_space()
                            self.set_text_char_spacing()
                elif tag == '<mark>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<mark>', self.maga_info[text_id]['<mark>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<mark>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<ins>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<ins>', self.maga_info[text_id]['<ins>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<ins>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<del>' :
                    self.set_text_size()
                    self.set_text_underline(text_id)
                    self.style_checking(text_id, '<del>', self.maga_info[text_id]['<del>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<del>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<sup>' :
                    self.set_text_size()
                    self.set_text_rise_sup(text_id)
                    self.style_checking(text_id, '<sup>', self.maga_info[text_id]['<sup>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<sup>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<sub>' :
                    self.set_text_size()
                    self.set_text_rise_sub(text_id)
                    self.style_checking(text_id, '<sub>', self.maga_info[text_id]['<sub>']['text_len'])
                    self.draw_text(self.maga_info[text_id]['<sub>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<i>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<i>', self.maga_info[text_id]['<i>']['text_len'])
                    self.set_html_italic_font(text_id)
                    self.draw_text(self.maga_info[text_id]['<i>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
                elif tag == '<b>' :
                    self.set_text_size()
                    self.style_checking(text_id, '<b>', self.maga_info[text_id]['<b>']['text_len'])
                    self.set_html_bold_font(text_id)
                    self.draw_html_text(self.maga_info[text_id]['<b>']['text_len'], text_id)
                    self.append_space()
                    self.set_text_char_spacing()
