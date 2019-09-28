import json
import recordtype
import requests
champ_data = requests.get(r'http://ddragon.leagueoflegends.com/cdn/9.15.1/data/en_US/champion/Aatrox.json')

class Champion:
    Champions = []
    def __init__(self, name, title, lore, allytips, enemytips, spells):
        self.name = name
        self.title = title
        self.lore = lore
        self.allytips = allytips
        self.enemytips = enemytips
        self.spells = spells
        Champion.Champions.append(self)

    def extract_spells(self):
        z = self.spells.copy()
        self.spells = []
        for spell in z:
            self.spells.append([spell['id'], spell['name'], spell['description']])
z = champ_data.json()['data']['Aatrox']

Champion(z['id'], z['title'], z['lore'], z['allytips'], z['enemytips'], z['spells'])
#print(z)
#for id in Champion.Champions[0].spells:
#    print(id)

Champion.Champions[0].extract_spells()
print(Champion.Champions[0].spells)
x = ''
