#! /usr/bin/env python3
import sys
import os
import subprocess
di2={}

# b1 and b2 will be the two input fasta file
b1=sys.argv[1]
b2=sys.argv[2]
database="makeblastdb -in "+sys.argv[1]+"  -dbtype nucl -parse_seqids"
os.system(database)
database2="makeblastdb -in "+sys.argv[2]+" -dbtype nucl -parse_seqids"
os.system(database2)
blast1="blastn -db "+b1+" -query "+b2+" -out orth1 -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen' "

os.system(blast1)
blast2="blastn -db "+b2+" -query "+b1+" -out orth1 -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen' "
os.system(blast2)
os.remove(""+sys.argv[1]+".ndb" )
os.remove(""+sys.argv[2]+".ndb")
os.remove(""+sys.argv[1]+".nhr")
os.remove(""+sys.argv[2]+".nhr")
os.remove(""+sys.argv[1]+".nin")
os.remove(""+sys.argv[2]+".nin")
os.remove(""+sys.argv[1]+".nog")
os.remove(""+sys.argv[2]+".nog")
os.remove(""+sys.argv[1]+".nos")
os.remove(""+sys.argv[2]+".nos")
os.remove(""+sys.argv[1]+".not")
os.remove(""+sys.argv[2]+".not")
os.remove(""+sys.argv[1]+".nsq")
os.remove(""+sys.argv[2]+".nsq")
os.remove(""+sys.argv[1]+".ntf")
os.remove(""+sys.argv[2]+".ntf")
os.remove(""+sys.argv[1]+".nto")
os.remove(""+sys.argv[2]+".nto")
# reciprocal hit algorithm
f1=open("orth","r")
f2=open("orth1","r")

d={}
a=[]
b=[]
orth_dict={}
for i in f1:
  a.append(i)

for i in range(len(a)):
    e=a[i].split("\t")
    qid=e[0]
    sid=e[1]
    d[qid]=sid
tem="lcl|"
di1={key:tem+str(value) for key , value in d.items()}
#print(di1)
# for second blast file
d2={}
for j in f2:
   b.append(j)
for line in range(len(b)):
    ele=b[line].split("\t")
    quid=ele[0]
    suid=ele[1]
    
    d2[quid]=suid
temp="lcl|"
di2={key:temp+str(value) for key , value in d2.items()}
#print(di2)
for i in di1.keys():
   q=di1[i]
  # print(q)
   if q in di2.keys():
     if i == di2[q]:
       orth_dict[q]=i
     ou=["{}       {}".format(k,v) for k , v in orth_dict.items()]
     ou="\n".join(ou)
qw=open("find_orthologous.output","w")
qw.write(ou)
qw.close()
    
