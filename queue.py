import datetime

class Queue():
    def __init__(self) -> None:
        self.usersInQueue: list = []
        self.type = ""
        self.nextRaceTime: datetime.datetime
    
    def GrabFirstFullRace(self) -> list:
        users = []
        max = 20
        if (len(self.usersInQueue < 20)):
            max = len(self.usersInQueue)
        for i in range(0, max):
            users.append(i)
        return users

normalQueue = Queue()
normalQueue.type = "normal"

sprintQueue = Queue()
sprintQueue.type = "sprint"

semiSprintQueue = Queue()
semiSprintQueue.type = "semiSprint"

enduranceQueue = Queue()
enduranceQueue.type = "endurance"