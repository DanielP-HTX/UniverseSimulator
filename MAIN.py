import pygame as pg, random, math, time, random as r, json,csv,wikipedia,io,requests

file = open("data.csv", "w" ,newline="")
writer = csv.writer(file)

width=1920
height=1080
pg.init()
#screen = pg.display.set_mode((width, height))
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
clock = pg.time.Clock()
done = False
MaxFramerate = 120
SpeedLevelChange = False
temp = 0

addNewPlanet = False

frameCount = 0
Speed = 1
zoom = 1
screenShiftX = 0
screenShiftY = 0
moveScreen = True
data = [0,0,0,0,0,0]
trails = True
vectors = False

G = 6.67 * 10**-11 * 333054

#Time and Date
TimeScale = 0.0001
SpeedLevel = 2
day = 1
month = 1
year = 2020
pause = False

#Primary and Secondary color
pc = (0,50,100)
sc = (200,100,0)

pg.font.init()
myfont = pg.font.SysFont('Agency FB', 45)
myfont1 = pg.font.SysFont('Agency FB', 26)
myfont2 = pg.font.SysFont('Agency FB', 20)
myfont3 = pg.font.SysFont('Agency FB', 55)
myfont4 = pg.font.SysFont('Agency FB', 32)

textsurface = myfont.render(str(day) + "-" +str(month)+ "-" +str(year), False, (255, 255, 255))

def map(value,istart,istop,ostart,ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
def dist(x1,y1,x2,y2):
    return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

class Button:
    def __init__(self, Xpos, Ypos, width, height, text, color, type):
        self.Xpos = Xpos
        self.Ypos = Ypos
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.press = False
        self.type = type

    def draw(self):
        if self.type == 1:
            pg.draw.line(screen,sc,(self.Xpos-self.width/4,self.Ypos+self.height/2),(self.Xpos+self.width/4,self.Ypos-self.height/2+self.height/2),3)
            pg.draw.line(screen,sc,(self.Xpos-self.width/4,self.Ypos+self.height/2),(self.Xpos+self.width/4,self.Ypos+self.height/2+self.height/2),3)
            pg.draw.line(screen, sc, (self.Xpos - self.width / 4 + self.width/2, self.Ypos+self.height/2),(self.Xpos + self.width / 4+ self.width/2, self.Ypos - self.height / 2+self.height/2), 3)
            pg.draw.line(screen, sc, (self.Xpos - self.width / 4+ self.width/2, self.Ypos+self.height/2),(self.Xpos + self.width / 4+ self.width/2, self.Ypos + self.height / 2+self.height/2), 3)
        elif self.type == 2:
            pg.draw.line(screen, sc, (self.Xpos + self.width / 4, self.Ypos+self.height/2),(self.Xpos - self.width / 4, self.Ypos - self.height / 2+self.height/2), 3)
            pg.draw.line(screen, sc, (self.Xpos + self.width / 4, self.Ypos+self.height/2),(self.Xpos - self.width / 4, self.Ypos + self.height / 2+self.height/2), 3)
            pg.draw.line(screen, sc, (self.Xpos + self.width / 4 + self.width / 2, self.Ypos+self.height/2),(self.Xpos - self.width / 4 + self.width / 2, self.Ypos - self.height / 2+self.height/2), 3)
            pg.draw.line(screen, sc, (self.Xpos + self.width / 4 + self.width / 2, self.Ypos+self.height/2),(self.Xpos - self.width / 4 + self.width / 2, self.Ypos + self.height / 2+self.height/2), 3)
        elif self.type == 3:
            pg.draw.rect(screen,sc,pg.Rect(self.Xpos,self.Ypos,self.width,self.height),2)
            textsurface = myfont2.render(self.text, False, sc)
            screen.blit(textsurface, (self.Xpos+5, self.Ypos+2))
        elif self.type == 4:
            pg.draw.line(screen,sc,(self.Xpos,self.Ypos),(self.Xpos+self.width,self.Ypos+self.height),2)
            pg.draw.line(screen,sc,(self.Xpos,self.Ypos+self.height),(self.Xpos+self.width,self.Ypos),2)
        elif self.type == 5:
            if addNewPlanet:
                pg.draw.rect(screen, (0,255,0), pg.Rect(self.Xpos, self.Ypos, self.width, self.height), 2)
            else:
                pg.draw.rect(screen,sc,pg.Rect(self.Xpos,self.Ypos,self.width,self.height),2)
            textsurface = myfont4.render(self.text, False, sc)
            screen.blit(textsurface, (self.Xpos+5, self.Ypos+2))



    def pressed(self):
        pos = pg.mouse.get_pos()
        mouseX = pos[0]
        mouseY = pos[1]

        if (self.press and mouseX > self.Xpos and mouseX < self.Xpos + self.width and mouseY > self.Ypos and mouseY < self.Ypos + self.height):
            self.press = False
            return True
        else:
            return False

    def mouseOver(self):
        pos = pg.mouse.get_pos()
        mouseX = pos[0]
        mouseY = pos[1]

        if (mouseX > self.Xpos and mouseX < self.Xpos + self.width and mouseY > self.Ypos and mouseY < self.Ypos + self.height):
            return True
        else:
            return False

#class PlanetGUI:

buttons = []
buttons.append(  Button(1000,75,15,15,"",sc,1)  )
buttons.append(  Button(14,78,15,15,"",sc,1)  )
buttons.append(  Button(140,78,15,15,"",sc,2)  )
buttons.append(  Button(190,10,43,30,"Reset",sc,3)  )
buttons.append(  Button(190,55,43,30,"",sc,3)  )
buttons.append(  Button(385,350,20,20,"",sc,4)  )
buttons.append(  Button(345,800,43,30," Save",sc,3)  )
buttons.append(  Button(190,880,85,30,"Delete Planet",sc,3)  )
buttons.append(  Button(370,30,115,45,"Add Planet",sc,5)  )

class Slider:

    def __init__(self,x,y,w,h,min,max,start):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min = min
        self.max = max
        self.start = start
        self.sliderX = map(self.start, self.min, self.max, self.x, self.x+self.w)
        self.sliderY = y
        self.start = start

        self.value = start

    def resetSlider(self):
        self.sliderX = map(self.start, self.min, self.max, self.x, self.x+self.w)
        self.value = self.start


    def draw(self):
        pg.draw.line(screen,sc,(self.x,self.y+self.h/2),(self.x+self.w,self.y+self.h/2),2)

        self.value = map(self.sliderX,self.x,self.w+self.x,self.min,self.max)

        pg.draw.rect(screen,sc,pg.Rect(self.sliderX,self.sliderY,15,self.h))

        if self.sliderX > self.x and self.sliderX < self.x + self.w and pg.mouse.get_pressed()[0] and pg.mouse.get_pos()[0] > self.sliderX - 15 and pg.mouse.get_pos()[0] < self.sliderX + 35 and pg.mouse.get_pos()[1] > self.sliderY and  pg.mouse.get_pos()[1] < self.sliderY + self.h:
            self.sliderX = pg.mouse.get_pos()[0] - 10
        if self.sliderX <= self.x: self.sliderX = self.x +1
        elif self.sliderX >= self.x+self.w: self.sliderX = self.x+self.w -5

sliders = []
sliders.append( Slider(250,83,100,10,6.67 * 10**-11 * 333054 * 0.1,6.67 * 10**-11 * 333054* 5,  6.67 * 10**-11 * 333054)  )
sliders.append( Slider(75,820,200,15,0.1,10,1)  )
sliders.append( Slider(655,45,80,10,5,40,15)  )
#sliders.append( Slider(270,65,100,10,2,10,5)  )

COLOR_INACTIVE = (sc)
COLOR_ACTIVE = (0,255,0)
FONT = pg.font.SysFont('Agency FB', 20)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        pg.draw.rect(screen, self.color, self.rect, 2)

input_boxes = []
input_boxes.append(  InputBox(500,35,60,25,"Name")  )
input_boxes.append(  InputBox(500,67,60,25,"Mass")  )


class Checkbox:

    def __init__(self, x, y, w, h, state):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = state

    def draw(self):
        pg.draw.rect(screen, sc, pg.Rect(self.x, self.y, self.w, self.h), 2)
        if self.state == True:
            pg.draw.line(screen, sc, (self.x, self.y), (self.x + self.w, self.y + self.h),2)
            pg.draw.line(screen, sc, (self.x, self.y + self.h), (self.x + self.w, self.y),2)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            mouseX = pos[0]
            mouseY = pos[1]
            if mouseX > self.x and mouseX < self.x + self.w and mouseY > self.y and mouseY < self.y + self.h:
                self.state = not self.state

checkboxes = []
checkboxes.append(  Checkbox(250,7,15,15,True)  )
checkboxes.append(  Checkbox(250,30,15,15,False)  )

class GUI:

    def __init__(self,Buttons,Sliders,Input_Boxes,checkboxes):
        self.buttons = Buttons
        self.sliders = Sliders
        self.Input_Boxes = Input_Boxes
        self.checkboxes = checkboxes

        self.ShowUpperMenu = True
        self.ShowPlanetMenu = False
        self.MainMenu = False
    #class Slider:

    #class PopUp:

    def PlanetWindow(self,data):
        global planets
        Xpos = 30
        Ypos = 325
        r = 40
        w = 400
        h = 600
        pg.draw.rect(screen,pc,pg.Rect(Xpos+r,Ypos,w-r*2,h))
        pg.draw.rect(screen,pc,pg.Rect(Xpos,Ypos+r,w,h-r*2))
        pg.draw.ellipse(screen,pc,pg.Rect(Xpos,Ypos,r*2,r*2))
        pg.draw.ellipse(screen,pc,pg.Rect(Xpos+w-r*2,Ypos,r*2,r*2))
        pg.draw.ellipse(screen,pc,pg.Rect(Xpos,Ypos+h-r*2,r*2,r*2))
        pg.draw.ellipse(screen,pc,pg.Rect(Xpos+w-r*2,Ypos+h-r*2,r*2,r*2))
        pg.draw.line(screen,sc,(Xpos,Ypos+r),(Xpos,Ypos+h-r),2)
        pg.draw.line(screen,sc,(Xpos+w,Ypos+r),(Xpos+w,Ypos+h-r),2)
        pg.draw.line(screen, sc, (Xpos+r, Ypos), (Xpos+w-r, Ypos), 2)
        pg.draw.line(screen, sc, (Xpos + r, Ypos+h), (Xpos + w - r, Ypos+h), 2)
        pg.draw.line(screen,sc,(Xpos+r,Ypos+r*2),(Xpos+w-r,Ypos+r*2),2)
        pg.draw.line(screen,sc,(Xpos+r,Ypos+r*6),(Xpos+w-r,Ypos+r*6),2)
        pg.draw.line(screen, sc, (Xpos + r, Ypos + r * 11), (Xpos + w - r, Ypos + r * 11), 2)
        pg.draw.line(screen, sc, (Xpos + r, Ypos + r * 13), (Xpos + w - r, Ypos + r * 13), 2)

        textsurface = myfont3.render(str(data[1]), False, (255, 255, 255))
        screen.blit(textsurface, (Xpos+r, Ypos+r*0.35))
        for i in range(0,len(data[0])):
            textsurface = myfont2.render(str(data[0][i]), False, (255, 255, 255))
            screen.blit(textsurface, (Xpos + r, Ypos + r*1.5+(25*(i+1))))

        textsurface = myfont1.render("Mass: "+str( (int(data[2])/1000) )+" earths", False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 6 + 4))
        textsurface = myfont1.render("Diameter: " + str(data[3]), False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 6.8 + 4))
        textsurface = myfont1.render("Temperature: " + str(data[4]), False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 7.6 + 4))
        textsurface = myfont1.render("Orbit Time: " + str(data[5]), False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 8.4 + 4))
        textsurface = myfont1.render("Gravity: " + str(data[6])+" G", False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 9.2 + 4))
        textsurface = myfont1.render("Distance from sun: " + str(data[7]), False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 10 + 4))

        textsurface = myfont1.render("Change the object's mass", False, (255, 255, 255))
        screen.blit(textsurface, (Xpos + r, Ypos + r * 11 + 4))

        self.buttons[5].draw()
        self.buttons[6].draw()
        self.buttons[7].draw()

        self.sliders[1].draw()
        textsurface = myfont1.render("X"+str(round(self.sliders[1].value,2)), False, (255, 255, 255))
        screen.blit(textsurface, (285, Ypos + r * 12))

        if self.buttons[6].pressed() and self.ShowPlanetMenu:
            for i in range(0,len(planets)):
                if planets[i].data[1] == data[1]:
                    planets[i].mass *= self.sliders[1].value
                    self.sliders[1].resetSlider()

        if self.buttons[7].pressed() and self.ShowPlanetMenu:
            for i in range(0, len(planets)-1):
                if planets[i].data[1] == data[1]:
                    planets.pop(i)

    def draw(self,data):
        global SpeedLevel, TimeScale, day, month, year, pause, G, SpeedLevelChange, addNewPlanet, trails, vectors

        if len(self.buttons)>0:
            self.buttons[0].draw()
            if self.buttons[0].pressed() == True:
                self.ShowUpperMenu = not self.ShowUpperMenu

        if self.ShowPlanetMenu:
            self.PlanetWindow(data)

        if self.ShowUpperMenu:

            #Buttons if pressed
            if self.buttons[1].pressed() and SpeedLevel > 1:
                SpeedLevel -= 1
                SpeedLevelChange = True
            elif self.buttons[2].pressed() and SpeedLevel < 5:
                SpeedLevel += 1
                SpeedLevelChange = True
            elif self.buttons[3].pressed(): reset()
            elif self.buttons[4].pressed(): pause = not pause
            elif self.buttons[5].pressed() and self.ShowPlanetMenu: self.ShowPlanetMenu = not self.ShowPlanetMenu
            elif self.buttons[8].pressed():
                addNewPlanet = not addNewPlanet

            #Upper Menu
            pg.draw.rect(screen,pc,pg.Rect(0,0,width/2-200,100))
            pg.draw.rect(screen,sc,pg.Rect(0,0,width/2-200,100),2)
            pg.draw.line(screen,sc,(0,65),(180,65),2)
            pg.draw.line(screen,sc,(180,0),(180,100),2)
            pg.draw.line(screen,sc,(242,0),(242,100),2)
            pg.draw.line(screen,sc,(360,0),(360,100),2)
            pg.draw.line(screen,sc,(360,50),(242,50),2)
            temp = ((198,63),(198,77),(208,70))
            pg.draw.polygon(screen,sc,temp)
            pg.draw.rect(screen,sc,pg.Rect(212,63,6,14))
            pg.draw.rect(screen,sc,pg.Rect(220,63,6,14))

            #SpeedLevel
            if SpeedLevel==1: TimeScale = 0.025
            elif SpeedLevel == 2: TimeScale = 0.05
            elif SpeedLevel == 3: TimeScale = 0.075
            elif SpeedLevel == 4: TimeScale = 0.09
            elif SpeedLevel == 5: TimeScale = 0.1
            #TimeScale = 1.00232

            #Time and Date
            if frameCount % int(43*(0.01/TimeScale)) == 0 and pause == False: day += 1
            if day > 30:
                day = 1
                month += 1
            if month > 12:
                month = 1
                year += 1
            textsurface = myfont.render(str(day) + "-" + str(month) + "-" + str(year), False, (255, 255, 255))
            screen.blit(textsurface, (12, 8))
            for i in range(0,5):
                pg.draw.circle(screen,(150,150,150),(40+i*20,85),6)
            for i in range(0,SpeedLevel):
                if i < 4:
                    pg.draw.circle(screen,(0,200,0),(40+i*20,85),6)
                else:
                    pg.draw.circle(screen,(255,100,0),(40+i*20,85),6)

            #InputBoxes
            for box in input_boxes:
                box.update()
                box.draw(screen)

            #CheckBox
            for checkbox in checkboxes:
                checkbox.draw()
            textsurface = myfont2.render("Trails", False, sc)
            screen.blit(textsurface, (270, 2))
            textsurface = myfont2.render("Vectors", False, sc)
            screen.blit(textsurface, (270, 25))

            trails = checkboxes[0].state
            vectors = checkboxes[1].state

            textsurface = myfont1.render("New Planet Attributes", False, sc)
            screen.blit(textsurface, (490, 3))
            textsurface = myfont2.render("Radius:                      "+str(int(self.sliders[2].value)), False, sc)
            screen.blit(textsurface, (610, 35))

            self.buttons[0].draw()
            self.buttons[1].draw()
            self.buttons[2].draw()
            self.buttons[3].draw()
            self.buttons[4].draw()
            self.buttons[8].draw()

            self.sliders[0].draw()
            self.sliders[2].draw()

            #Slider
            textsurface = myfont2.render("Gravity", False, sc)
            screen.blit(textsurface, (277, 55))
            G = sliders[0].value

GUI = GUI(buttons,sliders, input_boxes, checkboxes)

def reset():
    global planets, G, sliders, SpeedLevel, screenShiftX, screenShiftY
    screenShiftX = 0
    screenShiftY = 0
    planets = []
    planets = loadPlanets("planets.json",planets)
    G = 6.67 * 10 ** -11 * 333054
    sliders = []
    sliders.append(Slider(250, 83, 100, 10, G * 0.1, G * 5,G))
    sliders.append(Slider(75, 820, 200, 15, 0.1, 10, 1))
    sliders.append(Slider(655, 45, 80, 10, 5, 40, 15))
    GUI.sliders = sliders
    SpeedLevel = 2

def chunks(s, n): #Split string s into chunks of n charecters
    for start in range(0, len(s), n):
        yield s[start:start+n]

class Planet:
    def __init__(self, Xpos, Ypos, Xspeed, Yspeed, mass, radius, color,others,id,wikiSearch,data):

        self.x = Xpos
        self.y = Ypos
        self.xspeed = Xspeed
        self.yspeed = Yspeed
        self.mass = mass
        self.r = radius
        self.color = color
        self.others = others
        self.id = id
        self.shiftX = 0
        self.shiftY = 0

        self.trail = []
        self.trailShift = []
        self.trailLength = 150

        self.trailUpdateRate = 60

        self.temp = zoom

        self.test1 = 0
        self.test2 = 0

        self.data = self.wiki(wikiSearch,data)

    def wiki(self,wikiSearch,data):
        summary = wikipedia.summary(wikiSearch,chars=300)
        sum = []
        for chunk in chunks(summary, 54):
            sum.append(chunk)

        name = data[0]
        mass = data[1]
        diameter = data[2]
        surfaceTemp = data[3]
        orbitTime = data[4]
        gravity = data[5]
        distance = data[6]
        return (sum,name,mass,diameter,surfaceTemp,orbitTime,gravity,distance)

    def updateTrail(self,temp):
        if trails:
            for i in range(0, len(self.trail)):
                self.trail = []

    def draw(self,x,y,Fx):
        global SpeedLevelChange, temp
        #Change size acording to zoom
        r = int(self.r * (zoom * 1))
        self.test1 = self.x + self.shiftX + x - (r/2)
        self.test2 = self.y + self.shiftY + y - (r/2)
        pg.draw.ellipse(screen, self.color,pg.Rect(self.test1,self.test2, r+1, r+1))
        textsurface = myfont2.render(self.data[1], False, sc)
        screen.blit(textsurface, (self.test1+r*1.5, self.test2-r))

        if trails:
            if frameCount % 3 == 0:
                if len(self.trail) < self.trailLength:
                    self.trail.append([int(self.test1),int(self.test2)])
                else:
                    self.trail.pop(0)

            for i in range(0,len(self.trail)):

                pg.draw.line(screen,self.color,(int(self.trail[i-1][0]+r/2), int(self.trail[i-1][1]+r/2)),(int(self.trail[i][0]+r/2),int( self.trail[i][1]+r/2)),int((i/self.trailLength)*r*0.5))

        if vectors:
            pg.draw.line(screen,self.color,(self.test1+r/2,self.test2+r/2),(self.test1+self.xspeed*8+r/2,self.test2+r/2),2)
            pg.draw.line(screen,self.color,(self.test1+r/2,self.test2+r/2),(self.test1+r/2,self.test2+self.yspeed*8+r/2),2)

    def updateVelocity(self,pause):
        if pause == False:
            for i in range(self.id + 1, len(planets)):
                dst = dist(self.x,self.y,self.others[i].x,self.others[i].y)
                angle = math.atan2(self.y-self.others[i].y,self.x-self.others[i].x)
                force = G * self.mass * self.others[i].mass / dst**2

                self.xspeed -= (force/self.mass*TimeScale) * math.cos(angle)
                self.yspeed -= (force/self.mass*TimeScale) * math.sin(angle)

                self.others[i].xspeed += (force/self.others[i].mass*TimeScale) * math.cos(angle)
                self.others[i].yspeed += (force/self.others[i].mass*TimeScale) * math.sin(angle)

    def updatePosition(self,pause):
        if pause == False:
            self.x += self.xspeed*TimeScale
            self.y += self.yspeed*TimeScale

            centerY = height/2
            centerYDif = centerY - self.y
            zoomY = centerYDif * zoom
            self.shiftY = centerYDif - zoomY

            centerX = width / 2
            centerXDif = centerX - self.x
            zoomX = centerXDif * zoom
            self.shiftX = centerXDif - zoomX

def addPlanet(planets,pos,xspeed,yspeed,others,id,mass,radius,color,wiki,data):

    planets.append( Planet(pos[0],pos[1],  xspeed, yspeed, mass, radius,color,others,id,wiki,data))

    return planets

planets = []

#https://rhodesmill.org/pyephem/

def loadPlanets(fileName,planets):
    file = open(fileName, 'r', newline='')
    data = file.read()
    file.close()
    dict = json.loads(data)

    for i in range(0, len(dict["planets"])):
        position = (dict["planets"][i]["xpos"]+width/2, dict["planets"][i]["ypos"]+height/2)
        mass = dict["planets"][i]["mass"]
        xspeed = dict["planets"][i]["xspeed"]
        yspeed = dict["planets"][i]["yspeed"]
        radius = dict["planets"][i]["radius"]
        color = (dict["planets"][i]["color"][0],dict["planets"][i]["color"][1],dict["planets"][i]["color"][2])
        wiki = dict["planets"][i]["wiki"]
        data = []
        for j in range(0,len(dict["planets"][i]["data"])):
            data.append(dict["planets"][i]["data"][j])
        #data = (dict["planets"][i]["data"][0],)

        planets = addPlanet(planets,position,xspeed,yspeed,planets,len(planets),mass,radius,color,wiki,data)

    return planets

planets = loadPlanets("planets.json",planets)

startPos = (0,0)

def ZoomCoordinates(zoom,mouseX,mouseY):
    Var = -2959.66 * zoom ** 9 + 16031.75 * zoom ** 8 - 37905.75 * zoom ** 7 + 51394.44 * zoom ** 6 - 44124.69 * zoom ** 5 + 24975.78 * zoom ** 4 - 9394.75 * zoom ** 3 + 2304.09 * zoom ** 2 - 349.4 * zoom + 28.19
    Pos = (mouseX + Var * (mouseX - width / 2), mouseY + Var * (mouseY - height / 2))
    return Pos

data = planets[0].data

class Star:

    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.shiftX = 0
        self.shiftY = 0

    def DrawUpdate(self,x,y):

        centerY = height / 2
        centerYDif = centerY - self.y
        zoomY = centerYDif * zoom
        self.shiftY = centerYDif - zoomY

        centerX = width / 2
        centerXDif = centerX - self.x
        zoomX = centerXDif * zoom
        self.shiftX = centerXDif - zoomX

        pg.draw.circle(screen,(255,255,255),(int(self.x+self.shiftX+x),int(self.y+self.shiftY+y)),int(self.r*zoom))

stars = []
for i in range(0,800):
    stars.append(Star(random.randint(-width*5,width*5),random.randint(-4*width,width*3.5),random.randint(1,2)))

while True:
    screen.fill((0, 0, 0))

    for i in range(0,len(stars)):
        stars[i].DrawUpdate(screenShiftX,screenShiftY)

    pos = pg.mouse.get_pos()
    mouseX = pos[0]
    mouseY = pos[1]

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = False
        for box in input_boxes:
            box.handle_event(event)
        for checkbox in checkboxes:
            checkbox.handle_event(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()

        if event.type == pg.MOUSEBUTTONUP:

            for i in range(0,len(GUI.buttons)):
                GUI.buttons[i].press = False

            if pg.mouse.get_pos()[1] < height-40 and event.button == 1 and addNewPlanet and mouseY > 100:
                pos = pg.mouse.get_pos()
                if GUI.Input_Boxes[1].text == "Mass":
                    GUI.Input_Boxes[1].text = "1"
                g = (G*int(GUI.Input_Boxes[1].text))/(int(GUI.sliders[2].value*1000))
                data = [str(GUI.Input_Boxes[0].text), str(int(GUI.Input_Boxes[1].text)*1000), str(int(GUI.sliders[2].value*1000)), 'Unknown', 'Unknown', str(round(g,2)), 'Unknown']
                planets = addPlanet(planets,startPos,(screenStartPos[0]-(pos[0]-screenStartPos[0])-pos[0])*0.1,(screenStartPos[1]-(pos[1]-screenStartPos[1])-pos[1])*0.1, planets,len(planets),int(GUI.Input_Boxes[1].text),int(GUI.sliders[2].value),(random.randint(100,255),random.randint(100,255),random.randint(100,255)),"Planet Nine",data)
                startPos = (0,0)
                screenStartPos = (0,0)
                addNewPlanet = not addNewPlanet

        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(0,len(GUI.buttons)):
                if GUI.buttons[i].mouseOver:
                    GUI.buttons[i].press = True

            if event.button == 4 and zoom < 1:
                zoom += 0.005
                for i in range(0,len(planets)):
                    planets[i].updateTrail(1)
                round(zoom,2)
            elif event.button == 5 and zoom > 0.1:
                for i in range(0,len(planets)):
                    planets[i].updateTrail(2)
                zoom -= 0.005
                round(zoom, 2)

            if startPos == (0,0) and pg.mouse.get_pos()[1] < height-40 and event.button == 1 and addNewPlanet and mouseY > 100:
                mouseX = pg.mouse.get_pos()[0]
                mouseY = pg.mouse.get_pos()[1]
                if zoom <= 1:
                    startPos = ZoomCoordinates(zoom, mouseX, mouseY)
                    screenStartPos = (mouseX,mouseY)

    if pg.mouse.get_pressed()[0] and pg.mouse.get_pos()[1] < height-40 and addNewPlanet and mouseY > 100:
        pos = pg.mouse.get_pos()
        endPos = (screenStartPos[0]-(pos[0]-screenStartPos[0]),screenStartPos[1]-(pos[1]-screenStartPos[1]))
        pg.draw.line(screen,(255,0,0),screenStartPos,endPos,2)

    if mouseX <= 1:
        screenShiftX += 2
        for i in range(0, len(planets)):
            planets[i].updateTrail(2)
    elif mouseX >= width-1:
        screenShiftX -= 2
        for i in range(0, len(planets)):
            planets[i].updateTrail(2)
    elif mouseY <= 1:
        screenShiftY += 2
        for i in range(0, len(planets)):
            planets[i].updateTrail(2)
    elif mouseY >= height - 1:
        screenShiftY -= 2
        for i in range(0, len(planets)):
            planets[i].updateTrail(2)

    for i in range(0,len(planets)):
        planets[i].draw(screenShiftX,screenShiftY,frameCount)
        planets[i].updateVelocity(pause)
        planets[i].updatePosition(pause)

        if (i>0 and dist(planets[i].test1-6,planets[i].test2-6,mouseX,mouseY)<40 and pg.mouse.get_pressed()[0]):
            data = planets[i].data
            GUI.ShowPlanetMenu = True
        elif (i==0 and dist(planets[i].test1,planets[i].test2,mouseX,mouseY)<40 and pg.mouse.get_pressed()[0]):
            data = planets[i].data
            GUI.ShowPlanetMenu = True

    if addNewPlanet:
        screenShiftX = 0
        screenShiftY = 0
        GUI.ShowPlanetMenu = False

    GUI.draw(data)

    frameCount += 1
    pg.display.flip()
    clock.tick(MaxFramerate)