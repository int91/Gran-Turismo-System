import discord
import nextcord.embeds

from user import User
import sql

raceTypes = {
    "sprint":{
        "wins":sql.AddSprintWin,
        "podiums":sql.AddSprintPodium,
        "poles":sql.AddSprintPole,
        "total":sql.AddSprintTotal
    },
    "endurance":{
        "wins":sql.AddEnduranceWin,
        "podiums":sql.AddEndurancePodium,
        "poles":sql.AddEndurancePole,
        "total":sql.AddEnduranceTotal
    },
    "normal":{
        "wins":sql.AddNormalWin,
        "podiums":sql.AddNormalPodium,
        "poles":sql.AddNormalPole,
        "total":sql.AddNormalTotal
    },
    "semiSprint":{
        "wins":sql.AddSemiSprintWin,
        "podiums":sql.AddSemiSprintPodium,
        "poles":sql.AddSemiSprintPole,
        "total":sql.AddSemiSprintTotal
    }
}

positions = {
    1:"wins",
    2:"podiums",
    3:"podiums"
}

mmrs = {
    1:30,
    2:25,
    3:20,
    4:10,
    5:8,
    6:5,
    7:3,
    8:1
}

async def Register(ctx, name: str) -> None:
    if (not sql.UserExists(ctx.author.id)):
        u = User(name, ctx.author.id)
        if (sql.AddUserToDatabase(u)):
            embed = nextcord.embeds.Embed(title='Registration Success', description=f"Successfully Registered [{ctx.author}] as [{name}].")
        else:
            embed = nextcord.embeds.Embed(title='Registration Failed', description=f"The name you entered may be taken, try a different one.")
    else:
        embed = nextcord.embeds.Embed(title="Registration Failed", description=f"You already have an account registered.")
    await ctx.reply(embed=embed)

async def RaceResult(ctx, raceId: str, userName: str, qualifyingPos: int, finishPos: int) -> None:
    if (sql.AddRaceResult(raceId, userName, qualifyingPos, finishPos)):
        raceType = sql.GetRaceType(raceId)
        #Checks if the user finished within a podium or won
        if (finishPos in positions.keys()):
            var = positions[finishPos]
            raceTypes[raceType][var](userName)
        #Check if the user qualified in Pole
        if (qualifyingPos == 1):
            raceTypes[raceType]["poles"](userName)
        #Checks if user earned MMR then gives the MMR to the user
        if (finishPos in mmrs.keys()):
            sql.AddMmr(userName, mmrs[finishPos])
        #Adds 1 to total for that race type stat
        raceTypes[raceType]["total"](userName)

async def GetName(ctx, discordId: str):
    if ("<" in discordId):
        discordId = discordId.removeprefix("<@")
        discordId = discordId.removesuffix(">")
    await ctx.reply(f"{sql.GetUserName(discordId)}")