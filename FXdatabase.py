from pymongo import MongoClient
from bson.binary import Binary
from bson import ObjectId
from subprocess import call

Resolution = ["1", "5", "15", "30", "60", "240", "1440","10080"]
Epic = ['AUDUSD', 'EURUSD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDHUF', 'USDJPY', 'USDMXN', 'USDNOK', 'USDPLN', 'USDSEK', 'USDSGD', 'USDZAR']
Epic2 = {'AUDUSD': ['currencies', 'aud-usd'], 'EURUSD': ['currencies', 'eur-usd'], 'GBPUSD': ['currencies', 'gbp-usd'], 'NZDUSD': ['currencies', 'nzd-usd'], 'USDCAD': ['currencies', 'usd-cad'], 'USDCHF': ['currencies', 'usd-chf'], 'USDHUF': ['currencies', 'usd-huf'], 'USDJPY': ['currencies', 'usd-jpy'], 'USDMXN': ['currencies', 'usd-mxn'], 'USDNOK': ['currencies', 'usd-nok'], 'USDPLN': ['currencies', 'usd-pln'], 'USDSEK': ['currencies', 'usd-sek'], 'USDSGD': ['currencies', 'usd-sgd'], 'USDZAR': ['currencies', 'usd-zar']}

try:
    MongoClient().server_info()
except:
    call('start cmd /K mongod.exe --dbpath "C:\data"', cwd=r"C:\Program\MongoDB\Server\4.4\bin", shell=True)

DB=MongoClient().FX
"""
    for epic in Epic:
        for resolution in Resolution:
            collection=DB[epic][resolution]
            collection['rates'].drop()
            collection['data'].drop()
            collection['TA'].drop()
            collection['HA']['data'].drop()
            collection['HA']['TA'].drop()
"""

DB.General.create_index("Name") 
for epic in Epic:
    for resolution in Resolution:
        collection=DB[epic][resolution]
        collection['rates'].update_one({"Time":{"$exists":True}}, {"$set": {"Time":''}}, upsert=True)
        collection['rates'].create_index("Time") 
        collection['data'].update_one({"Time":{"$exists":True}}, {"$set": {"Time":''}}, upsert=True)
        collection['data'].create_index("Time") 
        #collection['TA'].update_one({"Time":{"$exists":True}}, {"$set": {"Time":''}}, upsert=True)
        #collection['TA'].create_index("Time") 
        collection['HA']['data'].update_one({"Time":{"$exists":True}}, {"$set": {"Time":''}}, upsert=True)
        collection['HA']['data'].create_index("Time") 
        #collection['HA']['TA'].update_one({"Time":{"$exists":True}}, {"$set": {"Time":''}}, upsert=True)
        #collection['HA']['TA'].create_index("Time") 

        collection['rates']
        collection['data']
        collection['MA']
        collection['TA']
        collection['ML']

del collection
