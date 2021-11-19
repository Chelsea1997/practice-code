#!/usr/bin/env python3
import argparse


parser=argparse.ArgumentParser(description='Count coordinates in genome bed seq')
parser.add_argument("--filename","-i",type = str,required=True)
args=parser.parse_args()
#q=args.i
f=open(args.filename,"r")
l=[]

l2=[]
final=[]

for i in f:
 if (i[:-1]=="\n"):
  i=i[:-1]
 t=i.split("\t")
 l.append((t[0],int(t[1]),int(t[2])))
l.sort(key=lambda x:x[1])


 #print(l)
min_val=l[1][1]
max_val=l[1][2]
#print(min_val,max_val)
for e in l:
  #print(e)
  if e[1] < min_val:
    min_val=e[1]
  if e[2] > max_val:
    max_val=e[2]
  #print(min_val,max_val)
for n in range(min_val,max_val):
 c=0
 for le in l:
   if (n >= le[1]) and (n < le[2]):
      c=c+1
     # print("the file is running")
 l2.append((l[0][0],n,n+1,c))
 #print(l2)

for n in range(0,len(l2)):
   if (n != 0) and (l2[n][3] == l2[n-1][3]):
     max_val=l2[n][2]
     
   
   elif (n !=0):
     # print("append")
      final.append((l2[n-1][0],min_val,max_val,l2[n-1][3]))
      min_val=l2[n][1]
      max_val=l2[n][2]
      #print(final)  
for k in final:
  if k[3] == 0:
    final.remove(k)
for k in final:
  #print("final")
  print(k[0]+"\t"+str(k[1])+"\t"+str(k[2])+"\t"+str(k[3])+"\n")

