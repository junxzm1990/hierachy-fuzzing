from bs4 import BeautifulSoup, NavigableString, Tag
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
                if column.has_attr('background_color') : #'background-color' in str(column) :
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
        print ("*****************", type(self.tables))
        num_tab = len(self.tables)
        print ("LOOK HERE ~~~~~~~~~~~~~~~~~~~~~~",num_tab)
        # update maga_info with TableID
        if isinstance(self.tables, Tag) :
            self.maga_info[0] = dict()
            # update each attributes
            self.row_col_num(self.tables, 0)
            self.cell_color(self.tables, 0)
            self.tab_border(self.tables, self.styles, 0)
            self.tab_merge_cell(self.tables, 0)
            # adding attributes to current handling table in maga_info
            self.maga_info[0]['row_col_num']=self.tab_stru[0]
            self.maga_info[0]['cell_color']=self.tab_cell_color[0]
            self.maga_info[0]['cell_content']=self.tab_cell_content[0]
            self.maga_info[0]['border_width']=self.tab_border_width[0]
            self.maga_info[0]['border_collapse']=self.tab_border_collapse[0]
            self.maga_info[0]['border_color']=self.tab_border_color[0]
            self.maga_info[0]['tab_padding']=self.tab_padding[0]
            self.maga_info[0]['merged_cell']=self.tab_merged_cell[0]
            self.maga_info[0]['text_font']=self.tab_cell_font[0]
        else :
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
    def __init__(self, maga_info, template, tag_cnt) : 
        self.maga_info = maga_info
        self.template = template
        self.tag_cnt = tag_cnt
    def create_tab(self, tableID) :
        # create each table start with its first row column number on first row
        self.template.write("int TableID" + str(tableID) + str(self.tag_cnt) + " = FQL->CreateTable(1, 1); \n" )
    def extend_tab(self, tableID) :
        self.template.write("FQL->AppendTableRows(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(self.maga_info[tableID]['row_col_num'][0]-1) + ") ; \n")
        self.template.write("FQL->AppendTableColumns(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(self.maga_info[tableID]['row_col_num'][1]-1) + ") ; \n")
        self.template.write("FQL->SetTableColumnWidth(TableID" + str(tableID) + str(self.tag_cnt) + ",1," + str(self.maga_info[tableID]['row_col_num'][1]) + ", 185); \n")
        self.template.write("FQL->SetTableRowHeight(TableID" + str(tableID) + str(self.tag_cnt) + ",1," + str(self.maga_info[tableID]['row_col_num'][0]) + ", 8); \n")
    def set_cell_color(self, tableID) :
        if self.maga_info[tableID]['cell_color'] != []:
            for cell in self.maga_info[tableID]['cell_color']:
                self.template.write("FQL->SetTableCellBackgroundColor(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(cell[0]) + "," + str(cell[1]) + "," + str(cell[0]) + "," + str(cell[1]) + "," + "0.2" + "," + "0.3" + "," + "0.5); \n")
        if self.maga_info[tableID]['cell_content'] != []:
            for cell in self.maga_info[tableID]['cell_content'] :
                self.template.write("FQL->SetTableCellContent(TableID" + str(tableID) + str(self.tag_cnt) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", L" + "\"" + str(cell[2]) + "\"" + "); \n")
        if self.maga_info[tableID]['text_font'] != [] : 
            for cell in self.maga_info[tableID]['text_font'] :
                self.template.write("FQL->SetTableCellTextColor(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(cell[0]) + "," + str(cell[1]) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", 0.1, 0.3, 0.5); \n")
                self.template.write("FQL->SetTableCellTextSize(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(cell[0]) + "," + str(cell[1]) + ", " + str(cell[0]) + ", " + str(cell[1]) + ", 0.01); \n")
    def set_tab_border(self, tableID) : 
        if self.maga_info[tableID]['border_collapse'] == 1 :
            self.template.write("FQL->SetTableThinBorders(TableID" + str(tableID) + str(self.tag_cnt) + ", 1, 0 , 0, 0); \n")
        if self.maga_info[tableID]['border_width'] == 1 :
            self.template.write("FQL->SetTableBorderWidth(TableID" + str(tableID) + str(self.tag_cnt) + ", 0, 10); \n")
        if self.maga_info[tableID]['border_color'] == 1 : 
            self.template.write("FQL->SetTableBorderColor(TableID" + str(tableID) + str(self.tag_cnt) + ", 0, 0.2, 0.3, 0.5); \n")
            self.template.write("FQL->SetTableCellBorderColor(TableID" + str(tableID) + str(self.tag_cnt) + ", 1, 1, FQL->GetTableRowCount(TableID" + str(tableID) + str(self.tag_cnt) + "), FQL->GetTableColumnCount(TableID" + str(tableID) + str(self.tag_cnt) + "), 0, 0.2, 0.3, 0.5); \n")
        if self.maga_info[tableID]['tab_padding'] == 1 :
            self.template.write("FQL->SetTableCellPadding(TableID" + str(tableID) + str(self.tag_cnt) + ", 1, 1, FQL->GetTableRowCount(TableID" + str(tableID) + str(self.tag_cnt) + "), FQL->GetTableColumnCount(TableID" + str(tableID) + str(self.tag_cnt) + "), 1, 10 ); \n")
    def merge_cell(self, tableID) :
        if self.maga_info[tableID]['merged_cell'] != [] :
            for cell in self.maga_info[tableID]['merged_cell']:
                if cell[0] == 'row' : 
                    self.template.write("FQL->MergeTableCells(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(cell[1]) + "," + str(cell[2]) + "," + str(cell[1]+int(cell[3])-1) + "," + str(cell[2]) + "); \n")
                if cell[0] == 'col' :
                    self.template.write("FQL->MergeTableCells(TableID" + str(tableID) + str(self.tag_cnt) + "," + str(cell[1]) + "," + str(cell[2]) + "," + str(cell[1]) + "," + str(cell[2]+int(cell[3])-1) + "); \n")
        
    def draw_tab(self, tableID) :
        self.template.write("FQL->DrawTableRows(TableID" + str(tableID) + str(self.tag_cnt) + ",36 ,36 ,FQL->PageHeight(), 1 ,0); \n")
    # entry of this class
    def api_order(self) :
        for tab in self.maga_info :
            self.create_tab(tab)
            self.extend_tab(tab)
            self.merge_cell(tab)
            self.set_cell_color(tab)
            self.set_tab_border(tab)
            self.draw_tab(tab)
        
