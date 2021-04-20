# Football-Fixtures

This program was designed by Prateek Chellani, as an adaptation of the Football-Stats Project, also created in Python serving a similar role. However, Football-Stats contains several additional features, compared to the original project, as well as Flask Compatibility. This project allows the user to load the application through the local host, and browse data scraped live from several credible websites. For a full list of differences between the projects, please see the table below

![alt text](https://imgur.com/5VljUXw.gif "Demo by Prateek Chellani")

 -----
 # Football-Fixtures vs Football-Stats

If you're planning on cloning one of these repositories, here's a brief comparision. 

|**Feature**        | **Football-Fixtures (This Project)**                         | **Football Stats**         | **Notes** |
|-------------------|--------------------------------------------------------------|----------------------------|----------------------------------------|
|All 20 PL Teams    | [X]                                                          | [X]                        |                                        |
|Flask FrontEnd     | [X]                                                          | [ ]                        |                                        |
|Console Runnable   | [ ]                                                          | [X]                        |                                        |
|Data Handling      | [X]                                                          | [X]                        |                                        |
|Record Transfers   | [X]                                                          | [ ]                        |                                        |
|Full-team Rosters  | [X]                                                          | [ ]                        |                                        |
|Live Data Retrieval| [X]                                                          | [ ]                        |  Partially included in Football Stats  |
|Enhanced UI        | [X]                                                          | [ ]                        |                                        |
|Top Scorer         | [X]                                                          | [ ]                        |                                        |
|Easy configuration | [X]                                                          | [ ]                        |                                        |
|CLI compatible     | [ ]                                                          | [X]                        |                                        |


 -----

# Supported Teams
All 20 teams registered in the English Premier League for the 2020-21 season valid inputs. In addition to this, the app contains support for live standings, fixtures and top scorers for the premier league in future seasons, and any teams that may get promoted into it. 

 -----
 
# Features

- [X] All 20 Premier League Teams.
- [X] Live Data retrieved from reliable websites
- [X] Golden Boot Race - Individual player stats for the top 15 scorers in the PL
- [X] Full team Rosters 
- [X] Transfer Records
- [X] Ability to perform multiple commands without having to restart the program. 
- [X] Contact Page
- [X] Results from all competitions, including the FA Cup, League Cup, and Continental Competitions
----


# Installation Instructions

If you are running this program for the first time, please follow steps 1-4. If you have run the program or have experience with python, skip to step 5. 

1. Clone this Repository. Can be done through CLI or via Github Desktop. 
2. Ensure that you have Python installed. (pip install python on Windows, yum -y install python on CentOS)
3. Install the required imports and packages - pandas, requests, bs4 (BeautifulSoup). (pip install pandas/requests/etc.)
   - Ensure that you install these in the correct folder (where you have installed Python, and intend to run the app from)
4. Ensure that you have a web-browser of your choice installed. 
5. Load up your script through Python. You can either browse the the directory where your main.py is located and open it in Python, or type python main.py into the terminal window in the correct folder. 
   - I strongly recommend using Python3 rather than Python2.
6. Once you run the program, browse to http://localhost:5000/ in your web browser, and use the Nav bar to navigate through a web-site as you normally would. 

 -----
# Troubleshooting 
1. **I get the error 'Failed to import Pandas/Requests/BS4**
   - Have you installed the required packages? Are the in the correct location?
   - If yes, and you still seem to be getting errors, try running the script in Python2 (This is the VEnv that packages install in by default)
2. **My python program automatically closes on opening**
   - Open it in a text editor via linux and check the error trace. 
3. **I seem to get a 404 page on the browser**
   - Wait a few minutes before refreshing. If this still doesn't work, try reseting with cleared cache - ctrl + shift + R
   - If this still doesn't work, check the error trace in stack editor. 
4. **The standings and Fixture tables show '....' instead of some scores.**
   - This is a known issue with the command line, due to the way Python formats it's output. The output should work normally on most computers, however if the screen size/console size is restricted, Python may replace data with '....' . This is why it's recommended to be used in the Web-Browser.
5. **I'm having other issues.**
   - Please reach out to me through Github, LinkedIn(https://www.linkedin.com/in/prateek-muneesh-chellani/) or the contact page on the app. 
