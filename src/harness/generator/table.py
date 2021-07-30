from bs4 import BeautifulSoup
import sys
import os
import string
import random
from random import choice
from string import ascii_uppercase



class HTML_TAB_STRU():
    def __init__(self, tables, styles) :
        # pass in soup's tables
        self.tables = tables
        self.styles = styles
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

    def row_col_num(self, tab, tab_id) :
        # how many columns(cells) does one row has;
        each_row_col_num = list()

        row_num = len(tab.find_all('tr'))
        # obtain each cells' number of each row and append the number to the list
        for row in tab.find_all('tr'):
            col_num = len(row.find_all('td')) + len(row.find_all('th'))
            each_row_col_num.append(col_num)
        if len(each_row_col_num) > 0 :
            col_num = max(each_row_col_num)
        else :
            col_num = 1
        self.tab_stru[tab_id] = (row_num, col_num)

    def cell_color(self, tab, tab_id) :
        self.tab_cell_color[tab_id] = list()
        self.tab_cell_content[tab_id] = list()
        self.tab_cell_font[tab_id] = list()
        row_num = 0 
        for row in tab.find_all('tr') :
            row_num += 1
            column_num = 0 
            for column in row.find_all(['th', 'td']) :
                column_num += 1
                content = ''.join(choice(ascii_uppercase) for i in range(6))
              #  try : 
              #      content = str(column.get_text()).strip().strip('/\"\\')[0:2]
              #  except ValueError:
              #      content = "1"
                self.tab_cell_content[tab_id].append((row_num, column_num, content))
                if 'background-color' in str(column) : #column.has_attr('background_color') 'background-color' in str(column) :
                    self.tab_cell_color[tab_id].append((row_num, column_num))
                if column.find_all('font') != [] :
                    self.tab_cell_font[tab_id].append((row_num, column_num))
                if column.has_attr('colspan') : #'colspan' in str(column) :
                    if column['colspan'] == "100%" :
                        column_num = self.tab_stru[tab_id][1]
                    else :
                        column_num += int(column['colspan']) - 1
    def tab_border(self, tab, style, tab_id) :
        # check if border width is set, if yes, 1
        if tab.has_attr('border') or 'border' in str(style):
            self.tab_border_width[tab_id] = 1
        else :
            self.tab_border_width[tab_id] = 0 
        if tab.has_attr('border-collapse') or 'border-collapse' in str(style) :
            self.tab_border_collapse[tab_id] = 1
        else :
            self.tab_border_collapse[tab_id] = 0 
        # check if border color is set, if yes, 1
        if tab.has_attr('bordercolor') or 'bordercolor' in str(style):
            self.tab_border_color[tab_id] = 1
        else : 
            self.tab_border_color[tab_id] = 0
        if tab.has_attr('padding') or 'padding' in str(style):
            self.tab_padding[tab_id] = 1
        else :
            self.tab_padding[tab_id] = 0
   
    def tab_merge_cell(self, tab, tab_id) :
        # check if current row has merged
        self.tab_merged_cell[tab_id] = list()
        row_num = 0
        for row in tab.find_all('tr') :
            row_num += 1
            column_num = 0
            for column in row.find_all(['th', 'td']) :
                column_num += 1
                if column.has_attr('colspan') :  #'colspan' in str(column) :
                    if column['colspan'] == '100%' :
                        self.tab_merged_cell[tab_id].append(('col', row_num, column_num, self.tab_stru[tab_id][1]-column_num + 1))
                        column_num = self.tab_stru[tab_id][1]
                    else :
                        self.tab_merged_cell[tab_id].append(('col', row_num, column_num, column['colspan']))
                        column_num += int(column['colspan']) - 1
                
                if column.has_attr('rowspan') : #'rowspan' in str(column) :
                    self.tab_merged_cell[tab_id].append(('row', row_num, column_num, column['rowspan']))
    
          
    
    # entry of this class
    def tab_parse(self) : 
        # how many tables in file
        num_tab = len(self.tables)
        # table structure
        for i in range(0, num_tab) :
            # update maga_info with TableID
            self.maga_info[i] = dict()
            # update each attributes
            self.row_col_num(self.tables[i], i)
            self.cell_color(self.tables[i], i)
            self.tab_border(self.tables[i], self.styles, i)
            self.tab_merge_cell(self.tables[i], i)
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
            # cell setting
        #print(self.maga_info)
        return self.maga_info
            
            


        
class PDF_TAB_API_MAP():
    def __init__(self, maga_info, template, tab) : 
        self.maga_info = maga_info
        self.template = template
        self.tab = tab 
   
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
        CreateTable_arg_1 = "CreateTable_RowCount" + str(tableID)
        CreateTable_arg_2 = "CreateTable_ColumnCount" + str(tableID)
        CreateTable_constrain_1 = "if (CreateTable_RowCount" + str(tableID) + " <=0 || CreateTable_RowCount" + str(tableID) + " > 150){ \n"
        CreateTable_constrain_2 = "if (CreateTable_ColumnCount" + str(tableID) + " <= 0 || CreateTable_ColumnCount" + str(tableID) + " > 150){ \n"
        self.arg_val(CreateTable_arg_1, "int", CreateTable_constrain_1, "150", "1")
        self.arg_val(CreateTable_arg_2, "int", CreateTable_constrain_2, "150", "1")
        # create each table start with its first row column number on first row
        self.template.write("int TableID" + str(tableID) + " = FQL->CreateTable("+ CreateTable_arg_1 + "," + CreateTable_arg_2 + "); \n" )

    def extend_tab(self, tableID) :
        ## API : InsertTableRows(TableID, Position, NewRowCount)
        InsertTableRows_arg_1 = "InsertTableRows_Position" + str(tableID)
        InsertTableRows_arg_2 = "InsertTableRows_NewRowCount" + str(tableID)
        InsertTableRows_constrain_1 = "if (InsertTableRows_Position"+ str(tableID) +" <= 0 || InsertTableRows_Position"+str(tableID)+" > CreateTable_RowCount"+str(tableID)+ "){ \n"
        InsertTableRows_constrain_2 = "if (InsertTableRows_NewRowCount"+ str(tableID) +" <= 0 || InsertTableRows_NewRowCount"+str(tableID)+" > 150){ \n"
        self.arg_val(InsertTableRows_arg_1, "int", InsertTableRows_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
        self.arg_val(InsertTableRows_arg_2, "int", InsertTableRows_constrain_2, "150", "1")
        self.template.write("FQL->InsertTableRows(TableID" + str(tableID) + "," + InsertTableRows_arg_1 +","+InsertTableRows_arg_2 + "); \n")
        
        ## API : InsertTableColumns(TableID, Position, NewColumnCount)
        InsertTableColumns_arg_1 = "InsertTableColumns_Position"+str(tableID)
        InsertTableColumns_arg_2 = "InsertTableColumns_NewColumnCount" + str(tableID)
        InsertTableColumns_constrain_1 = "if ("+InsertTableColumns_arg_1+" <=0 || "+ InsertTableColumns_arg_1 +" > CreateTable_ColumnCount"+str(tableID)+") { \n"
        InsertTableColumns_constrain_2 = "if ("+InsertTableColumns_arg_2+" <=0 || "+ InsertTableColumns_arg_2 +" > 150){ \n"
        self.arg_val(InsertTableColumns_arg_1, "int", InsertTableColumns_constrain_1, "CreateTable_ColumnCount"+str(tableID), "1")
        self.arg_val(InsertTableColumns_arg_2, "int", InsertTableColumns_constrain_2, "150", "1")
        self.template.write("FQL->InsertTableColumns(TableID"+str(tableID)+","+InsertTableColumns_arg_1 +","+ InsertTableColumns_arg_2 +"); \n")

        ## API : AppendTableRows(TableID, NewRowCount)
        AppendTableRows_arg_1 = "AppendTableRows_NewRowCount" + str(tableID)
        AppendTableRows_constrain_1 = "if (AppendTableRows_NewRowCount"+ str(tableID) +" <=0 || AppendTableRows_NewRowCount"+ str(tableID) +" > 150){ \n"
        self.arg_val(AppendTableRows_arg_1, "int", AppendTableRows_constrain_1, "150", "1")
        self.template.write("FQL->AppendTableRows(TableID" + str(tableID) + "," + AppendTableRows_arg_1 + ") ; \n")
        
        ## API : AppendTableColumn(TableID, NewColumnCount)
        AppendTableColumn_arg_1 = "AppendTableColumn_NewColumnCount" + str(tableID)
        AppendTableColumn_constrain_1 = "if (AppendTableColumn_NewColumnCount"+ str(tableID) +" <= 0 || AppendTableColumn_NewColumnCount" + str(tableID) +  " >150){\n"
        self.arg_val(AppendTableColumn_arg_1, "int", AppendTableColumn_constrain_1, "150", "1") 
        self.template.write("FQL->AppendTableColumns(TableID" + str(tableID) + "," + AppendTableColumn_arg_1 + ") ; \n")

        ## API : SetTableColumnWidth(TableID, FirstColumn, LastColumn)
        SetTableColumnWidth_arg_1 = "SetTableColumnWidth_FirstColumn" + str(tableID) 
        SetTableColumnWidth_constrain_1 = "if (SetTableColumnWidth_FirstColumn" + str(tableID) + "<= 0 || SetTableColumnWidth_FirstColumn" + str(tableID) + " > CreateTable_ColumnCount" + str(tableID) + "){ \n"
        SetTableColumnWidth_arg_2 = "SetTableColumnWidth_LastColumn" + str(tableID)
        SetTableColumnWidth_constrain_2 = "if (SetTableColumnWidth_LastColumn"+ str(tableID) + " < SetTableColumnWidth_FirstColumn"+ str(tableID) + " || SetTableColumnWidth_LastColumn" + str(tableID) +" > CreateTable_ColumnCount"+ str(tableID) +"){\n"
        SetTableColumnWidth_arg_3 = "SetTableColumnWidth_NewWidth" + str(tableID)
        SetTableColumnWidth_constrain_3 = "if (SetTableColumnWidth_NewWidth" + str(tableID)  + " <= 0.001 || SetTableColumnWidth_NewWidth" + str(tableID) + " > 500.001){\n"
        self.arg_val(SetTableColumnWidth_arg_1, "int", SetTableColumnWidth_constrain_1, "CreateTable_ColumnCount" + str(tableID), "1")
        self.arg_val(SetTableColumnWidth_arg_2, "int", SetTableColumnWidth_constrain_2, "CreateTable_ColumnCount"+str(tableID), "SetTableColumnWidth_FirstColumn"+str(tableID))
        self.arg_val(SetTableColumnWidth_arg_3, "double", SetTableColumnWidth_constrain_3, "500.001", "0.001" )
        self.template.write("FQL->SetTableColumnWidth(TableID" + str(tableID) + "," + SetTableColumnWidth_arg_1 + "," + SetTableColumnWidth_arg_2 + "," + SetTableColumnWidth_arg_3 + "); \n")
        
        ## API : SetTableRowHeight(TableID, FirstRow, LastRow, NewHeight)
        SetTableRowHeight_arg_1 = "SetTableRowHeight_FirstRow" + str(tableID)
        SetTableRowHeight_constrain_1 = "if ("+SetTableRowHeight_arg_1+"<=0 || "+SetTableRowHeight_arg_1 + " > CreateTable_RowCount"+str(tableID)+"){ \n"
        SetTableRowHeight_arg_2 = "SetTableRowHeight_LastRow" + str(tableID)
        SetTableRowHeight_constrain_2 = "if ("+ SetTableRowHeight_arg_2 +"< "+SetTableRowHeight_arg_1+" || "+SetTableRowHeight_arg_2+" > CreateTable_RowCount"+str(tableID)+"){\n"
        SetTableRowHeight_arg_3 = "SetTableRowHeight_NewHeight" + str(tableID)
        SetTableRowHeight_constrain_3 = "if ("+SetTableRowHeight_arg_3+" < 0.001 ||  "+ SetTableRowHeight_arg_3 +" > 500.001 ){ \n"
        self.arg_val(SetTableRowHeight_arg_1, "int", SetTableRowHeight_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
        self.arg_val(SetTableRowHeight_arg_2, "int", SetTableRowHeight_constrain_2, "CreateTable_RowCount"+str(tableID), "SetTableRowHeight_FirstRow"+str(tableID))
        self.arg_val(SetTableRowHeight_arg_3, "double", SetTableRowHeight_constrain_3, "500.001", "0.001")
        self.template.write("FQL->SetTableRowHeight(TableID"+str(tableID)+", "+SetTableRowHeight_arg_1+","+SetTableRowHeight_arg_2+","+SetTableRowHeight_arg_3+"); \n")

    def set_cell_color(self, tableID) :
        if self.maga_info[tableID]['cell_color'] != []:
            ## API : SetTableCellBackgroundColor(TableID, FirstRow, FirstColumn, LastRow, LastColumn, Red, Green, Blue) 
            SetTableCellBackgroundColor_arg_1 = "SetTableCellBackgroundColor_FirstRow"+str(tableID)
            SetTableCellBackgroundColor_arg_2 = "SetTableCellBackgroundColor_FirstColumn"+str(tableID)
            SetTableCellBackgroundColor_arg_3 = "SetTableCellBackgroundColor_LastRow"+str(tableID)
            SetTableCellBackgroundColor_arg_4 = "SetTableCellBackgroundColor_LastColumn"+str(tableID)
            SetTableCellBackgroundColor_arg_5 = "SetTableCellBackgroundColor_Red"+str(tableID)
            SetTableCellBackgroundColor_arg_6 = "SetTableCellBackgroundColor_Green" + str(tableID)
            SetTableCellBackgroundColor_arg_7 = "SetTableCellBackgroundColor_Blue" +str(tableID)
            SetTableCellBackgroundColor_constrain_1 = "if ("+SetTableCellBackgroundColor_arg_1+" <=0 || "+SetTableCellBackgroundColor_arg_1+" > CreateTable_RowCount"+str(tableID)+") { \n"
            SetTableCellBackgroundColor_constrain_2 = "if ("+SetTableCellBackgroundColor_arg_2+" <=0 || "+SetTableCellBackgroundColor_arg_2+" > CreateTable_ColumnCount"+str(tableID)+") { \n"
            SetTableCellBackgroundColor_constrain_3 = "if ("+SetTableCellBackgroundColor_arg_3+" <= "+SetTableCellBackgroundColor_arg_1+" || "+SetTableCellBackgroundColor_arg_3+" > CreateTable_RowCount"+str(tableID)+") { \n"
            SetTableCellBackgroundColor_constrain_4 = "if ("+SetTableCellBackgroundColor_arg_4+" <= "+SetTableCellBackgroundColor_arg_2+" || "+SetTableCellBackgroundColor_arg_4+" > CreateTable_ColumnCount"+str(tableID)+") { \n"
            SetTableCellBackgroundColor_constrain_5 = "if ("+SetTableCellBackgroundColor_arg_5+" < 0.001 || "+SetTableCellBackgroundColor_arg_5+" > 0.999) { \n"
            SetTableCellBackgroundColor_constrain_6 = "if ("+SetTableCellBackgroundColor_arg_6+" < 0.001 || "+SetTableCellBackgroundColor_arg_6+" > 0.999) { \n"
            SetTableCellBackgroundColor_constrain_7 = "if ("+SetTableCellBackgroundColor_arg_7+" < 0.001 || "+SetTableCellBackgroundColor_arg_7+" > 0.999) { \n"
            self.arg_val(SetTableCellBackgroundColor_arg_1, "int", SetTableCellBackgroundColor_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
            self.arg_val(SetTableCellBackgroundColor_arg_2, "int", SetTableCellBackgroundColor_constrain_2, "CreateTable_ColumnCount"+str(tableID), "1")
            self.arg_val(SetTableCellBackgroundColor_arg_3, "int", SetTableCellBackgroundColor_constrain_3, "CreateTable_RowCount"+str(tableID), "SetTableCellBackgroundColor_FirstRow" + str(tableID))
            self.arg_val(SetTableCellBackgroundColor_arg_4, "int", SetTableCellBackgroundColor_constrain_4, "CreateTable_ColumnCount"+str(tableID), "SetTableCellBackgroundColor_FirstColumn" + str(tableID))
            self.arg_val(SetTableCellBackgroundColor_arg_5, "double", SetTableCellBackgroundColor_constrain_5, "0.999", "0.001")
            self.arg_val(SetTableCellBackgroundColor_arg_6, "double", SetTableCellBackgroundColor_constrain_6, "0.999", "0.001")
            self.arg_val(SetTableCellBackgroundColor_arg_7, "double", SetTableCellBackgroundColor_constrain_7, "0.999", "0.001")
            # call API
            self.template.write("FQL->SetTableCellBackgroundColor(TableID" + str(tableID) + "," + SetTableCellBackgroundColor_arg_1 + "," + SetTableCellBackgroundColor_arg_2  + "," +SetTableCellBackgroundColor_arg_3 + "," +SetTableCellBackgroundColor_arg_4 + "," + SetTableCellBackgroundColor_arg_5 + "," + SetTableCellBackgroundColor_arg_6 + "," + SetTableCellBackgroundColor_arg_7 +"); \n")

        ## API : SetTableCellContent(TableID, RowNumber, ColumnNumber, HTMLText)
        if self.maga_info[tableID]['cell_content'] != []:
            for i in range(0, len(self.maga_info[tableID]['cell_content'])) :
                SetTableCellContent_arg_1 = "SetTableCellContent_RowNumber" + str(tableID) + str(i)
                SetTableCellContent_arg_2 = "SetTableCellContent_ColumnNumber" + str(tableID) + str(i)
                SetTableCellContent_constrain_1 = "if ("+SetTableCellContent_arg_1+" <= 0 || "+SetTableCellContent_arg_1+" > CreateTable_RowCount"+str(tableID)+"){\n"
                SetTableCellContent_constrain_2 = "if ("+SetTableCellContent_arg_2+" <= 0 || "+SetTableCellContent_arg_2+" > CreateTable_ColumnCount"+str(tableID)+"){\n"
                self.arg_val(SetTableCellContent_arg_1, "int", SetTableCellContent_constrain_1, "CreateTable_RowCount"+str(tableID), "1");
                self.arg_val(SetTableCellContent_arg_2, "int", SetTableCellContent_constrain_2, "CreateTable_ColumnCount"+str(tableID), "1");
               # Coutmized value setting for HTMLText
                self.template.write("size_t HTMLText_len" + str(tableID) +str(i) + " = 5; \n")
                self.template.write("std::string random_HTMLText" + str(tableID)+str(i) + " = random_string(HTMLText_len"+str(tableID)+str(i)+"); \n")
                self.template.write("const size_t W_HTMLText_len" + str(tableID)+str(i) + " = random_HTMLText" + str(tableID) +str(i)+ ".length() + 1; \n")
                self.template.write("wchar_t HTMLText"+str(tableID)+str(i)+"[W_HTMLText_len"+str(tableID)+str(i)+"];\n")
                self.template.write("swprintf(HTMLText"+str(tableID)+str(i)+", W_HTMLText_len"+str(tableID)+str(i)+", L\"%s\", random_HTMLText"+str(tableID)+str(i)+".c_str()) ; \n")
                self.template.write("FQL->SetTableCellContent(TableID" + str(tableID) + ", " + SetTableCellContent_arg_1 + ", " + SetTableCellContent_arg_2 + ", HTMLText"+str(tableID)+str(i)+"); \n")

        if self.maga_info[tableID]['text_font'] != [] : 
            ## API : SetTableCellTextColor(TableID, FirstRow, FirstColumn, LastRow, LastColumn, Red, Green, Blue)
            SetTableCellTextColor_arg_1 = "SetTableCellTextColor_FirstRow" + str(tableID)
            SetTableCellTextColor_arg_2 = "SetTableCellTextColor_FirstColumn" + str(tableID)
            SetTableCellTextColor_arg_3 = "SetTableCellTextColor_LastRow" + str(tableID)
            SetTableCellTextColor_arg_4 = "SetTableCellTextColor_LastColumn" + str(tableID)
            SetTableCellTextColor_arg_5 = "SetTableCellTextColor_Red" + str(tableID)
            SetTableCellTextColor_arg_6 = "SetTableCellTextColor_Green" + str(tableID)
            SetTableCellTextColor_arg_7 = "SetTableCellTextColor_Blue" + str(tableID)
            SetTableCellTextColor_constrain_1 = "if ("+SetTableCellTextColor_arg_1+" <= 0 || "+SetTableCellTextColor_arg_1+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellTextColor_constrain_2 = "if ("+SetTableCellTextColor_arg_2+" <= 0 || "+SetTableCellTextColor_arg_2+"> CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellTextColor_constrain_3 = "if (" +SetTableCellTextColor_arg_3 + " < "+SetTableCellTextColor_arg_1+" || "+SetTableCellTextColor_arg_3+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellTextColor_constrain_4 = "if ("+SetTableCellTextColor_arg_4+" < "+SetTableCellTextColor_arg_2+" || "+SetTableCellTextColor_arg_4+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellTextColor_constrain_5 = "if ("+SetTableCellTextColor_arg_5 + " < 0.001 || " + SetTableCellTextColor_arg_5+" > 0.999) { \n"
            SetTableCellTextColor_constrain_6 = "if ("+SetTableCellTextColor_arg_6 + " < 0.001 || "+SetTableCellTextColor_arg_6+" > 0.999) { \n"
            SetTableCellTextColor_constrain_7 = "if ("+SetTableCellTextColor_arg_7 + " < 0.001 || " + SetTableCellTextColor_arg_7 + " > 0.999) { \n"
            self.arg_val(SetTableCellTextColor_arg_1, "int", SetTableCellTextColor_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
            self.arg_val(SetTableCellTextColor_arg_2, "int", SetTableCellTextColor_constrain_2, "CreateTable_ColumnCount"+str(tableID), "1")
            self.arg_val(SetTableCellTextColor_arg_3, "int", SetTableCellTextColor_constrain_3, "SetTableCellTextColor_FirstRow"+str(tableID), "CreateTable_RowCount"+str(tableID))
            self.arg_val(SetTableCellTextColor_arg_4, "int", SetTableCellTextColor_constrain_4, "SetTableCellTextColor_FirstColumn"+str(tableID), "CreateTable_ColumnCount"+str(tableID))
            self.arg_val(SetTableCellTextColor_arg_5, "double", SetTableCellTextColor_constrain_5, "0.999", "0.001")
            self.arg_val(SetTableCellTextColor_arg_6, "double", SetTableCellTextColor_constrain_6, "0.999", "0.001")
            self.arg_val(SetTableCellTextColor_arg_7, "double", SetTableCellTextColor_constrain_7, "0.999", "0.001")
            # call API
            self.template.write("FQL->SetTableCellTextColor(TableID"+str(tableID)+","+ SetTableCellTextColor_arg_1+","+SetTableCellTextColor_arg_2+","+SetTableCellTextColor_arg_3+","+SetTableCellTextColor_arg_4+"," +SetTableCellTextColor_arg_5+","+SetTableCellTextColor_arg_6+","+SetTableCellTextColor_arg_7+"); \n")
            ## API : SetTableCellTextSize(TableID, FirstRow, FirstColumn,LastRow, LastColumn, NewTextSize)
            SetTableCellTextSize_arg_1 = "SetTableCellTextSize_FirstRow" + str(tableID)
            SetTableCellTextSize_arg_2 = "SetTableCellTextSize_FirstColumn" + str(tableID)
            SetTableCellTextSize_arg_3 = "SetTableCellTextSize_LastRow" + str(tableID)
            SetTableCellTextSize_arg_4 = "SetTableCellTextSize_LastColumn" + str(tableID)
            SetTableCellTextSize_arg_5 = "SetTableCellTextSize_NewTextSize" + str(tableID)
            SetTableCellTextSize_constrain_1 = "if ("+SetTableCellTextSize_arg_1+" <= 0 || "+SetTableCellTextSize_arg_1+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellTextSize_constrain_2 = "if ("+SetTableCellTextSize_arg_2+" <= 0 || "+SetTableCellTextSize_arg_2+"> CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellTextSize_constrain_3 = "if ("+SetTableCellTextSize_arg_3+" < "+SetTableCellTextSize_arg_1+" || "+SetTableCellTextSize_arg_3+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellTextSize_constrain_4 = "if ("+SetTableCellTextSize_arg_4+" < "+SetTableCellTextSize_arg_2+" || "+SetTableCellTextSize_arg_4+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellTextSize_constrain_5 = "if ("+SetTableCellTextSize_arg_5+" < 0.001 || " + SetTableCellTextSize_arg_5+" > 30.001) { \n"
            self.arg_val(SetTableCellTextSize_arg_1, "int", SetTableCellTextSize_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
            self.arg_val(SetTableCellTextSize_arg_2, "int", SetTableCellTextSize_constrain_2, "CreateTable_ColumnCount"+str(tableID), "1")
            self.arg_val(SetTableCellTextSize_arg_3, "int", SetTableCellTextSize_constrain_3, "CreateTable_RowCount"+str(tableID), "SetTableCellTextSize_FirstRow"+str(tableID))
            self.arg_val(SetTableCellTextSize_arg_4, "int", SetTableCellTextSize_constrain_4, "CreateTable_ColumnCount"+str(tableID), "SetTableCellTextSize_FirstColumn"+str(tableID))
            self.arg_val(SetTableCellTextSize_arg_5, "double", SetTableCellTextSize_constrain_5, "30.001", "0.001")
            # Call API 
            self.template.write("FQL->SetTableCellTextSize(TableID"+str(tableID)+","+ SetTableCellTextSize_arg_1+","+SetTableCellTextSize_arg_2+","+SetTableCellTextSize_arg_3+","+SetTableCellTextSize_arg_4+"," +SetTableCellTextSize_arg_5 + "); \n")
           
            

           # for cell in self.maga_info[tableID]['text_font'] :
           #     self.template.write("FQL->SetTableCellTextColor(TableID" + str(tableID) + "," + str(cell[0]) + "," + str(cell[1]) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", 0.1, 0.3, 0.5); \n")
           #     self.template.write("FQL->SetTableCellTextSize(TableID" + str(tableID) + "," + str(cell[0]) + "," + str(cell[1]) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", 0.01); \n")
    def set_tab_border(self, tableID) : 
        if self.maga_info[tableID]['border_collapse'] == 1 :
            ## API : SetTableThinkBorders(TableID, ThinBorders, Red, Green, Blue)
            SetTableThinBorders_arg_1 = "SetTableThinBorders_ThinBorders" + str(tableID)
            SetTableThinBorders_arg_2 = "SetTableThinBorders_Red" + str(tableID)
            SetTableThinBorders_arg_3 =  "SetTableThinBorders_Green" + str(tableID)
            SetTableThinBorders_arg_4 =  "SetTableThinBorders_Blue" + str(tableID)
            SetTableThinBorders_constrain_1 = "if ("+SetTableThinBorders_arg_1+" != 0 || "+SetTableThinBorders_arg_1+" != 1){ \n"
            SetTableThinBorders_constrain_2 = "if (" + SetTableThinBorders_arg_2 + " < 0.001 || " + SetTableThinBorders_arg_2 + " > 0.999) { \n"
            SetTableThinBorders_constrain_3 = "if (" + SetTableThinBorders_arg_3 + " < 0.001 || " + SetTableThinBorders_arg_3 + " > 0.999) { \n"
            SetTableThinBorders_constrain_4 ="if (" + SetTableThinBorders_arg_4 + " < 0.001 || " + SetTableThinBorders_arg_4 + " > 0.999) { \n"  
            self.arg_val(SetTableThinBorders_arg_1, "int", SetTableThinBorders_constrain_1, "1", "0")
            self.arg_val(SetTableThinBorders_arg_2, "double", SetTableThinBorders_constrain_2, "0.999", "0.001")
            self.arg_val(SetTableThinBorders_arg_3, "double", SetTableThinBorders_constrain_3, "0.999", "0.001")
            self.arg_val(SetTableThinBorders_arg_4, "double", SetTableThinBorders_constrain_4, "0.999", "0.001")
            # Call API
            self.template.write("FQL->SetTableThinBorders(TableID" + str(tableID) + ", " + SetTableThinBorders_arg_1 + ", " + SetTableThinBorders_arg_2 + ", " + SetTableThinBorders_arg_3 + ", " + SetTableThinBorders_arg_4 + "); \n")


        ## API : SetTableBorderWidth(TableID, BorderIndex, NewWidth)
        if self.maga_info[tableID]['border_width'] == 1 :
            SetTableBorderWidth_arg_1 = "SetTableBorderWidth_BorderIndex"+str(tableID)
            SetTableBorderWidth_constrain_1 = "if ("+SetTableBorderWidth_arg_1+" < 0 || "+SetTableBorderWidth_arg_1+" > 4){ \n"
            SetTableBorderWidth_arg_2 = "SetTableBorderWidth_NewWidth" + str(tableID)
            SetTableBorderWidth_constrain_2 = "if ("+SetTableBorderWidth_arg_2+" < 0.001 || "+SetTableBorderWidth_arg_2 +" > 50.001){ \n"
            self.arg_val(SetTableBorderWidth_arg_1, "int", SetTableBorderWidth_constrain_1, "4", "1")
            self.arg_val(SetTableBorderWidth_arg_2, "double", SetTableBorderWidth_constrain_2, "50.001", "0.001")

            # Call API
            self.template.write("FQL->SetTableBorderWidth(TableID" + str(tableID) + ","+SetTableBorderWidth_arg_1+","+ SetTableBorderWidth_arg_2+"); \n")

        ## API : SetTableBorderColor(TableID, BorderIndex, Red, Green, Blue)
        if self.maga_info[tableID]['border_color'] == 1 :
            SetTableBorderColor_arg_1 = "SetTableBorderColor_BorderIndex" + str(tableID)
            SetTableBorderColor_arg_2 = "SetTableBorderColor_Red" + str(tableID)
            SetTableBorderColor_arg_3 = "SetTableBorderColor_Green" + str(tableID) 
            SetTableBorderColor_arg_4 = "SetTableBorderColor_Blue" + str(tableID) 
            SetTableBorderColor_constrain_1 = "if ("+SetTableBorderColor_arg_1+" < 0 || "+SetTableBorderColor_arg_1+" > 4){ \n"           
            SetTableBorderColor_constrain_2 = "if (" + SetTableBorderColor_arg_2 + " < 0.001 || " + SetTableBorderColor_arg_2 + " > 0.999) { \n"            
            SetTableBorderColor_constrain_3 = "if (" + SetTableBorderColor_arg_3 + " < 0.001 || " + SetTableBorderColor_arg_3 + " > 0.999) { \n"             
            SetTableBorderColor_constrain_4 = "if (" + SetTableBorderColor_arg_4 + " < 0.001 || " + SetTableBorderColor_arg_4 + " > 0.999) { \n"             
            self.arg_val(SetTableBorderColor_arg_1, "int", SetTableBorderColor_constrain_1, "4", "1")
            self.arg_val(SetTableBorderColor_arg_2, "double", SetTableBorderColor_constrain_2, "0.999", "0.001")
            self.arg_val(SetTableBorderColor_arg_3, "double", SetTableBorderColor_constrain_3, "0.999", "0.001")
            self.arg_val(SetTableBorderColor_arg_4, "double", SetTableBorderColor_constrain_4, "0.999", "0.001")

            self.template.write("FQL->SetTableBorderColor(TableID" + str(tableID) + ", "+SetTableBorderColor_arg_1+","+SetTableBorderColor_arg_2+","+SetTableBorderColor_arg_3+","+SetTableBorderColor_arg_4+"); \n")

            ## API SetTableCellBorderColor(TableID, FirstRow, FirstColumn, LastRow, LastColumn, BorderIndex, Red, Green, Blue)
            
            SetTableCellBorderColor_arg_1 = "SetTableCellBorderColor_FirstRow" + str(tableID)
            SetTableCellBorderColor_arg_2 = "SetTableCellBorderColor_FirstColumn" + str(tableID)
            SetTableCellBorderColor_arg_3 = "SetTableCellBorderColor_LastRow" + str(tableID)
            SetTableCellBorderColor_arg_4 = "SetTableCellBorderColor_LastColumn" + str(tableID)
            SetTableCellBorderColor_arg_5 = "SetTableCellBorder_BorderIndex" + str(tableID)
            SetTableCellBorderColor_arg_6 = "SetTableCellBorderColor_Red" + str(tableID)
            SetTableCellBorderColor_arg_7 = "SetTableCellBorderColor_Green" + str(tableID)
            SetTableCellBorderColor_arg_8 = "SetTableCellBorderColor_Blue" + str(tableID)
            SetTableCellBorderColor_constrain_1 = "if ("+SetTableCellBorderColor_arg_1+" <= 0 || "+SetTableCellBorderColor_arg_1+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellBorderColor_constrain_2 = "if ("+SetTableCellBorderColor_arg_2+" <= 0 || "+SetTableCellBorderColor_arg_2+"> CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellBorderColor_constrain_3 = "if ("+SetTableCellBorderColor_arg_3 + " < "+SetTableCellBorderColor_arg_1+" || "+SetTableCellBorderColor_arg_3+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellBorderColor_constrain_4 = "if ("+SetTableCellBorderColor_arg_4+" < "+SetTableCellBorderColor_arg_1+" || "+SetTableCellBorderColor_arg_4+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellBorderColor_constrain_5 = "if ("+SetTableCellBorderColor_arg_5+" < 0 || "+SetTableCellBorderColor_arg_5+" > 4){\n"
            SetTableCellBorderColor_constrain_6 = "if ("+SetTableCellBorderColor_arg_6 + " < 0.001 || " + SetTableCellBorderColor_arg_6+" > 0.999) { \n"
            SetTableCellBorderColor_constrain_7 = "if ("+SetTableCellBorderColor_arg_7 + " < 0.001 || " + SetTableCellBorderColor_arg_7+" > 0.999) { \n"
            SetTableCellBorderColor_constrain_8 = "if ("+SetTableCellBorderColor_arg_8 + " < 0.001 || " + SetTableCellBorderColor_arg_8 + " > 0.999) { \n"
            self.arg_val(SetTableCellBorderColor_arg_1, "int", SetTableCellBorderColor_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
            self.arg_val(SetTableCellBorderColor_arg_2, "int", SetTableCellBorderColor_constrain_2, "CreateTable_ColumnCount"+str(tableID), "1")
            self.arg_val(SetTableCellBorderColor_arg_3, "int", SetTableCellBorderColor_constrain_3, "CreateTable_RowCount"+str(tableID), "SetTableCellBorderColor_FirstRow"+str(tableID))
            self.arg_val(SetTableCellBorderColor_arg_4, "int", SetTableCellBorderColor_constrain_4, "CreateTable_ColumnCount"+str(tableID), "SetTableCellBorderColor_FirstColumn"+str(tableID))
            self.arg_val(SetTableCellBorderColor_arg_5, "int", SetTableCellBorderColor_constrain_5, "4", "1")
            self.arg_val(SetTableCellBorderColor_arg_6, "double", SetTableCellBorderColor_constrain_6, "0.999", "0.001")
            self.arg_val(SetTableCellBorderColor_arg_7, "double", SetTableCellBorderColor_constrain_7, "0.999", "0.001")
            self.arg_val(SetTableCellBorderColor_arg_8, "double", SetTableCellBorderColor_constrain_8, "0.999", "0.001")
            # Call API
            self.template.write("FQL->SetTableCellBorderColor(TableID" + str(tableID) + ","+SetTableCellBorderColor_arg_1+","+SetTableCellBorderColor_arg_2+","+SetTableCellBorderColor_arg_3+","+SetTableCellBorderColor_arg_4+","+SetTableCellBorderColor_arg_5+","+SetTableCellBorderColor_arg_6+", "+SetTableCellBorderColor_arg_7+","+SetTableCellBorderColor_arg_8+"); \n")

        ## API : SetTableCellPadding(TableID, FirstRow, FirstColumn, LastRow,LastColumn, BorderIndex, NewPadding)
        if self.maga_info[tableID]['tab_padding'] == 1 :
            SetTableCellPadding_arg_1 = "SetTableCellPadding_FirstRow" + str(tableID)
            SetTableCellPadding_arg_2 = "SetTableCellPadding_FirstColumn" + str(tableID)
            SetTableCellPadding_arg_3 = "SetTableCellPadding_LastRow" + str(tableID)
            SetTableCellPadding_arg_4 = "SetTableCellPadding_LastColumn" + str(tableID)
            SetTableCellPadding_arg_5 = "SetTableCellPadding_BorderIndex" + str(tableID)
            SetTableCellPadding_arg_6 = "SetTableCellPadding_NewPadding" + str(tableID)
            SetTableCellPadding_constrain_1 = "if ("+SetTableCellPadding_arg_1+" <= 0 || "+SetTableCellPadding_arg_1+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellPadding_constrain_2 = "if ("+SetTableCellPadding_arg_2+" <= 0 || "+SetTableCellPadding_arg_2+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellPadding_constrain_3 = "if (" +SetTableCellPadding_arg_3 + " < "+SetTableCellPadding_arg_1+" || "+SetTableCellPadding_arg_3+" > CreateTable_RowCount"+str(tableID)+"){\n"
            SetTableCellPadding_constrain_4 = "if ("+SetTableCellPadding_arg_4+" < "+SetTableCellPadding_arg_2+" || "+SetTableCellPadding_arg_4+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            SetTableCellPadding_constrain_5 = "if ("+SetTableCellPadding_arg_5+" < 0 || "+SetTableCellPadding_arg_5+" > 4){\n"
            SetTableCellPadding_constrain_6 = "if ("+SetTableCellPadding_arg_6+" < 0.001 || " + SetTableCellPadding_arg_6+" > 30.001) { \n"
            self.arg_val(SetTableCellPadding_arg_1, "int", SetTableCellPadding_constrain_1, "CreateTable_RowCount"+str(tableID), "1")
            self.arg_val(SetTableCellPadding_arg_2, "int", SetTableCellPadding_constrain_2, "CreateTable_ColumnCount"+str(tableID), "1")
            self.arg_val(SetTableCellPadding_arg_3, "int", SetTableCellPadding_constrain_3, "CreateTable_RowCount"+str(tableID), "SetTableCellPadding_FirstRow"+str(tableID))
            self.arg_val(SetTableCellPadding_arg_4, "int", SetTableCellPadding_constrain_4, "CreateTable_ColumnCount"+str(tableID), "SetTableCellPadding_FirstColumn"+str(tableID))
            self.arg_val(SetTableCellPadding_arg_5, "int", SetTableCellPadding_constrain_5, "4", "1")
            self.arg_val(SetTableCellPadding_arg_6, "double", SetTableCellPadding_constrain_6, "30.001", "0.001")
            # Call API
            self.template.write("FQL->SetTableCellPadding(TableID" + str(tableID) + ","+SetTableCellPadding_arg_1+","+SetTableCellPadding_arg_2+","+SetTableCellPadding_arg_3+","+SetTableCellPadding_arg_4+","+SetTableCellPadding_arg_5+","+SetTableCellPadding_arg_6+"); \n")
    def merge_cell(self, tableID) :
        if self.maga_info[tableID]['merged_cell'] != [] :
        ## API : MergeTableCells(TableID, FirstRow, FirstColumn, LastRow, LastColumn)
 
            MergeTableCells_arg_1 = "MergeTableCells_FirstRow" + str(tableID)
            MergeTableCells_arg_2 = "MergeTableCells_FirstColumn" + str(tableID)
            MergeTableCells_arg_3 = "MergeTableCells_LastRow" + str(tableID)
            MergeTableCells_arg_4 = "MergeTableCells_LastColumn" + str(tableID)
            MergeTableCells_constrain_1 = "if ("+MergeTableCells_arg_1+" <= 0 || "+MergeTableCells_arg_1+" > CreateTable_RowCount"+str(tableID)+"){\n"
            MergeTableCells_constrain_2 = "if ("+MergeTableCells_arg_2+" <= 0 || "+MergeTableCells_arg_2+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            MergeTableCells_constrain_3 = "if ("+ MergeTableCells_arg_3 + " < "+MergeTableCells_arg_1+" || "+MergeTableCells_arg_3+" > CreateTable_RowCount"+str(tableID)+"){\n"
            MergeTableCells_constrain_4 = "if ("+ MergeTableCells_arg_4 + " < "+MergeTableCells_arg_2+" || "+MergeTableCells_arg_4+" > CreateTable_ColumnCount"+str(tableID)+"){ \n"
            self.arg_val(MergeTableCells_arg_1, "int", MergeTableCells_constrain_1, "CreateTable_RowCount"+str(tableID) , "1")
            self.arg_val(MergeTableCells_arg_2, "int", MergeTableCells_constrain_2, "CreateTable_ColumnCount"+str(tableID) , "1")
            self.arg_val(MergeTableCells_arg_3, "int", MergeTableCells_constrain_3, "CreateTable_RowCount"+str(tableID), "MergeTableCells_FirstRow"+str(tableID))
            self.arg_val(MergeTableCells_arg_4, "int", MergeTableCells_constrain_4, "CreateTable_ColumnCount"+str(tableID), "MergeTableCells_FirstColumn"+str(tableID))
           
            # Call API
            self.template.write("FQL->MergeTableCells(TableID"+str(tableID)+", "+MergeTableCells_arg_1+","+MergeTableCells_arg_2+","+MergeTableCells_arg_3+","+MergeTableCells_arg_4+"); \n") 
        
    def draw_tab(self, tableID) :
        ## API : DrawTableRows(TableID, Left, Top, Height, FirstRow, LastRow)
        DrawTableRows_arg_1 = "DrawTableRows_Left" + str(tableID) 
        DrawTableRows_arg_2 = "DrawTableRows_Top" + str(tableID)
        DrawTableRows_arg_3 = "DrawTableRows_Height" + str(tableID)
        DrawTableRows_arg_4 = "DrawTableRows_FirstRow" + str(tableID)
        DrawTableRows_arg_5 = "DrawTableRows_LastRow" + str(tableID)
        DrawTableRows_constrain_1 = "if ("+DrawTableRows_arg_1+"<=0.001 || "+DrawTableRows_arg_1+"> PageWidth ) { \n" 
        DrawTableRows_constrain_2 = "if ("+DrawTableRows_arg_2+"<=0.001 || "+DrawTableRows_arg_2+"> PageHeight ) { \n"
        DrawTableRows_constrain_3 = "if ("+DrawTableRows_arg_3+"<=0.001 || "+DrawTableRows_arg_3+"> PageHeight ) { \n"
        DrawTableRows_constrain_4 = "if ("+DrawTableRows_arg_4+"<=0 || "+DrawTableRows_arg_4+" > CreateTable_RowCount"+str(tableID)+") { \n"
        DrawTableRows_constrain_5 = "if ("+DrawTableRows_arg_5+"<0 || "+DrawTableRows_arg_5+" > CreateTable_RowCount"+str(tableID)+") { \n"
        self.arg_val(DrawTableRows_arg_1, "double",DrawTableRows_constrain_1,"PageWidth", "0.001" )
        self.arg_val(DrawTableRows_arg_2, "double",DrawTableRows_constrain_2,"PageHeight", "0.001" )
        self.arg_val(DrawTableRows_arg_3, "double",DrawTableRows_constrain_3,"PageHeight", "0.001" )
        self.arg_val(DrawTableRows_arg_4, "int", DrawTableRows_constrain_4, "CreateTable_RowCount"+str(tableID), "1")
        self.arg_val(DrawTableRows_arg_5, "int", DrawTableRows_constrain_5, "CreateTable_RowCount"+str(tableID), "0")
        self.template.write("FQL->DrawTableRows(TableID" + str(tableID) + ","+DrawTableRows_arg_1+" , "+DrawTableRows_arg_2+","+DrawTableRows_arg_3+","+DrawTableRows_arg_4+","+DrawTableRows_arg_5+"); \n")
    # entry of this class
    def api_order(self) :
        self.create_tab(self.tab)
        self.extend_tab(self.tab)
        self.merge_cell(self.tab)
        self.set_cell_color(self.tab)
        self.set_tab_border(self.tab)
        self.draw_tab(self.tab)
      #  for tab in self.maga_info :
      #      self.create_tab(tab)
      #      self.extend_tab(tab)
      #      self.merge_cell(tab)
      #      self.set_cell_color(tab)
      #      self.set_tab_border(tab)
      #      self.draw_tab(tab)
        

