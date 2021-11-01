import pygame as pg, sys
import random
pg.init()
screen = pg.display.set_mode((800, 600))

myimg = pg.image.load("/Users/kaya/Python/images/snowman.png")
myimg = pg.transform.scale(myimg, (50, 50))
myrect = pg.Rect(400, 500, 50, 50)

bulletimg = pg.image.load("/Users/kaya/Python/images/sumire.gif")
bulletimg = pg.transform.scale(bulletimg, (16, 16))
bulletrect = pg.Rect(400, -100, 16, 16)

ufoimg = pg.image.load("/Users/kaya/Python/images/bell.png")
ufoimg = pg.transform.scale(ufoimg, (50, 50))
ufos = []
for i in range(10):
    ux = random.randint(0,800)
    uy = -100 * i
    ufos.append(pg.Rect(ux, uy, 50, 50))
starimg = pg.image.load("/Users/kaya/Python/images/star.png")
starimg = pg.transform.scale(starimg, (12, 12))
stars = []
for i in range(60):
    star = pg.Rect(random.randint(0,800), 10 * i, 30, 30)
    star.w = random.randint(5,8)
    stars.append(star)

replay_img = pg.image.load("/Users/kaya/Python/images/replaybtn.png")

pushFlag = False
page = 1
score = 0

def button_to_jump(btn, newpage):
    global page, pushFlag
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]:
        pg.mixer.Sound("/Users/kaya/Python/sounds/pi.wav").play()
        if btn.collidepoint(mx, my) and pushFlag == False:
            page = newpage
            pushFlag = True
    else:
        pushFlag = False


def gamestage():
    
    global score
    global page
    screen.fill(pg.Color("LIGHT BLUE"))
    
    (mx, my) = pg.mouse.get_pos()
    mdown = pg.mouse.get_pressed()
    
    for star in stars:
        star.y += star.w
        screen.blit(starimg, star)
        if star.y > 600:
            star.x = random.randint(0,800)
            star.y = 0
    
    myrect.x = mx - 25
    screen.blit(myimg, myrect)
    
    if mdown[0] and bulletrect.y < 0:
        bulletrect.x = myrect.x + 25 - 8
        bulletrect.y = myrect.y
        pg.mixer.Sound("/Users/kaya/Python/sounds/beam.wav").play()
    if bulletrect.y >= 0:
        bulletrect.y += -15
        screen.blit(bulletimg, bulletrect)
    for ufo in ufos:
        ufo.y += 10
        screen.blit(ufoimg, ufo)
        if ufo.y > 600:
            ufo.x = random.randint(0,800)
            ufo.y = -100
        if ufo.colliderect(myrect):
            page = 2
            pg.mixer.Sound("/Users/kaya/Python/sounds/down.wav").play()
        if ufo.colliderect(bulletrect):
            score = score + 1000
            ufo.y = -100
            ufo.x = random.randint(0,800)
            bulletrect.y = -100
            pg.mixer.Sound("/Users/kaya/Python/sounds/piko.wav").play()
    score = score + 10
    font = pg.font.Font(None, 40)
    text = font.render("SCORE : "+str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20, 20))

def gamereset():
    global score
    score = 0
    myrect.x = 400
    myrect.y = 500
    bulletrect.y = -100
    for i in range(10):
        ufos[i] = pg.Rect(random.randint(0,800), -100 * i, 50, 50)

def gameover():
    screen.fill(pg.Color("LIGHT BLUE"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("BLUE"))
    screen.blit(text, (100, 200))
    btn1 = screen.blit(replay_img,(320, 480))
    font = pg.font.Font(None, 40)
    text = font.render("SCORE : "+str(score), True, pg.Color("WHITE"))
    screen.blit(text, (20, 20))
    button_to_jump(btn1, 1)
    if page == 1:
        gamereset()


while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()
    pg.display.update()
    pg.time.Clock().tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
