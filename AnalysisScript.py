import pandas
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
def SSTbehav(infilename):
    
    # Import from a csv file with a header
    df=pandas.read_csv(infilename,skipfooter=1)
    
    # Re-name columns
    df.columns = ['Block','TrialType','Arrow','Response','leftSSD','rightSSD','ACC','RT']
    
    # Check the number of stop trials
    if np.sum(df.TrialType) != 100:
        print("Stop trial number is wrong! (" + str(np.sum(df.TrialType)) + ")")
    
    # Compare correct GO RT vs. Failed Stop RT
    # GO RT should be slower than Failed Stop RT
    GoTrials = df.loc[(df.TrialType==0) & (df.ACC==1), :]
    FsTrials = df.loc[(df.loc[:,'ACC']==4) & (df.loc[:,'RT']<1000), :] # failed stop RT<1000ms included
    GoRT = np.mean(GoTrials.RT)
    FsRT = np.mean(FsTrials.RT)
    
    # Check if p(STOP) converges to .5
    StopTrialNum = np.sum(df.TrialType) # get # of stop trials
    SuccessStopNum = np.sum(df.ACC == 3) # get # of failed stop trials
    p_stop = SuccessStopNum/StopTrialNum
    
    # SSRT (Stop Signal Reaction Time) calculation with replacement with Go omission trials
    # Make a new RT2 column
    df.loc[:,'RT2'] = df.RT

    # Replace Go omission (miss) trials with longest GO RT
    df.loc[df.ACC==0,'RT2'] = np.max(df.RT2)
    
    # Get p(response|STOPSIGNAL): probability of failed stop
    FailedStopNum = np.sum(df.ACC == 4) # get # of failed stop trials
    p_resp = FailedStopNum / StopTrialNum # calculate p(respond|STOP)
    
    # Get RT from GO distribution
    # Find n-th fastest RT, here n = p_resp * 100
    AllGoTrials = df.loc[(df.TrialType==0), :]
    NthRT = np.percentile(np.sort(AllGoTrials.RT), p_resp*100)
    
    # Get one SSD from each trial (if left arrow -> get leftSSD)
    for i in range(0,df.shape[0]):
        if df.Arrow[0] == 1:
            df.loc[i,'SSD'] = df.leftSSD[i]
        else:
            df.loc[i,'SSD'] = df.rightSSD[i]

    # Get all stop trials
    StopTrials = df.loc[df.loc[:,'TrialType']==1,:]

    # Get mean SSD (SSDs in Go trials don't mean anything )
    avgSSD = np.mean(StopTrials.SSD)
    
    # Calculate SSRT 
    # Also calculate SSRT using mean method (meanGO RT - mean SSD)
    SSRTint = NthRT - avgSSD #integration method : NthGO RT - mean SSD
    SSRTmean = GoRT - avgSSD #mean method: mean correct GO RT - mean SSD


    return GoRT, FsRT, p_stop, avgSSD, SSRTint, SSRTmean
    
infiles = glob.glob("./Subject*.csv")
infiles = np.sort(infiles)

data = {'SubID':[],'GoRT':[], 'FsRT':[], 'p_stop':[], 'avgSSD':[], 'SSRTint':[], 'SSRTmean':[]}
df = pandas.DataFrame(data=data)

for i in range(0,len(infiles)):
    GoRT, FsRT, p_stop, avgSSD, SSRTint, SSRTmean = SSTbehav(infiles[i])
    data = {'SubID':infiles[i][9:12],'GoRT':GoRT, 'FsRT':FsRT, 'p_stop':p_stop, 'avgSSD':avgSSD, 'SSRTint':SSRTint, 'SSRTmean':SSRTmean}
    df1 = pandas.DataFrame(data=data, index=[0])
    df = df.append(df1)
#print(df)

t, p = stats.ttest_rel(df.GoRT ,df.FsRT)
print("GO RT vs. Failed Stop RT")
print("t(" + str(df.shape[0]-1) + ") = " + f"{t:.3f}" + ", p = " + f"{p:.3f}")

print(df)

df.to_csv('GroupData.csv')