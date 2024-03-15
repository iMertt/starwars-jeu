import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Initialisation des dimensions de la fenêtre et du titre
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

# Définition des couleurs utilisées
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)

# Définition du cadre de la zone de jeu
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Chargement des sons pour les tirs et les impacts
SON_TIR = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
SON_IMPACT = pygame.mixer.Sound('Assets/Grenade+1.mp3')

# Définition de la police et de la taille de la police pour l'affichage du score
POLICE_SCORE = pygame.font.SysFont('comicsans', 40)
POLICE_GAGNANT = pygame.font.SysFont('comicsans', 100)

# Définition du nombre d'images par seconde, de la vitesse des déplacements et de la vitesse des balles
FPS = 60
VEL = 5
VEL_BALLE = 7
MAX_BALLES = 3
LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU = 55, 40

# Définition des événements personnalisés pour détecter les impacts sur les vaisseaux
JAUNE_TOUCHE = pygame.USEREVENT + 1
ROUGE_TOUCHE = pygame.USEREVENT + 2

# Chargement des images des vaisseaux
IMAGE_VAISSEAU_JAUNE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
VAISSEAU_JAUNE = pygame.transform.rotate(pygame.transform.scale(
    IMAGE_VAISSEAU_JAUNE, (LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU)), 90)

IMAGE_VAISSEAU_ROUGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
VAISSEAU_ROUGE = pygame.transform.rotate(pygame.transform.scale(
    IMAGE_VAISSEAU_ROUGE, (LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU)), 270)

# Chargement de l'image de fond
FOND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def dessiner_fenetre(rouge, jaune, balles_rouges, balles_jaunes, sante_rouge, sante_jaune):
    WIN.blit(FOND, (0, 0))
    pygame.draw.rect(WIN, NOIR, BORDER)

    texte_sante_rouge = POLICE_SCORE.render(
        "Santé: " + str(sante_rouge), 1, BLANC)
    texte_sante_jaune = POLICE_SCORE.render(
        "Santé: " + str(sante_jaune), 1, BLANC)
    WIN.blit(texte_sante_rouge, (WIDTH - texte_sante_rouge.get_width() - 10, 10))
    WIN.blit(texte_sante_jaune, (10, 10))

    WIN.blit(VAISSEAU_JAUNE, (jaune.x, jaune.y))
    WIN.blit(VAISSEAU_ROUGE, (rouge.x, rouge.y))

    for balle in balles_rouges:
        pygame.draw.rect(WIN, ROUGE, balle)

    for balle in balles_jaunes:
        pygame.draw.rect(WIN, JAUNE, balle)

    pygame.display.update()


def deplacement_jaune_touches(touche_appuyee, jaune):
    if touche_appuyee[pygame.K_a] and jaune.x - VEL > 0:  # GAUCHE
        jaune.x -= VEL
    if touche_appuyee[pygame.K_d] and jaune.x + VEL + jaune.width < BORDER.x:  # DROITE
        jaune.x += VEL
    if touche_appuyee[pygame.K_w] and jaune.y - VEL > 0:  # HAUT
        jaune.y -= VEL
    if touche_appuyee[pygame.K_s] and jaune.y + VEL + jaune.height < HEIGHT - 15:  # BAS
        jaune.y += VEL


def deplacement_rouge_touches(touche_appuyee, rouge):
    if touche_appuyee[pygame.K_LEFT] and rouge.x - VEL > BORDER.x + BORDER.width:  # GAUCHE
        rouge.x -= VEL
    if touche_appuyee[pygame.K_RIGHT] and rouge.x + VEL + rouge.width < WIDTH:  # DROITE
        rouge.x += VEL
    if touche_appuyee[pygame.K_UP] and rouge.y - VEL > 0:  # HAUT
        rouge.y -= VEL
    if touche_appuyee[pygame.K_DOWN] and rouge.y + VEL + rouge.height < HEIGHT - 15:  # BAS
        rouge.y += VEL


def gerer_balles(balles_jaunes, balles_rouges, jaune, rouge):
    for balle in balles_jaunes:
        balle.x += VEL_BALLE
        if rouge.colliderect(balle):
            pygame.event.post(pygame.event.Event(ROUGE_TOUCHE))
            balles_jaunes.remove(balle)
        elif balle.x > WIDTH:
            balles_jaunes.remove(balle)

    for balle in balles_rouges:
        balle.x -= VEL_BALLE
        if jaune.colliderect(balle):
            pygame.event.post(pygame.event.Event(JAUNE_TOUCHE))
            balles_rouges.remove(balle)
        elif balle.x < 0:
            balles_rouges.remove(balle)


def dessiner_gagnant(texte):
    texte_affiche = POLICE_GAGNANT.render(texte, 1, BLANC)
    WIN.blit(texte_affiche, (WIDTH/2 - texte_affiche.get_width() /
                             2, HEIGHT/2 - texte_affiche.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    rouge = pygame.Rect(700, 300, LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU)
    jaune = pygame.Rect(100, 300, LARGEUR_VAISSEAU, HAUTEUR_VAISSEAU)

    balles_rouges = []
    balles_jaunes = []

    sante_rouge = 10
    sante_jaune = 10

    horloge = pygame.time.Clock()
    en_cours = True
    while en_cours:
        horloge.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(balles_jaunes) < MAX_BALLES:
                    balle = pygame.Rect(
                        jaune.x + jaune.width, jaune.y + jaune.height//2 - 2, 10, 5)
                    balles_jaunes.append(balle)
                    #SON_TIR.play()

                if event.key == pygame.K_RCTRL and len(balles_rouges) < MAX_BALLES:
                    balle = pygame.Rect(
                        rouge.x, rouge.y + rouge.height//2 - 2, 10, 5)
                    balles_rouges.append(balle)
                    #SON_TIR.play()

            if event.type == ROUGE_TOUCHE:
                sante_rouge -= 1
                #SON_IMPACT.play()

            if event.type == JAUNE_TOUCHE:
                sante_jaune -= 1
                #SON_IMPACT.play()

        texte_gagnant = ""
        if sante_rouge <= 0:
            texte_gagnant = "Jaune gagne !"

        if sante_jaune <= 0:
            texte_gagnant = "Rouge gagne !"

        if texte_gagnant != "":
            dessiner_gagnant(texte_gagnant)
            break

        touches_appuyees = pygame.key.get_pressed()
        deplacement_jaune_touches(touches_appuyees, jaune)
        deplacement_rouge_touches(touches_appuyees, rouge)

        gerer_balles(balles_jaunes, balles_rouges, jaune, rouge)

        dessiner_fenetre(rouge, jaune, balles_rouges, balles_jaunes,
                         sante_rouge, sante_jaune)

    main()


if __name__ == "__main__":
    main()
