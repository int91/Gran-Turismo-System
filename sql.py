import sqlite3

from user import User

globals()["con"] = None
globals()["cur"] = None

def ConnectToDB():
    globals()["con"] = sqlite3.connect('testing.db')
    globals()["cur"] = globals()["con"].cursor()

    #InitializeDatabase()

def CloseConnectionToDB():
    globals()["con"].close()

"""
GetUserName - Returns user name of that discordId
"""
def GetUserName(discordId: str) -> str:
    return globals()["cur"].execute('''SELECT name FROM users WHERE discordId=?''', (discordId, )).fetchall()[0][0]

"""
CreateRace - Adds a race to the races table with its type
"""
def CreateRace(type: str) -> None:
    if (type == "endurance" or type == "sprint" or type == "semiSprint" or type == "normal"):
        globals()["cur"].execute('''INSERT INTO races (type) VALUES (?)''', (type,))
        globals()["con"].commit()
"""
RaceResultExists - Checks to see if the race result already exists
"""
def RaceResultExists(raceId: str, discordId: str) -> bool:
    return not globals()["cur"].execute('''SELECT * FROM raceResults WHERE raceId=? AND discordId=?;''', (raceId, discordId,)).fetchall() == []

"""
AddResult - Adds a race result to the RaceResults table
"""
def AddRaceResult(raceId: str, discordId: str, qualifyingPos: int, finishPos: int) -> bool:
    #RaceExists(raceId) and 
    if (not RaceResultExists(raceId, discordId)):
        globals()["cur"].execute('''INSERT INTO raceResults (raceId, discordId, qualify, position) VALUES (?, ?, ?, ?)''', (raceId, discordId, qualifyingPos, finishPos, ))
        globals()["con"].commit()
        return True
    else:        
        return False

"""
AddMmr - Gives user mmr
"""
def AddMmr(userName: str, mmr: int) -> None:
    curMmr = globals()["cur"].execute('''SELECT mmr FROM users WHERE name=?''', (userName,)).fetchall()[0][0]
    curMmr += mmr
    globals()["cur"].execute('''UPDATE users SET mmr=? WHERE name=?''', (mmr, userName,))
    globals()["con"].commit()

"""
RaceExists - Checks to see if a race exists with the specified Id
"""
def RaceExists(id: int) -> bool:
    return not globals()["cur"].execute('''SELECT * FROM races WHERE id=?''', (id,)).fetchall() == []

"""
AddUserToDatabase - Will add the current user's account object to our database if a user with the entered name doesn't already exist.

This only checks names as we want user's name's to be unique.
"""
def AddUserToDatabase(user: User) -> bool:
    if (GetUserData(user.GetDiscordId()) == []):
        data_list = [
            user.GetDiscordId(),
            user.GetName(),
            user.GetMmr()
        ]

        stats_list = [
            user.GetName(),
            0,
            0,
            0,
            0
        ]

        globals()["cur"].execute('''INSERT INTO sprintStats (userName, wins, races, podiums, poles) VALUES (?, ?, ?, ?, ?);''', stats_list)
        globals()["con"].commit()
        globals()["cur"].execute('''INSERT INTO enduranceStats (userName, wins, races, podiums, poles) VALUES (?, ?, ?, ?, ?);''', stats_list)
        globals()["con"].commit()
        globals()["cur"].execute('''INSERT INTO normalStats (userName, wins, races, podiums, poles) VALUES (?, ?, ?, ?, ?);''', stats_list)
        globals()["con"].commit()
        globals()["cur"].execute('''INSERT INTO semiSprintStats (userName, wins, races, podiums, poles) VALUES (?, ?, ?, ?, ?);''', stats_list)
        globals()["con"].commit()
        globals()["cur"].execute('''INSERT INTO users (discordId, name, mmr) VALUES (?, ?, ?);''', data_list)
        globals()["con"].commit()
        return True
    else:
        print(f"[DATABASE] User with discord id [{user.GetDiscordId()}] already exists")
        return False

"""
DeleteUserData - Deletes data for that user using their Name
"""
def DeleteUserData(name: str) -> None:
    globals()["cur"].execute('''DELETE FROM users WHERE name=?;''', (name,))
    globals()["cur"].execute('''DELETE FROM semiSprintStats WHERE userName=?;''', (name,))
    globals()["cur"].execute('''DELETE FROM enduranceStats WHERE userName=?;''', (name,))
    globals()["cur"].execute('''DELETE FROM normalStats WHERE userName=?;''', (name,))
    globals()["cur"].execute('''DELETE FROM sprintStats WHERE userName=?;''', (name,))
    globals()["con"].commit()

"""
UserExists - Returns if a user exists via their DiscordId
"""
def UserExists(discordId: str) -> bool: 
    return not GetUserData(discordId) == []

"""
GetRaceType - Returns the type of a race by its id
"""
def GetRaceType(id: int) -> str:
    return globals()["cur"].execute('''SELECT type FROM races WHERE id=?''', (id,)).fetchall()[0][0]

"""
GetStats - Returns stats of a user's selected race series by their DiscordId
"""
def GetStats(tableType: str, discordId: str):
    return globals()["cur"].execute('''SELECT * FROM ?Stats WHERE discordId=?''', (tableType, discordId,)).fetchall()

"""
GetUserData - Returns a user's data by using their [discordId: str].

Will return an empty list [] if a user with the specified name does not exist.
"""
def GetUserData(discordId: str) -> list:
    return globals()["cur"].execute('''SELECT * FROM users WHERE discordId=?''', (discordId,)).fetchall()

"""
InitializeDatabase - Creates the SQL Database for things
"""
def InitializeDatabase() -> None:
    #Race Types Are As Follows: ROAD = 1, OVAL = 2, DIRT = 3
    #Series Is Determined By ID's
    #Official Values Are As Follows: UNOFFICIAL = 1, OFFICIAL = 2
    globals()["cur"].execute('''CREATE TABLE series (
        id INTEGER AUTO_INCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        nextRaceTime TEXT NOT NULL,
        lastRaceTime TEXT NOT NULL,
        PRIMARY KEY (id)
        )''')
    globals()["cur"].execute('''CREATE TABLE races (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        type INTEGER NOT NULL,
        split INTEGER NOT NULL,
        official INTEGER NOT NULL,
        seriesId INTEGER REFERENCES series(id) NOT NULL
        );''')
    globals()["cur"].execute('''CREATE TABLE raceResults(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        qualifyingPosition INTEGER NOT NULL,
        finishPosition INTEGER NOT NULL,
        userId INTEGER REFERENCES users(id) NOT NULL,
        raceId INTEGER REFERENCES races(id) NOT NULL
        );''')
    globals()["cur"].execute('''CREATE TABLE ratings (
        id INTEGER AUTO_INCREMENT,
        roadRating REAL NOT NULL,
        ovalRating REAL NOT NULL,
        dirtRating REAL NOT NULL,
        PRIMARY KEY (id)
        )''')
    globals()["cur"].execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        discordId TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        ratingId UBTEGER REFERENCES ratings(id)
    )''')