#include "/home/yifan/foxit_quick_pdf_library_1811_linux/Import/CPlusPlus/FoxitQPLLinuxCPP1811.h" 
#include "/home/yifan/foxit_quick_pdf_library_1811_linux/Import/CPlusPlus/FoxitQPLLinuxCPP1811.cpp" 
#include <iostream> 
#include <string> 
using namespace std; 
int main(int argc, char** argv) { 
std::wstring const wide(L"/home/yifan/foxit_quick_pdf_library_1811_linux/Libs/libFoxitQPL1811-linux-x64.so"); 
FoxitQPLLinuxCPP1811 * FQL = new FoxitQPLLinuxCPP1811(wide); 
cout << FQL->UnlockKey(L"jf33n75u9oj3nb9pn7mf5rt8y") << endl; 
FQL->SetGlobalOrigin(5); 
FQL->AddCJKFont(1); 
FQL->AddStandardFont(0); 
FQL->SetTextSize(6.88); 
FQL->SetTextMode(3); 
FQL->SetTextSize(6.88); 
int textID03= FQL->DrawText(100, 100, L"fqxJO1HdeSXQi"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->NewPage(); 
FQL->SetPageBox(1, 50, 50, 50, 50); 
FQL->AddCJKFont(1); 
FQL->AddStandardFont(0); 
FQL->SetTextSize(6.88); 
FQL->SetTextMode(3); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID04= FQL->DrawHTMLText(150, 150, 150, L"lH"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
int textID14= FQL->DrawText(100, 100, L"mLHP5LxtzluW2dyKtfOiEzDuBYEhuH0VxlQqBFGarhvXfTmT45x"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
int textID24= FQL->DrawText(100, 100, L"ZDazBHbLc7zYZKjeF6eL63T"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->NewPage(); 
FQL->SetPageBox(1, 50, 50, 50, 50); 
FQL->AddCJKFont(1); 
FQL->AddStandardFont(0); 
FQL->SetTextSize(6.88); 
FQL->SetTextMode(3); 
FQL->NewPage(); 
FQL->SetPageBox(1, 50, 50, 50, 50); 
FQL->AddCJKFont(1); 
FQL->AddStandardFont(0); 
FQL->SetTextSize(6.88); 
FQL->SetTextMode(3); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID06= FQL->DrawHTMLText(150, 150, 150, L"n0"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID16= FQL->DrawHTMLText(150, 150, 150, L"eq"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID26= FQL->DrawHTMLText(150, 150, 150, L"V0"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID36= FQL->DrawHTMLText(150, 150, 150, L"nQ"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID46= FQL->DrawHTMLText(150, 150, 150, L"nk"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID56= FQL->DrawHTMLText(150, 150, 150, L"vQ"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID66= FQL->DrawHTMLText(150, 150, 150, L"Xx"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID76= FQL->DrawHTMLText(150, 150, 150, L"MA"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID86= FQL->DrawHTMLText(150, 150, 150, L"uj"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID96= FQL->DrawHTMLText(150, 150, 150, L"Ko"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
FQL->SetTextSize(6.88); 
FQL->SetHTMLBoldFont(L"Default", 2); 
int textID106= FQL->DrawHTMLText(150, 150, 150, L"G7"); 
FQL->AppendSpace(2.68); 
FQL->SetTextCharSpacing(5.68); 
int formID006 = FQL->NewFormField( L"ljssr", 1); 
FQL->SetFormFieldValue(formID006,  L"bkkzv"); 
FQL->SetFormFieldBounds(formID006, 20 ,0, 100, 20); 
FQL->SetFormFieldAlignment(formID006, 2 ); 
int formID016 = FQL->NewFormField( L"zxhug", 3); 
FQL->SetFormFieldCheckStyle(formID016, 2, 0); 
FQL->SetFormFieldBounds(formID016, 20 ,20, 100, 20); 
FQL->SetFormFieldValue(formID016,  L"fpziy"); 
FQL->SetFormFieldBorderColor(formID016, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID016, 0.8, 0.5, 0.2); 
int formID026 = FQL->NewFormField( L"wafix", 3); 
FQL->SetFormFieldCheckStyle(formID026, 2, 0); 
FQL->SetFormFieldBounds(formID026, 20 ,40, 100, 20); 
FQL->SetFormFieldValue(formID026,  L"umqsh"); 
FQL->SetFormFieldBorderColor(formID026, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID026, 0.8, 0.5, 0.2); 
int formID036 = FQL->NewFormField( L"iiezh", 3); 
FQL->SetFormFieldCheckStyle(formID036, 2, 0); 
FQL->SetFormFieldBounds(formID036, 20 ,60, 100, 20); 
FQL->SetFormFieldValue(formID036,  L"kbczv"); 
FQL->SetFormFieldBorderColor(formID036, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID036, 0.8, 0.5, 0.2); 
int formID076 = FQL->NewFormField( L"djbve", 2); 
FQL->SetFormFieldBounds(formID076, 20 ,140, 100, 20); 
int FontID076=FQL->AddStandardFont(5); 
FQL->SetTextSize(10); 
FQL->AddFormFont(FontID076); 
FQL->SetFormFieldFont(formID076, FQL->GetFormFontCount()); 
FQL->SetFormFieldTextSize(formID076, 12); 
FQL->SetFormFieldValue(formID076,  L"pkjrz"); 
FQL->SetFormFieldAlignment(formID076, 2 ); 
FQL->SetFormFieldBorderColor(formID076, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID076, 0.8, 0.5, 0.2); 
FQL->SetFormFieldBorderStyle(formID076,1, 0 ,0 ,0 ); 
FQL->SetFormFieldHighlightMode(formID076, 3); 
FQL->FormFieldJavaScriptAction(formID076, L"U",L"lwvxn" ); 
int formID096 = FQL->NewFormField( L"gmzlg", 5); 
FQL-> SetFormFieldChoiceType(formID096, 4);
FQL->SetFormFieldBounds(formID096, 20 ,180, 100, 20); 
FQL->SetFormFieldBorderStyle(formID096,1, 0 ,0 ,0 ); 
int formID0960choice = FQL -> AddFormFieldChoiceSub(formID096, L"qvfjv", L"qvfjv"); 
int formID0961choice = FQL -> AddFormFieldChoiceSub(formID096, L"usoqb", L"usoqb"); 
int formID0962choice = FQL -> AddFormFieldChoiceSub(formID096, L"hfdgh", L"hfdgh"); 
int formID0963choice = FQL -> AddFormFieldChoiceSub(formID096, L"epscf", L"epscf"); 
int formID0964choice = FQL -> AddFormFieldChoiceSub(formID096, L"iuwts", L"iuwts"); 
int formID156 = FQL->NewFormField( L"akmpl", 6); 
FQL->SetFormFieldBounds(formID156, 20 ,100, 100, 20); 
FQL->SetFormFieldBorderStyle(formID156,1, 0 ,0 ,0 ); 
int formIDgender2main6 = FQL->NewFormField(L"jokkj", 4); 
int formIDgender206 = FQL->AddFormFieldSub(formIDgender2main6, L"jokkj06"); 
FQL->SetFormFieldBounds(formIDgender206, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender206, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender206, 0.8, 0.5, 0.2); 
int formIDgender3main6 = FQL->NewFormField(L"wkgur", 4); 
int formIDgender306 = FQL->AddFormFieldSub(formIDgender3main6, L"wkgur06"); 
FQL->SetFormFieldBounds(formIDgender306, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender306, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender306, 0.8, 0.5, 0.2); 
int formIDgender1main6 = FQL->NewFormField(L"nbviq", 4); 
int formIDgender106 = FQL->AddFormFieldSub(formIDgender1main6, L"nbviq06"); 
FQL->SetFormFieldBounds(formIDgender106, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender106, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender106, 0.8, 0.5, 0.2); 
int formIDgendermain6 = FQL->NewFormField(L"ycyon", 4); 
int formIDgender06 = FQL->AddFormFieldSub(formIDgendermain6, L"ycyon06"); 
FQL->SetFormFieldBounds(formIDgender06, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender06, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender06, 0.8, 0.5, 0.2); 
int formIDgender16 = FQL->AddFormFieldSub(formIDgendermain6, L"ycyon16"); 
FQL->SetFormFieldBounds(formIDgender16, 20 ,20, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender16, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender16, 0.8, 0.5, 0.2); 
int formIDgender26 = FQL->AddFormFieldSub(formIDgendermain6, L"ycyon26"); 
FQL->SetFormFieldBounds(formIDgender26, 20 ,40, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender26, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender26, 0.8, 0.5, 0.2); 
FQL->NewPage(); 
FQL->SetPageBox(1, 50, 50, 50, 50); 
FQL->SetFillColor(0.356957628096,0.164712484925,0.0200242445703); 
int circle0circle007 = FQL->DrawCircle(50, 50,40, 2 ); 
FQL->SetFillColor(0.835371122202,0.0476181081616,0.771391501089); 
int rect1rect107 = FQL->DrawBox(0, 0, 400, 100, 2);
FQL->SetFillColor(0.87618206888,0.0424824569371,0.52576742187); 
int rect_round2rect207 = FQL->DrawRoundedBox(50, 20, 150,150, 15, 2); 
 FQL->SetFillColor(0.935762529003,0.461667618704,0.770415444093); 
FQL->StartPath(100, 10); 
FQL->AddLineToPath(40, 198); 
FQL->DrawLine(100, 10,40, 198); 
FQL->StartPath(40, 198); 
FQL->AddLineToPath(190, 78); 
FQL->DrawLine(40, 198,190, 78); 
FQL->StartPath(190, 78); 
FQL->AddLineToPath(10, 78); 
FQL->DrawLine(190, 78,10, 78); 
FQL->StartPath(10, 78); 
FQL->AddLineToPath(160, 198); 
FQL->DrawLine(10, 78,160, 198); 
FQL->StartPath(160, 198); 
FQL->AddLineToPath(100, 10); 
FQL->DrawLine(160, 198,100, 10); 
FQL->SetFillColor(0.350387965488,0.880930898711,0.332340808214); 
int ellipse4ellipse407 = FQL->DrawEllipse(50, 500, 100, 70, 2); 
FQL->NewPage(); 
FQL->SetPageBox(1, 50, 50, 50, 50); 
int TableID08 = FQL->CreateTable(1, 1); 
FQL->AppendTableRows(TableID08,4) ; 
FQL->AppendTableColumns(TableID08,3) ; 
FQL->SetTableColumnWidth(TableID08,1,4, 185); 
FQL->SetTableRowHeight(TableID08,1,5, 8); 
FQL->MergeTableCells(TableID08,2,1,3,1); 
FQL->MergeTableCells(TableID08,4,1,5,1); 
FQL->SetTableCellContent(TableID08, 1, 1, L"IRKLIO"); 
FQL->SetTableCellContent(TableID08, 1, 2, L"UBKWYW"); 
FQL->SetTableCellContent(TableID08, 1, 3, L"FSESKX"); 
FQL->SetTableCellContent(TableID08, 1, 4, L"HCPWEQ"); 
FQL->SetTableCellContent(TableID08, 2, 1, L"MLHZNM"); 
FQL->SetTableCellContent(TableID08, 2, 2, L"TCFBXR"); 
FQL->SetTableCellContent(TableID08, 2, 3, L"PXISDU"); 
FQL->SetTableCellContent(TableID08, 2, 4, L"QDXLSA"); 
FQL->SetTableCellContent(TableID08, 3, 1, L"KEIWBF"); 
FQL->SetTableCellContent(TableID08, 3, 2, L"DIQNJA"); 
FQL->SetTableCellContent(TableID08, 3, 3, L"HLQOQW"); 
FQL->SetTableCellContent(TableID08, 4, 1, L"LIADXO"); 
FQL->SetTableCellContent(TableID08, 4, 2, L"ECFZTZ"); 
FQL->SetTableCellContent(TableID08, 4, 3, L"LMPIAD"); 
FQL->SetTableCellContent(TableID08, 4, 4, L"XVQAKI"); 
FQL->SetTableCellContent(TableID08, 5, 1, L"GJTCKC"); 
FQL->SetTableCellContent(TableID08, 5, 2, L"QNIMDM"); 
FQL->SetTableCellContent(TableID08, 5, 3, L"WNAJKK"); 
FQL->DrawTableRows(TableID08,36 ,36 ,FQL->PageHeight(), 1 ,0); 
int formID009 = FQL->NewFormField( L"bbkbx", 1); 
FQL->SetFormFieldValue(formID009,  L"ppeof"); 
FQL->SetFormFieldBounds(formID009, 20 ,0, 100, 20); 
FQL->SetFormFieldAlignment(formID009, 2 ); 
int formID019 = FQL->NewFormField( L"qwizw", 3); 
FQL->SetFormFieldCheckStyle(formID019, 2, 0); 
FQL->SetFormFieldBounds(formID019, 20 ,20, 100, 20); 
FQL->SetFormFieldValue(formID019,  L"enrwt"); 
FQL->SetFormFieldBorderColor(formID019, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID019, 0.8, 0.5, 0.2); 
int formID029 = FQL->NewFormField( L"ijsrj", 3); 
FQL->SetFormFieldCheckStyle(formID029, 2, 0); 
FQL->SetFormFieldBounds(formID029, 20 ,40, 100, 20); 
FQL->SetFormFieldValue(formID029,  L"ttjtp"); 
FQL->SetFormFieldBorderColor(formID029, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID029, 0.8, 0.5, 0.2); 
int formID039 = FQL->NewFormField( L"vqqzd", 3); 
FQL->SetFormFieldCheckStyle(formID039, 2, 0); 
FQL->SetFormFieldBounds(formID039, 20 ,60, 100, 20); 
FQL->SetFormFieldValue(formID039,  L"zpmox"); 
FQL->SetFormFieldBorderColor(formID039, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID039, 0.8, 0.5, 0.2); 
int formID079 = FQL->NewFormField( L"yrory", 2); 
FQL->SetFormFieldBounds(formID079, 20 ,140, 100, 20); 
int FontID079=FQL->AddStandardFont(5); 
FQL->SetTextSize(10); 
FQL->AddFormFont(FontID079); 
FQL->SetFormFieldFont(formID079, FQL->GetFormFontCount()); 
FQL->SetFormFieldTextSize(formID079, 12); 
FQL->SetFormFieldValue(formID079,  L"etvyy"); 
FQL->SetFormFieldAlignment(formID079, 2 ); 
FQL->SetFormFieldBorderColor(formID079, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formID079, 0.8, 0.5, 0.2); 
FQL->SetFormFieldBorderStyle(formID079,1, 0 ,0 ,0 ); 
FQL->SetFormFieldHighlightMode(formID079, 3); 
FQL->FormFieldJavaScriptAction(formID079, L"U",L"vaqmb" ); 
int formID099 = FQL->NewFormField( L"wojwf", 5); 
FQL-> SetFormFieldChoiceType(formID099, 4);
FQL->SetFormFieldBounds(formID099, 20 ,180, 100, 20); 
FQL->SetFormFieldBorderStyle(formID099,1, 0 ,0 ,0 ); 
int formID0990choice = FQL -> AddFormFieldChoiceSub(formID099, L"ktsuf", L"ktsuf"); 
int formID0991choice = FQL -> AddFormFieldChoiceSub(formID099, L"siqjn", L"siqjn"); 
int formID0992choice = FQL -> AddFormFieldChoiceSub(formID099, L"fmjad", L"fmjad"); 
int formID0993choice = FQL -> AddFormFieldChoiceSub(formID099, L"sivmz", L"sivmz"); 
int formID0994choice = FQL -> AddFormFieldChoiceSub(formID099, L"sndhd", L"sndhd"); 
int formIDgender2main9 = FQL->NewFormField(L"fjwqr", 4); 
int formIDgender209 = FQL->AddFormFieldSub(formIDgender2main9, L"fjwqr09"); 
FQL->SetFormFieldBounds(formIDgender209, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender209, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender209, 0.8, 0.5, 0.2); 
int formIDgender3main9 = FQL->NewFormField(L"ucvek", 4); 
int formIDgender309 = FQL->AddFormFieldSub(formIDgender3main9, L"ucvek09"); 
FQL->SetFormFieldBounds(formIDgender309, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender309, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender309, 0.8, 0.5, 0.2); 
int formIDgender1main9 = FQL->NewFormField(L"ehcdd", 4); 
int formIDgender109 = FQL->AddFormFieldSub(formIDgender1main9, L"ehcdd09"); 
FQL->SetFormFieldBounds(formIDgender109, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender109, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender109, 0.8, 0.5, 0.2); 
int formID0511 = FQL->NewFormField( L"omqum", 6); 
FQL->SetFormFieldBounds(formID0511, 20 ,100, 100, 20); 
FQL->SetFormFieldBorderStyle(formID0511,1, 0 ,0 ,0 ); 
int formIDgendermain11 = FQL->NewFormField(L"mmgzq", 4); 
int formIDgender011 = FQL->AddFormFieldSub(formIDgendermain11, L"mmgzq011"); 
FQL->SetFormFieldBounds(formIDgender011, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender011, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender011, 0.8, 0.5, 0.2); 
int formIDgender111 = FQL->AddFormFieldSub(formIDgendermain11, L"mmgzq111"); 
FQL->SetFormFieldBounds(formIDgender111, 20 ,20, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender111, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender111, 0.8, 0.5, 0.2); 
int formIDgender211 = FQL->AddFormFieldSub(formIDgendermain11, L"mmgzq211"); 
FQL->SetFormFieldBounds(formIDgender211, 20 ,40, 100, 20); 
FQL->SetFormFieldBorderColor(formIDgender211, 0.2, 0.5, 0.8); 
FQL->SetFormFieldBackgroundColor(formIDgender211, 0.8, 0.5, 0.2); 
int formID0012 = FQL->NewFormField( L"erhxr", 5); 
FQL-> SetFormFieldChoiceType(formID0012, 4);
FQL->SetFormFieldBounds(formID0012, 20 ,0, 100, 20); 
FQL->SetFormFieldBorderStyle(formID0012,1, 0 ,0 ,0 ); 
int formID00120choice = FQL -> AddFormFieldChoiceSub(formID0012, L"vunvu", L"vunvu"); 
int formID00121choice = FQL -> AddFormFieldChoiceSub(formID0012, L"hqnfz", L"hqnfz"); 
int formID00122choice = FQL -> AddFormFieldChoiceSub(formID0012, L"cyxit", L"cyxit"); 
std::string opt_random = "./" +  std::string("PDF.pdf"); 
const size_t len = opt_random.length() + 1; 
wchar_t opt_name[len]; 
swprintf(opt_name, len, L"%s", opt_random.c_str()); 
FQL->SaveToFile(opt_name); 
return 0;
} 
