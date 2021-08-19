#! /usr/bin/python3
import sys
import logging
import optparse
import subprocess
import os
import random
import string
import fitz
import time

logging.basicConfig(format = "%(asctime)-15s %(levelname)s:%(message)s", level=logging.INFO)

# global variables that are related to running the fuzzed binary
AFL_SHOWMAP = None
FUZZED_BINARY = None
BINARY_ARGS = None
MEM_LIMIT = None
TIME_OUT = None
OUTPUT = None
TMP_DIR = None

BLACKLIST = set()

ORIG_MEM_MAP = None

ALL_COVS = dict()
CUR_COVS = set()
CUR_UNIQ_COVS = set()

TMP_DIR='/dev/shm'


TIMEOUT = 1000 * 1 # set timeout as 1s

def remove_page(cur_pdf_output):
    doc = fitz.open(cur_pdf_output, filetype='pdf')
    page_cnt = doc.pageCount

    if page_cnt < 2:
        return 0

    cur_start_page = 0
    succeed_cnt = 0
    tmp_output_pdf = ('%s/%s.pdf' % (TMP_DIR, get_random_string(8)))
    # quick check. If CUR_UNIQ_COVS is NULL. Delete n-1 pages
    if len(CUR_UNIQ_COVS) == 0:
        try:
            doc.deletePageRange(0, page_cnt - 2)
            succeed_cnt = page_cnt - 1
        except:
            return 0
    '''
    while page_cnt > 1:
        for cur_idx in range(cur_start_page, page_cnt):
            page_cnt = doc.pageCount

            if page_cnt < 2:
                break

            try:
                doc.deletePage(cur_idx)
            except:
                continue

            try:
                doc.save(tmp_output_pdf)
            except ValueError:
                continue

            (r_code, covs) = get_covs(tmp_output_pdf)

            if len(covs) > 0 and len(CUR_UNIQ_COVS.difference(covs)) == 0:
                succeed_cnt += 1
                os.system('cp %s %s' % (tmp_output_pdf, cur_pdf_output))
            else:
                cur_start_page += 1
                doc = fitz.open(cur_pdf_output, filetype = 'pdf')
                page_cnt = doc.pageCount
                logging.info("Error. Next")
                break
    '''

    doc.save(tmp_output_pdf, garbage = 3)
    os.system('mv %s %s' % (tmp_output_pdf, cur_pdf_output))
    return succeed_cnt


def init_global_vars(options, args):
    '''
    initialize some global variables

    Args:
        options: options

    Returns:
        None
    '''
    global AFL_SHOWMAP, FUZZED_BINARY, BINARY_ARGS, MEM_LIMIT, TIMEOUT, OUTPUT, SAME_INPUT, TMP_DIR

    print (args)

    AFL_SHOWMAP = options.showmap
    FUZZED_BINARY = options.binary
    BINARY_ARGS = ' '.join(args)
    MEM_LIMIT = options.memory
    TIME_OUT = options.timeout
    OUTPUT = options.output

    #TMP_DIR = os.getenv('TMPDIR')

    if TMP_DIR == '' or not TMP_DIR:
        TMP_DIR = '/tmp'

    if '@@' not in BINARY_ARGS:
        logging.error("Only support the input is a file @@!")
        exit(-1)
    #SAME_INPUT = ('/tmp/%s.html' % get_random_string(8))

def get_random_string(length):
    '''
    generate random string with specific length

    Args:
        length

    Returns:
        random string
    '''
    letters = string.ascii_lowercase
    result_str = ''.join((random.choice(letters) for i in range(length)))
    return result_str

def run_showmap(pdf_input, output):
    '''
    run afl-showmap with specified seed

    Args:
        seed: the input file
        output: output file that store covs

    Returns:
        True if running correctly
    '''
    t_arg = ''

    if TIME_OUT:
        t_arg = ('-t %s' % TIME_OUT) 

    #tmp_output='/tmp/%s' % get_random_string(8)

    running_args = ('%s -m %s %s -Z -o %s -- %s %s' % 
            (AFL_SHOWMAP, MEM_LIMIT, t_arg, output, FUZZED_BINARY, BINARY_ARGS.replace('@@', pdf_input)))
    #running_args = ('%s -m %s %s -e -o %s -- %s %s %s' % 
    #        (AFL_SHOWMAP, MEM_LIMIT, t_arg, tmp_output, FUZZED_BINARY, pdf_input, BINARY_ARGS))

    args_list = running_args.split()

    showmap_run = subprocess.run(args_list, stdout = subprocess.PIPE, \
            stderr = subprocess.PIPE)

    if showmap_run.returncode:
        logging.error('Errors when running afl-showmap firstly!\n \
                The output message is %s\n, The error message is %s\n' % 
                (showmap_run.stdout, showmap_run.stderr))
        return False

    return True

def check_binary(binary):
    '''
    check if binary exists

    Args:
        binary: binary

    Returns:
        True if the binary exists
    '''
    c_output = subprocess.run(['which', binary], stdout = subprocess.PIPE)

    if os.path.exists(c_output.stdout.strip()):
        return True
    return False

def pre_check(options):
    '''
    pre check if required arguments exist

    Args:
        options: option

    Returns:
        None
    '''
    assert options.input != None, "Please input the seed to be analyzed with (-i)!"
    assert options.binary != None, "Please input the binary file that is fuzzed with (-b)!"
    assert options.output != None, "Please input the directory of output with (-o)!"


    # check the path of afl-showmap and binary is valid
    if not check_binary(options.showmap):
        logging.error('Please input the path of afl-showmap with (-s)!')
        exit(-1)

    # check the pat of tested binary is valid
    if not check_binary(options.binary):
        logging.error('Please input the path of tested binary with (-b)!')
        exit(-1)

    if not os.path.isdir(options.input):
        logging.error('Please input the directory of input files with (-i)!')
        exit(-1)

    if not os.path.isdir(options.output):
        mk_cmd = ('mkdir -p %s' % (options.output))
        mk_run = subprocess.run(mk_cmd.split(), stdout = subprocess.PIPE,\
                stderr = subprocess.PIPE)
        if mk_run.returncode != 0:
            logging.error('Error when mkdirring directory of output: %s' % options.output)
            exit(-1)

def collect_covs_of_seeds(input_dir):
    '''
    first running of the fuzzed binary.
    check if afl-whowmap runs normally
    and collect the covs of seed

    Args:
        seed: the input file that to be analyzed

    Returns:
        True if afl-showmap runs normally
    '''
    global ORIG_MEM_MAP
    global SAME_INPUT
    global ORIG_HTML_SIZE
    global ORIG_PDF_SIZE
    global BLACKLIST

    all_covs = dict()
    tmp_output = ('%s/%s' % (TMP_DIR, get_random_string(8)))

    logging.info('collecting covs...')

    for seed in os.listdir(input_dir):

        seed = os.path.join(input_dir, seed)

        if os.path.isdir(seed):
            continue

        if not run_showmap(seed, tmp_output):
            os.system('rm %s' % tmp_output)
            logging.error('[showmap error]: add %s to blacklist' % seed)
            BLACKLIST.add(os.path.basename(seed))
            continue


        with open(tmp_output, 'r+') as s_o:
            for line in s_o.readlines():
                if line.strip().isdigit():
                    cur_edge = int(line.strip())

                    if cur_edge in all_covs:
                        all_covs[cur_edge] += 1
                    else:
                        all_covs[cur_edge] = 1


    os.system('rm %s' % tmp_output)
    return (True, all_covs)

def get_covs(seed):
    '''
    first running of the fuzzed binary.
    check if afl-whowmap runs normally
    and collect the covs of seed

    Args:
        seed: the input file that to be analyzed

    Returns:
        True if afl-showmap runs normally
    '''

    covs = set()
    tmp_output = '%s/%s' % (TMP_DIR, get_random_string(8))

    if not run_showmap(seed, tmp_output):
        os.system('rm %s' % tmp_output)
        return (False, covs)

    with open(tmp_output, 'r+') as s_o:
        for line in s_o.readlines():
            if line.strip().isdigit():
                covs.add(int(line.strip()))

    os.system('rm %s' % tmp_output)

    return (True, covs)

def trim_pdf(seed):

    global ALL_COVS

    cur_time_start = int(round(time.time() * 1000))

    base_name_seed = os.path.basename(seed)
    cur_pdf_output = os.path.join(OUTPUT, base_name_seed)


    orig_pdf_size = os.path.getsize(seed)

    if os.path.exists(cur_pdf_output):
        os.system('rm %s' % cur_pdf_output)

    (_, cur_covs) = get_covs(seed)
    # get xrefs
    try:
        doc = fitz.open(seed, filetype='pdf')
        xrefs_cnt = doc.xrefLength()
        doc.save(cur_pdf_output)
    except:
        return

    succeed_cnt = remove_page(cur_pdf_output)
    #logging.info("UNIQ COVS is {}".format(CUR_UNIQ_COVS))

    skip = False

    tmp_output_pdf = ('%s/%s.pdf' % (TMP_DIR, get_random_string(8)))

    failed_cnt = 0

    for cur_xref in range(1, xrefs_cnt):

        if len(CUR_UNIQ_COVS) > 10:
            break

        cur_time = int(round(time.time() * 1000))

        if cur_time - cur_time_start > TIMEOUT:
            logging.warning("timeout. skip it!")
            break

        # do not try much time
        if failed_cnt > 10:
            break

        if not skip:
            doc = fitz.open(cur_pdf_output, filetype='pdf')

        skip = False

        try:
            del_obj = doc.xrefObject(cur_xref)
            doc._deleteObject(cur_xref)
        except:
            skip = True
            logging.error('Delete object error! %s' % repr(del_obj))
            continue

        logging.debug('[Trim]: deleteing %s' % (del_obj))

        try:
            doc.save(tmp_output_pdf)
        except ValueError:
            continue

        if len(CUR_UNIQ_COVS) == 0:
            succeed_cnt += 1
            os.system('cp %s %s' % (tmp_output_pdf, cur_pdf_output))
            skip = True
            continue

        (r_code, covs) = get_covs(tmp_output_pdf)

        # this is valid trimming
        if len(covs) > 0 and len(CUR_UNIQ_COVS.difference(covs)) == 0:
            logging.debug('trim valid!')
            succeed_cnt += 1
            os.system('cp %s %s' % (tmp_output_pdf, cur_pdf_output))
            skip = True
            failed_cnt = 0
        else:
            failed_cnt += 1


    doc = fitz.open(cur_pdf_output, filetype='pdf')
    doc.save(tmp_output_pdf, garbage = 3)
    os.system('mv %s %s' % (tmp_output_pdf, cur_pdf_output))

    (_, output_covs) = get_covs(cur_pdf_output)
    
    deleted_covs = cur_covs.difference(output_covs)

    for cur_cov in deleted_covs:
        if cur_cov not in ALL_COVS:
            continue
        ALL_COVS[cur_cov] -= 1

        if ALL_COVS[cur_cov] == 0:
            del ALL_COVS[cur_cov]

    # delete covs from ALL_COVS

    trimed_pdf_size = os.path.getsize(cur_pdf_output)
    optimized_rate = (1 - trimed_pdf_size / orig_pdf_size)
    if trimed_pdf_size == 0:
        trimed_pdf_size = orig_pdf_size

    logging.info('Save output %s' % (cur_pdf_output))
    logging.debug('Summary of file %s: remove %d objects' % (base_name_seed, succeed_cnt))
    logging.debug('Summary of file %s: pdf size(original): %d bytes' % (base_name_seed, orig_pdf_size))
    logging.debug('Summary of file %s: pdf size(after trimming): %d bytes' % (base_name_seed, trimed_pdf_size))
    logging.debug('Summary of file %s: optimized rate: %f' % (base_name_seed, optimized_rate))
            

def trim_seeds(in_dir):
    global CUR_UNIQ_COVS

    for cur_file in os.listdir(in_dir):

        if cur_file in BLACKLIST:
            continue

        seed = os.path.join(in_dir, cur_file)

        if os.path.isdir(seed):
            continue

        logging.info('current seed is %s' % seed)

        (r_code, cur_covs) = get_covs(seed)

        assert len(cur_covs) > 0, 'the length of cur_covs equals to 0!'

        CUR_UNIQ_COVS = set()

        for cov in cur_covs:
            if cov not in ALL_COVS or ALL_COVS[cov] == 1:
                CUR_UNIQ_COVS.add(cov)

        trim_pdf(seed)

def main():

    parser = optparse.OptionParser()

    parser.add_option('-i', '--input', dest = 'input', action = 'store', \
            type = 'string', help = 'the input directory that to be analyzed', default = None)
    parser.add_option('-b', '--binary', dest = 'binary', action = 'store', \
            type = 'string', help = 'the binary file that is fuzzed', default = None)
    parser.add_option('-s', '--showmap', dest = 'showmap', action = 'store', \
            type = 'string', help = 'the path of afl-showmap', default = 'afl-showmap')
    parser.add_option('-m', '--memory', dest = 'memory', action = 'store', \
            type = 'string', help = '[args of afl-showmap]: memory limit', default = 'none')
    parser.add_option('-t', '--timeout', dest = 'timeout', action = 'store', \
            type = 'string', help = '[args of afl-showmap]:time out', default = None)
    parser.add_option('-o', '--output', dest = 'output', action = 'store', \
            type = 'string', help = 'directory of output', default = None)

    (options, args) = parser.parse_args()
    print ("o, a", (options, args))

    pre_check(options)

    init_global_vars(options, args)

    global ALL_COVS
    
    (r_code, ALL_COVS) = collect_covs_of_seeds(options.input)

    if not r_code:
        logging.error('Try running afl-showmap error!')
        exit(-1)

    # remove object of pdf
    trim_seeds(options.input)

if __name__ == '__main__':
    main()
