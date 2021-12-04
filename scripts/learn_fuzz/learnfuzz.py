import optparse
import logging

logging.basicConfig(format = "%(asctime)-15s %(levelname)s:%(message)s", level=logging.DEBUG)

def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-m", "--model", dest = "model", action = "store", \
            type = "string", help = "the model pdf file", default = None)
    parser.add_option("-o", "--output", dest = "output", action = "store", \
            type = "string", help = "the output pdf file", default = None)
    parser.add_option("-a", "--added", dest = "added", action = "store", \
            type = "string", help = "the added object", default = None)

    (options, args) = parser.parse_args()
    if options.model == None or options.output == None or options.added == None:
        parser.print_help()
        exit(-1)
    
    return options

def read_obj(obj):
    f_obj = open(obj, 'rb')
    return f_obj.read()
    

def parse_pdf(model, obj, output):
    logging.debug('model file is %s' % model)
    m_f = open(model, 'rb')
    m_buffer = m_f.read()
    m_lines = m_buffer.split(b'\n')

    xref_off_line = None

    for line in m_lines[::-1]:
        if b'startxref' == line.strip():
            break
        xref_off_line = line

    xref_off = int(xref_off_line.decode('utf-8'))
    logging.debug("startxref is %s" % str(xref_off))

    objs_part = m_buffer[:xref_off]
    xref_part = m_buffer[xref_off:]

    xref_lines = xref_part.split(b'\n')
    
    # check if the first line is xref
    if b'xref' != xref_lines[0]:
        logging.error("Can't find xref!")
        exit(-1)

    xref_ids = xref_lines[1].decode('utf-8')
    split_id = xref_ids.split()
    start_id = int(split_id[0])
    xref_len = int(split_id[1])
    logging.debug("The xref table: start id is %d, size is %d" % (start_id, xref_len))

    # get last used object
    for replaced_id in reversed(range(xref_len)):
        cur_xref = xref_lines[replaced_id+2]
        if b'n' in cur_xref:
            break

    cur_xref_str = cur_xref.decode('utf-8')
    gen_num = int(cur_xref_str.split()[1])
    logging.debug("Replaced object is %s, id is %d, generation id is %d" % (cur_xref_str, replaced_id, gen_num))

    new_obj = read_obj(obj)
    # newly object's offset is in the old offset of xref
    new_obj_offset = xref_off
    new_xref_off = xref_off + len(new_obj)

    f_output = open(output, 'wb+')
    f_output.write(objs_part)
    
    append_obj_id = b"%d %d obj\n" % (replaced_id, gen_num + 1)
    end_obj = b"endobj\n"

    f_output.write(append_obj_id)
    f_output.write(new_obj)
    f_output.write(end_obj)
    new_xref_off += len(append_obj_id) + len(end_obj)

    logging.debug("Newly xref offset is %d" % new_xref_off)

    for (cur_id, xref_line) in enumerate(xref_lines):
        if cur_id == replaced_id + 2:
            f_output.write(b"%010d %05d n \n" % (new_obj_offset, gen_num + 1))
            continue
        f_output.write(xref_line)
        f_output.write(b'\n')

        if b'startxref' == xref_line:
            break

    f_output.write(b"%d\n"%new_xref_off)
    f_output.write(b"%%EOF")
    f_output.close()

    logging.info("Save output into %s" % output)

if __name__ == '__main__':

    options = parse_arguments()

    parse_pdf(options.model, options.added, options.output)



