from livewires import games
import random

games.init(screen_width = 1080, screen_height = 540, fps = 50)
space_image = games.load_image("space1.jpg", transparent = True)
games.screen.background = space_image

spaceship_image = games.load_image("spaceship.bmp", transparent = True)
spaceship = games.Sprite(image = spaceship_image, x = games.screen.width/2,y = games.screen.height - 30)

laser_image = games.load_image("redLaserRay.bmp", transparent = True)
laser = games.Sprite(image = laser_image, x = games.screen.width/2,y = games.screen.height - 50)


ufo_image = games.load_image("ufo.bmp", transparent = True)
ufo = games.Sprite(image = ufo_image, x = random.randint(50,games.screen.width/2 -50),y = 50)

games.screen.add(spaceship)
games.screen.add(laser)
games.screen.add(ufo)

games.screen.event_grab = True
games.mouse.is_visible = True
games.screen.mainloop()

