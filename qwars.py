#
# QWars
# *****
# 
# Created by Kevin Thomas 11/30/19.
# Modified by Kevin Thomas 12/03/19.
# Apache License, Version 2.0
# 
# QWars is a qgame which is a quantum pygame to which we interface
# directly with the IBMQ Research HQ at the Thomas J. Watson Research
# Center in the cloud.  QWars is a shoot-em-up game where you, 
# our hero, are flying the Q Ship which is armed with lasers
# to which various size lava rocks will be flying at you in addition 
# to a REAL IBMQ quantum computer to which is chosen when we make the
# initial network call as it selects the least busy device to 
# to start the game.  The results of our quantum circuit will produce
# values between 1 and 200 to which almost half will go into 00
# and the other half to 11.  There are 01 and 10 to account for noise.
# We use these values to seed our randomizer to make a truly exciting
# and unique experience with each new game!  Our story is as follows.
# Quantum supremacy has been achieved and an evil AI has taken control 
# as they have manufactured thousands of deep-fake copies of our 
# beloved quantum computers!  Your job as our hero is to shoot down 
# the fake imposter quantum machines and save the universe from the AI 
# singularity!
#


from qiskit import *
import pygame
import random
from os import path


def call_ibm():
    '''
    We start by first creating a circuit with 2 quantum
    registers and 2 classical registers.  We create superposition and
    entanglement and then measure.  We use 200 shots to which roughly
    50% of our values will populate 00 and the other roughly 50% of
    our values will populate 11.  There is a small number of shots 
    which will populate 01 and 10 as well.  We then call the IBM Q
    network to obtain the least busy device which we assign as a value
    to populate the attacking machine for our game play and then
    later seed the 4 values to make a truly unique gameplay experience
    with each instance.
    '''
    # Create a circuit with 1000 shots with 2 quantum regs and 2 classic regs.
    shots = 200
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    circuit = QuantumCircuit(qr, cr)

    # Create superposition.
    circuit.h(qr[0])
    # Create entanglement.
    circuit.cx(qr[0], qr[1])

    # Measure circuit.
    circuit.measure(qr, cr)

    # Load IBMQ account.
    IBMQ.load_account()

    # Look for the least busy quantum computer with the fewest number of queues.
    from qiskit.providers.ibmq import least_busy
    provider = IBMQ.get_provider(hub='ibm-q')
    IBMQ.get_provider(project='main')
    least_busy_device = provider.backends(filters=lambda x: x.configuration().n_qubits >= 5 
                                          and not x.configuration().simulator)
    backend = least_busy(least_busy_device)
    backend_name = backend.name()
    print('Calling {}, our REAL IBM Quantum Computer, please standby...'.format(backend_name))
    backend_new_name = provider.get_backend(backend_name)

    # Execute job on our quantum computer and store the results in new
    # variables, b_00, b_11, b_01, b_10 and create a try except 
    # statement to catch any 0 values.
    job = execute(circuit, shots=shots, backend=backend_new_name)
    from qiskit.tools.monitor import job_monitor
    job_monitor(job)
    result = job.result()
    counts = result.get_counts(circuit)
    try:
        b_00 = int(counts['00'])
    except:
        b_00 = 100
    try:
        b_11 = int(counts['11'])
    except:
        b_11 = 100
    try:
        b_01 = int(counts['01'])
    except:
        b_01 = 1
    try:
        b_10 = int(counts['10'])  
    except:
        b_10 = 1
    print('00 has {} counts!'. format(b_00))
    print('11 has {} counts!'. format(b_11))
    print('01 has {} counts!'. format(b_01))
    print('10 has {} counts!'. format(b_10))

    # We take the device and assign it to a variable
    # to which we will populate within our game.
    if backend_name == 'ibmq_16_melbourne':
        q_mob = 'melbourne.png'
    elif backend_name == 'ibmq_burlington':
        q_mob = 'burlington.png'
    elif backend_name == 'ibmq_essex':
        q_mob = 'essex.png'
    elif backend_name == 'ibmq_london':
        q_mob = 'london.png'
    elif backend_name == 'ibmq_ourense':
        q_mob = 'ourense.png'
    elif backend_name == 'ibmq_vigo':
        q_mob = 'vigo.png'
    elif backend_name == 'ibmqx2':
        q_mob = 'yorktown.png'
    else:
        q_mob = 'unknown.png'

    return q_mob, b_00, b_11, b_01, b_10


def draw_text(surf, text, size, x, y):
    '''
    Draw our text for our screens.
    '''
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    '''
    Instantiate new lava rocks and quantum
    computers.
    '''
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    '''
    Init our shield bar.
    '''
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    '''
    Init our player's available lives.
    '''
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    ''' 
    Create player class.  We use 'a' to move left and
    'd' to move right and 'space' to fire.
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    ''' 
    Create our lava rocks and quantum machines class.
    Here we use the values obtained from call_ibm to seed
    our randomizer functions below.
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(b_01, b_01+12)
        self.speedx = random.randrange(-b_10, b_10)
        self.rot = 0
        self.rot_speed = 0
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-b_00, -b_00+40)
            self.speedy = random.randrange(b_01, b_01+10)


class Bullet(pygame.sprite.Sprite):
    '''
    Create our bullet class.
    '''
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    ''' 
    Create our power-up class.
    '''
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    '''
    Create our explosion class.
    '''
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    ''' 
    Init welcome screen.
    '''
    screen.blit(background, background_rect)
    draw_text(screen, 'QWars', 64, WIDTH / 2, HEIGHT / 7)
    draw_text(screen, 'Use left & right arrows to move and space to fire!', 32,
              WIDTH / 2, HEIGHT * 5 / 12)
    draw_text(screen, 'Press any to begin!', 30, WIDTH / 2, HEIGHT * 6 / 12)
    draw_text(screen, 'Engineered and Developed by Kevin Thomas.', 24, WIDTH / 2, HEIGHT * 8 / 12)
    draw_text(screen, 'Artwork, music & sound effects by Kevin Thomas.', 24, WIDTH / 2, HEIGHT * 9 / 12)
    draw_text(screen, 'Apache License, Version 2.0', 24, WIDTH / 2, HEIGHT * 10 / 12)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False


if __name__ == '__main__':
    '''
    Call IBM and return the various values
    to seed our mob randomizer.
    '''
    q_mob, b_00, b_11, b_01, b_10 = call_ibm()


    '''
    Init Game.
    '''
    img_dir = path.join(path.dirname(__file__), 'img')
    snd_dir = path.join(path.dirname(__file__), 'snd')

    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    POWERUP_TIME = 2500

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("QWars")
    game_icon = pygame.image.load('img/qgame_icon.png')
    pygame.display.set_icon(game_icon)
    clock = pygame.time.Clock()
    font_name = pygame.font.match_font('verdana')


    '''
    Load game graphics.
    '''
    background = pygame.image.load(path.join(img_dir, "background.png")).convert()
    background_rect = background.get_rect()
    player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
    player_lives = pygame.image.load(path.join(img_dir, "life.png")).convert()
    player_lives_img = pygame.transform.scale(player_lives, (25, 25))
    player_lives_img.set_colorkey(BLACK)
    bullet_img = pygame.image.load(path.join(img_dir, "laser.png")).convert()
    meteor_images = []
    meteor_list = [q_mob, 'lava_1.png', 'lava_2.png',
                   'lava_3.png', 'lava_4.png']
    for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
    explosion_anim = {}
    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    explosion_anim['player'] = []
    for i in range(5):
        filename = 'explosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_anim['sm'].append(img_sm)
        filename = 'explosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        explosion_anim['player'].append(img)
    powerup_images = {}
    powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert()
    powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt.png')).convert()


    '''
    Load game sounds.
    '''
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser.ogg'))
    shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield.ogg'))
    power_sound = pygame.mixer.Sound(path.join(snd_dir, 'power.ogg'))
    expl_sounds = []
    for snd in ['explosion.ogg']:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'player_die.ogg'))
    pygame.mixer.music.load(path.join(snd_dir, 'qwars.ogg'))
    pygame.mixer.music.set_volume(1.75)
    pygame.mixer.music.play(loops=-1)


    '''
    Stage game init state.
    '''
    game_over = True
    running = True


    '''
    Init game loop.
    '''
    while running:
        if game_over:
            show_go_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(8):
                newmob()
            score = 0

        # Set FPS to function on all devices.
        clock.tick(FPS)

        # Process events.
        for event in pygame.event.get():
            # Check for quit.
            if event.type == pygame.QUIT:
                running = False

        # Update all sprites.
        all_sprites.update()

        # Check bullet hits a mob.
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob()

        # Check if a mob hits our player.
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            newmob()
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100

        # Check our player hit a powerup.
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(b_11-10, b_11)
                shield_sound.play()
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()

        # Check player dies and the explosion has finished playing.
        if player.lives == 0 and not death_explosion.alive():
            game_over = True

        # Draw and render screen.
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 40, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_lives_img)
        pygame.display.flip()

    # Terminate game UI.
    pygame.quit()