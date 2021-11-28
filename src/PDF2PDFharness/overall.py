import sys
import os
from PyPDF2 import PdfFileReader

import page_stru as PS
import form as FM

class GENERAL_API():
    def __init__(self, template):
        self.template = template

    def begin_line(self, foxit_loc, AFLpp_loc) :
        ######### LOADING LIBRARIES ###########################
        self.template.write("#include \"" + foxit_loc + "/Import/CPlusPlus/FoxitQPLLinuxCPP1811.h\" \n")
        self.template.write("#include \"" + foxit_loc + "/Import/CPlusPlus/FoxitQPLLinuxCPP1811.cpp\" \n")
        self.template.write("#include \"dlfcn.h\" \n")
        self.template.write("#include <string.h> \n")
        self.template.write("#include <iostream> \n")
        self.template.write("#include <stdio.h> \n")
        self.template.write("#include <stdlib.h>     /* srand, rand */ \n")
        self.template.write("#include <time.h>       /* time */ \n" )
        self.template.write("#include <cstdio> \n")
        self.template.write("#include <iterator> \n")
        self.template.write("#include <random> \n")
        self.template.write("#include <stdint.h> \n")
        self.template.write("#include <unistd.h> \n")
        self.template.write("#include <stddef.h> \n")
        self.template.write("#include <sys/shm.h> \n")
        self.template.write("#include <dlfcn.h> \n")
        self.template.write("#include \"" + AFLpp_loc  + "/utils/afl_frida_pdf/frida-gum.h\" \n")
        self.template.write("#include \"" + AFLpp_loc + "/config.h\" \n")
        self.template.write("#ifdef __APPLE__ \n")
        self.template.write("#include <mach/mach.h> \n")
        self.template.write("#include <mach-o/dyld_images.h> \n")
        self.template.write("#else \n")
        self.template.write("#include <sys/wait.h> \n")
        self.template.write("#include <sys/personality.h> \n")
        self.template.write("#endif \n")
        self.template.write("int debug = 0; \n")
        self.template.write("#define TARGET_LIBRARY \"" + foxit_loc + "/Libs/libFoxitQPL1811-linux-x64.so\" \n")
        ############# END LOADING lIBRARY #####################

        ############# RANDOM STRING ############################

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


        ################## MAIN FUNCTION #####################################
        self.template.write("using namespace std; \n")
        self.template.write("int main(int argc, char** argv) { \n")
        self.template.write("std::wstring const wide(L\"" + foxit_loc + "/Libs/libFoxitQPL1811-linux-x64.so\"); \n")
        self.template.write("FoxitQPLLinuxCPP1811 * FQL = new FoxitQPLLinuxCPP1811(wide); \n")
        self.template.write("cout << FQL->UnlockKey(L\"jf33n75u9oj3nb9pn7mf5rt8y\") << endl; \n")
        self.template.write("if (!getenv(\"AFL_FRIDA_TEST_INPUT\")) { \n")
        self.template.write("gum_init_embedded(); \n")
        self.template.write("if (!gum_stalker_is_supported()) { \n")
        self.template.write("gum_deinit_embedded(); \n")
        self.template.write("return 1; \n")
        self.template.write("} \n")
        self.template.write("GumStalker *stalker = gum_stalker_new(); \n")
        self.template.write("GumAddress     base_address; \n")
        self.template.write("if (argc > 2) {\n")
        self.template.write("base_address = gum_module_find_base_address(argv[1]); \n")
        self.template.write("} else { \n")
        self.template.write("base_address = gum_module_find_base_address(TARGET_LIBRARY); \n")
        self.template.write("} \n")
        self.template.write("GumMemoryRange code_range; \n")
        self.template.write("if (argc > 2) { \n")
        self.template.write("gum_module_enumerate_ranges(argv[1], GUM_PAGE_RX, enumerate_ranges, &code_range); \n")
        self.template.write("} else { \n")
        self.template.write("gum_module_enumerate_ranges(TARGET_LIBRARY, GUM_PAGE_RX, enumerate_ranges, &code_range); \n")
        self.template.write("} \n")
        self.template.write("guint64 code_start = code_range.base_address; \n")
        self.template.write("guint64 code_end = code_range.base_address + code_range.size; \n")
        self.template.write("range_t instr_range = {0, code_start, code_end}; \n")
        self.template.write("printf(\"Frida instrumentation: base=0x%lx instrumenting=0x%lx-%lx\\n\", base_address, code_start, code_end); \n")
        self.template.write("if (!code_start || !code_end) { \n")
        self.template.write("if (argc > 2){ \n")
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


        ################### read in input + must-call APIs ################
        ####### read in input
        self.template.write("const int BUFFERSIZE = 1024 * 100 ; \n")
        self.template.write("const char * fname = argv[1]; \n")
        self.template.write("FILE* filp = fopen(fname, \"rb\"); \n")
        self.template.write("if (!filp) { \n")
        self.template.write("printf(\"Error : could not open file %s\\n\", fname); \n")
        self.template.write("return -1; \n")
        self.template.write("} \n")
        self.template.write("char  buffer[BUFFERSIZE] = {0}; \n")
        self.template.write("int bytes_read = fread(buffer, sizeof(char), BUFFERSIZE, filp); \n")
        self.template.write("fclose(filp);")
        ####### END read in input
        ####### Must-call APIs 
        self.template.write("double PageHeight = FQL->PageHeight(); \n")
        self.template.write("double PageWidth = FQL->PageWidth(); \n")
        ## init index on buffer
        self.template.write("int index = 0; \n")
        ## init SetTableOrigin's args
        self.template.write("int Origin = 0; \n")
        self.template.write("if (bytes_read - index >= sizeof(int)){ \n")
        self.template.write("memcpy(&Origin, buffer + index, sizeof(int)); \n")
        self.template.write("if (Origin <= 0 || Origin >= PageWidth || Origin >= PageHeight){ \n")
        self.template.write("exit(0); \n")
        self.template.write("}else{ \n")
        self.template.write("index += sizeof(int); \n")
        self.template.write("} \n")
        self.template.write("}else{ \n")
        self.template.write("exit(0); \n")
        self.template.write("}\n")
        self.template.write("FQL->SetOrigin(Origin); \n")
        ###### END must-call APIs


    def end_line(self, pdf_opt_dir) :
        ############### Must-call APIs at end ###################
        ## init arg of SaveToFile API
        self.template.write("size_t name_len = 12; \n")
        self.template.write("std::string opt_random = \""+str(pdf_opt_dir)+"\" + random_string(name_len) + \".pdf\"; \n")
        self.template.write("const size_t len = opt_random.length() + 1; \n")
        self.template.write("wchar_t opt_name[len]; \n")
        self.template.write("swprintf(opt_name, len, L\"%s\", opt_random.c_str()); \n")
        self.template.write("FQL->SaveToFile(opt_name); \n")
        ############# END MUT-call APIs at end #################

        ############# FRIDA at end #############################
        self.template.write("gum_stalker_unfollow_me(stalker); \n")
        self.template.write("while (gum_stalker_garbage_collect(stalker)){ \n")
        self.template.write("g_usleep(10000);} \n")
        self.template.write("g_object_unref(stalker); \n")
        self.template.write("g_object_unref(transformer); \n")
        self.template.write("gum_deinit_embedded(); \n")
        self.template.write("} \n")
        self.template.write("return 0;\n")
        self.template.write("} \n")
        ############# FRIDA end ################################# 




############ entrance and related funcs #######################################

def page_stru(pdf_file, template) :

    ck_malform = 0 

    try :
        PdfFileReader(open(pdf_file,'rb'))
        ck_malform = 1
    except :
        print ("Malform!!!")
        pass

    if ck_malform == 1:
        pdf = PdfFileReader(open(pdf_file,'rb'), strict=False)
        # FORM : PARSE AND MAP through whole pdf (since forms cannot parsed precisely from each individual page)
        fm_fields = pdf.getFields()
        if fm_fields != None :
            fm_maga_info = FM.PDF_FORM_STRU(fm_fields).form_parse()
            if len(fm_maga_info)  > 0 :
                FM.PDF_FORM_API_MAP(fm_maga_info, template, 0).api_order()
        
 
        page_num = pdf.getNumPages()
        # PAGE : get each page and its text
        for cur_pg_num in range(0, page_num) :
            # PARSE TEXT, VG, IMG, TABLE in each page
            PS.PDF_PAGE_STRU(pdf, cur_pg_num, template).page_parse()


def main(argv) :
    pdf_file = argv[0]
    output_dir = argv[1]
    pdf_opt_dir = argv[2]
    foxit_loc = argv[3]
    AFLpp_loc = argv[4]
    file_name = str(pdf_file.split("/")[-1]).replace(" ", "").replace(",", "").replace(".", "")
    print ("@@@@@@@@@@@@@", file_name)
#    all_dict = dict_collect(pdf_file)



    os.makedirs(output_dir + "/" + file_name)
    out_f = open( output_dir + "/" + file_name + "/html_to_PDF_harness_template.cpp", "a")
        
    # Write General bein API lines in template
    GENERAL_API(out_f).begin_line(foxit_loc, AFLpp_loc)
    # page parse and map
    page_stru(pdf_file, out_f)
    # Write General end part API lines in template
    GENERAL_API(out_f).end_line(pdf_opt_dir)

                    
                


if __name__ == "__main__" :
    main(sys.argv[1:])
