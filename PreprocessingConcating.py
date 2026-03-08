import pandas as pd 
import os 
import glob

#for BEB
indir=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Datasets\BEB"
outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Concat\BEB.csv"
os.chdir(indir)
filelist=glob.glob("*.csv")
dflist=[]
for filename in filelist:
    print(filename)
    df=pd.read_csv(filename,sep=',', header=1)
    df.drop(df.columns[:2], axis=1, inplace=True)   #cutting columns
    df.drop(df.columns[1:], axis=1, inplace=True)
    df.drop(df.index[:256], axis=0, inplace=True)  #cutting rows
    df.drop(df.index[384:], axis=0, inplace=True)
    df.reset_index(inplace=True,drop = True)
    dflist.append(df)
concatdf=pd.concat(dflist,axis=1,ignore_index = True)
concatdf.to_csv(outfile,index=None)
df = pd.read_csv(outfile)
df = df.transpose() #rows and columns transposer 
df.to_csv(outfile,index=None)


#for CLN
indir=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Datasets\CLN"
outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Concat\CLN.csv"
os.chdir(indir)
filelist=glob.glob("*.csv")
dflist=[]
for filename in filelist:
    print(filename)
    df=pd.read_csv(filename,sep=',', header=1)
    df.drop(df.columns[:2], axis=1, inplace=True)   #cutting columns
    df.drop(df.columns[1:], axis=1, inplace=True)
    df.drop(df.index[:256], axis=0, inplace=True)  #cutting rows
    df.drop(df.index[384:], axis=0, inplace=True)
    df.reset_index(inplace=True,drop = True)
    dflist.append(df)
concatdf=pd.concat(dflist,axis=1,ignore_index = True)
concatdf.to_csv(outfile,index=None)
df = pd.read_csv(outfile)
df = df.transpose() #rows and columns transposer 
df.to_csv(outfile,index=None)

#for HVU
indir=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Datasets\HVU"
outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Concat\HVU.csv"
os.chdir(indir)
filelist=glob.glob("*.csv")
dflist=[]
for filename in filelist:
    print(filename)
    df=pd.read_csv(filename,sep=',', header=1)
    df.drop(df.columns[:2], axis=1, inplace=True)   #cutting columns
    df.drop(df.columns[1:], axis=1, inplace=True)
    df.drop(df.index[:256], axis=0, inplace=True)  #cutting rows
    df.drop(df.index[384:], axis=0, inplace=True)
    df.reset_index(inplace=True,drop = True)
    dflist.append(df)
concatdf=pd.concat(dflist,axis=1,ignore_index = True)
concatdf.to_csv(outfile,index=None)
df = pd.read_csv(outfile)
df = df.transpose() #rows and columns transposer 
df.to_csv(outfile,index=None)

#for MED
indir=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Datasets\MED"
outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Concat\MED.csv"
os.chdir(indir)
filelist=glob.glob("*.csv")
dflist=[]
for filename in filelist:
    print(filename)
    df=pd.read_csv(filename,sep=',', header=1)
    df.drop(df.columns[:2], axis=1, inplace=True)   #cutting columns
    df.drop(df.columns[1:], axis=1, inplace=True)
    df.drop(df.index[:256], axis=0, inplace=True)  #cutting rows
    df.drop(df.index[384:], axis=0, inplace=True)
    df.reset_index(inplace=True,drop = True)
    dflist.append(df)
concatdf=pd.concat(dflist,axis=1,ignore_index = True)
concatdf.to_csv(outfile,index=None)
df = pd.read_csv(outfile)
df = df.transpose() #rows and columns transposer 
df.to_csv(outfile,index=None)


#for WNK
indir=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Datasets\WNK"
outfile=r"C:\Users\usama\Desktop\Multi-Commands\Bilal's Data (Only)\Command-6\Concat\WNK.csv"
os.chdir(indir)
filelist=glob.glob("*.csv")
dflist=[]
for filename in filelist:
    print(filename)
    df=pd.read_csv(filename,sep=',', header=1)
    df.drop(df.columns[:2], axis=1, inplace=True)   #cutting columns
    df.drop(df.columns[1:], axis=1, inplace=True)
    df.drop(df.index[:256], axis=0, inplace=True)  #cutting rows
    df.drop(df.index[384:], axis=0, inplace=True)
    df.reset_index(inplace=True,drop = True)
    dflist.append(df)
concatdf=pd.concat(dflist,axis=1,ignore_index = True)
concatdf.to_csv(outfile,index=None)
df = pd.read_csv(outfile)
df = df.transpose() #rows and columns transposer 
df.to_csv(outfile,index=None)
