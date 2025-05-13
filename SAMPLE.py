#BINARY

import pickle
def wrt_bin():
    with open("finale.dat", "wb") as f:
        try:
            for i in range(int(input("enetr limit"))):
                d = {}
                d["NAME"]=str(input("enetr NAME"))
                d["ROLL NO"]=int(input("enetr ROLL NO"))
                d["MARK"]=int(input("enetr MARK"))
                print(d)
                pickle.dump(d,f)

        except:
            pass
def rd_bin():
        with open("finale.dat","rb") as f:
            try:
                while True:
                    e=pickle.load(f)
                    print(e)
            except:
                     pass
def up_bin():
        with open("finale.dat","rb+") as f:
            try:
                while True:
                    t=f.tell()
                    e=pickle.load(f)
                    if e["ROLL NO"]==4:
                        e["MARK"]+=1000
                        f.seek(t)
                        pickle.dump(e,f)
            except:
                 pass

rd_bin()


#csv
import csv
def wrt_csv():
    with open("fine.csv","w",newline="") as f:
        h=csv.writer(f)
        for i in range(int(input("enetr limit"))):
            #l=[name.rollno,mark
            n=str(input("enter int"))
            r = int(input("enter roll no"))
            m = int(input("enter mark"))
            h.writerow([n,r,m])

def rd_csv():
    with open("fine.csv","r") as f:
        h=csv.reader(f)
        for i in h:
            print(i)
def srch_csv():
    with open("fine.csv", "r") as f:
        h=csv.reader(f)
        for i in h:
            if int(i[2])>10:
                print(i)
