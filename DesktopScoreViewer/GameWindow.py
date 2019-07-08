import wx
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class GameWindow(wx.Frame):
    def __init__(self, parent, text, button):

        gameurl = "https://www.espn.com" + str(button.link.get('href'))
        #adds option to open browser in background
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(executable_path='/Users/josephjung/PycharmProjects/DesktopScoreViewer/geckodriver',
                                        options=options)
        self.driver.get(gameurl)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        #get game status
        gamestatus = soup.find('div', class_='mlbGamecast__pitchCount')
        balls = gamestatus.find('div', class_='pitchCount__item pitchCount__item--balls')
        strikes = gamestatus.find('div', class_='pitchCount__item pitchCount__item--strikes')
        outs = gamestatus.find('div', class_='pitchCount__item pitchCount__item--outs')

        self.ballcount = 0;
        self.strikecount = 0;
        self.outcount = 0;

        ball = balls.findAll('span')
        for b in ball:
            if(len(b.attrs['class']) > 1):
                self.ballcount += 1

        strike = strikes.findAll('span')
        for s in strike:
            if(len(s.attrs['class']) > 1):
                self.strikecount += 1

        out = outs.findAll('span')
        for o in out:
            if(len(o.attrs['class']) > 1):
                self.outcount += 1

        wx.Frame.__init__(self, parent, title=text, size=(400,222),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.gamepanel = wx.Panel(self)
        self.parent = parent
        self.gamewindowsizer = wx.BoxSizer(wx.VERTICAL)

        self.titledivider1 = wx.StaticBox(self.gamepanel)
        self.titledivider2 = wx.StaticBox(self.gamepanel)
        self.scoredivider = wx.StaticBox(self.gamepanel)
        self.titlesizer1 = wx.StaticBoxSizer(self.titledivider1, wx.HORIZONTAL)
        self.titlesizer2 = wx.StaticBoxSizer(self.titledivider2, wx.HORIZONTAL)
        self.scoresizer = wx.StaticBoxSizer(self.scoredivider, wx.HORIZONTAL)
        self.but = button

        self.hometext = wx.StaticText(self.gamepanel, label="HOME")
        self.awaytext = wx.StaticText(self.gamepanel, label="AWAY")
        self.inningtext = wx.StaticText(self.gamepanel, label="INNING")
        topfont = wx.Font(16, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.hometext.SetFont(topfont)
        self.awaytext.SetFont(topfont)

        self.titlesizer1.Add(self.hometext, 1, wx.CENTER | wx.EXPAND | wx.ALL, 1)
        self.titlesizer1.Add(self.inningtext, 1, wx.CENTER | wx.EXPAND | wx.ALL, 1)
        self.titlesizer1.Add(self.awaytext, 1, wx.CENTER | wx.EXPAND | wx.ALL, 1)

        teamfont = wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_MAX, wx.FONTWEIGHT_NORMAL)
        teamsplaying = self.but.gameinfo.findAll('span', class_="sb-team-abbrev")

        self.hometeam = wx.StaticText(self.gamepanel, label=teamsplaying[0].text)
        self.awayteam = wx.StaticText(self.gamepanel, label=teamsplaying[1].text)
        self.toptext = wx.StaticText(self.gamepanel, label="TOP")

        self.hometeam.SetFont(teamfont)
        self.awayteam.SetFont(teamfont)

        self.titlesizer2.Add(self.hometeam, 1, wx.CENTER | wx.EXPAND | wx.ALL, 1)
        self.titlesizer2.Add(self.toptext, 1, wx.CENTER | wx.EXPAND | wx.ALL, 1)
        self.titlesizer2.Add(self.awayteam, 1, wx.CENTER | wx.EXPAND | wx.ALL, 1)

        teamscores = soup.findAll('div', class_='score-container')
        gameinning = soup.find('span', class_='status-detail')

        self.homescore = wx.StaticText(self.gamepanel, label=teamscores[0].find('div').text)
        self.awayscore = wx.StaticText(self.gamepanel, label=teamscores[1].find('div').text)
        self.inning = wx.StaticText(self.gamepanel, label=gameinning.text)
        self.homescore.SetFont(topfont)
        self.awayscore.SetFont(topfont)
        self.inning.SetFont(topfont)

        self.scoresizer.Add(self.homescore, 1, wx.EXPAND | wx.CENTER, 1)
        self.scoresizer.Add(self.inning, 1, wx.EXPAND | wx.CENTER, 1)
        self.scoresizer.Add(self.awayscore, 1, wx.EXPAND | wx.CENTER, 1)

        self.gamewindowsizer.Add(self.titlesizer1, 1, wx.EXPAND | wx.CENTER)
        self.gamewindowsizer.Add(self.titlesizer2, 1, wx.EXPAND | wx.CENTER)
        self.gamewindowsizer.Add(self.scoresizer, 1, wx.EXPAND | wx.CENTER)
        self.gamepanel.SetSizerAndFit(self.gamewindowsizer)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnClose(self, event):
        self.driver.close()
        self.parent.Show()
        self.Destroy()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        ballbrush = wx.Brush("yellow", style=wx.BRUSHSTYLE_SOLID)
        dc.SetBrush(ballbrush)
        if self.ballcount == 0:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(ballbrush)
        dc.DrawCircle(25, 180, 7)
        if self.ballcount == 1:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(ballbrush)
        dc.DrawCircle(55, 180, 7)
        if self.ballcount == 2:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(ballbrush)
        dc.DrawCircle(85, 180, 7)
        if self.ballcount == 3:
            ballbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(ballbrush)
        dc.DrawCircle(115, 180, 7)

        strikebrush = wx.Brush("red", style=wx.BRUSHSTYLE_SOLID)
        dc.SetBrush(strikebrush)
        if self.strikecount == 0:
            strikebrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(strikebrush)
        dc.DrawCircle(175, 180, 7)
        if self.strikecount == 1:
            strikebrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(strikebrush)
        dc.DrawCircle(210, 180, 7)
        if self.strikecount == 2:
            strikebrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(strikebrush)
        dc.DrawCircle(245, 180, 7)

        outbrush = wx.Brush("red", style=wx.BRUSHSTYLE_SOLID)
        dc.SetBrush(outbrush)
        if self.outcount == 0:
            outbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(outbrush)
        dc.DrawCircle(375, 180, 7)
        if self.outcount == 1:
            outbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(outbrush)
        dc.DrawCircle(340, 180, 7)
        if self.outcount == 2:
            outbrush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
            dc.SetBrush(outbrush)
        dc.DrawCircle(305, 180, 7)