import requests
import json
from collections import namedtuple
from recordtype import recordtype
from bs4 import BeautifulSoup


key = 'RGAPI-fbe2dda4-170d-48fe-8151-00002d5eb332'
champion = namedtuple("champion", 'name, id')
item = namedtuple("item", 'name, id, cost')
summoner = namedtuple("summoner", 'name, Summonerid, Accountid, puuid')
champions = [] # This holds the champion name and ids
items = [] # This holds the items information
items_id = []
summoners = [] # This holds the summoners that we are looking up currently.
champ_information = []

request = requests.get(r'https://developer.riotgames.com/game-constants.html')
soup = BeautifulSoup(request.content, "html.parser")
c = soup.find_all('tbody')
maps = []
list_of_maps = []

c = c[2].find_all('td')
for i in c:
    maps.append(i.text)

for i in range(14):
    f = (maps[:3])
    del maps[:3]
    list_of_maps.append(f)

patch = '9.15.1'
counter = 0

champ_data = json.load(
    open(r'/Users/kennedy/Desktop/Python_Projects/RIOT_API/updatedchampion.json', encoding='utf8'))
item_data = json.load(
    open(r'/Users/kennedy/Desktop/Python_Projects/RIOT_API/League_items.json', encoding='utf8'))

for x in champ_data['data']:
    champions.append(champion(x, champ_data['data'][x]['key']))
champions.append(champion("No ban", -1))
for id in item_data['data']:
    items_id.append(id)

for itemz, id in zip(item_data['data'], items_id):
    items.append(item(item_data['data'][id]['name'], id, item_data['data'][id]['gold']['total']))
    #print(item_data['data'][id]['name'] + ': ' + item_data['data'][id]['description'])
    counter += 1


def get_summoner_name():
    summoner_name = input("Which summoner do you want to look up?")
    request = requests.get(
        r'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + "?api_key=" + key)
    player = summoner(request.json()["name"], request.json()['id'],
                      request.json()['accountId'], request.json()['puuid'])
    summoners.append(player)
    return request.json()["name"], request.json()['id'], request.json()['accountId'], request.json()['puuid']


def free_rotation():
    freeChamps = []
    request = requests.get(
        r'https://na1.api.riotgames.com/lol/platform/v3/champion-rotations' + "?api_key=" + key)
    for champ in champions:
        if int(champ.id) in request.json()['freeChampionIds']:
            freeChamps.append(champ.name)
    return freeChamps


def get_rank():
    request = requests.get(r'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/' +
                           get_summoner_name()[1] + "?api_key=" + key)
    if len(request.json()) == 0:
        print("No ranked data found.")
    else:
        print(request.json())


def get_status():
    status_list = []
    request = requests.get(
        r'https://na1.api.riotgames.com/lol/status/v3/shard-data' + "?api_key=" + key)
    # print(request.json()['services'])
    for status in request.json()['services']:
        #print(status['name'] + ': ' + status['status'])
        status_list.append(status['name'] + ': ' + status['status'])
    return status_list


def get_champion_abilities():
    for champs in champions:
        request = requests.get('http://ddragon.leagueoflegends.com/cdn/' +
                               patch + '/data/en_US/champion/' + champs.name + '.json')
        for x in request.json()['data'][champs.name]['spells']:
            print(x['id'] + '- ' + x['name'] + ': ' + x['description'] + '\n')


def get_match_history():
    champs_played = {}
    match_history = []
    request = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' +
                           get_summoner_name()[2] + "?api_key=" + key)

    for match in request.json()['matches']:
        match_history.append(match)

    for champion in match_history:
        for champ_id in champions:
            if champion['champion'] == int(champ_id.id):
                champion['champion'] = champ_id.name

    for x in match_history:
        if x['champion'] not in champs_played:
            champs_played[x['champion']] = 1
        else:
            champs_played[x['champion']] += 1

    print(champs_played)
    while True:
        look_up = input("Want to look at all the games with a perticular champion?")
        if look_up in champs_played:
            requested_matches = []
            for match in match_history:
                if look_up == match['champion'] or look_up == match['champion'].lower():
                    requested_matches.append(match)
                    print(match)
            break
        else:
            print("Please enter a valid champion")

    look_up = input("Do you want to look at a specific match?")
    if look_up.lower() == 'yes':
        look_up = int(input("Which game do you want to look at? 0-" +
                            str(len(requested_matches) - 1)))
    else:
        return

    request = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/' +
                           str(requested_matches[look_up]['gameId']) + "?api_key=" + key)
    print(request.json())
    print(request.json()['gameDuration'])
    print(request.json()['gameVersion'])
    print(request.json()['gameMode'])
    print(request.json()['gameType'])

    print("\nEnemy team:")
    print("Team ID:" + str(request.json()['teams'][0]['teamId']))
    print("Victory: " + str(request.json()['teams'][0]['win']))  # Enemy team
    print("First Blood: " + str(request.json()['teams'][0]['firstBlood']))
    print("First Tower: " + str(request.json()['teams'][0]['firstTower']))
    print("Baron Kills: " + str(request.json()['teams'][0]['baronKills']))
    print("Dragon Kills: " + str(request.json()['teams'][0]['dragonKills']))
    print("Rift Herald Kills: " + str(request.json()['teams'][0]['riftHeraldKills']))
    print("Tower Kills: " + str(request.json()['teams'][0]['towerKills']))
    print("Inhibitor Kills: " + str(request.json()['teams'][0]['inhibitorKills']))

    print("\nRequested Summoner's team:")
    print("Team ID:" + str(request.json()['teams'][1]['teamId']))
    print("Victory: " + str(request.json()['teams'][1]['win']))  # Enemy team
    print("First Blood: " + str(request.json()['teams'][1]['firstBlood']))
    print("First Tower: " + str(request.json()['teams'][1]['firstTower']))
    print("Baron Kills: " + str(request.json()['teams'][1]['baronKills']))
    print("Dragon Kills: " + str(request.json()['teams'][1]['dragonKills']))
    print("Rift Herald Kills: " + str(request.json()['teams'][1]['riftHeraldKills']))
    print("Tower Kills: " + str(request.json()['teams'][1]['towerKills']))
    print("Inhibitor Kills: " + str(request.json()['teams'][1]['inhibitorKills']))
    print("\n")

    banned_champs = []
    for ban in request.json()['teams'][0]['bans']:
        for champs in champions:
            if ban['championId'] == int(champs.id):
                banned_champs.append(champs.name)
    if banned_champs:
        print(banned_champs)
    if not banned_champs:
        print("No champions banned")
    banned_champs = []
    for ban in request.json()['teams'][1]['bans']:
        for champs in champions:
            if ban['championId'] == int(champs.id):
                banned_champs.append(champs.name)
    if banned_champs:
        print(banned_champs)
    if not banned_champs:
        print("No champions banned")

    team0 = []
    team1 = []
    match_information = recordtype("Match", 'summoner_name, champion, items, highestrank, kills, deaths, assists, '
                                            'phy_dmg_dealt_to_champs, mag_dmg_dealt_to_champs,'
                                            'total_dmg_dealt_to_champs, dmg_dealt_to_turrets, vision_score,'
                                            'total_dmg_taken, phy_dmg_taken, mag_dmg_taken, gold_earned,'
                                            'gold_spent, wards_bought, wards_placed, wards_killed, cs')
    match_info = []
    for i_ in request.json()['participants']:
        if int(i_['teamId']) == 100:
            team0.append((i_['teamId'], i_['participantId']))
        else:
            team1.append((i_['teamId'], i_['participantId']))

    for i_ in request.json()['participantIdentities']:
        print(i_)

    for counter_, a in enumerate(team0):
        for i_ in request.json()['participantIdentities']:
            if int(a[1]) == i_['participantId']:
                team0[counter_] = i_['player']['summonerName']

    for counter_, a in enumerate(team1):
        for i_ in request.json()['participantIdentities']:
            if int(a[1]) == i_['participantId']:
                team1[counter_] = i_['player']['summonerName']
    print(team0)
    print(team1)
    return match_history

def get_champ_info(): # Will get names, titles, lore, skills and tips for each champion
    global champ_information
    for champ in champions:
        try:
            request = requests.get(r'http://ddragon.leagueoflegends.com/cdn/' + patch +
                                '/data/en_US/champion/' + champ.name + '.json')
            z = request.json()['data'][champ.name]
            champ_information.append([z['id'], z['title'], z['lore'], z['allytips'], z['enemytips'], z['spells']])
        except:
            pass
    return champ_information
# print(list_of_maps)
# get_match_history()
#free = free_rotation()
#print(free)
#get_champ_info()

if __name__ == "__main__":
    for champion in get_champ_info():
        print(champion)
