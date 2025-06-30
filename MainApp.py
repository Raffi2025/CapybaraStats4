import streamlit as st
import requests, csv

#script for updating data:
#special url with all batting player data
batterurl = "https://stats.britishbaseball.org.uk/api/v1/stats/events/2025-a/index?section=players&stats-section=batting&language=en"
pitcherurl = "https://stats.britishbaseball.org.uk/api/v1/stats/events/2025-a/index?section=players&stats-section=pitching&team=&round=&split=&team=&split=&language=en"
#special chatgpt code to access all the data in the url
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://stats.britishbaseball.org.uk/",
    "Origin": "https://stats.britishbaseball.org.uk",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9",
}

#function for splitting the data into individual players
def SplitDataIntoPlayers(data, batter):
    playerList = []
    items = data.split("},{")
    for item in items:
        player = item.split(",")
        if (batter and (len(player) == 26 or len(player) == 28)) or (not batter and (len(player) == 31 or len(player) == 33)):
            playerList.append(player)
    return playerList

#function for parsing batter data
def ParseBatterData(unparsedBatterList):
    batters = []
    for batter in unparsedBatterList:
        #batter = unparsed batter
        player = {}
        player["Player"] = ParseName(batter[23])
        player["Team"] = batter[24].split(":")[1].strip('"')
        player["G"] = int(batter[0][-1:])
        player["AB"] = int(batter[2].split(":")[1])
        player["R"] = int(batter[3].split(":")[1])
        player["H"] = int(batter[4].split(":")[1])
        player["2B"] = int(batter[5].split(":")[1])
        player["3B"] = int(batter[6].split(":")[1])
        player["HR"] = int(batter[7].split(":")[1])
        player["RBI"] = int(batter[8].split(":")[1])
        player["TB"] = int(batter[9].split(":")[1])
        player["AVG"] = float(batter[10].split(":")[1]) / 1000
        player["SLG"] = float(batter[11].split(":")[1]) / 1000
        player["OBP"] = float(batter[12].split(":")[1]) / 1000
        player["OPS"] = float(batter[13].split(":")[1]) / 1000
        player["BB"] = int(batter[14].split(":")[1])
        player["HBP"] = int(batter[15].split(":")[1])
        player["SO"] = int(batter[16].split(":")[1])
        player["GDP"] = int(batter[17].split(":")[1])
        player["SF"] = int(batter[18].split(":")[1])
        player["SH"] = int(batter[19].split(":")[1])
        player["SB"] = int(batter[20].split(":")[1])
        player["CS"] = int(batter[21].split(":")[1])
        batters.append(player)
    return batters

#function for parsing pitcher data
def ParsePitcherData(unparsedPitcherList):
    pitchers = []
    for pitcher in unparsedPitcherList:
        #pitcher = unparsed pitcher
        player = {}
        player["Player"] = ParseName(pitcher[28])
        player["Team"] = pitcher[29].split(":")[1].strip('"')
        player["W"] = int(pitcher[0][-1:])
        player["L"] = int(pitcher[1].split(":")[1])
        player["ERA"] = float(pitcher[2].split(":")[1].strip('"'))
        player["APP"] = int(pitcher[3].split(":")[1])
        player["SV"] = int(pitcher[5].split(":")[1])
        player["CG"] = int(pitcher[6].split(":")[1])
        player["SHO"] = int(pitcher[7].split(":")[1])
        player["IP"] = float(pitcher[8].split(":")[1].strip('"'))
        player["H"] = int(pitcher[9].split(":")[1])
        player["R"] = int(pitcher[10].split(":")[1])
        player["ER"] = int(pitcher[11].split(":")[1])
        player["BB"] = int(pitcher[12].split(":")[1])
        player["SO"] = int(pitcher[13].split(":")[1])
        player["2B"] = int(pitcher[14].split(":")[1])
        player["3B"] = int(pitcher[15].split(":")[1])
        player["HR"] = int(pitcher[16].split(":")[1])
        player["AB"] = int(pitcher[17].split(":")[1])
        player["BAVG"] = float(pitcher[18].split(":")[1]) / 1000
        player["WP"] = int(pitcher[19].split(":")[1])
        player["HB"] = int(pitcher[20].split(":")[1])
        player["BK"] = int(pitcher[21].split(":")[1])
        player["SFA"] = int(pitcher[22].split(":")[1])
        player["SHA"] = int(pitcher[23].split(":")[1])
        player["GO"] = int(pitcher[24].split(":")[1])
        player["FO"] = int(pitcher[25].split(":")[1])
        player["WHIP"] = float(pitcher[26].split(":")[1].strip('"'))
        pitchers.append(player)
    return pitchers

#function for parsing player name
def ParseName(unparsedName):
    firstName = unparsedName.split(">")[4].split("<")[0]
    lastName = unparsedName.split(">")[1].split("<")[0]
    lastName = lastName[0] + lastName[1:].lower()
    name = firstName + " " + lastName
    return name

#function for calling functions to procure batter data
def GetBatterData():
    batterData = requests.get(batterurl, headers=headers).text
    unparsedBatterList = SplitDataIntoPlayers(batterData, batter=True)
    batterList = ParseBatterData(unparsedBatterList)
    return batterList

#function for calling functions to procure pitcher data
def GetPitcherData():
    pitcherData = requests.get(pitcherurl, headers=headers).text
    unparsedPitcherList = SplitDataIntoPlayers(pitcherData, batter=False)
    pitcherList = ParsePitcherData(unparsedPitcherList)
    return pitcherList

batterList = GetBatterData()
pitcherList = GetPitcherData()

def WriteListToCSV(fileName, playerList):
    with open(fileName, "w") as csvFile:
        columnNames = list(playerList[0].keys())
        writer = csv.DictWriter(csvFile, fieldnames=columnNames)
        writer.writeheader()
        for player in playerList:
            writer.writerow(player)

#WriteListToCSV("batters.csv", batterList)
#WriteListToCSV("pitchers.csv", pitcherList)

#Stats Maths
def leagueAverages(arr):
    totalOBP = 0
    totalSLG = 0
    validPeople = 0
    for player in arr:
        if player["PA"] >= 5:
            totalOBP += player["OBP"]
            totalSLG += player["SLG"]
            validPeople += 1
    return totalOBP, totalSLG, validPeople

def PlateAppearances(arr):
    for player in arr:
        PA = player["BB"] + player["HBP"] + player["SF"] + player["SH"] + player["AB"]
        player["PA"] = PA

def WalkPercentage(arr):
    for player in arr:
        try:
            BBPercentage = (player["BB"]/player["PA"])*100
            player["BB%"] = BBPercentage
        except:
            #player["BB%"] = "N/A"
            player["BB%"] = 0

def StrikeOutPercentage(arr):
    for player in arr:
        try:
            SOPercentage = (player["SO"]/player["PA"])*100
            player["SO%"] = SOPercentage
        except:
            #player["SO%"] = "N/A"
            player["SO%"] = 0

def StealSuccessRate(arr):
    for player in arr:
        try:
            SSR = (player["SB"]/(player["SB"] + player["CS"]))*100
            player["SSR"] = SSR
        except:
            #player["SSR"] = "N/A"
            player["SSR"] = 0

def Singles(arr):
    for player in arr:
        OneB = player["H"] - (player["2B"] + player["3B"] + player["HR"])
        player["1B"] = OneB

def IsolatedPower(arr):
    for player in arr:
        ISO = player["SLG"] - player["AVG"]
        player["ISO"] = ISO

def BattingAverageBIP(arr):
    for player in arr:
        try:
            BAbip = (player["H"] - player["HR"])/(player["AB"] - player["SO"] + player["SF"])
            player["BAbip"] = round(BAbip,3)
        except:
            #player["BAbip"] = "N/A"
            player["BAbip"] = 0

def OnBasePlusSluggingPlus(arr):
    totalOBP, totalSLG, validPeople = leagueAverages(batterList)
    for player in arr:
        OPSPlus = ((player["OBP"]/totalOBP) + (player["SLG"]/totalSLG) - 1)*100
        player["OPS+"] = int(OPSPlus)

def WeightedOnBaseAverage(batting, pitching):
    #Step 1
    TotalIP = 0
    for player in pitching:
        TotalIP += player["IP"]
    NumOuts = TotalIP * 3
    TotalRuns = 0
    for player in batting:
        TotalRuns += player["R"]
    RunsPerOut = TotalRuns/NumOuts
    #Step 2/3
    BBRV = RunsPerOut + 0.14
    HBPRV = BBRV + 0.0251
    OneBRV = BBRV + 0.155
    TwoBRV = OneBRV + 0.3
    ThreeBRV = TwoBRV + 0.27
    HRRV = 2
    BBRV += 1
    HBPRV += 1
    OneBRV += 1
    TwoBRV += 1
    ThreeBRV += 1
    HRRV += 1
    

    #Step 4
    TotalBB = 0
    for player in batting:
        TotalBB += player["BB"]
    TotalHBP = 0
    for player in batting:
        TotalHBP += player["HBP"]
    TotalOneB = 0
    for player in batting:
        TotalOneB += player["1B"]
    TotalTwoB = 0
    for player in batting:
        TotalTwoB += player["2B"]
    TotalThreeB = 0
    for player in batting:
        TotalThreeB += player["3B"]
    TotalHR = 0
    for player in batting:
        TotalHR += player["HR"]
    TotalPA = 0
    for player in batting:
        TotalPA += player["PA"]
    #Entire league wOBA
    global LeaguewOBA
    LeaguewOBA = ((BBRV*TotalBB) + (HBPRV*TotalHBP) + (OneBRV*TotalOneB) + (TwoBRV*TotalTwoB) + (ThreeBRV*TotalThreeB) + (HRRV*TotalHR))/TotalPA
    global wOBAScale
    wOBAScale = (totalOBP/validPeople)/LeaguewOBA
    #Step 6
    BBRV = BBRV * wOBAScale
    HBPRV = HBPRV * wOBAScale
    OneBRV = OneBRV * wOBAScale
    TwoBRV = TwoBRV * wOBAScale
    ThreeBRV = ThreeBRV * wOBAScale
    HRRV = HRRV * wOBAScale
    #Step 7
    for player in batting:
        try:
            player["wOBA"] = ((BBRV*player["BB"]) + (HBPRV*player["HBP"]) + (OneBRV*player["1B"]) + (TwoBRV*player["2B"]) + (ThreeBRV*player["3B"]) + (HRRV*player["HR"]))/(player["PA"])
        except:
            #player["wOBA"] = "N/A"
            player["wOBA"] = 0


def LeagueAveragewOBA(arr):
    total = 0
    count = 0 
    for player in arr:
        try:
            total += player["wOBA"]
            count += 1
        except:
            total = total
    return (total/count)


def WeightedRunsAboveAverage(arr):
    for player in arr:
        try:
            wRAA = (((player["wOBA"] - LAwOBA)/wOBAScale) * player["PA"])
            player["wRAA"] = wRAA
        except:
            #player["wRAA"] = "N/A"
            player["wRAA"] = 0

def WeightedRunsCreated(arr):
    global totalR, totalPA
    totalR = 0
    for player in arr:
        try:
            totalR += player["R"]
        except:
            totalR = totalR
    totalPA = 0
    for player in arr:
        try:
            totalPA += player["PA"]
        except:
            totalPA = totalPA
    for player in arr:
        try:
            player["wRC"] = (((player["wOBA"]-LAwOBA)/wOBAScale)+(totalR/totalPA)*player["PA"])
        except:
            player["wRC"] = 0


def WeightedRunsCreatedPlus(arr):
    totalwRCPA = 0 
    count = 0
    for player in arr:
        try:
            totalwRCPA += (player["wRC"])/(player["PA"])
            count += 1
        except:
            totalwRCPA = totalwRCPA
    for player in arr:
        try:
            player["wRC+"] = round((((((player["wRAA"]/player["PA"])+(totalR/totalPA))+((totalR/totalPA)-(1*(totalR/totalPA))))/(totalwRCPA/count))*100))
        except:
            player["wRC+"] = 0

def PitcherBF(arr):
    for player in arr:
        player["BF"] = (player["IP"]*3)+player["H"]+player["BB"]+player["HB"]

def PitcherStrikeOutPercentage(arr):
    for player in arr:
        try:
            player["SO%"] = (player["SO"] /player["BF"])*100
        except:
            player["SO"] = 0


def PitcherWalkPercentage(arr):
    for player in arr:
        try:
            player["BB%"] = (player["BB"] /player["BF"])*100
        except:
            player["BB%"] = 0

def PitcherGOPercentage(arr):
    for player in arr:
        try:
            player["GO%"] = (player["GO"] /player["BF"])*100
        except:
            player["GO%"] = 0

def PitcherFOPercentage(arr):
    for player in arr:
        try:
            player["FO%"] = (player["FO"] /player["BF"])*100
        except:
            player["FO%"] = 0

def XBHPercentage(arr):
    for player in arr:
        try: 
            player["XBH%"] = ((player["2B"]+player["3B"]+player["HR"])/player["H"])*100
        except:
            player["XBH%"] = 0

def WPoverBF(arr):
    for player in arr:
        try:
            player["WP/BF"] = player["WP"]/player["BF"]
        except:
            player["WP/BF"] = 0

def SOoverBB(arr):
    for player in arr:
        try:
            player["SO/BB"] = player["SO"]/player["BB"]
        except:
            player["SO/BB"] = 0   

def ERAplus(arr):
    totalERA = 0 
    for player in arr:
        totalERA += player["ERA"]
    totalERA = totalERA/len(arr)
    for player in arr:
        try:
            player["ERA+"] = round((totalERA/player["ERA"])*100)
        except:
            player["ERA+"] = 0

def PitcherBaBIP(arr):
    for player in arr:
        try:
            player["BAbip"] = (player["H"]-player["HR"])/(player["AB"]-player["SO"]-player["HR"]+player["SFA"])
        except:
            player["BAbip"] = 0

def PitcherAB(arr):
    for player in arr:
        try:
            player["AB"] = player["H"]/player["BAVG"]
        except:
            player["AB"] = 0

PlateAppearances(batterList)
totalOBP, totalSLG, validPeople = leagueAverages(batterList)
WalkPercentage(batterList)
StrikeOutPercentage(batterList)
StealSuccessRate(batterList)
Singles(batterList)
IsolatedPower(batterList)
BattingAverageBIP(batterList)
OnBasePlusSluggingPlus(batterList)
WeightedOnBaseAverage(batterList, pitcherList)
global LAwOBA
LAwOBA = LeagueAveragewOBA(batterList)
WeightedRunsAboveAverage(batterList)
WeightedRunsCreated(batterList)
WeightedRunsCreatedPlus(batterList)
PitcherBF(pitcherList)
PitcherStrikeOutPercentage(pitcherList)
PitcherWalkPercentage(pitcherList)
PitcherGOPercentage(pitcherList)
PitcherFOPercentage(pitcherList)
XBHPercentage(pitcherList)
WPoverBF(pitcherList)
SOoverBB(pitcherList)
ERAplus(pitcherList)
PitcherAB(pitcherList)
PitcherBaBIP(pitcherList)




WriteListToCSV("batters.csv", batterList)
WriteListToCSV("pitchers.csv", pitcherList)

total = 0
for player in pitcherList:
    total += player["IP"]
total = total / len(pitcherList)
print (total)

#streamlit app
page = st.navigation([st.Page("Batters.py"), st.Page("Pitchers.py")])
page.run()

#to run streamlit application:
#run file
#in terminal, run:
#python -m streamlit run "MainApp.py"
#in cmd run:
#pip freeze > requirements.txt
#to make requrements file
