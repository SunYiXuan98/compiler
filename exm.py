def to_string(s):
    isok=0
    for ind,ch in enumerate(s):
        if(ind==0):
            continue
        if(ch=='"'):
            isok=1
            break
    if(not isok):
        exit('no " match')
    return s[:ind+1],len(s[:ind+1])



