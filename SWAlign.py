#!/usr/bin/env python 3
import sys
#get the file input 
f1=open(sys.argv[1],"r")
f2=open(sys.argv[2],"r")
s1=""
s2=""
# printing the fasta file in string format
for line in f1:
   if not line.startswith(">"):
       line=line.strip()  
       s1=s1+line 
   
print("sequence 1 is :",s1)
for line in f2:
   if not line.startswith(">"):
       line=line.strip()  
       s2=s2+line
print("sequence 2 is :",s2) 
# creation of matrix 
m=len(s1)
n=len(s2)
match=+1
mismatch=-1
gap=-1
score=[[0 for _ in range(n+1)] for _ in range(m+1)]



def raw_score(a,b):
	if a ==b:
		return match
	elif a == '-' or b == '-':
		return gap
	else:
		return mismatch
	      
def alignment(s1,s2): 
	c=0   
# assigning score to second row and col:	      
	for i in range (m+1):
		
   		score[i][0]=0
	for j in range (n+1):
   		score[0][j]=0
   		
#print(score)

 
#final matrix
	for i in range (1,m+1):
		for j in range(1,n+1):
	
	     		match=score[i-1][j-1]+raw_score(s1[i-1],s2[j-1])
	     		o=score[i-1][j]+gap
	     		p=score[i][j-1]+gap
	     		score[i][j]=max(0,match,o,p)
	     		if score[i][j] >=c:
	     			c= score[i][j]
	     			q=i
	     			r=j
	     		
	for row in score:  
		print(*row,sep='\t')
# traceback the matrix to get alignment

	global align1
	align1=""
	global align2
	align2=""
	i=q
	j=r
	while score[i][j] != 0:
  		if i>0 and j>0 and score[i][j] == score[i-1][j-1] + 	   			raw_score(s1[i-1],s2[j-1]):
    			align1=align1+s1[i-1]
    			align2=align2+s2[j-1]
    			i=i-1
    			j=j-1
  		elif i>0 and score[i][j]==score[i-1][j] + gap:
   			align1=align1+s1[i-1]
   			align2=align2+"-"
   			i=i-1
  		else:
   			align1=align1+"-"
   			align2=align2+s2[j-1]
   			j=j-1
   			# to print from start
	align1=align1[ ::-1]
	align2=align2[ ::-1]
   			#print(align1,align2)
	return (align1,align2)

def outcome(align1,align2):
	d=""
	
	for i in range(max(len(align1),len(align2))):
		if align1[i]==align2[i]:
			d=d+"|"
		elif align1[i]=="-" or align2[i]=="-" :
			d=d+" "
		else:
			d=d+"*"
	return(d)



	#print(align1,align2)	
if __name__=='__main__':
	alignment(s1,s2)
	d=outcome(align1,align2)
	v=align1
	w=align2
	
	count=0
	for i in range(max(len(v),len(w))):
		if v[i] == w[i]:
			count=count+1
		elif v[i]== " " or w[i]==" ":
			count=count-1
		else:
			count=count-1
	
	
	print(align1)
	print(d)
	print(align2)
	print("score is :",count)
