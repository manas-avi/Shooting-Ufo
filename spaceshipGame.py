
# space ship shooter
#player must shoot he ufos before they reach the ground

from livewires import games,color
import random

games.init(screen_width = 540, screen_height = 540, fps = 50)
score = 0


class spaceship(games.Sprite):

    image = games.load_image("spaceship.bmp", transparent = True)
    laser_wait = 25
    laser_release = 0
    level = 100;
    is_shooting = True    
    def __init__(self):
        super(spaceship, self).__init__(image = spaceship.image,
                                  x = games.screen.width/2,
                                  bottom = games.screen.height - 30,
                                            is_collideable = False)
        
        self.scores = games.Text(value = score, size = 25, color = color.white,
                                top = 5, right = games.screen.width - 10, is_collideable = False)
        games.screen.add(self.scores)
        self.laser_release = 0		
		



        

    def xpos(self):
        xposition = int(self.x)
        return xposition
        
    def update(self):
        """ By keyboard """
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x = self.x + 5
        if games.keyboard.is_pressed(games.K_LEFT) :
            self.x = self.x - 5

        if games.keyboard.is_pressed(games.K_UP) :
            self.y = self.y - 5

        if games.keyboard.is_pressed(games.K_DOWN) :
            self.y = self.y + 5                        
        
        if self.left < 0:
            self.left = 0

        if self.y < 30:
            self.y = 30

        if self.bottom > games.screen.height - 30:
            self.bottom = games.screen.height - 30            
            
        if self.right > games.screen.width:
            self.right = games.screen.width

        if self.laser_release >0:
        	self.laser_release = self.laser_release -1    

        if games.keyboard.is_pressed(games.K_KP0) and self.laser_release == 0 and self.is_shooting:

            the_laser = laser(self.x,self.y) # on pressing space
            games.screen.add(the_laser)
            self.level = self.level - 0.1
            

            self.laser_release = self.laser_wait

        games.screen.remove(self.scores)
        self.scores = games.Text(value = score, size = 25, color = color.white,
                                top = 5, right = games.screen.width - 10 , is_collideable = False)
        games.screen.add(self.scores)
	

		

        self.check_drop()

    def check_drop(self):
        """ ufo falling rate """

        if random.randrange(int(self.level))==0:
        
            new_ufo = ufo()
            games.screen.add(new_ufo)

    def blast(self):
        great_blast = explosion(self.x,self.y)
        games.screen.add(great_blast)
        self.destroy()

class laser(games.Sprite):

    image = games.load_image("laser.bmp", transparent = True)
    sound = games.load_sound("laser.wav")
    speed = 4

    def __init__(self,xpos,ypos):
        super(laser,self).__init__(image = laser.image, x = xpos,
                                   bottom = ypos -20 ,
                                   dy = -self.speed)
        laser.sound.play()

    def update(self):
        if self.y == -40:
            self.destroy()



        
    def blast(self):
        self.destroy()
        

class explosion(games.Animation):
    
    sound = games.load_sound("explosion.wav")
    images = ["explosion1.bmp",
              "explosion2.bmp",
              "explosion3.bmp",
              "explosion4.bmp",
              "explosion5.bmp",
              "explosion6.bmp",
              "explosion7.bmp",
              "explosion8.bmp",
              "explosion9.bmp"]

    def __init__(self, xpos, ypos):
        super(explosion, self).__init__(images = explosion.images,
                                        x = xpos, y = ypos,
                                        repeat_interval = 5, n_repeats = 1,
                                        is_collideable = False)
        explosion.sound.play()

class ufo(games.Sprite):
    
    image = games.load_image("ufo.bmp", transparent = True)
    speed = 1
    xspeed = 0
    ufo_delay = 0
    delay_constant = 50
    
    def __init__(self):
        super(ufo,self).__init__(image = ufo.image, x = random.randint(50, games.screen.width-50),bottom = 50 , dy = ufo.speed)

        randomBehavior = random.randrange(6)

        if randomBehavior == 0:
        	self.dx = 2 + self.xspeed

        if randomBehavior == 1:
        	self.dx = -2 - self.xspeed

        if randomBehavior == 2:
        	self.dx = 6 + self.xspeed

        if randomBehavior == 3:
        	self.dx = -6 - self.xspeed

        if randomBehavior == 4:
        	self.dx = 4  + self.xspeed

        if randomBehavior == 5:
        	self.dx = -4 - self.xspeed	

        self.ufo_delay = 25

    def update(self):
        """ Check if bottom edge has reached screen bottom. """
        
        self.xspeed = self.xspeed+0.01
        if self.bottom > games.screen.height:
            self.end_game()
            self.destroy()

        if self.ufo_delay > 0:
        	self.ufo_delay -= 1

        if self.ufo_delay == 0:
        	self.ufo_delay = self.delay_constant
        	self.dy += 0.05 	




        self.overlap()

        if self.x <0:
        	self.dx = -self.dx

        if self.x >games.screen.width:
        	self.dx =-self.dx	





    def change_score(self):
    	global score
    	score = score +10


    def blast(self):
        """ Destroy self if overlaps. """
        self.destroy()
    
    def overlap(self):
       
        for objects in self.overlapping_sprites: 
            objects.blast()
            self.change_score() 
            great_blast = explosion(self.x,self.y)
            games.screen.add(great_blast)          
            self.blast()

    def end_game(self):

        
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 3 * games.screen.fps,
                                    after_death = games.screen.quit,
                                    is_collideable = False)
        spaceship.is_shooting = False
        games.screen.add(end_message)            


def main() :
    """ let us play """

    space_image = games.load_image("space.jpg", transparent = False)
    games.screen.background = space_image

    the_ufo = ufo()
    games.screen.add(the_ufo)

    the_spaceship = spaceship()
    games.screen.add(the_spaceship)


    games.screen.event_grab = True
    games.mouse.is_visible = False
    games.screen.mainloop()

#Go Go Go
main()  
