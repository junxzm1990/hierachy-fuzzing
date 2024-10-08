from bs4 import BeautifulSoup, NavigableString, Tag
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase



class PDF_TAB_STRU():
    def __init__(self, tab_num) :
#        # pass in soup's tables
        self.tab_num = tab_num
#        self.tables = tables
#        self.styles = styles
        # {tableID:{Attribute:{value}}}
        self.maga_info = dict()
        # attributes of each table
        self.tab_stru = dict()
        self.tab_cell_color = dict()
        self.tab_border_width = dict()
        self.tab_border_collapse = dict()
        self.tab_border_color = dict()
        self.tab_merged_cell = dict()
        self.tab_padding = dict()
        self.tab_cell_content = dict()
        self.tab_cell_font = dict()

    def rand_dice(self, lo, up) :
        dice_rs = random.randint(lo,up)
        return dice_rs

    def row_col_num(self, tab_id) :
        # how many columns(cells) does one row has;
        row_num = self.rand_dice(1, 5)
        # obtain each cells' number of each row and append the number to the list
        col_num = self.rand_dice(1, 10)
        self.tab_stru[tab_id] = (row_num, col_num)

    def cell_color(self,tab_id) :
        self.tab_cell_color[tab_id] = list()
        self.tab_cell_content[tab_id] = list()
        self.tab_cell_font[tab_id] = list()
        for row_num in range(0, self.tab_stru[tab_id][0]) :
            for col_num in range(0, self.tab_stru[tab_id][1] ) :
                content = ''.join(choice(ascii_uppercase) for i in range(6))
                self.tab_cell_content[tab_id].append((row_num, col_num, content))
                self.tab_cell_color[tab_id].append((row_num, col_num))
                self.tab_cell_font[tab_id].append((row_num, col_num))

    def tab_border(self, tab_id) :
        border_dice = self.rand_dice(0, 1) 
        if border_dice == 1 :
            self.tab_border_width[tab_id] = 1
        else :
            self.tab_border_width[tab_id] = 0
        coll_dice = self.rand_dice(0, 1)
        if coll_dice == 1 : 
            self.tab_border_collapse[tab_id] = 1
        else :
            self.tab_border_collapse[tab_id] = 0 
        bcolor_dice = self.rand_dice(0, 1) 
        if bcolor_dice == 1 :  
            self.tab_border_color[tab_id] = 1
        else : 
            self.tab_border_color[tab_id] = 0
        padding_dice = self.rand_dice(0, 1)
        if padding_dice == 1 :   
            self.tab_padding[tab_id] = 1
        else :
            self.tab_padding[tab_id] = 0
   
    def tab_merge_cell(self, tab_id) :
        self.tab_merged_cell[tab_id] = list()
        # decide if current table needs to be merged
        merge_dice = self.rand_dice(0, 1)
        if merge_dice == 1 :
            col_or_row = self.rand_dice(0, 1) 
            row_num = self.rand_dice(0, self.tab_stru[tab_id][0])
            col_num = self.rand_dice(0, self.tab_stru[tab_id][1])
            if col_or_row == 0 :
                self.tab_merged_cell[tab_id].append(('row', row_num, col_num, 3))
            elif col_or_row == 1 :
                self.tab_merged_cell[tab_id].append(('col', row_num, col_num, 3))
      
    # entry of this class
    def tab_parse(self) : 
        # how many tables in file
        #num_tab = len(self.tables)
        for i in range(0, self.tab_num) :
            # update maga_info with TableID
            self.maga_info[i] = dict()
            # update each attributes
            self.row_col_num(i)
            self.cell_color(i)
            self.tab_border(i)
            self.tab_merge_cell(i)
            # adding attributes to current handling table in maga_info
            self.maga_info[i]['row_col_num']=self.tab_stru[i]
            self.maga_info[i]['cell_color']=self.tab_cell_color[i]
            self.maga_info[i]['cell_content']=self.tab_cell_content[i]
            self.maga_info[i]['border_width']=self.tab_border_width[i]
            self.maga_info[i]['border_collapse']=self.tab_border_collapse[i]
            self.maga_info[i]['border_color']=self.tab_border_color[i]
            self.maga_info[i]['tab_padding']=self.tab_padding[i]
            self.maga_info[i]['merged_cell']=self.tab_merged_cell[i]
            self.maga_info[i]['text_font']=self.tab_cell_font[i]
        return self.maga_info
            
class PDF_TAB_API_MAP():
    def __init__(self, maga_info, template, tab, tag_cnt) : 
        self.maga_info = maga_info
        self.template = template
        self.tab = tab 
        self.tag_cnt = tag_cnt
   
    def arg_val(self, arg_name, arg_type, constrain, upper, lower):       
        self.template.write(arg_type + " "+ arg_name + "=(" + arg_type + ")0; \n")
        self.template.write("if (bytes_read - index >= sizeof(" + arg_type + ")) { \n")
        self.template.write(arg_name + " = *("+arg_type+"*)(buffer+index); \n")
        #self.template.write("memcpy(&" + arg_name + ", buffer + index, sizeof("+ arg_type +"));\n")
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

    def create_tab(self, tableID) :
        ## API : CreateTable(RowCount, ColumnCount)
        CreateTable_arg_1 = "CreateTable_RowCount" + str(tableID) + str(self.tag_cnt)
        CreateTable_arg_2 = "CreateTable_ColumnCount" + str(tableID)+ str(self.tag_cnt)
        CreateTable_constrain_1 = "if (CreateTable_RowCount" + str(tableID) + str(self.tag_cnt) + " <=0 || CreateTable_RowCount" + str(tableID) + str(self.tag_cnt) + " > 150){ \n"
        CreateTable_constrain_2 = "if (CreateTable_ColumnCount" + str(tableID) + str(self.tag_cnt) + " <= 0 || CreateTable_ColumnCount" + str(tableID) + str(self.tag_cnt) + " > 150){ \n"
        self.arg_val(CreateTable_arg_1, "int", CreateTable_constrain_1, "150", "1")
        self.arg_val(CreateTable_arg_2, "int", CreateTable_constrain_2, "150", "1")
        # create each table start with its first row column number on first row
        self.template.write("int TableID" + str(tableID) + str(self.tag_cnt) + " = FQL->CreateTable("+ CreateTable_arg_1 + "," + CreateTable_arg_2 + "); \n" )

    def extend_tab(self, tableID) :
        ## API : InsertTableRows(TableID, Position, NewRowCount)
        InsertTableRows_arg_1 = "InsertTableRows_Position" + str(tableID)+ str(self.tag_cnt)
        InsertTableRows_arg_2 = "InsertTableRows_NewRowCount" + str(tableID)+ str(self.tag_cnt)
        InsertTableRows_constrain_1 = "if (InsertTableRows_Position"+ str(tableID) + str(self.tag_cnt) +" <= 0 || InsertTableRows_Position"+str(tableID)+ str(self.tag_cnt) +" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) + "){ \n"
        InsertTableRows_constrain_2 = "if (InsertTableRows_NewRowCount"+ str(tableID) + str(self.tag_cnt) +" <= 0 || InsertTableRows_NewRowCount"+str(tableID)+ str(self.tag_cnt) +" > 150){ \n"
        self.arg_val(InsertTableRows_arg_1, "int", InsertTableRows_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
        self.arg_val(InsertTableRows_arg_2, "int", InsertTableRows_constrain_2, "150", "1")
        self.template.write("FQL->InsertTableRows(TableID" + str(tableID) + str(self.tag_cnt) + "," + InsertTableRows_arg_1 +","+InsertTableRows_arg_2 + "); \n")
        
        ## API : InsertTableColumns(TableID, Position, NewColumnCount)
        InsertTableColumns_arg_1 = "InsertTableColumns_Position"+str(tableID)+ str(self.tag_cnt)
        InsertTableColumns_arg_2 = "InsertTableColumns_NewColumnCount" + str(tableID)+ str(self.tag_cnt)
        InsertTableColumns_constrain_1 = "if ("+InsertTableColumns_arg_1+" <=0 || "+ InsertTableColumns_arg_1 +" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
        InsertTableColumns_constrain_2 = "if ("+InsertTableColumns_arg_2+" <=0 || "+ InsertTableColumns_arg_2 +" > 150){ \n"
        self.arg_val(InsertTableColumns_arg_1, "int", InsertTableColumns_constrain_1, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1")
        self.arg_val(InsertTableColumns_arg_2, "int", InsertTableColumns_constrain_2, "150", "1")
        self.template.write("FQL->InsertTableColumns(TableID"+str(tableID)+ str(self.tag_cnt) +","+InsertTableColumns_arg_1 +","+ InsertTableColumns_arg_2 +"); \n")

        ## API : AppendTableRows(TableID, NewRowCount)
        AppendTableRows_arg_1 = "AppendTableRows_NewRowCount" + str(tableID)+ str(self.tag_cnt)
        AppendTableRows_constrain_1 = "if (AppendTableRows_NewRowCount"+ str(tableID) + str(self.tag_cnt) +" <=0 || AppendTableRows_NewRowCount"+ str(tableID) + str(self.tag_cnt) +" > 150){ \n"
        self.arg_val(AppendTableRows_arg_1, "int", AppendTableRows_constrain_1, "150", "1")
        self.template.write("FQL->AppendTableRows(TableID" + str(tableID) + str(self.tag_cnt) + "," + AppendTableRows_arg_1 + ") ; \n")
        
        ## API : AppendTableColumn(TableID, NewColumnCount)
        AppendTableColumn_arg_1 = "AppendTableColumn_NewColumnCount" + str(tableID)+ str(self.tag_cnt)
        AppendTableColumn_constrain_1 = "if (AppendTableColumn_NewColumnCount"+ str(tableID) + str(self.tag_cnt) +" <= 0 || AppendTableColumn_NewColumnCount" + str(tableID) + str(self.tag_cnt) +  " >150){\n"
        self.arg_val(AppendTableColumn_arg_1, "int", AppendTableColumn_constrain_1, "150", "1") 
        self.template.write("FQL->AppendTableColumns(TableID" + str(tableID)+ str(self.tag_cnt)  + "," + AppendTableColumn_arg_1 + ") ; \n")

        ## API : SetTableColumnWidth(TableID, FirstColumn, LastColumn)
        SetTableColumnWidth_arg_1 = "SetTableColumnWidth_FirstColumn" + str(tableID) + str(self.tag_cnt)
        SetTableColumnWidth_constrain_1 = "if (SetTableColumnWidth_FirstColumn" + str(tableID)+ str(self.tag_cnt)  + "<= 0 || SetTableColumnWidth_FirstColumn" + str(tableID)+ str(self.tag_cnt)  + " > CreateTable_ColumnCount" + str(tableID)+ str(self.tag_cnt)  + "){ \n"
        SetTableColumnWidth_arg_2 = "SetTableColumnWidth_LastColumn" + str(tableID)+ str(self.tag_cnt)
        SetTableColumnWidth_constrain_2 = "if (SetTableColumnWidth_LastColumn"+ str(tableID)+ str(self.tag_cnt)  + " < SetTableColumnWidth_FirstColumn"+ str(tableID)+ str(self.tag_cnt)  + " || SetTableColumnWidth_LastColumn" + str(tableID)+ str(self.tag_cnt)  +" > CreateTable_ColumnCount"+ str(tableID)+ str(self.tag_cnt)  +"){\n"
        SetTableColumnWidth_arg_3 = "SetTableColumnWidth_NewWidth" + str(tableID)+ str(self.tag_cnt)
        SetTableColumnWidth_constrain_3 = "if (SetTableColumnWidth_NewWidth" + str(tableID) + str(self.tag_cnt)  + " <= 0.001 || SetTableColumnWidth_NewWidth" + str(tableID) + str(self.tag_cnt) + " > 500.001){\n"
        self.arg_val(SetTableColumnWidth_arg_1, "int", SetTableColumnWidth_constrain_1, "CreateTable_ColumnCount" + str(tableID)+ str(self.tag_cnt) , "1")
        self.arg_val(SetTableColumnWidth_arg_2, "int", SetTableColumnWidth_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "SetTableColumnWidth_FirstColumn"+str(tableID)+ str(self.tag_cnt) )
        self.arg_val(SetTableColumnWidth_arg_3, "double", SetTableColumnWidth_constrain_3, "500.001", "0.001" )
        self.template.write("FQL->SetTableColumnWidth(TableID" + str(tableID) + str(self.tag_cnt) + "," + SetTableColumnWidth_arg_1 + "," + SetTableColumnWidth_arg_2 + "," + SetTableColumnWidth_arg_3 + "); \n")
        
        ## API : SetTableRowHeight(TableID, FirstRow, LastRow, NewHeight)
        SetTableRowHeight_arg_1 = "SetTableRowHeight_FirstRow" + str(tableID)+ str(self.tag_cnt)
        SetTableRowHeight_constrain_1 = "if ("+SetTableRowHeight_arg_1+"<=0 || "+SetTableRowHeight_arg_1 + " > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
        SetTableRowHeight_arg_2 = "SetTableRowHeight_LastRow" + str(tableID)+ str(self.tag_cnt)
        SetTableRowHeight_constrain_2 = "if ("+ SetTableRowHeight_arg_2 +"< "+SetTableRowHeight_arg_1+" || "+SetTableRowHeight_arg_2+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
        SetTableRowHeight_arg_3 = "SetTableRowHeight_NewHeight" + str(tableID)+ str(self.tag_cnt)
        SetTableRowHeight_constrain_3 = "if ("+SetTableRowHeight_arg_3+" < 0.001 ||  "+ SetTableRowHeight_arg_3 +" > 500.001 ){ \n"
        self.arg_val(SetTableRowHeight_arg_1, "int", SetTableRowHeight_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
        self.arg_val(SetTableRowHeight_arg_2, "int", SetTableRowHeight_constrain_2, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "SetTableRowHeight_FirstRow"+str(tableID)+ str(self.tag_cnt) )
        self.arg_val(SetTableRowHeight_arg_3, "double", SetTableRowHeight_constrain_3, "500.001", "0.001")
        self.template.write("FQL->SetTableRowHeight(TableID"+str(tableID)+ str(self.tag_cnt) +", "+SetTableRowHeight_arg_1+","+SetTableRowHeight_arg_2+","+SetTableRowHeight_arg_3+"); \n")

    def set_cell_color(self, tableID) :
        if self.maga_info[tableID]['cell_color'] != []:
            ## API : SetTableCellBackgroundColor(TableID, FirstRow, FirstColumn, LastRow, LastColumn, Red, Green, Blue) 
            SetTableCellBackgroundColor_arg_1 = "SetTableCellBackgroundColor_FirstRow"+str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_arg_2 = "SetTableCellBackgroundColor_FirstColumn"+str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_arg_3 = "SetTableCellBackgroundColor_LastRow"+str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_arg_4 = "SetTableCellBackgroundColor_LastColumn"+str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_arg_5 = "SetTableCellBackgroundColor_Red"+str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_arg_6 = "SetTableCellBackgroundColor_Green" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_arg_7 = "SetTableCellBackgroundColor_Blue" +str(tableID)+ str(self.tag_cnt)
            SetTableCellBackgroundColor_constrain_1 = "if ("+SetTableCellBackgroundColor_arg_1+" <=0 || "+SetTableCellBackgroundColor_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
            SetTableCellBackgroundColor_constrain_2 = "if ("+SetTableCellBackgroundColor_arg_2+" <=0 || "+SetTableCellBackgroundColor_arg_2+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
            SetTableCellBackgroundColor_constrain_3 = "if ("+SetTableCellBackgroundColor_arg_3+" <= "+SetTableCellBackgroundColor_arg_1+" || "+SetTableCellBackgroundColor_arg_3+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
            SetTableCellBackgroundColor_constrain_4 = "if ("+SetTableCellBackgroundColor_arg_4+" <= "+SetTableCellBackgroundColor_arg_2+" || "+SetTableCellBackgroundColor_arg_4+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
            SetTableCellBackgroundColor_constrain_5 = "if ("+SetTableCellBackgroundColor_arg_5+" < 0.001 || "+SetTableCellBackgroundColor_arg_5+" > 0.999) { \n"
            SetTableCellBackgroundColor_constrain_6 = "if ("+SetTableCellBackgroundColor_arg_6+" < 0.001 || "+SetTableCellBackgroundColor_arg_6+" > 0.999) { \n"
            SetTableCellBackgroundColor_constrain_7 = "if ("+SetTableCellBackgroundColor_arg_7+" < 0.001 || "+SetTableCellBackgroundColor_arg_7+" > 0.999) { \n"
            self.arg_val(SetTableCellBackgroundColor_arg_1, "int", SetTableCellBackgroundColor_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellBackgroundColor_arg_2, "int", SetTableCellBackgroundColor_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellBackgroundColor_arg_3, "int", SetTableCellBackgroundColor_constrain_3, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellBackgroundColor_FirstRow" + str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellBackgroundColor_arg_4, "int", SetTableCellBackgroundColor_constrain_4, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellBackgroundColor_FirstColumn" + str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellBackgroundColor_arg_5, "double", SetTableCellBackgroundColor_constrain_5, "0.999", "0.001")
            self.arg_val(SetTableCellBackgroundColor_arg_6, "double", SetTableCellBackgroundColor_constrain_6, "0.999", "0.001")
            self.arg_val(SetTableCellBackgroundColor_arg_7, "double", SetTableCellBackgroundColor_constrain_7, "0.999", "0.001")
            # call API
            self.template.write("FQL->SetTableCellBackgroundColor(TableID" + str(tableID)+ str(self.tag_cnt)  + "," + SetTableCellBackgroundColor_arg_1 + "," + SetTableCellBackgroundColor_arg_2  + "," +SetTableCellBackgroundColor_arg_3 + "," +SetTableCellBackgroundColor_arg_4 + "," + SetTableCellBackgroundColor_arg_5 + "," + SetTableCellBackgroundColor_arg_6 + "," + SetTableCellBackgroundColor_arg_7 +"); \n")

        ## API : SetTableCellContent(TableID, RowNumber, ColumnNumber, HTMLText)
        if self.maga_info[tableID]['cell_content'] != []:
            for i in range(0, len(self.maga_info[tableID]['cell_content'])) :
                SetTableCellContent_arg_1 = "SetTableCellContent_RowNumber" + str(tableID) + str(self.tag_cnt) + str(i)
                SetTableCellContent_arg_2 = "SetTableCellContent_ColumnNumber" + str(tableID) + str(self.tag_cnt) + str(i)
                SetTableCellContent_constrain_1 = "if ("+SetTableCellContent_arg_1+" <= 0 || "+SetTableCellContent_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
                SetTableCellContent_constrain_2 = "if ("+SetTableCellContent_arg_2+" <= 0 || "+SetTableCellContent_arg_2+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
                self.arg_val(SetTableCellContent_arg_1, "int", SetTableCellContent_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1");
                self.arg_val(SetTableCellContent_arg_2, "int", SetTableCellContent_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1");
               # Coutmized value setting for HTMLText
                self.template.write("size_t HTMLText_len" + str(tableID)+ str(self.tag_cnt)  +str(i) + " = 5; \n")
                self.template.write("std::string random_HTMLText" + str(tableID)+ str(self.tag_cnt) +str(i) + " = random_string(HTMLText_len"+str(tableID)+ str(self.tag_cnt) +str(i)+"); \n")
                self.template.write("const size_t W_HTMLText_len" + str(tableID)+ str(self.tag_cnt) +str(i) + " = random_HTMLText" + str(tableID)+ str(self.tag_cnt)  +str(i)+ ".length() + 1; \n")
                self.template.write("wchar_t HTMLText"+str(tableID)+ str(self.tag_cnt) +str(i)+"[W_HTMLText_len"+str(tableID)+ str(self.tag_cnt) +str(i)+"];\n")
                self.template.write("swprintf(HTMLText"+str(tableID)+ str(self.tag_cnt) +str(i)+", W_HTMLText_len"+str(tableID)+ str(self.tag_cnt) +str(i)+", L\"%s\", random_HTMLText"+str(tableID)+ str(self.tag_cnt) +str(i)+".c_str()) ; \n")
                self.template.write("FQL->SetTableCellContent(TableID" + str(tableID)+ str(self.tag_cnt)  + ", " + SetTableCellContent_arg_1 + ", " + SetTableCellContent_arg_2 + ", HTMLText"+str(tableID)+ str(self.tag_cnt) +str(i)+"); \n")

        if self.maga_info[tableID]['text_font'] != [] : 
            ## API : SetTableCellTextColor(TableID, FirstRow, FirstColumn, LastRow, LastColumn, Red, Green, Blue)
            SetTableCellTextColor_arg_1 = "SetTableCellTextColor_FirstRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_arg_2 = "SetTableCellTextColor_FirstColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_arg_3 = "SetTableCellTextColor_LastRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_arg_4 = "SetTableCellTextColor_LastColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_arg_5 = "SetTableCellTextColor_Red" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_arg_6 = "SetTableCellTextColor_Green" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_arg_7 = "SetTableCellTextColor_Blue" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextColor_constrain_1 = "if ("+SetTableCellTextColor_arg_1+" <= 0 || "+SetTableCellTextColor_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellTextColor_constrain_2 = "if ("+SetTableCellTextColor_arg_2+" <= 0 || "+SetTableCellTextColor_arg_2+"> CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellTextColor_constrain_3 = "if (" +SetTableCellTextColor_arg_3 + " < "+SetTableCellTextColor_arg_1+" || "+SetTableCellTextColor_arg_3+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellTextColor_constrain_4 = "if ("+SetTableCellTextColor_arg_4+" < "+SetTableCellTextColor_arg_2+" || "+SetTableCellTextColor_arg_4+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellTextColor_constrain_5 = "if ("+SetTableCellTextColor_arg_5 + " < 0.001 || " + SetTableCellTextColor_arg_5+" > 0.999) { \n"
            SetTableCellTextColor_constrain_6 = "if ("+SetTableCellTextColor_arg_6 + " < 0.001 || "+SetTableCellTextColor_arg_6+" > 0.999) { \n"
            SetTableCellTextColor_constrain_7 = "if ("+SetTableCellTextColor_arg_7 + " < 0.001 || " + SetTableCellTextColor_arg_7 + " > 0.999) { \n"
            self.arg_val(SetTableCellTextColor_arg_1, "int", SetTableCellTextColor_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellTextColor_arg_2, "int", SetTableCellTextColor_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellTextColor_arg_3, "int", SetTableCellTextColor_constrain_3, "SetTableCellTextColor_FirstRow"+str(tableID)+ str(self.tag_cnt) , "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellTextColor_arg_4, "int", SetTableCellTextColor_constrain_4, "SetTableCellTextColor_FirstColumn"+str(tableID)+ str(self.tag_cnt) , "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellTextColor_arg_5, "double", SetTableCellTextColor_constrain_5, "0.999", "0.001")
            self.arg_val(SetTableCellTextColor_arg_6, "double", SetTableCellTextColor_constrain_6, "0.999", "0.001")
            self.arg_val(SetTableCellTextColor_arg_7, "double", SetTableCellTextColor_constrain_7, "0.999", "0.001")
            # call API
            self.template.write("FQL->SetTableCellTextColor(TableID"+str(tableID)+ str(self.tag_cnt) +","+ SetTableCellTextColor_arg_1+","+SetTableCellTextColor_arg_2+","+SetTableCellTextColor_arg_3+","+SetTableCellTextColor_arg_4+"," +SetTableCellTextColor_arg_5+","+SetTableCellTextColor_arg_6+","+SetTableCellTextColor_arg_7+"); \n")
            ## API : SetTableCellTextSize(TableID, FirstRow, FirstColumn,LastRow, LastColumn, NewTextSize)
            SetTableCellTextSize_arg_1 = "SetTableCellTextSize_FirstRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextSize_arg_2 = "SetTableCellTextSize_FirstColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextSize_arg_3 = "SetTableCellTextSize_LastRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextSize_arg_4 = "SetTableCellTextSize_LastColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextSize_arg_5 = "SetTableCellTextSize_NewTextSize" + str(tableID)+ str(self.tag_cnt)
            SetTableCellTextSize_constrain_1 = "if ("+SetTableCellTextSize_arg_1+" <= 0 || "+SetTableCellTextSize_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellTextSize_constrain_2 = "if ("+SetTableCellTextSize_arg_2+" <= 0 || "+SetTableCellTextSize_arg_2+"> CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellTextSize_constrain_3 = "if ("+SetTableCellTextSize_arg_3+" < "+SetTableCellTextSize_arg_1+" || "+SetTableCellTextSize_arg_3+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellTextSize_constrain_4 = "if ("+SetTableCellTextSize_arg_4+" < "+SetTableCellTextSize_arg_2+" || "+SetTableCellTextSize_arg_4+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellTextSize_constrain_5 = "if ("+SetTableCellTextSize_arg_5+" < 0.001 || " + SetTableCellTextSize_arg_5+" > 30.001) { \n"
            self.arg_val(SetTableCellTextSize_arg_1, "int", SetTableCellTextSize_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellTextSize_arg_2, "int", SetTableCellTextSize_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellTextSize_arg_3, "int", SetTableCellTextSize_constrain_3, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellTextSize_FirstRow"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellTextSize_arg_4, "int", SetTableCellTextSize_constrain_4, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellTextSize_FirstColumn"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellTextSize_arg_5, "double", SetTableCellTextSize_constrain_5, "30.001", "0.001")
            # Call API 
            self.template.write("FQL->SetTableCellTextSize(TableID"+str(tableID)+ str(self.tag_cnt) +","+ SetTableCellTextSize_arg_1+","+SetTableCellTextSize_arg_2+","+SetTableCellTextSize_arg_3+","+SetTableCellTextSize_arg_4+"," +SetTableCellTextSize_arg_5 + "); \n")
           
            

           # for cell in self.maga_info[tableID]['text_font'] :
           #     self.template.write("FQL->SetTableCellTextColor(TableID" + str(tableID) + "," + str(cell[0]) + "," + str(cell[1]) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", 0.1, 0.3, 0.5); \n")
           #     self.template.write("FQL->SetTableCellTextSize(TableID" + str(tableID) + "," + str(cell[0]) + "," + str(cell[1]) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", 0.01); \n")
    def set_tab_border(self, tableID) : 
        if self.maga_info[tableID]['border_collapse'] == 1 :
            ## API : SetTableThinkBorders(TableID, ThinBorders, Red, Green, Blue)
            SetTableThinBorders_arg_1 = "SetTableThinBorders_ThinBorders" + str(tableID)+ str(self.tag_cnt)
            SetTableThinBorders_arg_2 = "SetTableThinBorders_Red" + str(tableID)+ str(self.tag_cnt)
            SetTableThinBorders_arg_3 =  "SetTableThinBorders_Green" + str(tableID)+ str(self.tag_cnt)
            SetTableThinBorders_arg_4 =  "SetTableThinBorders_Blue" + str(tableID)+ str(self.tag_cnt)
            SetTableThinBorders_constrain_1 = "if ("+SetTableThinBorders_arg_1+" != 0 || "+SetTableThinBorders_arg_1+" != 1){ \n"
            SetTableThinBorders_constrain_2 = "if (" + SetTableThinBorders_arg_2 + " < 0.001 || " + SetTableThinBorders_arg_2 + " > 0.999) { \n"
            SetTableThinBorders_constrain_3 = "if (" + SetTableThinBorders_arg_3 + " < 0.001 || " + SetTableThinBorders_arg_3 + " > 0.999) { \n"
            SetTableThinBorders_constrain_4 ="if (" + SetTableThinBorders_arg_4 + " < 0.001 || " + SetTableThinBorders_arg_4 + " > 0.999) { \n"  
            self.arg_val(SetTableThinBorders_arg_1, "int", SetTableThinBorders_constrain_1, "1", "0")
            self.arg_val(SetTableThinBorders_arg_2, "double", SetTableThinBorders_constrain_2, "0.999", "0.001")
            self.arg_val(SetTableThinBorders_arg_3, "double", SetTableThinBorders_constrain_3, "0.999", "0.001")
            self.arg_val(SetTableThinBorders_arg_4, "double", SetTableThinBorders_constrain_4, "0.999", "0.001")
            # Call API
            self.template.write("FQL->SetTableThinBorders(TableID" + str(tableID)+ str(self.tag_cnt)  + ", " + SetTableThinBorders_arg_1 + ", " + SetTableThinBorders_arg_2 + ", " + SetTableThinBorders_arg_3 + ", " + SetTableThinBorders_arg_4 + "); \n")


        ## API : SetTableBorderWidth(TableID, BorderIndex, NewWidth)
        if self.maga_info[tableID]['border_width'] == 1 :
            SetTableBorderWidth_arg_1 = "SetTableBorderWidth_BorderIndex"+str(tableID)+ str(self.tag_cnt)
            SetTableBorderWidth_constrain_1 = "if ("+SetTableBorderWidth_arg_1+" < 0 || "+SetTableBorderWidth_arg_1+" > 4){ \n"
            SetTableBorderWidth_arg_2 = "SetTableBorderWidth_NewWidth" + str(tableID)+ str(self.tag_cnt)
            SetTableBorderWidth_constrain_2 = "if ("+SetTableBorderWidth_arg_2+" < 0.001 || "+SetTableBorderWidth_arg_2 +" > 50.001){ \n"
            self.arg_val(SetTableBorderWidth_arg_1, "int", SetTableBorderWidth_constrain_1, "4", "1")
            self.arg_val(SetTableBorderWidth_arg_2, "double", SetTableBorderWidth_constrain_2, "50.001", "0.001")

            # Call API
            self.template.write("FQL->SetTableBorderWidth(TableID" + str(tableID)+ str(self.tag_cnt)  + ","+SetTableBorderWidth_arg_1+","+ SetTableBorderWidth_arg_2+"); \n")

        ## API : SetTableBorderColor(TableID, BorderIndex, Red, Green, Blue)
        if self.maga_info[tableID]['border_color'] == 1 :
            SetTableBorderColor_arg_1 = "SetTableBorderColor_BorderIndex" + str(tableID)+ str(self.tag_cnt)
            SetTableBorderColor_arg_2 = "SetTableBorderColor_Red" + str(tableID)+ str(self.tag_cnt)
            SetTableBorderColor_arg_3 = "SetTableBorderColor_Green" + str(tableID) + str(self.tag_cnt)
            SetTableBorderColor_arg_4 = "SetTableBorderColor_Blue" + str(tableID) + str(self.tag_cnt)
            SetTableBorderColor_constrain_1 = "if ("+SetTableBorderColor_arg_1+" < 0 || "+SetTableBorderColor_arg_1+" > 4){ \n"           
            SetTableBorderColor_constrain_2 = "if (" + SetTableBorderColor_arg_2 + " < 0.001 || " + SetTableBorderColor_arg_2 + " > 0.999) { \n"            
            SetTableBorderColor_constrain_3 = "if (" + SetTableBorderColor_arg_3 + " < 0.001 || " + SetTableBorderColor_arg_3 + " > 0.999) { \n"             
            SetTableBorderColor_constrain_4 = "if (" + SetTableBorderColor_arg_4 + " < 0.001 || " + SetTableBorderColor_arg_4 + " > 0.999) { \n"             
            self.arg_val(SetTableBorderColor_arg_1, "int", SetTableBorderColor_constrain_1, "4", "1")
            self.arg_val(SetTableBorderColor_arg_2, "double", SetTableBorderColor_constrain_2, "0.999", "0.001")
            self.arg_val(SetTableBorderColor_arg_3, "double", SetTableBorderColor_constrain_3, "0.999", "0.001")
            self.arg_val(SetTableBorderColor_arg_4, "double", SetTableBorderColor_constrain_4, "0.999", "0.001")

            self.template.write("FQL->SetTableBorderColor(TableID" + str(tableID)+ str(self.tag_cnt)  + ", "+SetTableBorderColor_arg_1+","+SetTableBorderColor_arg_2+","+SetTableBorderColor_arg_3+","+SetTableBorderColor_arg_4+"); \n")

            ## API SetTableCellBorderColor(TableID, FirstRow, FirstColumn, LastRow, LastColumn, BorderIndex, Red, Green, Blue)
            
            SetTableCellBorderColor_arg_1 = "SetTableCellBorderColor_FirstRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_2 = "SetTableCellBorderColor_FirstColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_3 = "SetTableCellBorderColor_LastRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_4 = "SetTableCellBorderColor_LastColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_5 = "SetTableCellBorder_BorderIndex" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_6 = "SetTableCellBorderColor_Red" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_7 = "SetTableCellBorderColor_Green" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_arg_8 = "SetTableCellBorderColor_Blue" + str(tableID)+ str(self.tag_cnt)
            SetTableCellBorderColor_constrain_1 = "if ("+SetTableCellBorderColor_arg_1+" <= 0 || "+SetTableCellBorderColor_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellBorderColor_constrain_2 = "if ("+SetTableCellBorderColor_arg_2+" <= 0 || "+SetTableCellBorderColor_arg_2+"> CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellBorderColor_constrain_3 = "if ("+SetTableCellBorderColor_arg_3 + " < "+SetTableCellBorderColor_arg_1+" || "+SetTableCellBorderColor_arg_3+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellBorderColor_constrain_4 = "if ("+SetTableCellBorderColor_arg_4+" < "+SetTableCellBorderColor_arg_1+" || "+SetTableCellBorderColor_arg_4+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellBorderColor_constrain_5 = "if ("+SetTableCellBorderColor_arg_5+" < 0 || "+SetTableCellBorderColor_arg_5+" > 4){\n"
            SetTableCellBorderColor_constrain_6 = "if ("+SetTableCellBorderColor_arg_6 + " < 0.001 || " + SetTableCellBorderColor_arg_6+" > 0.999) { \n"
            SetTableCellBorderColor_constrain_7 = "if ("+SetTableCellBorderColor_arg_7 + " < 0.001 || " + SetTableCellBorderColor_arg_7+" > 0.999) { \n"
            SetTableCellBorderColor_constrain_8 = "if ("+SetTableCellBorderColor_arg_8 + " < 0.001 || " + SetTableCellBorderColor_arg_8 + " > 0.999) { \n"
            self.arg_val(SetTableCellBorderColor_arg_1, "int", SetTableCellBorderColor_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellBorderColor_arg_2, "int", SetTableCellBorderColor_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellBorderColor_arg_3, "int", SetTableCellBorderColor_constrain_3, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellBorderColor_FirstRow"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellBorderColor_arg_4, "int", SetTableCellBorderColor_constrain_4, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellBorderColor_FirstColumn"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellBorderColor_arg_5, "int", SetTableCellBorderColor_constrain_5, "4", "1")
            self.arg_val(SetTableCellBorderColor_arg_6, "double", SetTableCellBorderColor_constrain_6, "0.999", "0.001")
            self.arg_val(SetTableCellBorderColor_arg_7, "double", SetTableCellBorderColor_constrain_7, "0.999", "0.001")
            self.arg_val(SetTableCellBorderColor_arg_8, "double", SetTableCellBorderColor_constrain_8, "0.999", "0.001")
            # Call API
            self.template.write("FQL->SetTableCellBorderColor(TableID" + str(tableID)+ str(self.tag_cnt)  + ","+SetTableCellBorderColor_arg_1+","+SetTableCellBorderColor_arg_2+","+SetTableCellBorderColor_arg_3+","+SetTableCellBorderColor_arg_4+","+SetTableCellBorderColor_arg_5+","+SetTableCellBorderColor_arg_6+", "+SetTableCellBorderColor_arg_7+","+SetTableCellBorderColor_arg_8+"); \n")

        ## API : SetTableCellPadding(TableID, FirstRow, FirstColumn, LastRow,LastColumn, BorderIndex, NewPadding)
        if self.maga_info[tableID]['tab_padding'] == 1 :
            SetTableCellPadding_arg_1 = "SetTableCellPadding_FirstRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellPadding_arg_2 = "SetTableCellPadding_FirstColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellPadding_arg_3 = "SetTableCellPadding_LastRow" + str(tableID)+ str(self.tag_cnt)
            SetTableCellPadding_arg_4 = "SetTableCellPadding_LastColumn" + str(tableID)+ str(self.tag_cnt)
            SetTableCellPadding_arg_5 = "SetTableCellPadding_BorderIndex" + str(tableID)+ str(self.tag_cnt)
            SetTableCellPadding_arg_6 = "SetTableCellPadding_NewPadding" + str(tableID)+ str(self.tag_cnt)
            SetTableCellPadding_constrain_1 = "if ("+SetTableCellPadding_arg_1+" <= 0 || "+SetTableCellPadding_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellPadding_constrain_2 = "if ("+SetTableCellPadding_arg_2+" <= 0 || "+SetTableCellPadding_arg_2+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellPadding_constrain_3 = "if (" +SetTableCellPadding_arg_3 + " < "+SetTableCellPadding_arg_1+" || "+SetTableCellPadding_arg_3+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            SetTableCellPadding_constrain_4 = "if ("+SetTableCellPadding_arg_4+" < "+SetTableCellPadding_arg_2+" || "+SetTableCellPadding_arg_4+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            SetTableCellPadding_constrain_5 = "if ("+SetTableCellPadding_arg_5+" < 0 || "+SetTableCellPadding_arg_5+" > 4){\n"
            SetTableCellPadding_constrain_6 = "if ("+SetTableCellPadding_arg_6+" < 0.001 || " + SetTableCellPadding_arg_6+" > 30.001) { \n"
            self.arg_val(SetTableCellPadding_arg_1, "int", SetTableCellPadding_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellPadding_arg_2, "int", SetTableCellPadding_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "1")
            self.arg_val(SetTableCellPadding_arg_3, "int", SetTableCellPadding_constrain_3, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellPadding_FirstRow"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellPadding_arg_4, "int", SetTableCellPadding_constrain_4, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "SetTableCellPadding_FirstColumn"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(SetTableCellPadding_arg_5, "int", SetTableCellPadding_constrain_5, "4", "1")
            self.arg_val(SetTableCellPadding_arg_6, "double", SetTableCellPadding_constrain_6, "30.001", "0.001")
            # Call API
            self.template.write("FQL->SetTableCellPadding(TableID" + str(tableID) + str(self.tag_cnt) + ","+SetTableCellPadding_arg_1+","+SetTableCellPadding_arg_2+","+SetTableCellPadding_arg_3+","+SetTableCellPadding_arg_4+","+SetTableCellPadding_arg_5+","+SetTableCellPadding_arg_6+"); \n")
    def merge_cell(self, tableID) :
        if self.maga_info[tableID]['merged_cell'] != [] :
        ## API : MergeTableCells(TableID, FirstRow, FirstColumn, LastRow, LastColumn)
 
            MergeTableCells_arg_1 = "MergeTableCells_FirstRow" + str(tableID)+ str(self.tag_cnt)
            MergeTableCells_arg_2 = "MergeTableCells_FirstColumn" + str(tableID)+ str(self.tag_cnt)
            MergeTableCells_arg_3 = "MergeTableCells_LastRow" + str(tableID)+ str(self.tag_cnt)
            MergeTableCells_arg_4 = "MergeTableCells_LastColumn" + str(tableID)+ str(self.tag_cnt)
            MergeTableCells_constrain_1 = "if ("+MergeTableCells_arg_1+" <= 0 || "+MergeTableCells_arg_1+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            MergeTableCells_constrain_2 = "if ("+MergeTableCells_arg_2+" <= 0 || "+MergeTableCells_arg_2+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            MergeTableCells_constrain_3 = "if ("+ MergeTableCells_arg_3 + " < "+MergeTableCells_arg_1+" || "+MergeTableCells_arg_3+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +"){\n"
            MergeTableCells_constrain_4 = "if ("+ MergeTableCells_arg_4 + " < "+MergeTableCells_arg_2+" || "+MergeTableCells_arg_4+" > CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) +"){ \n"
            self.arg_val(MergeTableCells_arg_1, "int", MergeTableCells_constrain_1, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt)  , "1")
            self.arg_val(MergeTableCells_arg_2, "int", MergeTableCells_constrain_2, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt)  , "1")
            self.arg_val(MergeTableCells_arg_3, "int", MergeTableCells_constrain_3, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "MergeTableCells_FirstRow"+str(tableID)+ str(self.tag_cnt) )
            self.arg_val(MergeTableCells_arg_4, "int", MergeTableCells_constrain_4, "CreateTable_ColumnCount"+str(tableID)+ str(self.tag_cnt) , "MergeTableCells_FirstColumn"+str(tableID)+ str(self.tag_cnt) )
           
            # Call API
            self.template.write("FQL->MergeTableCells(TableID"+str(tableID)+ str(self.tag_cnt) +", "+MergeTableCells_arg_1+","+MergeTableCells_arg_2+","+MergeTableCells_arg_3+","+MergeTableCells_arg_4+"); \n") 
        
    def draw_tab(self, tableID) :
        ## API : DrawTableRows(TableID, Left, Top, Height, FirstRow, LastRow)
        DrawTableRows_arg_1 = "DrawTableRows_Left" + str(tableID) + str(self.tag_cnt)
        DrawTableRows_arg_2 = "DrawTableRows_Top" + str(tableID)+ str(self.tag_cnt)
        DrawTableRows_arg_3 = "DrawTableRows_Height" + str(tableID)+ str(self.tag_cnt)
        DrawTableRows_arg_4 = "DrawTableRows_FirstRow" + str(tableID)+ str(self.tag_cnt)
        DrawTableRows_arg_5 = "DrawTableRows_LastRow" + str(tableID)+ str(self.tag_cnt)
        DrawTableRows_constrain_1 = "if ("+DrawTableRows_arg_1+"<=0.001 || "+DrawTableRows_arg_1+"> PageWidth ) { \n" 
        DrawTableRows_constrain_2 = "if ("+DrawTableRows_arg_2+"<=0.001 || "+DrawTableRows_arg_2+"> PageHeight ) { \n"
        DrawTableRows_constrain_3 = "if ("+DrawTableRows_arg_3+"<=0.001 || "+DrawTableRows_arg_3+"> PageHeight ) { \n"
        DrawTableRows_constrain_4 = "if ("+DrawTableRows_arg_4+"<=0 || "+DrawTableRows_arg_4+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
        DrawTableRows_constrain_5 = "if ("+DrawTableRows_arg_5+"<0 || "+DrawTableRows_arg_5+" > CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) +") { \n"
        self.arg_val(DrawTableRows_arg_1, "double",DrawTableRows_constrain_1,"PageWidth", "0.001" )
        self.arg_val(DrawTableRows_arg_2, "double",DrawTableRows_constrain_2,"PageHeight", "0.001" )
        self.arg_val(DrawTableRows_arg_3, "double",DrawTableRows_constrain_3,"PageHeight", "0.001" )
        self.arg_val(DrawTableRows_arg_4, "int", DrawTableRows_constrain_4, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "1")
        self.arg_val(DrawTableRows_arg_5, "int", DrawTableRows_constrain_5, "CreateTable_RowCount"+str(tableID)+ str(self.tag_cnt) , "0")
        self.template.write("FQL->DrawTableRows(TableID" + str(tableID)+ str(self.tag_cnt)  + ","+DrawTableRows_arg_1+" , "+DrawTableRows_arg_2+","+DrawTableRows_arg_3+","+DrawTableRows_arg_4+","+DrawTableRows_arg_5+"); \n")
    # entry of this class
    def api_order(self) :
        self.create_tab(self.tab)
        self.extend_tab(self.tab)
        self.merge_cell(self.tab)
        self.set_cell_color(self.tab)
        self.set_tab_border(self.tab)
        self.draw_tab(self.tab)
        

