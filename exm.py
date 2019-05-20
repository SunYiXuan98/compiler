with open('test/c.txt','r') as f:
    s=f.read()


def delete(s,start,end):
    return s[:start]+s[end+1:],s[start:end+1]

def insert(s,start,s1):
    return s[:start]+s1+s[start:]


while(1):
    start=s.find('for')
    if(start==-1):
        break
    end=start
    c=0
    while(1):
        if(s[end]=='{'):
            c+=1
        if(s[end]=='}'):
            c-=1
            if(c==0):
                break
        end+=1

    s,s_for=delete(s,start,end)

    init_start=4
    init_end=s_for.find(";")

    s_for,s_init=delete(s_for,init_start,init_end)


    bool_start=4
    bool_end=s_for.find(";")
    s_for,s_bool=delete(s_for,bool_start,bool_end)
    s_bool=s_bool[:-1]

    last_start=4
    last_end=s_for.find(")")-1
    s_for,s_last=delete(s_for,last_start,last_end)
    s_last+=';'

    s_for=insert(s_for,4,s_bool)
    s_for=insert(s_for,len(s_for)-1,s_last)
    s_for=s_for.replace('for','while',1)
    s_for=s_init+s_for
    s=insert(s,start,s_for)




