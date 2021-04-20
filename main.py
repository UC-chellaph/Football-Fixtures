import pyodbc
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

currentMD = 1
# --*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*----*-- #

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

teamsmap = {
    'fc-arsenal': 142,
    'aston-villa': 154,
    'brighton-amp-hove-albion': 381,
    'fc-burnley': 435,
    'fc-chelsea': 536,
    'crystal-palace': 646,
    'fc-everton': 942,
    'fc-fulham': 1055,
    'leeds-united': 1524,
    'leicester-city': 1527,
    'fc-liverpool': 1563,
    'manchester-city': 1718,
    'manchester-united': 1724,
    'newcastle-united': 1823,
    'sheffield-united': 2328,
    'fc-southampton': 2471,
    'tottenham-hotspur': 2590,
    'west-bromwich-albion': 2744,
    'west-ham-united': 2802,
    'wolverhampton-wanderers': 2848
}

transfermarktTeamsMap = {
    "manchester-city": 281,
    "tottenham-hotspur": 148,
    "fc-arsenal": 11,
    "aston-villa": 405,
    "brighton-amp-hove-albion": 1237,
    "fc-burnley": 1132,
    "fc-chelsea": 631,
    "crystal-palace": 873,
    "fc-everton": 29,
    "fc-fulham": 931,
    "leeds-united": 399,
    "leicester-city": 1003,
    "fc-liverpool": 31,
    "manchester-united": 985,
    "newcastle-united": 762,
    "sheffield-united": 350,
    "fc-southampton": 180,
    "west-bromwich-albion": 984,
    "west-ham-united": 379,
    "wolverhampton-wanderers": 543
}

def getTeamRosters(teamname):
    link = "https://www.transfermarkt.co.uk/" + teamname + "/kader/verein/%s/saison_id/2020/plus/1" % transfermarktTeamsMap[teamname]

    r = requests.get(link, headers=headers)

    soup = bs(r.content, 'html.parser')

    Player_Name = []  # List that will receive all the players names

    player_tag = soup.find_all("a", {"class": "spielprofil_tooltip"})

    for tag in player_tag:
        Player_Name.append(tag.text)

    del Player_Name[1::2]

    nationality = []
    nationTag = soup.find_all("td", {"class": "zentriert"})

    for tag_nation in nationTag:
        nationFlag = tag_nation.find("img", {"class": "flaggenrahmen"}, {"title": True})

        if (nationFlag != None):
            nationality.append(nationFlag['title'])

    transfer_fee = []

    feeTag = soup.find_all("td", {"class": "rechts hauptlink"})

    for tagTransferFee in feeTag:
        PriceTag = tagTransferFee.text[:-2]
        transfer_fee.append(PriceTag)

    prevClub = []
    prevClubTag = soup.find_all("td", {"class": "zentriert"})

    for table in prevClubTag:
        prevClubBadge = table.find("img")
        if (prevClubBadge != None):
            prevClub.append(prevClubBadge['alt'])

    del prevClub[0::2]

    dataTable = soup.find("table", {"class": "items"})
    cellValues = []
    dateValues = []
    rows = dataTable.find_all("td", {"class": "zentriert"})
    for row in rows:
        cellVal = row.text.replace('\n', '')
        if (cellVal != ""):
            cellValues.append(cellVal)

    dateJoined = []

    dateValues.append(cellValues[4::6])
    for value in dateValues:
        for x in value:
            dateJoined.append(x)

    shirtValues = []
    shirtNumber = []

    shirtValues.append(cellValues[0::6])
    for value in shirtValues:
        for x in value:
            shirtNumber.append(x)

    print(shirtNumber)

    col_headers = ["Name", "Nationality", "Jersey Number", "Value", "Previous Club", "Joined On"]

    df = pd.DataFrame(list(zip(Player_Name, nationality,shirtNumber,transfer_fee,prevClub,dateJoined)),
                      columns=col_headers)


    consolidated = [df]
    return pd.concat(consolidated)

def getTeamTransfers(teamname):
    link = "https://www.transfermarkt.co.uk/" + teamname + "/transferrekorde/verein/%s" % transfermarktTeamsMap[
        teamname]

    r = requests.get(link, headers=headers)

    # Creating a Soup
    soup = bs(r.content, 'html.parser')

    Player_Name = []  # List that will receive all the players names

    player_tag = soup.find_all("a", {"class": "spielprofil_tooltip"})

    for tag in player_tag:
        Player_Name.append(tag.text)

    previousCountry = []  # List that will receive all the names of the countries of the players’s previous leagues.

    prevCountryTag = soup.find_all("td", {"class": None})

    for tag_country in prevCountryTag:
        countryFlag = tag_country.find("img", {"class": "flaggenrahmen"}, {"title": True})

        if (countryFlag != None):  # We will test if we have found any matches than add them
            previousCountry.append(countryFlag['title'])

    nationality = []
    nationTag = soup.find_all("td", {"class": "zentriert"})

    for tag_nation in nationTag:
        nationFlag = tag_nation.find("img", {"class": "flaggenrahmen"}, {"title": True})

        if (nationFlag != None):
            nationality.append(nationFlag['title'])

    transfer_fee = []

    feeTag = soup.find_all("td", {"class": "rechts hauptlink"})

    for tagTransferFee in feeTag:
        PriceTag = tagTransferFee.text
        PriceTag = PriceTag
        transfer_fee.append(PriceTag)

    prevClub = []
    prevClubTag = soup.find_all("table", {"class": "inline-table"})

    for table in prevClubTag:
        prevClubName = table.find("td", {"class": "hauptlink"})
        prevClub.append(prevClubName.text.replace('\n', ''))

    del prevClub[0::2]

    del prevClub[10:]
    del Player_Name[10:]
    del nationality[10:]
    del transfer_fee[10:]

    df = pd.DataFrame({"Player Name": Player_Name, "Nationality": nationality,
                       "Transfer Fee (In Millions of Euros)": transfer_fee, "Previous Club": prevClub})

    consolidated = [df]
    return pd.concat(consolidated)

def getAllCompResults(teamname):
    teamnamealias = teamname
    link = 'https://www.soccerbase.com/teams/team.sd?team_id=%s&comp_id=1' % teamsmap[teamnamealias]

    consolidated = []
    print('Acquiring live %s data...' % teamnamealias)

    headers = ['Competition', 'Home Team', 'Home Score', 'Away Scores', 'Away Team', 'Date Time']
    r = requests.get('%s&teamTabs=results' % link)
    soup = bs(r.content, 'html.parser')

    h_scores = [int(i.text) for i in soup.select('.score a em:first-child')]
    a_scores = [int(i.text) for i in soup.select('.score a em + em')]

    limit = len(a_scores)
    comps = [i.text for i in soup.select('.tournament a', limit=limit)]
    dates = [i.text for i in soup.select('.dateTime .hide', limit=limit)]
    h_teams = [i.text for i in soup.select('.homeTeam a', limit=limit)]
    a_teams = [i.text for i in soup.select('.awayTeam a', limit=limit)]

    df = pd.DataFrame(list(zip(comps, h_teams, h_scores, a_scores, a_teams, dates)),
                      columns=headers)
    consolidated.append(df)

    return pd.concat(consolidated)

def getTopScorer():
    link = 'https://www.transfermarkt.co.uk/premier-league/torschuetzenliste/wettbewerb/GB1/saison_id/2020/altersklasse/alle/detailpos//plus/1'

    r = requests.get(link, headers=headers)

    # Creating a Soup
    soup = bs(r.content, 'html.parser')

    Player_Name = []  # List that will receive all the players names

    playerTagTable = soup.find_all("table", {"class": "inline-table"})

    for table in playerTagTable:
        playerName = table.find("td", {"class": "hauptlink"})
        Player_Name.append(playerName.text.replace('\n', ''))
        del Player_Name[15:]

    nationality = []
    nationTag = soup.find_all("td", {"class": "zentriert"})

    for tag_nation in nationTag:
        nationFlag = tag_nation.find("img", {"class": "flaggenrahmen"}, {"title": True})

        if (nationFlag != None):
            nationality.append(nationFlag['title'])
    del nationality[20:]

    club = []
    clubTag = soup.find_all("td", {"class": "zentriert"})

    for tag in clubTag:
        clubBadge = tag.find("img")
        if (clubBadge != None):
            club.append(clubBadge['alt'])
    del club[0::2]
    del club[15:]

    games = []
    goals = []
    dataTag = soup.find_all("td", {"class": "zentriert"})

    for tag in dataTag:
        data = tag.find('a')
        if (data != None):
            if data.text != "":
                games.append(data.text)
                goals.append(data.text)

    del games[1::2]
    del goals[0::2]

    minsPerG = []
    dataTable = soup.find("table", {"class": "items"})

    minutesTag = dataTable.find_all("td", {"class": "rechts"})

    for tag in minutesTag:
        minsPerG.append(tag.text.replace("'", ""))

    del minsPerG[0::2]

    cellValues = []
    penaltyValues = []
    rows = dataTable.find_all("td", {"class": "zentriert"})
    for row in rows:
        cellVal = row.text.replace('\n', '')
        if (cellVal != ""):
            cellValues.append(cellVal)

    penalties = []

    penaltyValues.append(cellValues[4::7])
    for value in penaltyValues:
        for x in value:
            penalties.append(x)

    assistValues = []
    assists = []

    assistValues.append(cellValues[3::7])
    for value in assistValues:
        for x in value:
            assists.append(x)

    col_headers = ["Name", "Club", "Nationality", "Games", "Goals", "Assists", "Penalties", "Mins per Goal"]

    df = pd.DataFrame(list(zip(Player_Name, club, nationality, games, goals, assists, penalties, minsPerG)),
                      columns=col_headers)

    return df

def getTopAssists():
    link = 'https://www.transfermarkt.co.uk/premier-league/torschuetzenliste/wettbewerb/GB1/saison_id/2020/altersklasse/alle/detailpos//plus/1'

    r = requests.get(link, headers=headers)

    # Creating a Soup
    soup = bs(r.content, 'html.parser')

    Player_Name = []  # List that will receive all the players names

    playerTagTable = soup.find_all("table", {"class": "inline-table"})

    for table in playerTagTable:
        playerName = table.find("td", {"class": "hauptlink"})
        Player_Name.append(playerName.text.replace('\n', ''))
        del Player_Name[5:]

    nationality = []
    nationTag = soup.find_all("td", {"class": "zentriert"})

    for tag_nation in nationTag:
        nationFlag = tag_nation.find("img", {"class": "flaggenrahmen"}, {"title": True})

        if (nationFlag != None):
            nationality.append(nationFlag['title'])
    del nationality[20:]

    club = []
    clubTag = soup.find_all("td", {"class": "zentriert"})

    for tag in clubTag:
        clubBadge = tag.find("img")
        if (clubBadge != None):
            club.append(clubBadge['alt'])
    del club[0::2]
    del club[10:]

    games = []
    goals = []
    dataTag = soup.find_all("td", {"class": "zentriert"})

    for tag in dataTag:
        data = tag.find('a')
        if (data != None):
            if data.text != "":
                games.append(data.text)
                goals.append(data.text)

    del games[1::2]
    del goals[0::2]

    minsPerG = []
    dataTable = soup.find("table", {"class": "items"})

    minutesTag = dataTable.find_all("td", {"class": "rechts"})

    for tag in minutesTag:
        minsPerG.append(tag.text.replace("'", ""))

    del minsPerG[0::2]

    cellValues = []
    penaltyValues = []
    rows = dataTable.find_all("td", {"class": "zentriert"})
    for row in rows:
        cellVal = row.text.replace('\n', '')
        if (cellVal != ""):
            cellValues.append(cellVal)

    penalties = []

    penaltyValues.append(cellValues[4::7])
    for value in penaltyValues:
        for x in value:
            penalties.append(x)

    assistValues = []
    assists = []

    assistValues.append(cellValues[3::7])
    for value in assistValues:
        for x in value:
            assists.append(x)

    col_headers = ["Name", "Club", "Assists", "Games Played", "Nationality", "Mins per Goal", "Penalties"]

    df = pd.DataFrame(list(zip(Player_Name, club, assists, games, nationality, minsPerG, penalties)),
                      columns=col_headers)

    # Sort Not Working

    df.columns = df.columns.str.strip()
    df.sort_values(by="Assists", ascending=False)
    consolidated = [df]
    return pd.concat(consolidated)

def getAllFixtures(week):
    consolidated = []

    col_headers = ['Home Team', 'Scores', 'Away Team', 'Goal Scorers']

    r = requests.get(
        f'https://www.transfermarkt.com/premier-league/spieltag/wettbewerb/GB1/plus/?saison_id=2020&spieltag={week}',
        headers=headers)
    soup = bs(r.content, 'html.parser')

    divs = soup.find_all('div', class_='box')
    teamnames = [i.text for i in soup.select('.vereinprofil_tooltip')]
    for team in teamnames:
        if len(team) < 4:
            teamnames.remove(team)
    teamnames = teamnames[:20]

    home_teams = []
    away_teams = []
    for i in range(0, len(teamnames)):
        if i % 2:
            away_teams.append(teamnames[i])
        else:
            home_teams.append(teamnames[i])

    results = [i.text for i in soup.select('.matchresult')]

    match_scorers = []
    scorers = []
    match_isses = ['-:-', 'cancelled', 'postponed', 'TBA']

    if results[0] in match_isses and results[1] in match_isses and results[2] in match_isses:
        scorers = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    else:
        for match in divs:
            for scorer in match.select('.spielprofil_tooltip'):
                match_scorers.append(scorer.text)
            del match_scorers[0::2]
            if match_scorers == []:
                match_scorers = '-'
            else:
                seperator = ', '
                match_scorers = seperator.join(match_scorers)
            scorers.append(str(match_scorers))
            match_scorers = []
        del scorers[0:2]
        del scorers[-3:]

    df = pd.DataFrame(list(zip(home_teams, results, away_teams, scorers)),
                      columns=col_headers)
    consolidated.append(df)

    return pd.concat(consolidated)

def get_live_Standings():
    consolidated = []

    r = requests.get("https://www.soccerbase.com/tournaments/tournament.sd?comp_id=1")
    soup = bs(r.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    teamnames = [i.text for i in soup.select('.table .bull')]
    played = []
    for row in rows:
        data = row.find_all('td')

        if len(data) > 0:
            cell = data[2]
            played.append(cell.text)

    won = []
    for row in rows:
        data = row.find_all('td')

        if len(data) > 0:
            homeCell = data[3]
            awayCell = data[8]
            won.append(int(homeCell.text) + int(awayCell.text))

    drawn = []
    for row in rows:
        data = row.find_all('td')

        if len(data) > 0:
            homeCell = data[4]
            awayCell = data[9]
            drawn.append(int(homeCell.text) + int(awayCell.text))

    lost = []
    for row in rows:
        data = row.find_all('td')

        if len(data) > 0:
            homeCell = data[5]
            awayCell = data[10]
            lost.append(int(homeCell.text) + int(awayCell.text))

    goalDiff = []
    for row in rows:
        data = row.find_all('td')

        if len(data) > 0:
            cell = data[13]
            goalDiff.append(cell.text)

    points = []
    for row in rows:
        data = row.find_all('td')

        if len(data) > 0:
            cell = data[14]
            points.append(cell.text)

    headers = ['Team Name', 'Played', 'Won', 'Drawn', 'Lost', 'GD', 'Points']

    df = pd.DataFrame(list(zip(teamnames, played, won, drawn, lost, goalDiff, points)),
                      columns=headers)

    consolidated.append(df)
    return pd.concat(consolidated)
