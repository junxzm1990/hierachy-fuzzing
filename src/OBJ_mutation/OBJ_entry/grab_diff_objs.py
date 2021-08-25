import sys

#def file_unbreakable() : 

#def obj_unbreakable() : 

#def obj_breakable():
    # - CHARACTER :  type(content) != int && [ ] not in content
    # - INT : type(conntent) == int && [ ] not in content 
    # - OBJ : [ ] in content && R in cotnent 
    # - LIST_LIKE : [ xxx xxx xxx xxx xxx ]
    # - SYMBOLs : << >>  
def recur_find_pre_token (tag_content, breakable_objs , content, rd_cnt) :
    pre_token_idx = breakable_objs.index(content) - rd_cnt
    pre_token_name = breakable_objs[pre_token_idx].split(' ')[0]
    if pre_token_name in tag_content :
        update_content = content.split(" ")
        tag_content[pre_token_name] = tag_content[pre_token_name] + update_content
    else :
        rd_cnt += 1
        recur_find_pre_token(tag_content, breakable_objs, content, rd_cnt)

def obj_stru_reserve(breakable_objs) :
    tag_content = dict()
    for i in breakable_objs :
    # store token and its following content 
        if "/" in i :
           if len(i.split(' ')) > 1 :
               if i.split(' ')[0] in tag_content :
                   for j in i.split(' ')[1:] :
                       tag_content[i.split(' ')[0]].append(j)
               else :
                   tag_content[i.split(' ')[0]] = [i.split(' ')[1]]
                   for j in i.split(' ')[2:] :
                       tag_content[i.split(' ')[0]].append(j)
           else :
               if i.split(' ')[0] not in tag_content :
                   tag_content[i.split(' ')[0]] = []
        else :
            # some content takes more than line (second line not start with "/")
            
            if "00000 n" not in i and "obj" not in i and ">>" not in i and "<<" not in i:
                recur_find_pre_token(tag_content, breakable_objs, i, 1) 
            # some content has no "/" because it belongs to xref
            if "00000 n" in i : 
                continue
            # objs' start and end point
            elif "obj" in i :
                continue 
            elif "<<" in i :
                continue
            elif ">>" in i :
                continue
    return tag_content

def main(argv) :
    diff_raw_path = argv
    breakable_objs = list()
    breakable_stream = list()
    unbreakable_token = list()
    with open (diff_raw_path) as fr :
        stream = False
        for line in fr :
            if 'stream' in line.strip() and "end" not in line.strip():
                stream = True
                continue
            elif 'endstream' in line.strip() :
                stream = False
                continue 
            elif stream == True: 
                breakable_stream.append(line)
            # Collecting breakable entries 
            if "      >" in line and line not in breakable_stream :
                breakable_objs.append(line.strip().replace('>\t', ''))
            # Collecting unbreakable entries
            elif line != ">>":
                unbreakable_token.append(line.strip().split('\t')[0])
    # dictionarying TOKEN(TAG) & its Content 
    token_content = obj_stru_reserve(breakable_objs)
    #print (breakable_stream)
    return [token_content, breakable_stream]
