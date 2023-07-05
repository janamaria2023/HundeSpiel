import sys
import pygame
import H_Katzenjagd


N_MIN_OBJEKTE = 10
F_BREITE = 500
F_HOEHE = 800

pygame.init()
fenster = pygame.display.set_mode((F_BREITE, F_HOEHE))
pygame.display.set_caption("Mein Hundespiel")


background_image = pygame.image.load('wiese4.jpg')
background_image = pygame.transform.scale(background_image, (F_BREITE, F_HOEHE))

getroffen_flop = pygame.mixer.Sound("death-sound.mp3")
getroffen_top = pygame.mixer.Sound("success-sound.mp3")
game_over = pygame.mixer.Sound("game-over.mp3")


sprites = pygame.sprite.Group()
hund = H_Katzenjagd.Hund(F_BREITE, F_HOEHE)
sprites.add(hund)
uhr = pygame.time.Clock()

t_kollision_top = -100
t_kollision_flop = -100


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()
        
    n_neue_objekte = N_MIN_OBJEKTE - len(sprites) + hund.punkte // 2
    
    for i in range(n_neue_objekte):
        sprites.add(H_Katzenjagd.Zufallsobjekt(F_BREITE, F_HOEHE))
    
    for sprite in sprites:
        
        if sprite != hund and pygame.sprite.collide_rect(hund, sprite):
            if sprite.gut:
                hund.punkte += 1
                t_kollision_top = pygame.time.get_ticks()
            else:
                hund.leben -= 1
                t_kollision_flop = pygame.time.get_ticks()
                if hund.leben <= 0:
                    fenster.fill((255, 0, 0))
                    
                    pygame.time.wait(1000)
                    H_Katzenjagd.text("GAME OVER", fenster, (F_BREITE / 2, F_HOEHE / 2), 50)
                    H_Katzenjagd.text(str(hund.punkte) + "punkte", fenster, (F_BREITE / 2, F_HOEHE / 2 + 60), 30)
                    pygame.display.flip()
                    pygame.mixer.Sound.play(game_over)
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()
            sprite.kill()
            
    if pygame.time.get_ticks() - t_kollision_flop < 50:
        fenster.fill((255, 0, 0))
        pygame.mixer.Sound.play(getroffen_flop)

    elif pygame.time.get_ticks() -t_kollision_top < 50:
        fenster.fill((0,255, 0))
        pygame.mixer.Sound.play(getroffen_top)

    else:
        fenster.blit( background_image, ( 0,0 ) )
            
    sprites.update()
    sprites.draw(fenster)
    
    H_Katzenjagd.text("punkte: " + str(hund.punkte), fenster, (F_BREITE - 100, F_HOEHE -50), 30)
    H_Katzenjagd.text("leben: " + str(hund.leben), fenster, (80, F_HOEHE - 50), 30)

    pygame.display.flip()
    uhr.tick(40)
