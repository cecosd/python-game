import pygame

class Game(object):
    def __init__(self, pygameInstance, screenWidth, screenHeight):
        self.start = True
        self.displayFrequency = 30
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.pygame = pygameInstance
        self.pygame.init()
    
    def clock(self):
        clock = self.pygame.time.Clock()
        clock.tick(self.displayFrequency)

    def openGameWindow(self):
        return self.pygame.display.set_mode((self.screenWidth, self.screenHeight))

    def eventListener(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.start = False


class Figure(object):
    def __init__(self, win, x, y, width, height):
        self.x = x
        self.y = y
        self.moveVel = 10
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.jump = False
        self.jumpMax = 10
        self.events = []
        self.draw(win)

    def __getattr__(self, name):
        return self[name]


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def setEvents(self, events):
        self.events = events

    def manageAxisEvents(self):
        if self.events[pygame.K_LEFT] or self.events[pygame.K_RIGHT]:
            moveLeft = self.events[pygame.K_LEFT]
            self.move('x', moveLeft)
        if self.events[pygame.K_UP] or self.events[pygame.K_DOWN]:
            moveUp = self.events[pygame.K_UP]
            self.move('y', moveUp)

    def makeJump(self):
        self.jump = True

    def jumpEvent(self):
        if self.jump:
            if self.jumpMax >= -10:
                moveUp = True
                if not(self.jumpMax):
                    moveUp = False
                self.move('y', moveUp, self.jumpMax * 2)
                self.jumpMax -= 1
            else:
                self.jump = False
                self.jumpMax = 10

    def actionEventListener(self):
        pass
        # if self.events[pygame.K_SPACE]:
        #     if not self.jump:
        #         self.makeJump()

    def eventsDispatcher(self):
        # jump dispatcher
        self.jumpEvent()
            
    def move(self, axis, movePositive, velosity = None):
        prop = getattr(self, axis)

        if velosity is None: 
            vel = self.moveVel 
        else: 
            vel = velosity

        if movePositive:
            setattr(self, axis, prop - vel)
        else:
            setattr(self, axis, prop + vel)

game = Game(pygame, 850, 480)
win = game.openGameWindow()
fig = Figure(win, 300, 300, 20, 20)

def redrawGameWindow():
    win.fill((0,0,0))
    fig.draw(win)
    pygame.display.update()

while game.start:
    # loop delay
    game.clock()
    # listen for click events
    game.eventListener(pygame.event.get())
    # get all key events for the current loop
    fig.setEvents(pygame.key.get_pressed())
    # manage movements on x/y axis
    fig.manageAxisEvents()
    # listen for action key events
    fig.actionEventListener()
    fig.eventsDispatcher()

    redrawGameWindow()

pygame.quit()