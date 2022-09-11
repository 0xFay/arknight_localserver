import mitmproxy.http
from mitmproxy import http
import json, random

Servers = ["ak-gs-gf.hypergryph.com"]

dangerous = ["android.bugly.qq.com"]

blacklist = [
    'char_504_rguard','char_507_rsnipe','char_506_rmedic',
    'char_505_rcast','token_10000_silent_healrb','token_10001_deepcl_tentac',
    'token_10003_cgbird_bird','token_10004_otter_motter','token_10005_mgllan_drone1',
    'token_10005_mgllan_drone2','token_10005_mgllan_drone3','token_10006_vodfox_doll',
    'token_10007_phatom_twin','token_10008_cqbw_box','token_10009_weedy_cannon',
    'token_10010_folivo_car','token_10011_beewax_oblisk','token_10012_rosmon_shield',
    'token_10013_robin_mine','token_10013_robin_mine','token_10014_bstalk_crab',
    'token_10015_dusk_drgn','trap_001_crate','trap_002_emp',
    'trap_003_gate','trap_005_sensor','trap_006_antidr',
    'trap_007_ballis','trap_008_farm','trap_009_battery',
    'trap_010_frosts','trap_011_ore','trap_012_mine',
    'trap_013_blower','trap_014_tower','trap_015_tree',
    'trap_016_peon','trap_018_bomb','trap_019_electric',
    'trap_020_roadblock','trap_021_flame','trap_022_frosts_friend',
    'trap_023_ore_friend','trap_024_npcsld','trap_025_prison',
    'trap_026_inverter','trap_027_stone','char_508_aguard',
    'char_511_asnipe','char_509_acast','char_510_amedic']


init_diamondShard = 60000 #合成玉
init_gold = 1000000 #龙门币
init_gachaTicket = 0 #单抽票
init_androidDiamond = 1 #安卓原石
init_iosDiamond = 1 #ios原石
init_tenGachaTicket = 0 #十连卷
init_ap = 1000 # 体力


def random_pick(some_list,probabilities):
        x=random.uniform(0,1)
        cumulative_probability=0.0
        for item,item_probability in zip(some_list,probabilities):
            cumulative_probability+=item_probability
            #print(x)
            #print(cumulative_probability)
            if x < cumulative_probability:
                break
        return item

def draw_card():
    draw_number = random_pick([5,4,2,3],[0.02,0.08,0.4,0.5])
    pool = json.loads(open('./pool_table.json', 'r', encoding='UTF-8').read())
    if draw_number == 5:
        card = random.choice(pool['poolInfo'][0]['charIdList'])
    elif draw_number == 4:
        card = random.choice(pool['poolInfo'][1]['charIdList'])
    elif draw_number == 3:
        card = random.choice(pool['poolInfo'][2]['charIdList'])
    elif draw_number == 2:
        card = random.choice(pool['poolInfo'][3]['charIdList'])
    return card

def getlevel(rarity):
    if rarity == 5:
        return [2,90,2,3]
    elif rarity == 4:
        return [2,80,1,2]
    elif rarity == 3:
        return [2,70,0,1]
    elif rarity == 2:
        return [1,55,0,1]
    else:
        return [0,30,-1,0]


class Shipwreck:
    def __init__(self):
        self.init_diamondShard = 60000 #合成玉
        self.diamondShard = self.init_diamondShard
        self.init_gold = 1000000 #龙门币
        self.init_gachaTicket = 0 #单抽票
        self.init_androidDiamond = 1 #安卓原石
        self.init_iosDiamond = 1 #ios原石
        self.init_tenGachaTicket = 0 #十连卷
        self.init_ap = 1000 # 体力
        self.ap = 0
        self.lastApAddTime = 0

        self.character_table = json.loads(open('./character_table.json', 'r', encoding='UTF-8').read())
        
        self.charGroup = {}
        self.chars = {}
        self.dexNav_character = {}
        self.building_chars = {}
        charnumber = 1
        
        self.stageId = ''
        self.squads = {}
        self.local_slots = {}

        for i in self.character_table:
            if i not in blacklist:

                self.charGroup.setdefault(i,{'favorPoint':0})

                rarity = self.character_table[i]['rarity']
                level = getlevel(rarity)
                if i != 'char_002_amiya':
                    skill_number = level[3]
                else:
                    skill_number = 3
                skill = []
                for g in range(skill_number):
                    skill_1 =   {
                            "completeUpgradeTime": -1,
                            "skillId": self.character_table[i]['skills'][g]['skillId'],
                            "specializeLevel": 3,
                            "state": 0,
                            "unlock": 1
                        }
                    skill.append(skill_1)
                #print(skill)
                self.chars.setdefault(str(charnumber),{
                    "charId": i,
                    "defaultSkillIndex": level[2],
                    "evolvePhase": level[0],
                    "exp": 0,
                    "favorPoint": 240000,
                    "gainTime": 1612617450,
                    "instId": charnumber,
                    "level": level[1],
                    "mainSkillLvl": 7,
                    "potentialRank": 5,
                    "skills": skill,
                    "skin": i+"#1"
                        })

                self.dexNav_character.setdefault(i,{
                    "charInstId": charnumber,
                    "count": 5
                        })

                self.building_chars.setdefault(str(charnumber),
                    {
                    "ap": 8640000,
                    "bubble": {
                        "assist": {
                            "add": -1,
                            "ts": 0
                        },
                        "normal": {
                            "add": -1,
                            "ts": 0
                        }
                    },
                    "changeScale": 0,
                    "charId": i,
                    "index": -1,
                    "lastApAddTime": 1613964678,
                    "roomSlotId": "",
                    "workTime": 0
                    })

                charnumber = charnumber +1


    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        print(flow.request.host)


    def request(self,flow):
        if flow.request.host in Servers and flow.request.path.startswith("/quest/battleStart"):
            #flow.request.headers["Host"] = "66.151.51.19"
            #flow.request.set_content(b'')
            text = flow.request.get_text()
            json_text = json.loads(text)
            json_text['squad'] = self.squads["0"]
            #flow.response = http.HTTPResponse.make(404)
            flow.request.set_text(json.dumps(json_text))


        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            #请求时重定向请求
            #flow.request.headers["Host"] = "66.151.51.19"
            text = flow.request.get_text()
            json_text = json.loads(text)
            self.local_slots = json_text['slots']
            print(self.squads)
            json_text['slots'] = self.squads["0"]["slots"]
            flow.request.set_text(json.dumps(json_text))


        elif flow.request.host in Servers and flow.request.path.startswith("/gacha/advancedGacha"):
            #抽卡请求时重定向请求
            flow.request.headers["Host"] = "66.151.51.19"
            flow.request.set_content(b'')
        elif flow.request.host in Servers and flow.request.path.startswith("/gacha/tenAdvancedGacha"):
            #抽卡请求时重定向请求
            flow.request.headers["Host"] = "66.151.51.19"
            flow.request.set_content(b'')

        #elif flow.request.host not in Servers:
        #    flow.response = http.HTTPResponse.make(404)
        elif flow.request.host in dangerous:
            #抽卡请求时重定向请求
            flow.request.headers["Host"] = "66.151.51.19"
            flow.request.set_content(b'')


    def response(self,flow: mitmproxy.http.HTTPFlow):
        if flow.request.host in Servers and flow.request.path.startswith("/account/syncData"):
            text = flow.response.get_text()
            json_text = json.loads(text)
            print(flow.request.headers['uid'])
            print('-----------------')
            json_text['user']['building']['chars'] = self.building_chars
            json_text['user']['dexNav']['character'] = self.dexNav_character
            json_text['user']['troop']['charGroup'] = self.charGroup
            json_text['user']['troop']['chars'] = self.chars
            json_text['user']['status']['androidDiamond'] = self.init_androidDiamond
            json_text['user']['status']['diamondShard'] = self.init_diamondShard
            json_text['user']['status']['gold'] = self.init_gold
            json_text['user']['status']['gachaTicket'] = self.init_gachaTicket
            #json_text['user']['status']['iosDiamond'] = init_iosDiamond
            json_text['user']['status']['tenGachaTicket'] = self.init_tenGachaTicket
            self.ap = json_text['user']['status']['ap']
            self.lastApAddTime = json_text['user']['status']['lastApAddTime']
            self.squads = json_text['user']['troop']['squads']
            #print(self.squads)
            print('success')
            flow.response.set_text(json.dumps(json_text))

        elif flow.request.host in Servers and flow.request.path.startswith("/quest/squadFormation"):
            #请求时重定向请求
            text = flow.response.get_text()
            json_text = json.loads(text)
            json_text['playerDataDelta']['modified']['troop']['squads']["0"]["slots"] = self.local_slots
            flow.response.set_text(json.dumps(json_text))


        elif flow.request.host in Servers and flow.request.path.startswith("/gacha/advancedGacha"):
            flow.response = http.HTTPResponse.make(200)
            json_text = json.loads(open('./shotst.json', 'r', encoding='UTF-8').read())

            charget = draw_card()
            charget_number = self.dexNav_character[charget]['charInstId']
            
            json_text['charGet'] = {
                    "charId": charget,
                    "charInstId": charget_number,
                    "isNew": 1,
                    "itemGet": [
                        {
                            "count": 1,
                            "id": "4004",
                            "type": "HGG_SHD"
                                }
                            ]
                        }
            self.diamondShard = self.diamondShard - 600
            json_text['playerDataDelta']['modified']['troop']['chars'] = {charget_number:self.chars[str(charget_number)]}
            json_text['playerDataDelta']['modified']['troop']['charGroup'] = {charget: self.charGroup[charget]}
            json_text['playerDataDelta']['modified']['status']['diamondShard'] = self.diamondShard
            flow.response.set_text(json.dumps(json_text))

        #elif flow.request.host in Servers and flow.request.path.startswith("/gacha/advancedGacha"):
        #    print('')

        elif flow.request.host in Servers and flow.request.path.startswith("/gacha/tenAdvancedGacha"):
            flow.response = http.HTTPResponse.make(200)
            json_text = {"gachaResultList": [], "playerDataDelta": {"deleted": {}, "modified": {}}, "result": 0}
            charget_list = []
            for i in range(10):
                charget = draw_card()
                charget_number = self.dexNav_character[charget]['charInstId']
                charget_list.append({
                    "charId": charget,
                    "charInstId": charget_number,
                    "isNew": 1,
                    "itemGet": [
                        {
                            "count": 1,
                            "id": "4004",
                            "type": "HGG_SHD"
                                }
                            ]
                        })
                
                self.diamondShard = self.diamondShard - 600
                #json_text['playerDataDelta']['modified']['troop']['chars'] = {charget_number:self.chars[str(charget_number)]}
                #json_text['playerDataDelta']['modified']['troop']['charGroup'] = {charget: self.charGroup[charget]}
                #json_text['playerDataDelta']['modified']['status']['diamondShard'] = self.diamondShard
            json_text['gachaResultList'] = charget_list
            flow.response.set_text(json.dumps(json_text))

addons = [
    Shipwreck()
]
#mitmweb.exe -s .\test2.py --ssl-insecure -p 8080