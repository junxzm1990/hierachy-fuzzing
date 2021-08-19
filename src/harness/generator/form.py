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
        input_num = len(form.find_all("input"))
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
                    if inpt.has_attr("name") :
                        self.form_type_ret[form_id][cnt] = "radio_"+str(inpt["name"])
                    else :
                        self.form_type_ret[form_id][cnt] = "radio"
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
        for button in form.find_all("button") : 
            self.form_type_ret[form_id][cnt] = "button"

        return self.form_type_ret

    def form_parse(self) :
        # how many forms in file 
        num_form = len(self.forms)
        # form structure
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
        self.tag_cnt = tag_cnt
        self.radio_sub_group = dict()

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
                self.template.write("int formID" + str(formID) + str(cnt) + str(self.tag_cnt) + " = FQL->NewFormField( L\""+Title_rand +"\", " + FieldType + "); \n")
        elif len(FieldType) != 0 :
            self.template.write("int formID" + str(formID) + str(cnt) + str(self.tag_cnt) + " = FQL->NewFormField( L\""+Title_rand +"\", " + FieldType[0] + "); \n")
            # API SetFormFieldChoiceType(formID, ChoiceType(0-4))
            SetFormFieldChoiceType_arg_1 = "SetFormFieldChoiceType_ChoiceType" + str(formID) + str(cnt) + str(self.tag_cnt)
            SetFormFieldChoiceType_constrain_1 = "if ("+ SetFormFieldChoiceType_arg_1 + " < 0 || "+ SetFormFieldChoiceType_arg_1 + " > 4) { \n"  
            self.arg_val(SetFormFieldChoiceType_arg_1, "double", SetFormFieldChoiceType_constrain_1, "4", "0")
            self.template.write("FQL-> SetFormFieldChoiceType(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", " + SetFormFieldChoiceType_arg_1 + ");\n")
        return FieldType
    def set_form_chk_style(self, formID, cnt) :
        # API SetFormFieldCheckStyle(formID, CheckStyle(0-7), Position(0-2))
        SetFormFieldCheckStyle_arg_1 = "SetFormFieldCheckStyle_CheckStyle" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldCheckStyle_arg_2 = "SetFormFieldCheckStyle_Position" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldCheckStyle_constrain_1 = "if ("+ SetFormFieldCheckStyle_arg_1 + " < 0 || "+ SetFormFieldCheckStyle_arg_1 + " > 7) { \n"
        SetFormFieldCheckStyle_constrain_2 = "if ("+ SetFormFieldCheckStyle_arg_2 + " < 0 || "+ SetFormFieldCheckStyle_arg_2 + " > 2) { \n"
        self.arg_val(SetFormFieldCheckStyle_arg_1, "int", SetFormFieldCheckStyle_constrain_1, "7", "0")
        self.arg_val(SetFormFieldCheckStyle_arg_2, "int", SetFormFieldCheckStyle_constrain_2, "2", "0")
        self.template.write("FQL->SetFormFieldCheckStyle(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", " + SetFormFieldCheckStyle_arg_1 + ", " +  SetFormFieldCheckStyle_arg_2 + "); \n")
    def set_form_choice_sub (self, formID, cnt, sub_cnt) :
        for i in range(0, int(sub_cnt)) : 
            letters = string.ascii_lowercase
            Title_rand = ''.join(random.choice(letters) for i in range(5))
            self.template.write("int formID" + str(formID) + str(cnt) + str(self.tag_cnt) + str(i) + "choice = FQL -> AddFormFieldChoiceSub(formID" + str(formID) + str(cnt) + str(self.tag_cnt) + ", L\""+Title_rand+"\", L\"" +Title_rand+"\"); \n")
    def set_form_format_mode(self) :
        # API SetFormFieldFormatMode(NewFormatMode)
        self.template.write("int SetFormFieldFormatMode_NewFormatMode"+str(self.tag_cnt)+"=(int)0; \n")
        self.template.write("if (bytes_read - index >= sizeof(int)) { \n")
        self.template.write("SetFormFieldFormatMode_NewFormatMode"+str(self.tag_cnt)+" = *(int*)(buffer+index); \n")
        self.template.write("if (SetFormFieldFormatMode_NewFormatMode"+str(self.tag_cnt)+" != 0 || SetFormFieldFormatMode_NewFormatMode"+str(self.tag_cnt)+"!= 15 ) {\n")
        self.template.write("SetFormFieldFormatMode_NewFormatMode"+str(self.tag_cnt)+"= (rand() > RAND_MAX/2) ? 0 : 15; \n")
        self.template.write("}else{ \n")
        self.template.write("index += sizeof(int);\n")
        self.template.write("} \n")
        self.template.write("}else{ \n")
        self.template.write("exit(0); \n")
        self.template.write("} \n")
        self.template.write("FQL->SetFormFieldFormatMode(SetFormFieldFormatMode_NewFormatMode"+str(self.tag_cnt)+"); \n") 
    # 2nd Necessay -------------------------------------------
    def set_form_visibility(self,formID, cnt) : 
    # API SetFormFieldVisible(formID, Visible(0-1))
        SetFormFieldVisible_arg_1 = "SetFormFieldVisible_Visible" + str(formID) + str(cnt) + str(self.tag_cnt) 
        SetFormFieldVisible_constrain_1 = "if ("+ SetFormFieldVisible_arg_1 + " < 0 || " + SetFormFieldVisible_arg_1 + " > 1 ) { \n"
        self.arg_val(SetFormFieldVisible_arg_1, "int", SetFormFieldVisible_constrain_1, "1", "0")
        self.template.write("FQL->SetFormFieldVisible(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", "+ SetFormFieldVisible_arg_1 + "); \n") 
    def add_set_form_font(self, formID, cnt) :
        # API AddStandardFont(StandardFontID(0-13))
        AddStandardFont_arg_1 = "AddStandardFont_StandardFontID" + str(formID) + str(cnt) + str(self.tag_cnt) 
        AddStandardFont_constrain_1 = "if ("+ AddStandardFont_arg_1 + " < 0 || " + AddStandardFont_arg_1 + " > 13 ) { \n" 
        self.arg_val(AddStandardFont_arg_1, "int", AddStandardFont_constrain_1, "13", "0") 
        self.template.write("int FontID"+str(formID)+str(cnt)+str(self.tag_cnt) + "=FQL->AddStandardFont(" + AddStandardFont_arg_1 + "); \n")
        # API SetTextSize(TextSize(double))
        SetTextSize_arg_1 = "SetTextSize_TextSize" + str(formID) + str(cnt) + str(self.tag_cnt) 
        SetTextSize_constrain_1 = "if (" + SetTextSize_arg_1 + "< 0.001 || " + SetTextSize_arg_1 + " > 50.001) { \n"
        self.arg_val(SetTextSize_arg_1, "double", SetTextSize_constrain_1, "50.001", "0.001") 
        self.template.write("FQL->SetTextSize(" + SetTextSize_arg_1 + "); \n")
        self.template.write("FQL->AddFormFont(FontID"+str(formID)+str(cnt)+str(self.tag_cnt) + "); \n")
        self.template.write("FQL->SetFormFieldFont(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", FQL->GetFormFontCount()); \n")
        # API SetFormFieldTextSize(formID, NewTextSize(double))
        SetFormFieldTextSize_arg_1 = "SetFormFieldTextSize_NewTextSize" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldTextSize_constrain_1 = "if (" + SetFormFieldTextSize_arg_1 + "< 0.001 || " + SetFormFieldTextSize_arg_1 + " > 50.001) { \n"
        self.arg_val(SetFormFieldTextSize_arg_1, "double", SetFormFieldTextSize_constrain_1, "50.001", "0.001") 
        self.template.write("FQL->SetFormFieldTextSize(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", " + SetFormFieldTextSize_arg_1 + "); \n")
    def set_form_value(self, formID, cnt) :
        letters = string.ascii_lowercase
        Title_rand = ''.join(random.choice(letters) for i in range(5))
        self.template.write("FQL->SetFormFieldValue(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ",  L\""+Title_rand +"\"); \n")
    def set_form_bounds(self, formID, cnt) :
        # API SetFormFieldBounds(formID, Left, Top, Width, Height)
        SetFormFieldBounds_arg_1 = "SetFormFieldBounds_Left" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBounds_arg_2 = "SetFormFieldBounds_Top" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBounds_arg_3 = "SetFormFieldBounds_Width" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBounds_arg_4 = "SetFormFieldBounds_Height" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBounds_constrain_1 = "if (" + SetFormFieldBounds_arg_1 + "< 0.001 || " + SetFormFieldBounds_arg_1 + " > 200.001) { \n"
        SetFormFieldBounds_constrain_2 = "if (" + SetFormFieldBounds_arg_2 + "< 0.001 || " + SetFormFieldBounds_arg_2 + " > 200.001) { \n"
        SetFormFieldBounds_constrain_3 = "if (" + SetFormFieldBounds_arg_3 + "< 0.001 || " + SetFormFieldBounds_arg_3 + " > 200.001) { \n"
        SetFormFieldBounds_constrain_4 = "if (" + SetFormFieldBounds_arg_4 + "< 0.001 || " + SetFormFieldBounds_arg_4 + " > 200.001) { \n"
        self.arg_val(SetFormFieldBounds_arg_1, "double", SetFormFieldBounds_constrain_1, "200.001", "0.001")
        self.arg_val(SetFormFieldBounds_arg_2, "double", SetFormFieldBounds_constrain_2, "200.001", "0.001")
        self.arg_val(SetFormFieldBounds_arg_3, "double", SetFormFieldBounds_constrain_3, "200.001", "0.001")
        self.arg_val(SetFormFieldBounds_arg_4, "double", SetFormFieldBounds_constrain_4, "200.001", "0.001")
        self.template.write("FQL->SetFormFieldBounds(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + "," +  SetFormFieldBounds_arg_1 + " ,"+ SetFormFieldBounds_arg_2 +", " +  SetFormFieldBounds_arg_3 + ", " + SetFormFieldBounds_arg_4  + "); \n")
    def set_form_align(self, formID, cnt) :
        # API SetFormFieldAlignment(formID, Alignment(0-2))
        SetFormFieldAlignment_arg_1 = "SetFormFieldAlignment_Alignment" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldAlignment_constrain_1 = "if ("+ SetFormFieldAlignment_arg_1 + " < 0 || "+ SetFormFieldAlignment_arg_1 + " > 2) { \n"
        self.arg_val(SetFormFieldAlignment_arg_1, "int", SetFormFieldAlignment_constrain_1, "2", "0")
        self.template.write("FQL->SetFormFieldAlignment(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", " + SetFormFieldAlignment_arg_1 + " ); \n")

    # 3rd Necessay ----------------------------------------------
    def set_form_color(self, formID, cnt) :
        # border
        # API SetFormFieldBorderColor(formID, Red, Green, Blue)
        SetFormFieldBorderColor_arg_1 = "SetFormFieldBorderColor_Red" + str(formID) + str(cnt) +  str(self.tag_cnt)
        SetFormFieldBorderColor_arg_2 = "SetFormFieldBorderColor_Green" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBorderColor_arg_3 = "SetFormFieldBorderColor_Blue" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBorderColor_constrain_1 = "if (" + SetFormFieldBorderColor_arg_1 + "< 0.001 || " + SetFormFieldBorderColor_arg_1 + " > 0.999) { \n"
        SetFormFieldBorderColor_constrain_2 = "if (" + SetFormFieldBorderColor_arg_2 + "< 0.001 || " + SetFormFieldBorderColor_arg_2 + " > 0.999) { \n"
        SetFormFieldBorderColor_constrain_3 = "if (" + SetFormFieldBorderColor_arg_3 + "< 0.001 || " + SetFormFieldBorderColor_arg_3 + " > 0.999) { \n"
        self.arg_val(SetFormFieldBorderColor_arg_1, "double", SetFormFieldBorderColor_constrain_1, "0.999", "0.001")
        self.arg_val(SetFormFieldBorderColor_arg_2, "double", SetFormFieldBorderColor_constrain_2, "0.999", "0.001")
        self.arg_val(SetFormFieldBorderColor_arg_3, "double", SetFormFieldBorderColor_constrain_3, "0.999", "0.001")
        
        self.template.write("FQL->SetFormFieldBorderColor(formID" + str(formID) + str(cnt) + str(self.tag_cnt) + ", " + SetFormFieldBorderColor_arg_1 + ", " + SetFormFieldBorderColor_arg_2  +  ", " +  SetFormFieldBorderColor_arg_3 +  "); \n")
        # background
        # API SetFormFieldBackgroundColor(formID, Red, Green, Blue)
        SetFormFieldBackgroundColor_arg_1 = "SetFormFieldBackgroundColor_Red" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBackgroundColor_arg_2 = "SetFormFieldBackgroundColor_Green" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBackgroundColor_arg_3 = "SetFormFieldBackgroundColor_Blue" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBackgroundColor_constrain_1 = "if (" + SetFormFieldBackgroundColor_arg_1 + "< 0.001 || " + SetFormFieldBackgroundColor_arg_1 + " > 0.999) { \n"
        SetFormFieldBackgroundColor_constrain_2 = "if (" + SetFormFieldBackgroundColor_arg_2 + "< 0.001 || " + SetFormFieldBackgroundColor_arg_2 + " > 0.999) { \n"
        SetFormFieldBackgroundColor_constrain_3 = "if (" + SetFormFieldBackgroundColor_arg_3 + "< 0.001 || " + SetFormFieldBackgroundColor_arg_3 + " > 0.999) { \n"
        self.arg_val(SetFormFieldBackgroundColor_arg_1, "double", SetFormFieldBackgroundColor_constrain_1, "0.999", "0.001")
        self.arg_val(SetFormFieldBackgroundColor_arg_2, "double", SetFormFieldBackgroundColor_constrain_2, "0.999", "0.001")
        self.arg_val(SetFormFieldBackgroundColor_arg_3, "double", SetFormFieldBackgroundColor_constrain_3, "0.999", "0.001")
        
        self.template.write("FQL->SetFormFieldBackgroundColor(formID" + str(formID) + str(cnt) + str(self.tag_cnt) + "," + SetFormFieldBackgroundColor_arg_1 +  ", "  +  SetFormFieldBackgroundColor_arg_2  + ", " +  SetFormFieldBackgroundColor_arg_3 + "); \n")
    def set_form_border_style(self, formID, cnt) :
        # API SetFormFieldBorderStyle(formID, Width(int), Style(0-3), DashOn(double), DashOff(double))
        SetFormFieldBorderStyle_arg_1 = "SetFormFieldBorderStyle_Width" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBorderStyle_arg_2 = "SetFormFieldBorderStyle_Style" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBorderStyle_arg_3 = "SetFormFieldBorderStyle_DashOn" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBorderStyle_arg_4 = "SetFormFieldBorderStyle_DashOff" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldBorderStyle_constrain_1 = "if ("+ SetFormFieldBorderStyle_arg_1 + " < 0.001 || "+ SetFormFieldBorderStyle_arg_1 + " > 50.001) { \n"
        SetFormFieldBorderStyle_constrain_2 = "if ("+ SetFormFieldBorderStyle_arg_2 + " < 0 || "+ SetFormFieldBorderStyle_arg_2 + " > 3) { \n"
        SetFormFieldBorderStyle_constrain_3 = "if ("+ SetFormFieldBorderStyle_arg_3 + " < 0.001 || "+ SetFormFieldBorderStyle_arg_3 + " > 50.001) { \n"
        SetFormFieldBorderStyle_constrain_4 = "if ("+ SetFormFieldBorderStyle_arg_4 + " < 0.001 || "+ SetFormFieldBorderStyle_arg_4 + " > 50.001) { \n"
        self.arg_val(SetFormFieldBorderStyle_arg_1, "double", SetFormFieldBorderStyle_constrain_1, "50.001", "0.001")
        self.arg_val(SetFormFieldBorderStyle_arg_2, "int", SetFormFieldBorderStyle_constrain_2, "3", "0")
        self.arg_val(SetFormFieldBorderStyle_arg_3, "double", SetFormFieldBorderStyle_constrain_3, "50.001", "0.001")
        self.arg_val(SetFormFieldBorderStyle_arg_4, "double", SetFormFieldBorderStyle_constrain_4, "50.001", "0.001")
        self.template.write("FQL->SetFormFieldBorderStyle(formID" + str(formID) + str(cnt) + str(self.tag_cnt) +  "," + SetFormFieldBorderStyle_arg_1 + ", "+SetFormFieldBorderStyle_arg_2 +","+ SetFormFieldBorderStyle_arg_3 +", " + SetFormFieldBorderStyle_arg_4 + " ); \n")
    def set_form_hlight(self, formID, cnt) :
        # API SetFormFieldHighlightMode(formID, newMode(0-3))
        SetFormFieldHighlightMode_arg_1 = "SetFormFieldHighlightMode_NewMode" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldHighlightMode_constrain_1 = "if (" + SetFormFieldHighlightMode_arg_1 + " < 0 || " + SetFormFieldHighlightMode_arg_1 + " > 3) { \n" 
        self.arg_val(SetFormFieldHighlightMode_arg_1, "int", SetFormFieldHighlightMode_constrain_1, "3", "0")
        self.template.write("FQL->SetFormFieldHighlightMode(formID" + str(formID)+str(cnt) + str(self.tag_cnt) + ", " + SetFormFieldHighlightMode_arg_1  + "); \n")
    def set_form_icon(self, formID, cnt) :
        # API SetFormFieldIcon(formID, IconType(0-2), CaptureID(int))
        SetFormFieldIcon_arg_1 = "SetFormFieldIcon_IconType" + str(formID) + str(cnt) + str(self.tag_cnt)
        SetFormFieldIcon_constrain_1 = "if (" + SetFormFieldIcon_arg_1 + " < 0 || " + SetFormFieldIcon_arg_1 + " > 2 ) { \n"
        self.arg_val(SetFormFieldIcon_arg_1, "int", SetFormFieldIcon_constrain_1, "2", "0")
        self.template.write("FQL->SetFormFieldIcon(formID" + str(formID) + str(cnt) + str(self.tag_cnt) + ", "+SetFormFieldIcon_arg_1+", FQL->CapturePage(1)) ; \n" ) 
    def form_jsa_weblk(self, formID, cnt) :
        letters = string.ascii_lowercase
        JS_rand = ''.join(random.choice(letters) for i in range(5))
        self.template.write("FQL->FormFieldJavaScriptAction(formID"+str(formID)+str(cnt)+str(self.tag_cnt) + ", L\"U\",L\""+JS_rand+"\" ); \n")
    def set_form_caption(self, formID, cnt) :
        letters = string.ascii_lowercase
        CP_rand = ''.join(random.choice(letters) for i in range(5))
        self.template.write("FQL->SetFormFieldCaption(formID" + str(formID) + str(cnt) + str(self.tag_cnt) + ", L\""+ CP_rand +"\" ); \n")

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
                self.template.write("int formID"+name+ "main"+str(self.tag_cnt) +" = FQL->NewFormField(L\""+Title_rand+"\", 4); \n")
                for j in range(0, sub_cnt):
                    # add sub form to main
                    self.template.write("int formID"+name+ str(j)+str(self.tag_cnt) +" = FQL->AddFormFieldSub(formID"+name+"main" +str(self.tag_cnt)+ ", L\""+Title_rand+str(j)+str(self.tag_cnt) + "\"); \n")
                    # set form bounds (on sub)
                    self.set_form_bounds(name, j)
                    self.set_form_caption(name, j)
                    self.set_form_visibility(name, j)
                    self.set_form_hlight(name, j)
                    self.set_form_icon(name, j)
                    self.set_form_color(name, j)
                
        


    def api_order(self) :
        print(self.maga_info)
        self.set_form_format_mode()
        for form in self.maga_info :
            for cnt in self.maga_info[form] :
                FieldType = self.new_form(form, cnt)
                if FieldType == "1" : 
                    self.set_form_value(form, cnt)
                    self.set_form_bounds(form, cnt)
                    self.set_form_align(form, cnt)
                    self.set_form_visibility(form, cnt)
                    self.set_form_hlight(form, cnt)
                    self.set_form_icon(form, cnt)
                elif FieldType == "2" :
                    self.set_form_bounds(form, cnt)
                    self.set_form_caption(form, cnt)
                    self.add_set_form_font(form, cnt)
                    self.set_form_value(form, cnt)
                    self.set_form_align(form, cnt)
                    self.set_form_color(form, cnt)
                    self.set_form_border_style(form, cnt)
                    self.set_form_hlight(form, cnt)
                    self.set_form_icon(form, cnt)
                    self.form_jsa_weblk(form, cnt)
                    self.set_form_visibility(form, cnt)
                elif FieldType == "3" :
                    self.set_form_chk_style(form, cnt)
                    self.set_form_caption(form, cnt)
                    self.set_form_bounds(form, cnt)
                    self.set_form_value(form, cnt)
                    self.set_form_color(form, cnt)
                    self.set_form_visibility(form, cnt)
                    self.set_form_hlight(form, cnt)
                    self.set_form_icon(form, cnt)
                elif FieldType.split(":")[0] == "5" :
                    self.set_form_bounds(form, cnt)
                    self.set_form_border_style(form, cnt)
                    self.set_form_choice_sub(form,cnt, FieldType.split(":")[1])
                    self.set_form_visibility(form, cnt)
                    self.set_form_hlight(form, cnt)
                    self.set_form_icon(form, cnt)
                elif FieldType == "6" :
                    self.set_form_bounds(form, cnt)
                    self.set_form_border_style(form, cnt)
                    self.set_form_visibility(form, cnt)
                    self.set_form_hlight(form, cnt)
                    self.set_form_icon(form, cnt)
        self.set_form_radio_dependency() 
		     

