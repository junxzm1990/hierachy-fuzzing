from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase

class HTML_FORM_STRU() : 
    def __init__(self, forms) :
        # pass in soup' forms
        self.forms = forms

        #{formID:{Attribute:{value}}}
        self.maga_info = dict()
        # attributes of each form
        self.form_type_cate = dict() # text, button, checkbox
        # ...
       
        self.form_type_ret = dict()


    def form_type(self, form, form_id) :
        # {formID : {cnt : type}}
        self.form_type_ret[form_id] = dict()
        #input_num = len(form.find_all("input"))
        cnt = 0 
        for inpt in form.find_all("input") :
            if inpt.has_attr("type") : 
                text_types = ["text", "week", "month", "url", "time", "tel", "search", "number", "file", "email", "datetime-local"]
                button_types = ["button", "submit", "reset"]
                if inpt["type"] in text_types:
                    self.form_type_ret[form_id][cnt] = "text"
                elif inpt["type"] in button_types :
                    self.form_type_ret[form_id][cnt] = "button" 
                elif inpt["type"] == "radio" :
                    self.form_type_ret[form_id][cnt] = "radio_"+str(inpt["name"])
                elif inpt["type"] == "checkbox" :
                    self.form_type_ret[form_id][cnt] = "checkbox"
            cnt += 1
        # choice form options in different tags
        for select in form.find_all("select") : 
            self.form_type_ret[form_id][cnt] = "choice_" + str(len(select.find_all("option")))
            cnt += 1 
        for datalist in form.find_all("datalist") :
            self.form_type_ret[form_id][cnt] = "choice_" + str(len(datalist.find_all("option")))
            cnt += 1
        for optgroup in form.find_all("optgroup") :
            self.form_type_ret[form_id][cnt] = "choice_" + str(len(optgroup.find_all("option")))
            cnt += 1
        for canvas in form.find_all("canvas") :
            self.form_type_ret[form_id][cnt] = "signiture"

        return self.form_type_ret

    def form_parse(self) :
        # how many forms in file 
        num_form = len(self.forms)
        # form structure
        # update maga_info with formID
        if isinstance(self.forms, Tag) :
            self.maga_info[0] = dict()
            # update each attributes
            self.form_type(self.forms, 0)
            # adding attributues to current handling form in maga_info
            self.maga_info[0] = self.form_type_ret[0]
        else :
            for i in range(0, num_form) :
                # update maga_info with formID
                self.maga_info[i] = dict()
                # update each attributes
                self.form_type(self.forms[i], i)
                # adding attributues to current handling form in maga_info
                self.maga_info[i] = self.form_type_ret[i]
        return self.maga_info

class PDF_FORM_API_MAP() : 
    def __init__(self, maga_info, template, tag_cnt) :
        self.maga_info = maga_info
        self.template = template
        self.radio_sub_group = dict()
        self.tag_cnt = tag_cnt

    # 1st Necessary --------------------------------------------- 
    def new_form(self, formID, cnt) :
        FieldType = str()
        letters = string.ascii_lowercase
        Title_rand = ''.join(random.choice(letters) for i in range(5))
        if self.maga_info[formID][cnt] == "text" :
            FieldType = "1"
        elif self.maga_info[formID][cnt] == "button" :
            FieldType = "2" 
        elif self.maga_info[formID][cnt] == "checkbox" :
            FieldType = "3" 
        elif self.maga_info[formID][cnt][0:6] == "radio_" :
            if self.maga_info[formID][cnt][6:] in self.radio_sub_group:
                self.radio_sub_group[self.maga_info[formID][cnt][6:]] += 1
            else :
                self.radio_sub_group.update({self.maga_info[formID][cnt][6:]:1})
            FieldType = "4"
        elif self.maga_info[formID][cnt][0:7] == "choice_" :
            FieldType = "5:"+self.maga_info[formID][cnt][7:]
        elif self.maga_info[formID][cnt] == "signiture" : 
            FieldType = "6"
        if len(FieldType) == 1 : 
            if FieldType != "4":
                self.template.write("int formID" + str(formID) + str(cnt) + str(self.tag_cnt)+" = FQL->NewFormField( L\""+Title_rand +"\", " + FieldType + "); \n")
        else :
            self.template.write("int formID" + str(formID) + str(cnt) + str(self.tag_cnt) + " = FQL->NewFormField( L\""+Title_rand +"\", " + FieldType[0] + "); \n")
            self.template.write("FQL-> SetFormFieldChoiceType(formID"+str(formID)+str(cnt)+ str(self.tag_cnt) + ", 4);\n")
        return FieldType
    def set_form_chk_style(self, formID, cnt) :
        self.template.write("FQL->SetFormFieldCheckStyle(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", 2, 0); \n")
    def set_form_choice_sub (self, formID, cnt, sub_cnt) :
        for i in range(0, int(sub_cnt)) : 
            letters = string.ascii_lowercase
            Title_rand = ''.join(random.choice(letters) for i in range(5))
            self.template.write("int formID" + str(formID) + str(cnt) + str(self.tag_cnt) + str(i) + "choice = FQL -> AddFormFieldChoiceSub(formID" + str(formID) + str(cnt) + str(self.tag_cnt) + ", L\""+Title_rand+"\", L\"" +Title_rand+"\"); \n")
    # 2nd Necessay -------------------------------------------
    def add_set_form_font(self, formID, cnt) :
        self.template.write("int FontID"+str(formID)+str(cnt)+str(self.tag_cnt)+"=FQL->AddStandardFont(5); \n")
        self.template.write("FQL->SetTextSize(10); \n")
        self.template.write("FQL->AddFormFont(FontID"+str(formID)+str(cnt)+str(self.tag_cnt)+"); \n")
        self.template.write("FQL->SetFormFieldFont(formID"+str(formID)+str(cnt)+str(self.tag_cnt)+", FQL->GetFormFontCount()); \n")
        self.template.write("FQL->SetFormFieldTextSize(formID"+str(formID)+str(cnt)+str(self.tag_cnt) +", 12); \n")
    def set_form_value(self, formID, cnt) :
        letters = string.ascii_lowercase
        Title_rand = ''.join(random.choice(letters) for i in range(5))
        self.template.write("FQL->SetFormFieldValue(formID"+str(formID)+str(cnt)+str(self.tag_cnt)+",  L\""+Title_rand +"\"); \n")
    def set_form_bounds(self, formID, cnt) :
        print ("FORM!!!!!!!!!!!!!!!!!", formID)
        self.template.write("FQL->SetFormFieldBounds(formID"+str(formID)+str(cnt)+str(self.tag_cnt)+", 20 ,"+ str(cnt * 20) +", 100, 20); \n")
    def set_form_align(self, formID, cnt) :
        self.template.write("FQL->SetFormFieldAlignment(formID"+str(formID)+str(cnt)+str(self.tag_cnt)+", 2 ); \n")

    # 3rd Necessay ----------------------------------------------
    def set_form_color(self, formID, cnt) :
        # border
        self.template.write("FQL->SetFormFieldBorderColor(formID" + str(formID) + str(cnt) + str(self.tag_cnt)+", 0.2, 0.5, 0.8); \n")
        # background
        self.template.write("FQL->SetFormFieldBackgroundColor(formID" + str(formID) + str(cnt) + str(self.tag_cnt)+", 0.8, 0.5, 0.2); \n")
    def set_form_border_style(self, formID, cnt) :
        self.template.write("FQL->SetFormFieldBorderStyle(formID" + str(formID) + str(cnt) + str(self.tag_cnt)+",1, 0 ,0 ,0 ); \n")
    def set_form_hlight(self, formID, cnt) :
        self.template.write("FQL->SetFormFieldHighlightMode(formID" + str(formID)+str(cnt) + str(self.tag_cnt)+", 3); \n")
    def form_jsa_weblk(self, formID, cnt) :
        letters = string.ascii_lowercase
        JS_rand = ''.join(random.choice(letters) for i in range(5))
        self.template.write("FQL->FormFieldJavaScriptAction(formID"+str(formID)+str(cnt)+str(self.tag_cnt)+", L\"U\",L\""+JS_rand+"\" ); \n")
  

    # *** important dependencies -------------------------------------
    def set_form_radio_dependency (self) : 
        if len(self.radio_sub_group) > 0 :
            for i in self.radio_sub_group.items() : 
                # how many sub-form we need to create
                sub_cnt = int(i[1])
                # create main form first 
                letters = string.ascii_lowercase
                Title_rand = ''.join(random.choice(letters) for i in range(5))
                name = ''.join(c for c in i[0] if c not in '(){}<>[]-=@#$%^&*+\/:;?!~`|')
                self.template.write("int formID"+name+"main"+str(self.tag_cnt)+" = FQL->NewFormField(L\""+Title_rand+"\", 4); \n")
                for j in range(0, sub_cnt):
                    # add sub form to main
                    self.template.write("int formID"+name+str(j)+str(self.tag_cnt)+" = FQL->AddFormFieldSub(formID"+name+"main"+str(self.tag_cnt)+", L\""+Title_rand+str(j)+str(self.tag_cnt)+"\"); \n")
                    # set form bounds (on sub)
                    self.set_form_bounds(name, j)
                    self.set_form_color(name, j)
                
        


    def api_order(self) :
        print(self.maga_info)
        for form in self.maga_info :
            for cnt in self.maga_info[form] :
                FieldType = self.new_form(form, cnt)
                if FieldType == "1" : 
                    self.set_form_value(form, cnt)
                    self.set_form_bounds(form, cnt)
                    self.set_form_align(form, cnt)
                elif FieldType == "2" :
                    self.set_form_bounds(form, cnt)
                    self.add_set_form_font(form, cnt)
                    self.set_form_value(form, cnt)
                    self.set_form_align(form, cnt)
                    self.set_form_color(form, cnt)
                    self.set_form_border_style(form, cnt)
                    self.set_form_hlight(form, cnt)
                    self.form_jsa_weblk(form, cnt)
                elif FieldType == "3" :
                    self.set_form_chk_style(form, cnt)
                    self.set_form_bounds(form, cnt)
                    self.set_form_value(form, cnt)
                    self.set_form_color(form, cnt)
                elif FieldType.split(":")[0] == "5" :
                    self.set_form_bounds(form, cnt)
                    self.set_form_border_style(form, cnt)
                    self.set_form_choice_sub(form,cnt, FieldType.split(":")[1])
                elif FieldType == "6" :
                    self.set_form_bounds(form, cnt)
                    self.set_form_border_style(form, cnt)
        self.set_form_radio_dependency() 
		     




