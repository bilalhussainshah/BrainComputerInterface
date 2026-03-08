import scipy.stats
import pandas as pd 
import numpy
from numpy.fft import fft
from numpy import zeros, floor, log10, log


##########################################################################

dflist=[]

#FILE 1
file1=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Concat\First\BEB.csv"
df=pd.read_csv(file1)
df['Class'] = 1
dflist.append(df)

#FILE 2
file2=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Concat\First\CLN.csv"
df2=pd.read_csv(file2)
df2['Class'] = 2
dflist.append(df2)

outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Tests\Stage-2 (First)\Stage-2_Complete.csv"
concatdf=pd.concat(dflist,axis=0,ignore_index = True)       #axis=0 for row addition
concatdf.to_csv(outfile,index=None)



#######################################################################
#######################################################################

###############____Bin Power________##################
def bin_power(X,Band,Fs):
	C = fft(X)
	C = abs(C)
	Power =zeros(len(Band)-1)
	for Freq_Index in range(0,len(Band)-1):
		Freq = float(Band[Freq_Index])										
		Next_Freq = float(Band[Freq_Index+1])
		Power[Freq_Index] = sum(C[int(floor(Freq/Fs*len(X))):int(floor(Next_Freq/Fs*len(X)))])
	Power_Ratio = Power/sum(Power)
	return Power, Power_Ratio	
###################################################
 
################____entropy_simple____################
def ent(data):
    p_data= data.value_counts()/len(data) # calculates the probabilities
    entr= scipy.stats.entropy(p_data)  # input probabilities to get the entropy 
    return entr
######################################################

###############____s_Entropy________##################    
def spectral_entropy(X, Band, Fs, Power_Ratio = None):
	
	if Power_Ratio is None:
		Power,Power_Ratio = bin_power(X, Band, Fs)

	Spectral_Entropy = 0
	for i in range(0, len(Power_Ratio) - 1):
		Spectral_Entropy += Power_Ratio[i] * log(Power_Ratio[i])
	Spectral_Entropy /= log(len(Power_Ratio))	# to save time, minus one is omitted
	return -1 * Spectral_Entropy
#########################################################################################    

###############____Fdiff________##################
def first_order_diff(X):
	D=[]
	
	for i in range(1,len(X)):
		D.append(X[i]-X[i-1])

	return D
#################################################################

###############____pfd________##################
def pfd(X, D=None):
	
	if D is None:																						## Xin Liu
		D = first_order_diff(X)
	N_delta= 0; #number of sign changes in derivative of the signal
	for i in range(1,len(D)):
		if D[i]*D[i-1]<0:
			N_delta += 1
	n = len(X)
	return log10(n)/(log10(n)+log10(n/n+0.4*N_delta))
#################################################################

def hjorth(X, D=None):

    if D is None:
        D = numpy.diff(X)
        D = D.tolist()

    D.insert(0, X[0])  # pad the first difference
    D = numpy.array(D)

    n = len(X)

    M2 = float(sum(D ** 2)) / n
    TP = sum(numpy.array(X) ** 2)
    M4 = 0
    for i in range(1, len(D)):
        M4 += (D[i] - D[i - 1]) ** 2
    M4 = M4 / n

    return numpy.sqrt(M2 / TP), numpy.sqrt(
        float(M4) * TP / M2 / M2
    )  # Hjorth Mobility and Complexity

##########################################################################################
#################____MAIN______################
    
hjorthlist=list()
Power=list()
Power_Ratio=list()
sorting=list()
pfdlist=list()
spec_entr=list()
entr=list()

file=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Tests\Stage-2 (First)\Stage-2_Complete.csv"
outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Tests\Stage-2 (First)\Stage-2_Train.csv"

df = pd.read_csv(file)
Class=df["Class"]
df=df.drop("Class",axis=1)
df.dropna(inplace=True)

df1=df.T
band = [0.5,4,7,12,30,100]
dflist=pd.DataFrame()

powr=[]
powr_rat=[]
hjorth_val=[]

shape = df1.shape 
length=shape[1]

dflist['Mean'] = df.mean(axis=1)
dflist['Peak'] = df.max(axis=1)
dflist['Variance'] = df.var(axis=1)
dflist['Min'] = df.min(axis=1)

for x in range(0, length):
  data1 = df1[x]
  powr,powr_rat = bin_power(data1,band,128)
  Power.append(powr)
  Power_Ratio.append(powr_rat)

for i in range(0, length):
    sorting.append(Power[i][0])

dflist['Power-0'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power[i][1])

dflist['Power-1'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power[i][2])

dflist['Power-2'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power[i][3])

dflist['Power-3'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power[i][4])

dflist['Power-4'] = sorting
del sorting[:]


for i in range(0, length):
    sorting.append(Power_Ratio[i][0])

dflist['PSI-0'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power_Ratio[i][1])

dflist['PSI-1'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power_Ratio[i][2])

dflist['PSI-2'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power_Ratio[i][3])

dflist['PSI-3'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(Power_Ratio[i][4])

dflist['PSI-4'] = sorting
del sorting[:]


for x in range(0, length):
  data1 = df1[x]
  
  pfdx = pfd(data1)
  pfdlist.append(pfdx)
dflist['PFD'] = pfdlist

band1 = [0.5,4,7,12,30,100]
entr_sp=[]
for x in range(0, length):
  data1 = df1[x]
  entr_sp= spectral_entropy(data1,band1,128)
  spec_entr.append(entr_sp)

dflist['Spec-Entr'] = spec_entr

ent_val=[]
for y in range(0, length):
  data2 = df1[y]
  ent_val= ent(data2)
  entr.append(ent_val)
  
dflist['entropy'] = entr

for y in range(0, length):
  data2 = df1[y]
  hjorth_val= hjorth(data2)
  hjorthlist.append(hjorth_val)
  
for i in range(0, length):
    sorting.append(hjorthlist[i][0])

dflist['Hjorth-0'] = sorting
del sorting[:]

for i in range(0, length):
    sorting.append(hjorthlist[i][1])

dflist['Hjorth-1'] = sorting
del sorting[:]

dflist['Class'] = Class
dflist.to_csv(outfile,index=None)


