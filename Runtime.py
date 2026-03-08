###########################___________LIBRARIES IMPORT____________############################
import scipy.stats
import pandas as pd 
import numpy
from numpy.fft import fft
from numpy import zeros, floor, log10, log

import mne

import time
import os

import glob

import shutil
###########################_____________FEATURE FUNCTIONS FOR RUNTIME____________#################################################
###############____Spectral Power________##################
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
 
################____Entropy____################
def ent(data):
    p_data= data.value_counts()/len(data) # calculates the probabilities
    entr= scipy.stats.entropy(p_data)  # input probabilities to get the entropy 
    return entr

###############____Shannon_Entropy________##################    
def spectral_entropy(X, Band, Fs, Power_Ratio = None):
	
	if Power_Ratio is None:
		Power,Power_Ratio = bin_power(X, Band, Fs)

	Spectral_Entropy = 0
	for i in range(0, len(Power_Ratio) - 1):
		Spectral_Entropy += Power_Ratio[i] * log(Power_Ratio[i])
	Spectral_Entropy /= log(len(Power_Ratio))	# to save time, minus one is omitted
	return -1 * Spectral_Entropy

###############____First Order diff________##################
def first_order_diff(X):
	D=[]
	
	for i in range(1,len(X)):
		D.append(X[i]-X[i-1])

	return D

###############____Petrosian Fractal Dimension________##################
def pfd(X, D=None):
	
	if D is None:																						
		D = first_order_diff(X)
	N_delta= 0; #number of sign changes in derivative of the signal
	for i in range(1,len(D)):
		if D[i]*D[i-1]<0:
			N_delta += 1
	n = len(X)
	return log10(n)/(log10(n)+log10(n/n+0.4*N_delta))

###############____Hjorth Parameters________##################
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
######################################################################################################

##################################___Class Check___################################################
def result(test,outfile):
           
        dft = pd.read_csv(outfile)
        array = dft.values
                
        X = array[:,0:19]
        Y = array[:,19]
       
        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X = sc.fit_transform(X)
        test = sc.transform(test)
       
        # Applying LDA
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
        lda = LDA()
        X = lda.fit_transform(X, Y)
        test = lda.transform(test)          #for Prediction
           
        from sklearn.ensemble import RandomForestClassifier
        classifier=RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
        classifier.fit(X, Y)
        
        """
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
        classifier.fit(X, Y)
        
        from sklearn.neighbors import KNeighborsClassifier
        classifier = KNeighborsClassifier()
        classifier.fit(X, Y)
        """
        
        y_pred = classifier.predict(test)
        return y_pred
       
############################______MAIN RUNTIME______##################################### 
ask='1'
num=0

while(ask=='1'):
        
    
        num=int(num)
        num=num+1
        num=str(num)
                    
        
        ask=input("\nPress 1 to start operation: \n");
        
        if(ask=='1'):
            os.startfile("C:\Program Files (x86)\Emotiv Xavier TestBench v3.1.21\EmotivXavierTestBench.exe")

            indir=r'C:\Program Files (x86)\Emotiv Xavier TestBench v3.1.21'
            os.chdir(indir)
                                 
            filelist=[]
            while len(filelist)==0:
                print("File Not Found")
                time.sleep(1)
            
                filelist0=glob.glob('*.edf')        #for Deleting both
                filelist=glob.glob('*.edf')         #using only edf
                filelist2=glob.glob('*.md.edf')     #removing md.edf
            
                for filename in filelist2:
                    filelist.remove(filename)
                    
            print("\nFile Found\n")
            filepath=indir + "/" + filelist[0]
            
            time.sleep(10)
                      
            edf = mne.io.read_raw_edf(filepath)
            header = ','.join(edf.ch_names)
          
           
            df1 = edf.to_data_frame() 
            df = df1
            
                        
            
            dflist=[]
            df.dropna(inplace=True)
            df.drop(df.columns[:2], axis=1, inplace=True)
            df.drop(df.columns[1:], axis=1, inplace=True)
            df.drop(df.index[:256], axis=0, inplace=True)
            df.drop(df.index[384:], axis=0, inplace=True)
            df.reset_index(inplace=True,drop = True)  #index reset
            dflist.append(df)
            data=pd.concat(dflist,axis=1,ignore_index = True)  #index reset
            
            hjorthlist=list()
            Power=list()
            Power_Ratio=list()
            
            df=data
            df2=data.T
            band = [0.5,4,7,12,30,100]
            dflist=pd.DataFrame()
            
            powr=[]
            powr_rat=[]
            hjorth_val=[]
            
            
            dflist['Mean'] = df2.mean(axis=1)
            dflist['Peak'] = df2.max(axis=1)
            dflist['Variance'] = df2.var(axis=1)
            dflist['Min'] = df2.min(axis=1)
            
            data1=df2.iloc[0]
            powr,powr_rat = bin_power(data1,band,128)
            Power.append(powr)
            Power_Ratio.append(powr_rat)
            
            
            dflist['Power-0'] = Power[0][0]
            dflist['Power-1'] = Power[0][1]
            dflist['Power-2'] = Power[0][2]
            dflist['Power-3'] = Power[0][3]
            dflist['Power-4'] = Power[0][4]
            
            dflist['PSI-0'] = Power_Ratio[0][0]
            dflist['PSI-1'] = Power_Ratio[0][1]
            dflist['PSI-2'] = Power_Ratio[0][2]
            dflist['PSI-3'] = Power_Ratio[0][3]
            dflist['PSI-4'] = Power_Ratio[0][4]
            
            dflist['PFD'] = pfd(data1)
            
            dflist['Spec-Entr'] = spectral_entropy(data1,band,128)
            
            dflist['entropy'] = ent(data1)
            
            hjorth_val= hjorth(data1)
            hjorthlist.append(hjorth_val)
            
            dflist['Hjorth-0'] = hjorth_val[0]
            dflist['Hjorth-1'] = hjorth_val[1]
            
            testing_file=dflist            
            
##############################TESTING_STAGES##########################

            #STAGE 1:
            file1=r"C:\Users\Bilal\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Tests\Stage-1\Stage-1_Train.csv"
            stage1= result(testing_file,file1)
            
            if(stage1==1):
                file2=r"C:\Users\Bilal\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Tests\Stage-2 (First)\Stage-2_Train.csv"
                stage2= result(testing_file,file2)
                ##############################################################
                if(stage2==1):                    
                        print("\n\nSTAGE-1: ACTION IDENTIFIED\n\n")
                        print("\n\nSTAGE-2: ACTION IDENTIFIED AS Eye Movement\n\n")
                        print("\n\nSTAGE-3: BOTH EYE BLINK\n\n")
                    
                    
                    
                else:
                        print("\n\nSTAGE-1: ACTION IDENTIFIED\n\n")
                        print("\n\nSTAGE-2: ACTION IDENTIFIED AS Eye Movement\n\n")
                        print("\n\nSTAGE-3: CLENCH\n\n")              
                        
            else:
                file2=r"C:\Users\Bilal\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Path-1\Tests\Stage-2 (Second)\Stage-2_Train.csv"
                stage2= result(testing_file,file2)
                ##############################################################
                if(stage2==1):                  
                    print("\n\nSTAGE-1: ACTION IDENTIFIED\n\n")
                    print("\n\nSTAGE-2: ACTION IDENTIFIED AS Headshake Movement\n\n")
                    print("\n\nSTAGE-3: Headshake Up\n\n")
                else:
                        print("\n\nSTAGE-1: ACTION IDENTIFIED\n\n")
                        print("\n\nSTAGE-2: ACTION IDENTIFIED AS Eye Movement\n\n")
                        print("\n\nSTAGE-3: WINK\n\n")              

            
            
            print("\nRestarting\n")
            time.sleep(1)
             
            outfile="C:/Users/Bilal/Desktop/Multi-Commands/Bilal's Data (Only)/Command-6/Path-1/Runtime" + '/' + num + '.csv'
            
            outfile2="C:/Users/Bilal/Desktop/Multi-Commands/Bilal's Data (Only)/Command-6/Path-1/Runtime" + '/' + num + '.edf'
            outfile3="C:/Users/Bilal/Desktop/Multi-Commands/Bilal's Data (Only)/Command-6/Path-1/Runtime" + '/' + num + '.md.edf'
            
            df1.to_csv(outfile,index=None)
            shutil.copy(filelist0[0], outfile2)
            shutil.copy(filelist0[1], outfile3)
            
            os.system("taskkill /f /im EmotivXavierTestBench.exe")
            time.sleep(3)
            for i in range(0, len(filelist0)): 
                os.remove(filelist0[i]) 
                print("\n" + filelist0[i] + " Deleted\n")
        else:
             print("\nThank you\n")
