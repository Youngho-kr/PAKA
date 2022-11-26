import requests
from urllib import parse
from datetime import datetime
import pprint
import os

pp = pprint.PrettyPrinter(indent = 4)


class userData:
    def __init__(self, summonerName):
        f = open("C:\\Users\\ad1234\\Desktop\\programming\\PAKA\\LOL_API_KEY.txt", "r")
        self.apiDefault = {
            'region': 'https://kr.api.riotgames.com',
        'regionAsia': 'https://asia.api.riotgames.com',
        'key': f.readline(),
        'summonerName': summonerName,
        }
        f.close()
        self.apiDefault['encodingName'] = parse.quote(self.apiDefault['summonerName'])

        self.request_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.apiDefault['key'],
        }

        urlSummoner = f"{self.apiDefault['region']}/lol/summoner/v4/summoners/by-name/{self.apiDefault['encodingName']}"
        
        self.summoner = requests.get(urlSummoner, headers=self.request_header).json()
        pp.pprint(self.summoner)

        if("status" not in self.summoner.keys()):
            self.apiDefault["summonerId"] = self.summoner['id']
            self.apiDefault["summonerPuuid"] = self.summoner['puuid']

        pp.pprint(self.summoner)

    def isExistSummoner(self):
        # 반환 값에 ["stauts"]["status_code"] 값이 있으면 존재x
        # 반환 값이 200이 아니면 존재x
        if("status" in self.summoner.keys()):
            print("no summoner")
            return False
        return True

    # return 값
    # 0 게임 진행중
    # 1 게임 종료 후 3분이내
    # 2 게임 종료 후 3분 초과
    def isCurrentGame(self):
        urlCurrentGame = f"{self.apiDefault['region']}/lol/spectator/v4/active-games/by-summoner/{self.apiDefault['summonerId']}"
        currentGame = requests.get(urlCurrentGame, headers=self.request_header).json()

        if(currentGame['status']['status_code'] == 404):
            urlMatch = f"{self.apiDefault['regionAsia']}/lol/match/v5/matches/by-puuid/{self.apiDefault['summonerPuuid']}/ids?start=0&count=1"
            match = requests.get(urlMatch, headers = self.request_header).json()

            # 끝난 지 3분 이내
            matchId = match[0]
            urlMatchInfo = f"{self.apiDefault['regionAsia']}/lol/match/v5/matches/{matchId}"
            self.matchInfo = requests.get(urlMatchInfo, headers = self.request_header).json()
            #pp.pprint(self.matchInfo)

            curTimestamp = datetime.now().timestamp()
            print(curTimestamp)
            gameTimestamp = self.matchInfo['info']['gameEndTimestamp']
            gameTimestamp = gameTimestamp // 1000
            print(gameTimestamp)
            print(curTimestamp - gameTimestamp)
            if(curTimestamp - gameTimestamp < 3 * 60): ###
                print('gameTime < 3minute')
                return 1

            return 2

        else:
            print("game is going...")
            print(currentGame)
            return 0

    def checkCarry(self):
        # 게임 승리확인

        userList= self.matchInfo["metadata"]["participants"]
        self.userNum = userList.index(self.apiDefault['summonerPuuid'])
        print(self.userNum)

        isWin = self.matchInfo["info"]["participants"][self.userNum]['win']
        print(isWin)
        return isWin


    def getChampionName(self):
        userList= self.matchInfo["metadata"]["participants"]
        self.userNum = userList.index(self.apiDefault['summonerPuuid'])
        print(self.userNum)
        
        pp.pprint(self.matchInfo["info"]["participants"][self.userNum])
        championName = self.matchInfo["info"]["participants"][self.userNum]['championName']
        
        return championName
        

if __name__ == "__main__":
    user = userData('변명맨')
    