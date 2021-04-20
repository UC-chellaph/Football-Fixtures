import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

link = 'https://www.transfermarkt.co.uk/premier-league/torschuetzenliste/wettbewerb/GB1/saison_id/2020/altersklasse/alle/detailpos//plus/1'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

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

print(getTeamRosters("tottenham-hotspur"))
