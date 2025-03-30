import pygame  # Pygame'i teek animatsioonide ja mängude loomiseks.
import sys  # Süsteemimoodul programmi lõpetamiseks.

# Pygame'i initsialiseerimine.
pygame.init()

# Konstandid (ekraani suurus, kiirused).
WIDTH, HEIGHT = 640, 480  # Ekraani laius ja kõrgus.
FPS = 60  # Kaadrisagedus (frames per second).
BALL_SPEED_X, BALL_SPEED_Y = 5, -5  # Palli algne liikumise kiirus x- ja y-suunas.
PADDLE_SPEED = 7  # Aluse liikumise kiirus.

# Värvid (RGB formaadis).
LIGHT_BLUE = (135, 206, 250)  # Taustavärv (helesinine toon).
WHITE = (255, 255, 255)  # Teksti värv (valge).

# Ekraani seadistamine
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Loob ekraani määratud suurusega.
pygame.display.set_caption("PingPong")  # Mängu akna pealkiri.

# Palli ja aluse piltide laadimine
ball_image = pygame.image.load('ball.png')  # Laeb palli pildi failist.
ball_image = pygame.transform.scale(ball_image, (20, 20))  # Muudab palli suuruseks 20x20.

paddle_image = pygame.image.load('pad.png')  # Laeb aluse pildi failist.
paddle_image = pygame.transform.scale(paddle_image, (120, 20))  # Muudab aluse suuruseks 120x20.

# Taustamuusika
pygame.mixer.music.load('background_music.mp3')  # Laeb taustamuusika failist.
pygame.mixer.music.play(-1)  # Esitab taustamuusikat lõputult.

# Palli seadistamine.
ball_rect = ball_image.get_rect()
ball_rect.x = WIDTH // 2 - ball_rect.width // 2
ball_rect.y = HEIGHT // 2 - ball_rect.height // 2
# Asetab palli ekraani keskele.

# Aluse seadistamine.
paddle_rect = paddle_image.get_rect()
paddle_rect.x = WIDTH // 2 - paddle_rect.width // 2
paddle_rect.y = HEIGHT // 1.5
# Asetab aluse ekraani keskkohast allapoole.

# Punktide süsteem.
score = 0

# Fond teksti kuvamiseks ekraanil.
font = pygame.font.SysFont(None, 36)

# Kell kaadrisageduse kontrollimiseks.
clock = pygame.time.Clock()

# Ajastamise muutujad.
start_time = pygame.time.get_ticks()  # Mängu algusaeg millisekundites.


def display_game_over(score):
    """Kuvab mängu lõppu ja skoori."""
    screen.fill(LIGHT_BLUE)
    game_over_text = font.render(f"Mäng läbi! Teie skoor on: {score}", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Ootab kolm sekundit enne programmi lõpetamist.


# Mängu tsükkel.
while True:
    # Kasutaja sisendi käsitlemine.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            # Kui kasutaja sulgeb akna, lõpetatakse programm.

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_rect.left > 0:
        paddle_rect.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle_rect.right < WIDTH:
        paddle_rect.x += PADDLE_SPEED
    # Klaviatuuri abil aluse liigutamine vasakule ja paremale ning piiramine ekraani servadega.

    # Palli liikumise loogika.
    ball_rect.x += BALL_SPEED_X
    ball_rect.y += BALL_SPEED_Y

    # Palli kokkupõrge seintega (ülemine ja alumine serv).
    if ball_rect.top <= 0:
        BALL_SPEED_Y *= -1
        # Kui pall puudutab ülemist serva, pööratakse y-kiirus vastupidiseks.

    if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
        BALL_SPEED_X *= -1
        # Kui pall puudutab vasakut või paremat serva, pööratakse x-kiirus vastupidiseks.

    # Pall jääb alla serva (mäng lõppeb).
    if ball_rect.bottom >= HEIGHT:
        display_game_over(score)
        pygame.quit()
        sys.exit()
        # Kuvatakse mängu lõpp ja skoor ning programm lõpetatakse.

    # Palli kokkupõrge alusega.
    if paddle_rect.colliderect(ball_rect) and BALL_SPEED_Y > 0:
        BALL_SPEED_Y *= -1
        offset = (ball_rect.centerx - paddle_rect.centerx) / (paddle_rect.width / 2)

        BALL_SPEED_X += offset * abs(BALL_SPEED_X) * 0.5

        if abs(BALL_SPEED_X) < 2:
            BALL_SPEED_X += (0.5 if offset > 0 else -0.5)
        score += 1
        # Kui pall puutub alust ja liigub allapoole (y-kiirus >0), pööratakse y-kiirus vastupidiseks ning lisatakse punkt.
        # Offset muudab palli põrkumise nurka vastavalt kokkupuutepunktile.
        # Lisatud tingimus: kui x-kiirus muutub liiga väikeseks (<2), lisatakse sellele väike nihkeväärtus,
        # et vältida otse üles-alla põrkumist.

    # Kiiruse suurendamine iga 20 sekundi järel.
    current_time = pygame.time.get_ticks()
    if (current_time - start_time) >= 20000:
        BALL_SPEED_X *= 1.1 if BALL_SPEED_X > 0 else -1.1
        BALL_SPEED_Y *= 1.1 if BALL_SPEED_Y > 0 else -1.1
        start_time = current_time
        # Suurendab palli kiirust iga 20 sekundi järel ja lähtestab ajastaja.

    # Kõikide objektide joonistamine ekraanile.
    screen.fill(LIGHT_BLUE)
    screen.blit(ball_image, ball_rect)  # Joonistab palli ekraanile kasutades pilti.
    screen.blit(paddle_image, paddle_rect)  # Joonistab aluse ekraanile kasutades pilti.

    # Kuvab skoori ekraani vasakus ülanurgas.
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Ekraani uuendamine ja kaadrisageduse kontrollimine.
    pygame.display.flip()
    clock.tick(FPS)
