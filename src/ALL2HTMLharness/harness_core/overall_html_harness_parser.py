import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from bs4 import BeautifulSoup, NavigableString, Tag
import os
import string
#from random import seed
#from random import random
import random
from random import choice
from string import ascii_uppercase

import vector_graphic as VG
import form as FM
import table as TAB
import text as TX
import page_stru as PS    

class GENERAL_API():
    def __init__(self, template):
        self.template = template

    def begin_line(self, foxit_loc, AFLpp_loc) :
        ######### LOADING LIBRARIES ###########################
        self.template.write("#include \"/archive/wt-4.9.0/migrate/wt_header.h\" \n")
        self.template.write("#include <iostream> \n") 
        self.template.write("#include \"dlfcn.h\" \n")
        self.template.write("#include <string.h>\n")
        self.template.write("#include <stdio.h>\n")
        self.template.write("#include <cstdio>\n")
        self.template.write("#include <iterator>\n")
        self.template.write("#include <random>\n")
        self.template.write("#include <stdint.h>\n")
        self.template.write("#include <unistd.h>\n")
        self.template.write("#include <stddef.h>\n")
        self.template.write("#include <sys/shm.h>\n")
        self.template.write("#include <dlfcn.h>\n")
        self.template.write("#include <time.h>\n")
        self.template.write("#include \"/archive/wt-4.9.0/my_examples/hello/frida-gum.h\"\n")
        self.template.write("#include \"/archive/AFL++LARGE/config.h\"\n")
        self.template.write("#ifdef __APPLE__\n")
        self.template.write("#include <mach/mach.h>\n")
        self.template.write("#include <mach-o/dyld_images.h>\n")
        self.template.write("#else\n")
        self.template.write("#include <sys/wait.h>\n")
        self.template.write("#include <sys/personality.h>\n")
        self.template.write("#endif\n")
        self.template.write("int debug = 0;\n")
        self.template.write("#define TARGET_LIBRARY \"/archive/wt-4.9.0/build_test/src/libwt.so.4.9.0\" \n")
        ############# END LOADING lIBRARY #####################

        ############# RANDOM STRING ############################

        self.template.write("using namespace Wt;\n")
        self.template.write("using namespace std; \n")
        self.template.write("std::string random_string(std::size_t length){ \n")
        self.template.write("const std::string CHARACTERS = \"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\"; \n")
        self.template.write("std::random_device random_device; \n")
        self.template.write("std::mt19937 generator(random_device()); \n")
        self.template.write("std::uniform_int_distribution<> distribution(0, CHARACTERS.size() - 1); \n")
        self.template.write("std::string random_string; \n")
        self.template.write("for (std::size_t i = 0; i < length; ++i){ \n")
        self.template.write("random_string += CHARACTERS[distribution(generator)]; \n")
        self.template.write("} \n")
        self.template.write("return random_string; \n")
        self.template.write("} \n")

        ########### END RANDOM STRING #########################

        ########### RANDOM INT ####################################
        self.template.write("int random_int(int upper, int lower){ \n")
        self.template.write("int random_int; \n")
        self.template.write("srand (time(NULL)); \n")
        self.template.write("random_int = rand() % (upper-lower + 1) + lower; \n")
        self.template.write("return random_int; \n")
        self.template.write("}\n")
        ########### END RANDOM INT ################################


        ########### RANDOM DOUBLE #################################
        self.template.write("double random_double(double upper, int lower){ \n")
        self.template.write("double random_double; \n")
        self.template.write("srand (time(NULL)); \n")
        self.template.write("random_double = (double)rand() / RAND_MAX; \n")
        self.template.write("return random_double; \n")
        self.template.write("} \n")

        ########### END RANDOM DOUBLE #############################

        ########### AFL INIT ###############################
        self.template.write("int  __afl_sharedmem_fuzzing = 1; \n")
        self.template.write("extern unsigned int * __afl_fuzz_len; \n")
        self.template.write("extern unsigned char *__afl_fuzz_ptr; \n")
        self.template.write("extern uint8_t *        __afl_area_ptr; \n")
        self.template.write("extern \"C\"{ \n")
        self.template.write("void instr_basic_block(GumStalkerIterator *iterator, GumStalkerOutput *output, gpointer user_data); \n")
        self.template.write("void afl_setup(void); \n")
        self.template.write("void afl_start_forkserver(void); \n")
        self.template.write("int  __afl_persistent_loop(unsigned int max_cnt); \n")
        self.template.write("static volatile char AFL_PERSISTENT[] = \"##SIG_AFL_PERSISTENT##\"; \n")
        self.template.write("int __afl_persistent_loop(unsigned int); \n")
        self.template.write("static volatile char AFL_DEFER_FORKSVR[] = \"##SIG_AFL_DEFER_FORKSRV##\"; \n")
        self.template.write("void __afl_manual_init(); \n")
        self.template.write("static __thread guint64 previous_pc; \n")
        self.template.write("} \n")
        ########## END AFL INIT #############################

 ########### FRIDA INIT ####################################
        self.template.write("typedef struct { \n")
        self.template.write("GumAddress base_address; \n")
        self.template.write("guint64    code_start, code_end; \n")
        self.template.write("} range_t; \n")
        self.template.write("inline static void afl_maybe_log(guint64 current_pc) { \n")
        self.template.write("current_pc = (current_pc >> 4) ^ (current_pc << 8); \n")
        self.template.write("current_pc &= MAP_SIZE - 1; \n")
        self.template.write("__afl_area_ptr[current_pc ^ previous_pc]++; \n")
        self.template.write("previous_pc = current_pc >> 1; \n")
        self.template.write("} \n")
        self.template.write("static void on_basic_block(GumCpuContext *context, gpointer user_data) { \n")
        self.template.write("afl_maybe_log((guint64)user_data); \n")
        self.template.write("} \n")
        self.template.write("void instr_basic_block(GumStalkerIterator *iterator, GumStalkerOutput *output, gpointer user_data) { \n")
        self.template.write("range_t *range = (range_t *)user_data; \n")
        self.template.write("const cs_insn *instr; \n")
        self.template.write("gboolean       begin = TRUE; \n ")
        self.template.write("while (gum_stalker_iterator_next(iterator, &instr)) { \n")
        self.template.write("if (begin) { \n")
        self.template.write("if (instr->address >= range->code_start && instr->address <= range->code_end) { \n")
        self.template.write("gum_stalker_iterator_put_callout(iterator, on_basic_block, (gpointer)instr->address, NULL); \n")
        self.template.write("begin = FALSE;")
        self.template.write("} \n")
        self.template.write("} \n")
        self.template.write("gum_stalker_iterator_keep(iterator); \n")
        self.template.write("} \n")
        self.template.write("} \n")
        self.template.write("static int enumerate_ranges(const GumRangeDetails *details, gpointer user_data) { \n")
        self.template.write("GumMemoryRange *code_range = (GumMemoryRange *)user_data; \n")
        self.template.write("memcpy(code_range, details->range, sizeof(*code_range)); \n")
        self.template.write("return 0; \n")
        self.template.write("} \n")

        ################## END FRIDA INIT ####################################


############################ START Wt ###############################
        self.template.write("class HelloApplication : public Wt::WApplication \n")


        self.template.write("{\n")
        self.template.write("public:\n")
        self.template.write("HelloApplication(const Wt::WEnvironment& env);\n")
#        self.template.write("private:\n")
#        self.template.write("Wt::WLineEdit *nameEdit_;\n")
#        self.template.write("Wt::WText     *greeting_;\n")
#        self.template.write("void greet();\n")
        self.template.write("};\n")


        self.template.write("HelloApplication::HelloApplication(const Wt::WEnvironment& env) \n" )
        self.template.write(": WApplication(env) \n" )
        self.template.write("{ \n" )
        self.template.write("setTitle(random_string(20)); \n" )

############################ END Wt ###############################
    

    def end_line(self, pdf_opt_dir) :
  ################## MAIN FUNCTION #####################################
        self.template.write("} \n" )
        self.template.write("int main(int argc, char** argv) { \n")
        self.template.write("if (!getenv(\"AFL_FRIDA_TEST_INPUT\")) { \n")
        self.template.write("gum_init_embedded(); \n")
        self.template.write("if (!gum_stalker_is_supported()) { \n")
        self.template.write("gum_deinit_embedded(); \n")
        self.template.write("return 1; \n")
        self.template.write("} \n")
        self.template.write("GumStalker *stalker = gum_stalker_new(); \n")
        self.template.write("GumAddress     base_address; \n")
        self.template.write("if (argc > 8) {\n")
        self.template.write("base_address = gum_module_find_base_address(argv[1]); \n")
        self.template.write("} else { \n")
        self.template.write("base_address = gum_module_find_base_address(TARGET_LIBRARY); \n")
        self.template.write("} \n")
        self.template.write("GumMemoryRange code_range; \n")
        self.template.write("if (argc > 8) { \n")
        self.template.write("gum_module_enumerate_ranges(argv[1], GUM_PAGE_RX, enumerate_ranges, &code_range); \n")
        self.template.write("} else { \n")
        self.template.write("gum_module_enumerate_ranges(TARGET_LIBRARY, GUM_PAGE_RX, enumerate_ranges, &code_range); \n")
        self.template.write("} \n")
        self.template.write("guint64 code_start = code_range.base_address; \n")
        self.template.write("guint64 code_end = code_range.base_address + code_range.size; \n")
        self.template.write("range_t instr_range = {0, code_start, code_end}; \n")
        self.template.write("printf(\"Frida instrumentation: base=0x%lx instrumenting=0x%lx-%lx\\n\", base_address, code_start, code_end); \n")
        self.template.write("if (!code_start || !code_end) { \n")
        self.template.write("if (argc > 8){ \n")
        self.template.write("fprintf(stderr, \"Error: no valid memory address found for %s\\n\",argv[1]); \n")
        self.template.write("} else { \n")
        self.template.write("fprintf(stderr, \"Error: no valid memory address found for %s\\n\", TARGET_LIBRARY); \n")
        self.template.write("} \n")
        self.template.write("exit(-1); \n")
        self.template.write("} \n")
        self.template.write("GumStalkerTransformer *transformer = gum_stalker_transformer_make_from_callback(instr_basic_block, &instr_range, NULL); \n")
        self.template.write("memcpy(__afl_area_ptr, (void *)AFL_PERSISTENT, sizeof(AFL_PERSISTENT) + 1); \n")
        self.template.write("memcpy(__afl_area_ptr + 32, (void *)AFL_DEFER_FORKSVR, sizeof(AFL_DEFER_FORKSVR) + 1); \n")
        self.template.write("__afl_manual_init(); \n")
        self.template.write("gum_stalker_follow_me(stalker, transformer, NULL); \n")
        self.template.write(" while (__afl_persistent_loop(1) != 0) { \n")
        self.template.write("previous_pc = 0; \n")
        self.template.write("#ifdef _DEBUG \n")
        self.template.write("fprintf(stderr, \"CLIENT crc: %016llx len: %u\\n\", hash64(__afl_fuzz_ptr, *__afl_fuzz_len), *__afl_fuzz_len); \n")
        self.template.write("fprintf(stderr, \"RECV:\"); \n")
        self.template.write("for (int i = 0; i < *__afl_fuzz_len; i++){ \n")
        self.template.write("fprintf(stderr, \"%02x\", __afl_fuzz_ptr[i]); \n")
        self.template.write("} \n")
        self.template.write("fprintf(stderr, \"\\n\"); \n")
        self.template.write("#endif \n")
        self.template.write("if (*__afl_fuzz_len > 0) { \n")
        self.template.write("__afl_fuzz_ptr[*__afl_fuzz_len] = 0; \n")
        self.template.write("} \n")
        self.template.write("} \n")

        ################## read in input + must-call APIs ################
        ###### read in input
        self.template.write("const int BUFFERSIZE = 1024 * 100 ; \n")
        self.template.write("const char * fname = argv[7]; \n")
        self.template.write("FILE* filp = fopen(fname, \"rb\"); \n")
        self.template.write("if (!filp) { \n")
        self.template.write("printf(\"Error : could not open file %s\\n\", fname); \n")
        self.template.write("return -1; \n")
        self.template.write("} \n")
        self.template.write("char  buffer[BUFFERSIZE] = {0}; \n")
        self.template.write("int bytes_read = fread(buffer, sizeof(char), BUFFERSIZE, filp); \n")
        self.template.write("fclose(filp);")
	self.template.write("gum_stalker_unfollow_me(stalker);\n")
        self.template.write("while (gum_stalker_garbage_collect(stalker))\n")
	self.template.write("{\n")
        self.template.write("        g_usleep(10000);}\n")
        self.template.write("g_object_unref(stalker);\n")
        self.template.write("g_object_unref(transformer);\n")
        self.template.write("gum_deinit_embedded();\n")
	self.template.write("}\n")
        ######## END read in input
	self.template.write("Wt::WRun(argc, argv, [](const Wt::WEnvironment &env) { \n")
	self.template.write("return std::make_unique<HelloApplication>(env); \n")
	self.template.write("}); \n")
	self.template.write("return 0; \n")
        self.template.write("} \n")
        ####### END must-call APIs

# NEW : Building the HTML strucure tree
def traverse(soup) :
    if soup is not None :
        if soup.name is not None:
           stru = [soup.name]
           for child in soup.children :
               if child.name is not None :
                   stru.append(traverse(child))
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
                       pages = soup.find(i)
                       PS.HTML_PAGE_STRU(soup.find('div'), out_f, cnt).div_parse()
                       pages.decompose()
                  # elif i in ['p', 'span', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'blockquote', 'code', 'ul', 'ol', 'dl', 'mark', 'ins', 'del', 'sup', 'sub', 'i', 'b'] :
                  #     texts = soup.find(i)
                  #     if len(texts) != 0 :
                  #          maga_info = TX.HTML_TEXT_STRU(texts).text_parse()
                  #          if len(maga_info) > 0 :
                  #              TX.PDF_TEXT_API_MAP(maga_info, out_f, cnt).api_order()
                  #     texts.decompose()
                  # elif i == 'svg' :
                  #     VGs = soup.find(i)
                  #     if len(VGs) != 0 :
                  #         maga_info_vg = VG.HTML_VGs_STRU(VGs).VG_parse()
                  #         if len(maga_info_vg) > 0 :
                  #             VG.PDF_VGs_API_MAP(maga_info_vg, out_f, cnt).api_order()
                  #     VGs.decompose()
                  # elif i == 'img' :
                  #     IMGs = soup.find(i)
                  #     if len(IMGs) != 0 :
                  #         maga_info_img = VG.HTML_IMGs_STRU(IMGs).IMG_parse()
                  #         if len(maga_info_img) > 0 :
                  #             VG.PDF_IMGs_API_MAP(maga_info_img, out_f, cnt).api_order()
                  #     IMGs.decompose()
                  # elif i == 'style' :
                  #     STYLEs = soup.find(i)
                  #     if len(STYLEs) != 0 :
                  #         maga_info_style = VG.HTML_STYLEs_STRU(STYLEs).STYLE_parse()
                  #         if len(maga_info_style) > 0 :
                  #              VG.PDF_STYLEs_API_MAP(maga_info_style, out_f, cnt).api_order()
                  #     STYLEs.decompose()
                   elif i == 'form' :
                       forms = soup.find(i)
                       if len(forms) != 0 :
                           maga_info = FM.HTML_FORM_STRU(forms).form_parse()
                           if len(maga_info) > 0 :
                               FM.PDF_FORM_API_MAP(maga_info, out_f, cnt).api_order()
                       forms.decompose()
                  # elif i == 'table' :
                  #     tables = soup.find(i)
                  #     styles = soup.find('style')
                  #     if len(tables) > 0 :
                  #         maga_info = TAB.HTML_TAB_STRU(tables, styles).tab_parse()
                  #         if len(maga_info) > 0 and len(maga_info) < 20:
                  #             tableID = 0
                  #             for tab in maga_info:
                  #             
                  #                 # if file contains table, map its structure to PDF API
                  #                 TAB.PDF_TAB_API_MAP(maga_info, out_f, tableID, cnt).api_order()
                  #                 tableID += 1
                  #     tables.decompose()
            cnt += 1
            cur_root = stru[0]

def main(argv) :
    html_file = argv[0]
    output_dir = argv[1]
    pdf_opt_dir = argv[2]
    foxit_loc = argv[3]
    AFLpp_loc = argv[4]
    file_name = str(html_file.split("/")[-1]).replace(" ","").replace(",", "").replace(".", "").replace("\\","")
    print ("@@@@@@@", file_name)
    # load in html content to soup
    in_f = open(html_file, 'r').read()
    soup = BeautifulSoup(in_f, 'lxml')

    # NEW : build DOC TREE structure
    stru_tree = traverse(soup.find('html'))

    if stru_tree != {} :
        os.makedirs(output_dir + "/" + file_name)
        out_f = open( output_dir + "/" + file_name + "/html_to_HTML_harness_template.cpp", "a")
        # Write General bein API lines in template
        GENERAL_API(out_f).begin_line(foxit_loc, AFLpp_loc)
#
#        # parsing and mapping based on DOC TREE structure
        cnt = 0
        iter_tree(soup.find('html'), stru_tree, '', out_f, cnt)
#
        GENERAL_API(out_f).end_line(pdf_opt_dir)
#    else :
#        print ("NOTHING CAN BE PARSED !")


if __name__ == "__main__" :
    main(sys.argv[1:])
