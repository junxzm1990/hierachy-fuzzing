import optparse
import logging
import os
logging.basicConfig(format = "%(asctime)-15s %(levelname)s:%(message)s", level=logging.DEBUG)

def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest = "input", action = "store", \
            type = "string", help = "the input directory", default = None)
    parser.add_option("-t", "--template", dest = "template", action = "store", \
            type = "string", help = "the input directory", default = None)
    parser.add_option("-o", "--output", dest = "output", action = "store", \
            type = "string", help = "the output directory", default = None)

    (options, args) = parser.parse_args()

    if options.input == None or options.output == None:
        parser.print_help()
        exit(-1)

    if not os.path.exists(options.output):
        os.makedirs(options.output)

    return options

def run(options):
    template_list = list()
    for f in os.listdir(options.template):

        f_path = os.path.join(options.template, f)

        if os.path.isdir(f_path):
            cotninue

        template_list.append(f_path)

    template_len = len(template_list)
    cur_index = 0
    for f in os.listdir(options.input):

        cur_path = os.path.join(options.input, f)
        if os.path.isdir(cur_path):
            continue

        cur_template = template_list[cur_index % template_len]

        output = os.path.join(options.output, f)

        cur_index += 1

        run_cmd = 'python3 learnfuzz.py -m %s -a %s -o %s' % (cur_template, cur_path, output)
        os.system(run_cmd)

def main():
    options = parse_arguments()

    run(options)

if __name__ == '__main__':
    main()
