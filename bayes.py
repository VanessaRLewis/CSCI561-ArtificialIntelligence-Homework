from timeit import sys,itertools
from decimal import *
import os
disNum = 0
patNum = 0
inf = None #file pointer
f = None #file pointer
getcontext().prec=5

def readIn(fileName):
	inf = open(fileName, "r")
	disNum = int(inf.read(1))
	patNum = int(inf.readline().strip())
	disDict = {} #disDict dict
	sympDict = {} #sympDict dict
	disName=[]
	symName=[]
	
	#reading file, storing diseases and sympDict probabilities
	for i in range(disNum):
		disInfo=inf.readline().split() #String to store disInfo line in a string
		disDict[disInfo[0]]={}  #making disInfo values 0
		disName.append(disInfo[0]); #adding to list of disDict names
		disDict[disInfo[0]]["symp"]=int(disInfo[1])
		disDict[disInfo[0]]["prob"]=float(disInfo[2])
		#print(disDict)
		S4DList=eval(inf.readline()) #making list of symp
		posProb=eval(inf.readline()) #making list of P(s|d)
		negProb=eval(inf.readline()) #making list of P(s|d')
		sympDict[disInfo[0]]={}  #symp(disInfo)=null
		symName.append(S4DList) #adding to list of symptom names
		for j in range(disDict[disInfo[0]]["symp"]):
			sympDict[disInfo[0]][S4DList[j]]={}
			sympDict[disInfo[0]][S4DList[j]]["pos"]=float(posProb[j])
			sympDict[disInfo[0]][S4DList[j]]["neg"]=float(negProb[j])
	outputstr=""
	#reading patients data from file and their calculations
	for i in range(patNum):
		patDict={} #pat dict
		outputstr+="Patient-"+str(i+1)+":\n"
		#print(str1)
		#reading data
		for d in range(disNum):
			patDict[disName[d]]={} #dict within a dict
			patInfo=eval(inf.readline())
			for s in range(disDict[disName[d]]["symp"]):
				patDict[disName[d]][symName[d][s]]=patInfo[s]
		#question 1
		op1={}
		for d in disDict:
			num=disDict[d]["prob"]
			den=1-disDict[d]["prob"]
			for s in sympDict[d]:
				if patDict[d][s]=='T':
					num*=sympDict[d][s]["pos"]
					den*=sympDict[d][s]["neg"]
				elif patDict[d][s]=='F':
					num*=(1-sympDict[d][s]["pos"])
					den*=(1-sympDict[d][s]["neg"])				
			ans=num/(num+den)
			ans=round(ans,4)
			op1[d]=str(ans)			
		#print(op1)
		outputstr+=str(op1)+"\n"
		
		#question 2
		op2={}
		for d in disDict:
			num=disDict[d]["prob"]
			den=1-disDict[d]["prob"]
			unProbList=[]
			unSymList=[]
			permList=[]
			for s in sympDict[d]:
				if patDict[d][s]=='T':
					num*=sympDict[d][s]["pos"]
					den*=sympDict[d][s]["neg"]
				elif patDict[d][s]=='F':
					num*=(1-sympDict[d][s]["pos"])
					den*=(1-sympDict[d][s]["neg"])
				elif patDict[d][s]=='U':
					unSymList.append(s)
			for i in range(len(unSymList)):
				dummy=['T','F']
				permList.append(dummy)
			permList=list(itertools.product(*permList))
			for i in range(len(permList)):
				newNum=1
				newDen=1
				for j in range(len(unSymList)):
					if permList[i][j]=='T':
						newNum*=sympDict[d][unSymList[j]]["pos"]
						newDen*=sympDict[d][unSymList[j]]["neg"]
					elif permList[i][j]=='F':
						newNum*=(1-sympDict[d][unSymList[j]]["pos"])
						newDen*=(1-sympDict[d][unSymList[j]]["neg"])
				ans=(num*newNum)/((num*newNum)+(den*newDen))
				ans=round(ans,4)
				ans="{0:.4f}".format(ans)
				unProbList.append(ans)
			op2[d]=[str((min(unProbList))),str((max(unProbList)))]
		#print(op2)
		outputstr+=str(op2)+"\n"
		
		# question 3
		op3={}
		for d in disDict:
			num=disDict[d]["prob"]
			den=1-disDict[d]["prob"]
			unValList=[]
			unSymList=[]
			maxA=0
			minB=0			
			for s in sympDict[d]:
				if patDict[d][s]=='T':
					num*=sympDict[d][s]["pos"]
					den*=sympDict[d][s]["neg"]
				elif patDict[d][s]=='F':
					num*=(1-sympDict[d][s]["pos"])
					den*=(1-sympDict[d][s]["neg"])
				elif patDict[d][s]=='U':
					unSymList.append(s)
			for i in range(len(unSymList)):
				#unknown is true
				newNum=num*sympDict[d][unSymList[i]]["pos"]
				newDen=den*sympDict[d][unSymList[i]]["neg"]
				ans=newNum/(newNum+newDen)
				if i==0:
					maxA=ans
					unValList.append(unSymList[i])
					unValList.append('T')
					minB=ans
					unValList.append(unSymList[i])
					unValList.append('T')
				else:
					if ans>maxA:
						maxA=ans
						unValList[0]=unSymList[i]
						unValList[1]='T'
					if ans<minB:
						minB=ans
						unValList[2]=unSymList[i]
						unValList[3]='T'
				#unknown is false
				newNum=num*(1-sympDict[d][unSymList[i]]["pos"])
				newDen=den*(1-sympDict[d][unSymList[i]]["neg"])
				ans=newNum/(newNum+newDen)			
				if ans>maxA:
					maxA=ans
					unValList[0]=unSymList[i]
					unValList[1]='F'
				if ans<minB:
					minB=ans
					unValList[2]=unSymList[i]
					unValList[3]='F'
			op3[d]=unValList				
		#print(op3)
		outputstr+=str(op3)+"\n"
	inf.close()
	return outputstr
	
def writeOut(filename,outStr):
	f = open(filename,"w")
	f.write(outStr)
	f.close()


def main():
	out=readIn(sys.argv[2])
	print "Contents of output file"
	print "------------------------------------------------------------------"
	print out
	print "------------------------------------------------------------------"
	file_name=os.path.basename(sys.argv[2])
	print file_name
	file_name=file_name.split(".")
	output_name=file_name[0]
	output_name+="_inference.txt"
	writeOut(output_name,out)
	
	
main()