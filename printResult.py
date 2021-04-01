import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta

def getTable(TechIndMatrix, Epic, Resolution):

    Rank = {'USD':[0]*(len(Resolution)+1)}
   
    i = [int((datetime.now() + timedelta(hours=-1)).strftime('%M')),int((datetime.now() + timedelta(hours=-1)).strftime('%H')),int((datetime.now() + timedelta(hours=-1)).strftime('%w'))]
    Terminate = np.array([(2-((i[0]+i[1]*60+i[2]*60*24)%int(resolution))/int(resolution)) for resolution in Resolution])
 
    missedEpic=[]
    for epic in Epic:
        
        i = np.mean([TechIndMatrix[epic][resolution].meanClose for resolution in Resolution])
        if i==0:
            missedEpic+=[epic]
        i = Terminate*np.array([TechIndMatrix[epic][resolution].DirectionValue*TechIndMatrix[epic][resolution].meanClose for resolution in Resolution])/i
        i = i/4 + 1/4*Terminate*np.array([TechIndMatrix[epic][resolution].DirectionValue for resolution in Resolution])

        j = []
        maxRes = '1'
        for resolution in Resolution:
            if((abs(TechIndMatrix[epic][resolution].ClassicalIndicator)>2)&(TechIndMatrix[epic][resolution].ClassicalIndicator*TechIndMatrix[epic][resolution].CandlestickPattern>=0)&(TechIndMatrix[epic][resolution].ClassicalIndicator*TechIndMatrix[epic][resolution].MachineLearning>=0)):
                j += [int(np.sign(TechIndMatrix[epic][resolution].ClassicalIndicator))*int(resolution)]
                maxRes = resolution

        if(epic[:3]=='USD'):
            Rank[epic[3:]] = list(-np.around(i,1)) + [-round(sum(i),1)] + [list(-np.array(j))] + [TechIndMatrix[epic]['Sentiment']] + [str(list(-TechIndMatrix[epic]['RiskRewards'][1]))[1:-1]] + [TechIndMatrix[epic]['RiskRewards'][0]]# + ['; '.join(TechIndMatrix[epic]['News'])]
        else:
            Rank[epic[:3]] = list(np.around(i,1)) + [round(sum(i),1)] + [j] + [TechIndMatrix[epic]['Sentiment']] + [str(list(TechIndMatrix[epic]['RiskRewards'][1]))[1:-1]] + [TechIndMatrix[epic]['RiskRewards'][0]]# + ['; '.join(TechIndMatrix[epic]['News'])]

    Table = [[i[0]]+i[1] for i in sorted(Rank.items(), key=lambda x: x[1][-5], reverse=True)]
    
    Table = pd.DataFrame([i[1:] for i in Table],[i[0] for i in Table],Resolution+['Tot 28']+['Buy/Sell']+['Sent.']+['RR']+['RR2'])#+['News'])#+['BBDev']+['BBbreakout']).to_string())
    
    return Table



def printResult(TechIndMatrix, Epic, Resolution):

    print()
    print("*************")
    print(getTable(TechIndMatrix, Epic, Resolution).to_string())
    print("*************")
    print(TechIndMatrix["EURUSD"]["1"].lastModified, datetime.now().strftime('%H:%M:%S'))#,missedEpic)

    #print('\n'.join(TechIndMatrix['RiskRewards']))
