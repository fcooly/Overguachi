import json
import requests
import pickle
import sys


#We create two classes to store the data scrapped by the API

class player:
    def __init__(self,**entries):
        self.__dict__.update(entries)
        
        
class Hero:
    def __init__(self,**entries):
        self.__dict__.update(entries)        

''' Basic wrapping functions to get the profile of a user and the statistics for specific heroes.
    Includes an option to return the data in JSON format if needed.'''

def get_profile(battletag,platform,region,option=0):

    api_url = '{0}/{1}/{2}/{3}/profile'.format(api_url_base,platform,region,battletag)

    response = requests.get(api_url)

    if response.status_code == 200:
        if option == 0:
            play = player(**json.loads(response.content.decode('utf-8')))
            play.region = region
            play.platform = platform
            play.battletag = battletag
            return play
        elif option == 1:
            return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
    
def get_hero(battletag,hero,platform,region,option=0):

    api_url = '{0}/{1}/{2}/{3}/heroes/{4}'.format(api_url_base,platform,region,battletag,hero)

    response = requests.get(api_url)

    if response.status_code == 200:
        if option == 0:
            play = Hero(**json.loads(response.content.decode('utf-8')))
            play.region = region
            play.platform = platform
            play.battletag = battletag
            play.hero = hero
            return play
        elif option == 1:
            return json.loads(response.content.decode('utf-8'))
    else:
        return None    

#Checks if a user exists. If positive, returns the platform and region of the given user.     
def check_user(battletag):
    out = (0,0)
    for region in regions:
        for platform in platforms:
            partial = get_profile(battletag,platform,region,1)
            if 'error' not in partial.keys():
                out = (platform,region)
                
    if out[1] == 0:
        print('User {0} does not exist'.format(battletag))
    return out   

#This function gets the whole stats for all the heroes for a given user
def get_user_stats(battletag,platform,region):
    final_dict = {}
    for hero in heroes_list:
        partial_object = get_hero(battletag,hero,platform,region)
        try:
            partial_dict = partial_object.quickPlayStats['careerStats'][hero]
            final_dict[hero] = partial_dict
        except KeyError:
            pass
            
    return final_dict  



if __name__ == "__main__":

    #Open the cache or creates it as an empty dictionary if it does not exist
    try:
        with open('cache.pkl', 'rb') as handle:
            cache = pickle.load(handle)
    except:
        cache = {}
    
    
    #Several initialization parameters, including the base url of the API and the heroes list    
    api_url_base = 'https://ow-api.com/v1/stats'
    platforms = ['psn','pc']
    regions = ['eu','us']


    attack = ['doomfist','genji','mccree','pharah','reaper','soldier76','sombra','tracer']
    defense = ['bastion','hanzo','junkrat','mei','torbjorn','widowmaker']
    tank = ['dVa','orisa','reinhardt','roadhog','winston','zarya']
    support = ['ana','lucio','mercy','moira','symmetra','zenyatta']
    heroes_list = attack + defense + tank + support    


    #Loops over the list of players, creates the cache of statistics and save it to the disk.

    players = [] #The list of players is empty for privacity reasons.
    
    for player in players:
        if player not in cache.keys() or option == 1:
            (platform,region) = check_user(player)
            if platform != 0:
                cache[player] = get_user_stats(player,platform,region)
                print('{0} done'.format(player))
    with open('cache_OW.pkl', 'wb') as handle:
        pickle.dump(cache, handle, protocol = pickle.HIGHEST_PROTOCOL)       

