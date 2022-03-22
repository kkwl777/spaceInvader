
import pygame
import random


class Block(pygame.sprite.Sprite):
    """ This class represents the blocks. """

    def __init__(self, png):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load(png)

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        cat = pygame.image.load('catt.png')
        cat = pygame.transform.scale(cat, (20, 20))
        self.image = cat

        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])

        self.image.fill(pygame.color.THECOLORS['black'])

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3


class Bullet2(pygame.sprite.Sprite):

    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])

        self.image.fill(pygame.color.THECOLORS['red'])

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """

        self.rect.y += 6


class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        pygame.init()
        # --- Create the window
        # Set the height and width of the screen
        self.screen_width = 1280
        self.screen_height = 640
        self.screen = pygame.display.set_mode(
            [self.screen_width, self.screen_height])

        self.num_blocks = 100
        self.running = False
        # --- Sprite lists

        # This is a list of every sprite. All blocks and the player block as well.
        self.all_sprites_list = pygame.sprite.Group()

        # List of each block in the game
        self.block_list = pygame.sprite.Group()

        # List of each bullet
        self.bullet_list = pygame.sprite.Group()
        self.bullet_list2 = pygame.sprite.Group()

        # --- Create the sprites

        for i in range(self.num_blocks):
            # This represents a block

            block = Block('pepe.png')
            block.image = pygame.transform.scale(block.image, (20, 20))
            block.rect = block.image.get_rect()

            # Set a random location for the block
            block.rect.x = random.randrange(self.screen_width)
            block.rect.y = random.randrange(
                self.screen_height / 2)  # don't go all the way down

            # Add the block to the list of objects
            self.block_list.add(block)
            self.all_sprites_list.add(block)

        # Create a red player block
        self.player = Player()
        self.all_sprites_list.add(self.player)

        self.score = 0
        # this number is fairly arbitrary - just move the player off the bottom of the screen a bit based on the height of the player
        self.player.rect.y = self.screen_height - self.player.rect.height * 2

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                bullet = Bullet()
                # Set the bullet so it is where the player is
                bullet.rect.x = self.player.rect.x
                bullet.rect.y = self.player.rect.y
                # Add the bullet to the lists
                self.all_sprites_list.add(bullet)
                self.bullet_list.add(bullet)
            for enemy in self.block_list:
                rand = random.randint(0, 100)
                if rand < 1:
                    enemyBullet = Bullet2()
                    # Set the bullet so it is where the player is
                    enemyBullet.rect.x = enemy.rect.x
                    enemyBullet.rect.y = enemy.rect.y
                    # Add the bullet to the lists
                    self.all_sprites_list.add(enemyBullet)
                    self.bullet_list2.add(enemyBullet)

    def update(self):
        # Call the update() method on all the sprites
        self.all_sprites_list.update()

        # Calculate mechanics for each bullet
        for bullet1 in self.bullet_list2:

            # For each block hit, remove the bullet and add to the score
            if pygame.sprite.collide_rect(bullet1, self.player):
                print("GAME OVER!")
                self.running = False

            # if pygame.sprite.collide_rect(bullet1, self.bullet_list[0]):
            #     print("GAME OVER!")
            #     self.running = False

        for bullet in self.bullet_list:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(
                bullet, self.block_list, True)

            # For each block hit, remove the bullet and add to the score
            for block in block_hit_list:
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)
                self.score += 1
                print(self.score)

            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < (0 - bullet.rect.height):
                self.bullet_list.remove(bullet)
                self.all_sprites_list.remove(bullet)

    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.color.THECOLORS['white'])

        # Draw all the spites
        self.all_sprites_list.draw(self.screen)

    def run(self):
        self.running = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while self.running:
            # --- Event processing
            self.poll()

            # --- Handle game logic
            self.update()

            # --- Draw a frame
            self.draw()

            # Update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit the frames per second
            clock.tick(60)


if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shuting down...")
    pygame.quit()
