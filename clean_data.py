import json
import requests
import pickle
import csv
import sys
import time
import pandas as pd


#We define two functions which parse the time variables and convert them to seconds

def parse_time(string):
    spliting=string.split( )
    time = float(spliting[0])
    if spliting[1] == 'minutes' or spliting[1] == 'minute':
        time = time * 60
    elif spliting[1] == 'hour' or spliting[1] == 'hours':
        time = time * 3600
    
    
    return time

def parse_times2(string):
    if string == 0:
        return 0
    else:
        spliting = string.split(':')
        long = len(spliting)
        if long == 1:
            time = int(spliting[0])
        elif long == 2:
            time = int(spliting[1])+60*int(spliting[0])
        elif long == 3:
            time = int(spliting[2])+60*int(spliting[1])+3600*int(spliting[0])
        
        return time
    
    
#This function simply identifies the class of a given hero

def check_class(hero):
    clas='ee'
    if hero in attack:
        clas='attack'
    elif hero in defense:
        clas='defense'
    elif hero in tank:
        clas='tank'
    elif hero in support:
        clas='support'
    return clas
    


if __name__ == "__main__":
    
    #We start by opening the cache that we created previously and defining the heroes list.
    with open('cache_OW.pickle', 'rb') as handle:
        cache = pickle.load(handle)

    attack = ['doomfist','genji','mccree','pharah','reaper','soldier76','sombra','tracer']
    defense = ['bastion','hanzo','junkrat','mei','torbjorn','widowmaker']
    tank = ['dVa','orisa','reinhardt','roadhog','winston','zarya']
    support = ['ana','lucio','mercy','moira','symmetra','zenyatta']
    heroes_list = attack + defense + tank + support    


    '''We will flatten now the data. We will generate a new dictionary with the same structure
    than the entry data {player:hero:{data}....} where the data dictionary will contain the
    information for the quick play stats of each individual hero
    '''
    data = {}
    for player in cache.keys():
        data[player] = {}
        for hero in cache[player].keys():
            data[player][hero] = {}
            data[player][hero].update(cache[player][hero]['game'])
            data[player][hero].update(cache[player][hero]['combat'])
            data[player][hero].update(cache[player][hero]['matchAwards'])
            partial=data[player][hero]['timePlayed']
            if partial == '--':
                partial = '0 seconds'
            data[player][hero]['timePlayed'] = parse_time(partial)

    #We now create a pandas dataframe out of the data, dropping the player name and cleaning it a bit, by dropping weird columns

    final=pd.DataFrame()
    for player in data.keys():
        for hero in data[player].keys():
            dicti=data[player][hero]
            dicti.update({'hero':hero})
            dfp=pd.Series(dicti)
            dfp=dfp.to_frame().transpose()
            final=pd.concat([final,dfp])
    final=final.fillna(value=0)     
    final=final.drop(columns='overwatchGuid0x0860000000000033')



    final=final.drop('winPercentage',axis=1) #Win percentage can be computed easily by comparing total games and won games, so we drop it.
    final['class'] = final['hero'].apply(check_class) #We create a new column with the class of the hero.
    final['criticalHitsAccuracy'] = final['criticalHitsAccuracy'].str.rstrip('%').astype('float') / 100.0 #We convert percentages to absolute values.
    final['weaponAccuracy'] = final['weaponAccuracy'].str.rstrip('%').astype('float') / 100.0
    final=final.fillna(value=0)  

    final['objectiveTime']=final['objectiveTime'].apply(parse_times2) #We parse the times variables and reset the index.
    final['timeSpentOnFire']=final['timeSpentOnFire'].apply(parse_times2)
    final=final.reset_index().drop('index',axis=1)

    final.to_csv('OW_dataset.csv')