import pickle
import numpy as np
from FXdatabase import *


class TechInd:

    lastModified=''
    def __init__(self):
        self.DirectionValue=0
        self.meanClose=1
        self.ClassicalIndicator=0
        self.CandlestickPattern=0
        self.MachineLearning=0
        self.Volatility=0
        self.Performance=''
        self.Range=[]
        self.Levels=[]
        self.RiskRewardRatio=[]
        self.Other={}


def init(epic, Resolution, epic2):
       
    techIndMatrix = {}

    techIndMatrix['streamPrice'] = 0

    techIndMatrix['Sentiment'] = ''

    techIndMatrix['RiskRewards']='',np.array([])

    if(epic[:3]=='USD'):
        techIndMatrix['Name'] = epic[3:]
    else:
        techIndMatrix['Name'] = epic[:3]
       
    for resolution in Resolution:
        techIndMatrix[resolution]=TechInd()
        
    return techIndMatrix

def INIT(Epic, Resolution, Epic2):
   
    #lastModified = {}
   
    TechIndMatrix = {}
   
    for epic in Epic:
       
        #lastModified[epic] = {}
       
        TechIndMatrix[epic] = init(epic, Resolution, Epic2[epic])

    return TechIndMatrix

def loadData(DB, Epic, Epic2, Resolution):
    TechIndMatrix={}
    for epic in Epic:
        try:#if DB.General.count_documents({"Name":{"$exists":True, '$in':['TechIndMatrix/'+epic]}})==1:
            TechIndMatrix[epic]=pickle.loads(DB.General.find_one({'Name': 'TechIndMatrix/'+epic})['bin-data'])
        except:#else:
            TechIndMatrix[epic] = init(epic, Resolution, Epic2[epic])

    return TechIndMatrix

TechIndMatrix = loadData(DB, Epic, Epic2, Resolution)

def saveData(DB, Epic, TechIndMatrix):
    for epic in Epic:
        pickled = pickle.dumps(TechIndMatrix[epic])
        DB.General.update_one({'Name':'TechIndMatrix/'+epic},{'$set':{'bin-data':Binary(pickled)}}, upsert=True)


