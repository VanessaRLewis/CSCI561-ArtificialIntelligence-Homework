from timeit import sys,itertools
__author__="Vanessa"

f = None #filepointer
inp = []  #list of eval i/p sentences
n = 0    #no of input sentences
outp =[]  #list of ans

def readInput(filename):
    f = open(filename, "r")
    global n
    n = int(f.readline())
    print "Number of lines in input file: ", n
    
    for i in range(n):
        inp.append(eval(f.readline()))

    f.close()
    
def implication(sen):
    lenSen = len(sen)
    conn = sen[0]
    temp = [] #temporary list which holds workin parts of o/p
    
    for i in range(1,lenSen):
        temp.append(sen[i])
    
    lenTemp = len(temp)
    for i in range(lenTemp):
        t2 = temp[i]
        if isinstance(t2, list):
            t2 = implication(t2)
            temp[i] = t2
            
    if conn == "implies":
        conn = "or"
        A = temp[0]
        
        l1 = []
        l1.append("not")
        l1.append(A)
        temp[0] = l1
                      
    lenTemp = len(temp)    
    sen = []
    sen.append(conn)
    for i in range(lenTemp):
        sen.append(temp[i])
    
    return sen

def neg(sen) :  
    if isinstance(sen, str) :
        p = sen
    else :
        conn = sen[0]
        if conn == "not" :
            temp = sen[1]
            if isinstance(temp, str) :
                p = []
                p.append("not")
                p.append(temp) 
            else :
                inConn = temp[0]
                if inConn == "not" :
                    p = neg(temp[1])
                else :
                    if inConn == "and":
                        inConn = "or"
                    elif inConn == "or":
                        inConn = "and"
                    
                    p = [inConn]
                    lenTemp = len(temp);
                    for i in range(1,lenTemp):
                        p += [neg(["not", temp[i]])]
        else :
            p = [conn]
            lenSen = len(sen)
            for i in range(1,lenSen):
                p +=  [neg(sen[i])]

    return p

def orHandler(t3):
    sen = []
    if isinstance(t3, str):
        return t3
    
    lenSen = len(t3)
    for i in range(lenSen):
        p = t3[i]
        if isinstance(p, list):
            if p[0] == "and":
                sen.append("and")
                lenTemp = len(p)
                for j in range(1,lenTemp):
                    l1 = []
                    if i != 0:
                        for k in range(i):
                            l1.append(t3[k])
                    l1.append(p[j])
                    for k in range(i+1, lenSen):
                        l1.append(t3[k])
                    sen.append(orHandler(l1))
            break;

    if len(sen) == 0:
        if isinstance(t3, str):
            return t3
        
        lenSen = len(t3)
        sen.append("or")
        for i in range(lenSen):
            sen.append(t3[i])
        
    return sen
    
def distb(sen):
    if isinstance(sen, list):
        conn = sen[0]
        temp = [] #temporary list which holds workin parts of o/p
    
        lenSen = len(sen)
        for i in range(1,lenSen):
            temp.append(sen[i])
            
        lenSen = len(temp)
        for i in range(lenSen):
            temp[i] = distb(temp[i])
        
        if conn == "and":
            sen = []
            sen.append(conn)
        
            for i in range(lenSen):
                sen.append(distb(temp[i]))
        elif len(temp) > 1:
            sen = orHandler( temp )
    return sen

def orAdding(sen, flag):
    lenSen = len(sen)
    
    for i in range(lenSen):
        p = sen[i]
        if isinstance(p, list) and p[0] != "not":
            p.insert(0, "or")
    if flag:        
        sen.insert(0, "and")
        return sen    
            
    return sen[0]
	
def extbrackOr(sen):
    lenSen = len(sen)
    if isinstance(sen, list) and lenSen > 2:
        p = []
        for i in range(1,lenSen):
            p += extbrackOr(sen[i])
        return p
    return [sen]

def extbrackAnd(sen):
    lenSen = len(sen)
    if isinstance(sen, list) and lenSen > 2:
        conn = sen[0]
        if conn == "and":
            p = []
            for i in range(1,lenSen):
                p += extbrackAnd(sen[i])
            return p
        if conn == "or":
            p = []
            for i in range(1,lenSen):
                p += extbrackOr(sen[i])
            return [p]
        
    return [sen]


def innerDup(sen) :
    #removes all duplicate strings from list  sen
    if isinstance(sen, str):
        return sen
    
    if len(sen) == 0 :
        w = sen #temp copy of sentence
    else :
        A = sen[0]
        temp = sen[1:]
        temp = innerDup(temp)
        if A in temp :
            w = temp
        else :
            if isinstance(temp, list):
                w = [A] + temp
            else:
                w = [A] + [temp]
    return w


def dup(sen):
    result = []
    for p in sen :
        p =  innerDup(p)
        if p not in result:
            duplicates = list(itertools.permutations(p, len(p)))
            duplicatesList = [list(elem) for elem in duplicates]
            flag = True
            for dup in duplicatesList:
                if dup in result:
                    flag = False
                    break
            if flag:
                result += [p]
    return result

def Bicondition(sen):
    lenSen = len(sen)
    conn = sen[0]
    temp = [] #temporary list which holds workin parts of o/p
    
    for i in range(1,lenSen): 
        temp.append(sen[i])  #temp with ele other than connective
    
    lenTemp = len(temp)
    for i in range(lenTemp):
        t2 = temp[i] #2nd temporary list which ele other than connective when going recursive
        if isinstance(t2, list):
            t2 = Bicondition(t2)
            temp[i] = t2
            
    if conn == "iff":
        conn = "and"
        A = temp[0]
        B = temp[1]
        
        l1 = []
        l1.append("implies")
        l1.append(A)
        l1.append(B)
        temp[0] = l1
        
        l2 = []
        l2.append("implies")
        l2.append(B)
        l2.append(A)
        temp[1] = l2
    
    lenTemp = len(temp)    
    sen = []
    sen.append(conn)
    for i in range(lenTemp):
        sen.append(temp[i])
    
    return sen
	
	
def corner(p):
    if isinstance(p, list) and len(p) == 2:
        conn = p[0]
        if conn != "not":
            p = p[1]
    if len(p) == 1 and isinstance(p[0], str):
            p = p[0];

    lenSen = len(p)
    if isinstance(p, list):
        sen = []
        for i in range(lenSen):
            sen.append(corner(p[i]))
        return sen
    return p

def writeout(filename):
    f = open(filename, "w")
    
    for i in range(n):
        outFile = outp[i]
        if isinstance(outFile, list):
            outFile = str(outFile) + "\n"
            outFile = outFile.replace("'", "\"");
        else:
            outFile = '"' + outFile +'"\n'
        f.write(outFile)
        
    f.close()


def main():
    readInput(sys.argv[2])
    
    for i in range(n):
        outFile = inp[i]
        if len(outFile) == 0:
            outp.append(outFile)
            print "Sentence", i+1, ": ", inp[i]
            print "CNF form: ", outp[i]
            continue
        if len(outFile) == 1 and isinstance(outFile[0], str):
            outp.append(outFile)
            print "Sentence", i+1, ": ", inp[i]
            print "CNF form: ", outp[i]
            continue
        outp.append(Bicondition(inp[i]))
        outp[i] = implication(outp[i])
        outp[i] = neg(outp[i])
        outp[i] = distb(outp[i])
        conn = outp[i][0]
        if conn == "and":
            flag = True
        else:
            flag = False
        outp[i] = extbrackAnd(outp[i])
        outp[i] = orAdding(outp[i], flag)
        outp[i] = dup(outp[i])
        outp[i] = corner(outp[i])

        print "\n"
        print "Sentence", i+1, ": ", inp[i]
        print "CNF form: ", outp[i]
    
    writeout("sentences_CNF.txt")

main()