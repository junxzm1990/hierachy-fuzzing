import os
import sys
import json


def json_dump(class_obj) :

    with open('class_obj.json' , 'w') as d :
        json.dump(class_obj,d)
    
def obj_col(cur_f, class_obj, dic_ls, stream_ls) :
    with open (cur_f, 'rb') as fr :
        obj_bool = False
        dic_bool = 0
        stream_bool = 0
        for line in fr :
           try :
               line.decode('utf-8')
               line.decode('ascii')
           except :
               line = line.decode('latin-1')
           if "0 obj" in line.strip() :
               obj_bool = True
           elif "endobj" in line.strip() : 
               obj_bool = False 
           elif obj_bool == True :
               # BOOLEAN :
               if 'true' in line or 'false' in line :
                   if 'Bool' not in class_obj :
                       class_obj.update({'Bool' : [line]})
                   else :
                       class_obj['Bool'].append(line)
               # STRING :
               if '<' in line and '>' in line :
                   if 'String' not in class_obj :
                       class_obj.update({'String' : [line[line.index('<'):line.index('>')+1]]})
                   else :
                       class_obj['String'].append(line[line.index('<'):line.index('>')+1])
               if '(' in line and ')' in line :
                   if 'String' not in class_obj :
                       class_obj.update({'String' : [line[line.index('('):line.index(')')+1]]})
                   else :
                       class_obj['String'].append(line[line.index('('):line.index(')')+1])
               # NAME :
               if '/' in line :
                   if 'Name' not in class_obj :
                       class_obj.update({'Name' : [line]})
                   else :
                       class_obj['Name'].append(line)
               # ARRAY :
               if '[' in line and ']' in line :
                   if 'Array' not in class_obj :
                       class_obj.update({'Array' : [line[line.index('['):line.index(']')+1]]})
                   else :
                       class_obj['Array'].append(line[line.index('['):line.index(']')+1])
               # NULL :
               if 'null' in line :
                   if 'Null' not in class_obj :
                       class_obj.update({'Null' : [line]})
                   else :
                       class_obj['Null'].append(line)
               # NUMBER :
               for i in line.strip("\n").split(" ") :
                   try :
                       float(i)
                       if "R" not in line :
                           if 'Number' not in class_obj :
                               class_obj.update({'Number' : [i]})
                           else :
                               class_obj['Number'].append(i)
                   except :
                       continue

           # DICTIONARY :
           if "<<" == line.strip() :
               dic_ls.append([line])
               dic_bool = 1
           elif ">>" == line.strip() :
               dic_bool = 0
               if len(dic_ls) > 0 :
                   dic_ls[-1].append(line)
           elif dic_bool == 1 :
               dic_ls[-1].append(line)
           class_obj['Dictionary'] = dic_ls

           # STREAM
           if line.strip() == "stream" :
               stream_bool = 1
               stream_ls.append([line])
           elif line.strip() == "endstream" :
               stream_bool = 0
               if len(stream_ls) > 0 :
                   stream_ls[-1].append(line)
           elif stream_bool == 1 :
               stream_ls[-1].append(line)
           class_obj['Stream'] = stream_ls

    return class_obj

def main (argv) :

    tg_dir = argv[0]

    class_obj = dict()
    dic_ls = list()
    stream_ls = list()
    
    for pdf in os.listdir(tg_dir) :
        cur_f = tg_dir + "/" + pdf
        obj_col(cur_f, class_obj, dic_ls, stream_ls)

    for i in class_obj.keys() :
        try :
            print (i)
            class_obj[i] = set(class_obj[i])
            print (type(class_obj[i]), len(class_obj[i]))
            class_obj[i] = list(class_obj[i])
            print (type(class_obj[i]), len(class_obj[i]))
        except :
            pass
    json_dump(class_obj) 

if __name__ == "__main__" :
    main(sys.argv[1:]) 
