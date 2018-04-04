#!/usr/bin/python3
import pygame
#Can get this at https://github.com/Nearoo/pygame-text-input
import pygame_textinput



#how many pixels should an object move on each tick?
ANIM_SPEED = 1
#limit frame rate to FPS with clock.tick(FPS) in your main loop.
FPS = 60
#go fullscreen on 'f' keypress. TODO: have pygame determine fullscreen size.
FULLSCREEN_DIM = (1366,768)
#prepend log statements with 'if VERBOSE == True:' and quickly toggle it on/off for debugging.
VERBOSE = True

clock = pygame.time.Clock()
pygame.init()

def init_display(WIDTH,HEIGHT):
    global screen,background
    SIZE = WIDTH, HEIGHT
    if WIDTH <= 800:
        screen = pygame.display.set_mode(SIZE)
    if WIDTH > 800:
        screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
    background = screen.copy()
    background.fill((0, 0, 0, 0))
    screen.blit(background, (0, 0))

init_display(800,600)

#get 'close enough' to target. returns how close we are in px.
def calc_distance(c1,c2):
    test = max( (abs(c1[0] - c2[0])), (abs(c1[1] - c2[1])) )
    return(test)

class SimpleObject: #totally change me

    def __init__(self, title, image, target, position, speed=ANIM_SPEED, otherthings=None):
        self.title    = title
        self.image    = image
        self.target   = image.get_rect().move(*target)
        self.position = image.get_rect().move(*position)
        self.speed    = speed
        self.otherthings = otherthings

    #sending 'tick' here from clock.tick() can be useful to controlling movement speed, but not always needed.
    #'update' to be called each animation step. can be anything. this moves us towards target set in self.target.
    #could even have multiple methods and a conditional call in main loop, go crazy
    def update(self,tick=0):
        if calc_distance(
          (self.position.x,self.position.y),
          (self.target.x,self.target.y)   ) <= ANIM_SPEED:
                self.position.x = self.target.x
                self.position.y = self.target.y
                return True

        if self.position.y > self.target.y:
            self.position.y -= self.speed
        elif self.position.y < self.target.y:
            self.position.y += self.speed

        if self.position.x > self.target.x:
            self.position.x -= self.speed
        elif self.position.x < self.target.x:
            self.position.x += self.speed
        return False

    #second part of animation cycle. see below in main loop.
    def draw(self, screen):
        screen.blit(self.image, self.position)


#make an onscreen prompt to take text entry. returns phrase entered.
#uses pygame_textinput from
#https://raw.githubusercontent.com/Nearoo/pygame-text-input/master/pygame_textinput.py
def input(location=[10,10],prompt=None,size=30):
    color=(106, 90, 205, 0)
    if prompt is not None:
        font = pygame.font.SysFont("Arial", size)
        prompt_surface = font.render(prompt, True, color)
        prompt_location = location
        location=[prompt_surface.get_rect().width+20,location[1]]
    textinput = pygame_textinput.TextInput(
                font_family="Arial",
                font_size = size,
                text_color=color,
                antialias=True              )
    events = ""
    while textinput.update(events) == False: #returns true at Enter key
        events = pygame.event.get()
        if prompt_surface:
            screen.blit(prompt_surface,prompt_location)
        screen.blit(textinput.get_surface(),location)
        pygame.display.update()
        clock.tick(FPS)
    return(textinput.get_text())

#does all the hokey pokey required to make a word of a certain size
#and returns it as a SimpleObject, ready to be sent wherever or animated however.
animated_objects = []
def create_word_blurb(word):
    global animated_objects #keep track of all objects.
    color=(106, 90, 96, 0)
    font = pygame.font.SysFont("Arial", 30) #30 is size
    surface = font.render(word, True, color)
    print('surface '+str(surface))
    middle_of_display = ( screen.get_width()/2, screen.get_height()/2 )
    #(title, image, target, position, otherthings=None):
    wordObject = SimpleObject(
            word, surface,position=(350,350),target=(10,10)  )
    animated_objects.append(wordObject)
    return wordObject


#main. some setup, then enter draw/update/check for input endless loop.
def main():
    myword = create_word_blurb('hello world')

    #Hopefully this can help troubleshoot, and also illustrate how to access an object's attributes.
    #Getting/setting position or target is done with 'object.target.x = 300' or 'object.position.y = 10'
    if VERBOSE == True:
        for i in animated_objects:
            for k,v in zip(i.__dict__.keys(),i.__dict__.values()):
                print ("{}: {}".format(k,v) )
            print("position: {},{}".format(i.position.x,i.position.y))
            print("target: {},{}".format(i.target.x,i.target.y))
            print("-------------------------")

    myword.target.x,myword.target.y = (400,30)

#### Main update/draw/listen loop ####
    running = True
    while running:
        tick=clock.tick(FPS)  # Limit the framerate to FPS

        # DRAW GAME OBJECTS
        screen.blit(background, (0, 0))  # Fill entire screen.
        for x in animated_objects:
                x.draw(screen)
        # UPDATE GAME OBJECTS
        for x in animated_objects:
            x.update(tick)

        pygame.display.update()

        # HANDLE EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                cx,cy = pygame.mouse.get_pos()
                print("clicked {},{}".format(cx,cy))
                for i in animated_objects:
                    if i.position.collidepoint(cx,cy) == True:
                        print("Clicked: {}".format(i.title) )
            #keyboard keys
            if event.type == pygame.KEYDOWN:
                try: event.key
                except: event.key="0"
                if event.key == pygame.K_q: #Q - quit
                    print("Quitting due to 'q' press")
                    pygame.quit()
                if event.key == pygame.K_t: #N - enter text
                        new_entry = input(prompt='your prompt:')
                        print("user entered: {}".format(new_entry) )
                if event.key == pygame.K_f: #F - full screen
                    if screen.get_width() > 800:
                        init_display(800,600)
                        break
                    if screen.get_width() == 800:
                        init_display(*FULLSCREEN_DIM)



if __name__ == '__main__':
    main()
