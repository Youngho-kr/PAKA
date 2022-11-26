import tkinter as tk
import lol
import os
import sys
from pygame  import mixer

class App(tk.Tk):
    summonerName=''
    user=lol.userData(summonerName)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # ??
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = False)
        container.grid_rowconfigure(0, weight= 1)
        container.grid_columnconfigure(0, weight = 1)

        # 기본설정
        self._frame = None
        self.title("PAKA")
        self.geometry("600x400")
        self.resizable(False, False)

        # frame 저장
        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["LoginPage"] = LoginPage(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["LoginPage"].grid(row=0, column=0, sticky="nsew")
        '''
        for F in (StartPage, LoginPage):
            pageName = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[pageName] = frame

            # ??
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        '''


        # 초기화면
        self.showFrame("StartPage")

    # 화면 전환
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()


class StartPage(tk.Frame):
    # 소환사명
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # 배경화면
        background = tk.PhotoImage(file = "C:\\Users\\ad1234\\Desktop\\programming\\PAKA\\background_resize.png")
        backgroundLabel = tk.Label(self, image = background, relief = 'sunken')
        backgroundLabel.image = background
        backgroundLabel.pack()

        tk.Label(self, text="Start Page", font = ('Helvetica', 18, "bold")).pack()

        enterName = tk.Label(self)
        enterName.pack()

        # 기본 값 설정
        enterSummonerName = tk.Entry(self)
        enterSummonerName.insert(0, "Akaps")
        enterSummonerName.place(x = 220, y = 350)

        # 버튼 누르면 소환사명 저장
        mainButton = tk.Button(self, text='시작', command = lambda: self.getSummonerName(enterSummonerName))
        mainButton.place(x = 375, y = 345)

        # 소환사명 유효한지 확인
        #if(self.checkSummonerName()):
            #controller.showFrame("LoginPage")

    def summonerNameError(self):
        errorMessage = tk.Label(self, text = "존재하지 않는 소환사입니다", font=("Arial", 10), bg='black', fg='white')
        errorMessage.place(x = 215, y = 300)

    # 유효한 소환사명인지 확인
    def checkSummonerName(self):
        print("checkSummonerName")
        if(self.controller.summonerName==''):
            self.summonerNameError()
            return False
        else:
            self.controller.user = lol.userData(self.controller.summonerName)
            if(self.controller.user.isExistSummoner() == False):
                self.summonerNameError()
                print("no summoner")
                return False
            else:
                print("input exists")
                return True

    # 소환사명이 유효하면 페이지 전환
    def getSummonerName(self, enterSummonerName):
        self.controller.summonerName = enterSummonerName.get()
        if(self.checkSummonerName()):
            # LoginPage.refresh()
            self.controller.frames["LoginPage"].refresh()
            self.controller.showFrame("LoginPage")



class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        background = tk.PhotoImage(file = "C:\\Users\\ad1234\\Desktop\\programming\\PAKA\\background_black.png")
        backgroundLabel = tk.Label(self, image = background, relief = 'sunken')
        backgroundLabel.image = background
        backgroundLabel.pack()
        

        refreshImage = tk.PhotoImage(file = "C:\\Users\\ad1234\\Desktop\\programming\\PAKA\\squirrel_resize.png")
        mainButton = tk.Button(self, image = refreshImage, command=lambda: self.refresh()) # empty???
        mainButton.image = refreshImage
        mainButton.place(x=510, y=0)

        # 새로고침
        #refreshButton = tk.Button(self, image="C:\\Users\\ad1234\\Desktop\\programming\\PAKA\\.png", command=lambda: self.refresh(), bg='white')
        #refreshButton.pack()

    def refresh(self):
        # summonerName으로 API정보 불러오기
        # API정보 저장하고 Carry확인후 노래 재생
        summonerNameTitle = tk.Label(self, text=self.controller.summonerName, font=("Arial", 35), bg='black', fg='white')
        summonerNameTitle.place(x=20, y=20)
        print(self.controller.summonerName)

        # 0 게임 진행중
        # 1 게임 종료 후 3분이내
        # 2 게임 종료 후 3분 초과
        flag = self.controller.user.isCurrentGame()
        championName = self.controller.user.getChampionName()
        championNameLabel = tk.Label(self, text=championName, font=("Arial", 20), bg='black', fg='white')
        championNameLabel.place(x=20, y=150)
        
        if(flag == 0):
            gameGoingLabel = tk.Label(self, text="game is going...", font=("Arial", 20), bg='black', fg='white')
            gameGoingLabel.place(x=20, y=80)
        elif(flag == 1):
            if(self.controller.user.checkCarry() == True):
                carryLabel = tk.Label(self, text="이게... 아니면...", font=("Arial", 20), bg='black', fg='white')
                carryLabel.place(x=20, y=80)
                self.playMusic()
            else:
                goodGameLabel = tk.Label(self, text="good game...", font=("Arial", 20), bg='black', fg='white')
                goodGameLabel.place(x=20, y=80)
        elif(flag == 2):
            goodGameLabel = tk.Label(self, text="good game...", font=("Arial", 20), bg='black', fg='white')
            goodGameLabel.place(x=20, y=80)

        print("refresh")


    def playMusic(self):
        mixer.init()
        mixer.music.load("C:\\Users\\ad1234\\Desktop\\programming\\PAKA\\music.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

if __name__ == "__main__":
    print(os.getcwd())

    app = App()
    app.mainloop()