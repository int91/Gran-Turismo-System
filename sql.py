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
AddSprintWin - Adds 1 to sprintStats wins
"""
def AddSprintWin(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT wins FROM sprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE sprintStats SET wins=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()
    AddSprintPodium(userName)

"""
AddSprintPodium - Adds 1 to sprintStats podiums
"""
def AddSprintPodium(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT podiums FROM sprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE sprintStats SET podiums=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddSprintPole - Adds 1 to sprintStats poles
"""
def AddSprintPole(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT poles FROM sprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE sprintStats SET poles=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddSprintTotal - Adds 1 to sprintStats total
"""
def AddSprintTotal(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT races FROM sprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE sprintStats SET races=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddNormalWin - Adds 1 to normalStats wins
"""
def AddNormalWin(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT wins FROM normalStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE normalStats SET wins=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()
    AddNormalPodium(userName)

"""
AddNormalPodium - Adds 1 to normalStats podiums
"""
def AddNormalPodium(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT podiums FROM normalStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE normalStats SET podiums=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddNormalPole - Adds 1 to normalStats poles
"""
def AddNormalPole(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT poles FROM normalStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE normalStats SET poles=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddNormalTotal - Adds 1 to normalStats total
"""
def AddNormalTotal(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT races FROM normalStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE normalStats SET races=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddEnduranceWin - Adds 1 to enduranceStats wins
"""
def AddEnduranceWin(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT wins FROM enduranceStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE enduranceStats SET wins=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()
    AddNormalPodium(userName)

"""
AddEndurancePodium - Adds 1 to enduranceStats podiums
"""
def AddEndurancePodium(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT podiums FROM enduranceStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE enduranceStats SET podiums=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddEndurancePole - Adds 1 to enduranceStats poles
"""
def AddEndurancePole(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT poles FROM enduranceStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE enduranceStats SET poles=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddEnduranceTotal - Adds 1 to enduranceStats total
"""
def AddEnduranceTotal(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT races FROM enduranceStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE enduranceStats SET races=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddSemiSprintWin - Adds 1 to semiSprintStats wins
"""
def AddSemiSprintWin(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT wins FROM semiSprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE semiSprintStats SET wins=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()
    AddNormalPodium(userName)

"""
AddSemiSprintPodium - Adds 1 to semiSprintStats podiums
"""
def AddSemiSprintPodium(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT podiums FROM semiSprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE semiSprintStats SET podiums=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddSemiSprintPole - Adds 1 to semiSprintStats poles
"""
def AddSemiSprintPole(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT poles FROM semiSprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE semiSprintStats SET poles=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()

"""
AddSemiSprintTotal - Adds 1 to semiSprintStats total
"""
def AddSemiSprintTotal(userName: str) -> bool:
    value = globals()["cur"].execute('''SELECT races FROM semiSprintStats WHERE userName=?''', (userName, )).fetchall()
    value = value[0][0]+1
    globals()["cur"].execute('''UPDATE semiSprintStats SET races=? WHERE userName=?''', (value, userName, ))
    globals()["con"].commit()



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
    globals()["cur"].execute('''CREATE TABLE races (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        type TEXT NOT NULL
        );''')
    globals()["cur"].execute('''CREATE TABLE raceResults(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        raceId INTEGER NOT NULL,
        discordId TEXT NOT NULL,
        qualify INTEGER NOT NULL,
        position INTEGER NOT NULL
        );''')
    globals()["cur"].execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        discordId TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        mmr INTEGER NOT NULL
    )''')
    globals()["cur"].execute('''CREATE TABLE sprintStats (
        userName TEXT NOT NULL UNIQUE,
        wins INTEGER NOT NULL,
        races INTEGER NOT NULL,
        podiums INTEGER NOT NULL,
        poles INTEGER NOT NULL,
        PRIMARY KEY (userName)
    )''')
    globals()["cur"].execute('''CREATE TABLE enduranceStats (
        userName TEXT NOT NULL UNIQUE,
        wins INTEGER NOT NULL,
        races INTEGER NOT NULL,
        podiums INTEGER NOT NULL,
        poles INTEGER NOT NULL,
        PRIMARY KEY (userName)
    )''')
    globals()["cur"].execute('''CREATE TABLE normalStats (
        userName TEXT NOT NULL UNIQUE,
        wins INTEGER NOT NULL,
        races INTEGER NOT NULL,
        podiums INTEGER NOT NULL,
        poles INTEGER NOT NULL,
        PRIMARY KEY (userName)
    )''')
    globals()["cur"].execute('''CREATE TABLE semiSprintStats (
        userName TEXT NOT NULL UNIQUE,
        wins INTEGER NOT NULL,
        races INTEGER NOT NULL,
        podiums INTEGER NOT NULL,
        poles INTEGER NOT NULL,
        PRIMARY KEY (userName)
    )''')