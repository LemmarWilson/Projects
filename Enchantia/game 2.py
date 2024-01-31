import pygame
from pygame import mixer
import csv

import constants
from damage import Damage
from weapon import Weapon
from items import Item
from world import World
from screen_fade import ScreenFade
from button import Button

"""
=======================================================================================================================
                                    Handling Characters
=======================================================================================================================
"""


def handle_events(moving_left, moving_right, moving_up, moving_down):
    """
    Handle keyboard events for player movement.

    Args:
        Moving_left (bool): Current state of moving left.
        Moving_right (bool): Current state of moving right.
        Moving_up (bool): Current state of moving up.
        Moving_down (bool): Current state of moving down.

    Returns:
        Tuple[bool]: Updated states of moving_left, moving_right, moving_up, moving_down.
        :param moving_down:
        :param moving_up:
        :param moving_right:
        :param moving_left:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                moving_down = True

        # Keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                moving_down = False

    return moving_left, moving_right, moving_up, moving_down


"""
=======================================================================================================================
                                    Drawing Functions
=======================================================================================================================
"""


def draw_info(screen, player, level):
    """
    Draw Panel with player's health information.
    """

    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50), 2)

    """
    Draw player's health information.
    """

    half_heart_drawn = False

    # Define font
    font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

    # Load heart images
    heart_empty = scale_image(load_hearts("empty"), constants.ITEM_SCALE)
    heart_full = scale_image(load_hearts("full"), constants.ITEM_SCALE)
    heart_half = scale_image(load_hearts("half"), constants.ITEM_SCALE)

    # Draw player's health hearts
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif player.health % 20 > 0 and not half_heart_drawn:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
    # Level text
    draw_text(
        "LEVEL: " + str(level),
        font,
        constants.WHITE,
        constants.SCREEN_WIDTH / 2,
        15,
        screen,
    )

    # Draw player's score
    draw_text(
        f"X{player.score}",
        font,
        constants.WHITE,
        constants.SCREEN_WIDTH - 100,
        15,
        screen,
    )


def draw_text(text, font, text_color, x, y, screen):
    """
    Draw text on the screen.
    """
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


"""
=======================================================================================================================
                                    Utility Functions
=======================================================================================================================
"""


def load_character_animation_list(num_frames=4):
    """
    Load the animation list for characters.

    Args:
        num_frames (int): Number of frames per animation (default is 4).

    Returns:
        List[List[List[pygame.Surface]]]: primary animation list.
    """
    characters = [
        "elf",
        "imp",
        "skeleton",
        "goblin",
        "muddy",
        "tiny_zombie",
        "big_demon",
    ]
    animation_types = ["idle", "run"]
    master_animation_list = []

    for character in characters:
        character_animations = []
        for animation in animation_types:
            # Reset a temporary list of images for each animation type
            temp_list = []
            for i in range(num_frames):
                img_path = f"assets/images/characters/{character}/{animation}/{i}.png"
                img = pygame.image.load(img_path).convert_alpha()
                img = scale_image(img, constants.SCALE)
                temp_list.append(img)

            character_animations.append(temp_list)

        master_animation_list.append(character_animations)

    return master_animation_list


def load_hearts(heart_type):
    """
    Load the heart image.

    Returns:
        pygame.Surface: The loaded heart image.
    """
    heart = pygame.image.load(
        f"assets/images/items/heart_{heart_type}.png"
    ).convert_alpha()
    return heart


def load_weapon(weapon_name):
    """
    Load the weapon images.

    Args:
        weapon_name (str): The name of the weapon.

    Returns:
        pygame.Surface: The loaded weapon image.
    """
    img_path = f"assets/images/weapons/{weapon_name}.png"
    weapon_image = pygame.image.load(img_path).convert_alpha()
    if weapon_name == "fireball":
        return scale_image(weapon_image, constants.FIREBALL_SCALE)
    return scale_image(weapon_image, constants.WEAPON_SCALE)


def load_coin():
    """
    Load the coin animation images.
    """
    coin_images = []
    for i in range(4):
        img_path = f"assets/images/items/coin_f{i}.png"
        coin_image = pygame.image.load(img_path).convert_alpha()
        coin_images.append(scale_image(coin_image, constants.ITEM_SCALE))
    return coin_images


def load_tile_images():
    """
    Load the tile images.
    """
    tile_list = []
    for tile_type in range(constants.TILE_TYPES):
        tile = pygame.image.load(f"assets/images/tiles/{tile_type}.png").convert_alpha()
        tile_images = pygame.transform.scale(
            tile, (constants.TILE_SIZE, constants.TILE_SIZE)
        )
        tile_list.append(tile_images)
    return tile_list


def load_world(player_level=None):
    """
    Load the world map.
    """

    level = player_level
    if level is None:
        level = 1
    else:
        level = player_level + 1

    world_data = helper_create_tile_list()

    # Load level data
    with open(f"levels/level{level}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    return world_data


def load_button(button_type):
    """
    Load the button images.
    """
    img_path = f"assets/images/buttons/button_{button_type}.png"
    button_image = pygame.image.load(img_path).convert_alpha()
    return scale_image(button_image, constants.BUTTON_SCALE)


def helper_create_tile_list():
    # Create an empty tile list
    new_world_data = []
    for row in range(constants.TILE_ROWS):
        r = [-1] * constants.TILE_COLS
        new_world_data.append(r)

    return new_world_data


def reset_level(damage_group, arrow_group, item_group, fireball_group):
    # Empty groups
    damage_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    new_list = helper_create_tile_list()

    return new_list


def scale_image(image, scale):
    """
    Scale the given image by the specified scale factor.

    Args:
        image (pygame.Surface): The image to be scaled.
        Scale (float): The scale factor.

    Returns:
        pygame.Surface: The scaled image.
        :param image:
        :param scale:
    """
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))


"""
=======================================================================================================================
                                    Game Loop
=======================================================================================================================
"""


def main():
    """
    Main game loop.
    """
    # Initialize Pygame and mixer
    mixer.init()
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Enchantia")  # Title
    start_game = False
    pause_game = False
    start_intro = False
    level = 1

    # Create a clock for FPS
    clock = pygame.time.Clock()

    # Define player movement
    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False

    """
    Loading in sound effects
    
    """

    # Load sounds
    pygame.mixer.music.load("assets/audio/music.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 5000)

    # Load sounds effects
    shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
    shot_fx.set_volume(0.5)
    hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
    hit_fx.set_volume(0.5)
    coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
    coin_fx.set_volume(0.5)
    heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
    heal_fx.set_volume(0.5)

    """
    
    Load items in a list to generate in the game tiles
    """
    items_images_list = []
    # Load coin images
    coin_image = load_coin()

    # Load health potion images
    potion_image = scale_image(
        pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),
        constants.POTION_SCALE,
    )
    items_images_list.append(potion_image)
    items_images_list.append(coin_image)

    # Load weapon image
    bow_image = load_weapon("bow")
    arrow_image = load_weapon("arrow")
    fireball_image = load_weapon("fireball")
    start_image = load_button("start")
    resume_image = load_button("resume")
    restart_image = load_button("restart")
    exit_image = load_button("exit")

    # Load in tile map images
    tile_images = load_tile_images()

    # Load animations for player and mobs
    master_animation_list = load_character_animation_list()

    world = World()
    # Create the world
    world_data = load_world()
    world.process_data(
        world_data, tile_images, items_images_list, master_animation_list
    )

    # Create the player
    # 0:elf, 1:imp, 2:skeleton, 3:goblin, 4:muddy, 5: tiny_zombie, 6: big_demon
    player = world.player

    # Create the weapon
    bow = Weapon(bow_image, arrow_image)

    # Create a list of enemies
    enemy_list = world.character_list

    # Create sprite groups
    damage_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    fireball_group = pygame.sprite.Group()

    # Creating the score coin
    score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_image, True)
    item_group.add(score_coin)

    # Add item from world data
    for item in world.items_list:
        item_group.add(item)

    # Create the screen fade
    intro_fade = ScreenFade(screen, 1, constants.BLACK, 4)
    dead_fade = ScreenFade(screen, 2, constants.RED, 4)

    # Creating button
    start_button = Button(
        constants.SCREEN_WIDTH // 2 - 135,
        constants.SCREEN_HEIGHT // 2 - 150,
        start_image,
    )
    resume_button = Button(
        constants.SCREEN_WIDTH // 2 - 175,
        constants.SCREEN_HEIGHT // 2 - 150,
        resume_image,
    )
    restart_button = Button(
        constants.SCREEN_WIDTH // 2 - 5,
        constants.SCREEN_HEIGHT // 2 + 110,
        restart_image,
    )

    exit_button = Button(
        constants.SCREEN_WIDTH // 2 - 110,
        constants.SCREEN_HEIGHT // 2 + 50,
        exit_image,
    )

    level_complete = False

    # Main Game Loop
    running = True
    while running:
        # Set FPS
        clock.tick(constants.FPS)

        # Check if game has started
        if not start_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill(constants.MENU_BG)
            # Draw buttons
            # Check if mouse press start button and start the game
            if start_button.draw(screen):
                start_game = True
                start_intro = True
            # Check if mouse press exit button
            if exit_button.draw(screen):
                running = False

        else:
            # Draw the screen
            screen.fill(constants.BG)

            if player.alive:
                # Calculate Player Movement
                dx = 0
                dy = 0
                moving_left, moving_right, moving_up, moving_down = handle_events(
                    moving_left, moving_right, moving_up, moving_down
                )

                if moving_right:
                    dx = constants.SPEED
                if moving_left:
                    dx = -constants.SPEED
                if moving_up:
                    dy = -constants.SPEED
                if moving_down:
                    dy = constants.SPEED

                # Update the world based on player movement
                screen_scroll, level_complete = player.move(
                    dx, dy, world.obstacles_tiles, world.exit_tile
                )
                world.update(screen_scroll)

                # Iterate through the enemies
                for enemy in enemy_list:
                    # Run the enemy AI
                    fireball = enemy.ai(
                        player, world.obstacles_tiles, screen_scroll, fireball_image
                    )
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive:
                        # Update the enemy
                        enemy.update()

                # Update the player and weapon
                player.update()
                arrow = bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shot_fx.play()
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(
                        screen_scroll, world.obstacles_tiles, enemy_list
                    )
                    if damage:
                        damage_text = Damage(
                            damage_pos.centerx, damage_pos.y, str(damage), constants.RED
                        )
                        damage_group.add(damage_text)
                        hit_fx.play()
                damage_group.update(screen_scroll)
                fireball_group.update(screen_scroll, player)

                # Update the items
                item_group.update(screen_scroll, player, coin_fx, heal_fx)

            # Draw the world
            world.draw(screen)

            # Drawing the enemies on the screen
            for enemy in enemy_list:
                enemy.draw(screen)
                pass

            # Draw the player and weapon
            player.draw(screen)
            bow.draw(screen)
            for arrow in arrow_group:
                arrow.draw(screen)
            for fireballs in fireball_group:
                fireballs.draw(screen)
            damage_group.draw(screen)

            # Draw the items
            item_group.draw(screen)

            # Draw player's health information
            draw_info(screen, player, level)

            # Draw score coin
            score_coin.draw(screen)

            # Check if the level is complete
            if level_complete:
                start_intro = True
                level += 1
                world_data = reset_level(
                    damage_group, arrow_group, item_group, fireball_group
                )
                # Load level data
                with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)

                world = World()
                world.process_data(
                    world_data, tile_images, items_images_list, master_animation_list
                )
                temp_hp = player.health
                temp_score = player.score
                player = world.player
                player.health = temp_hp
                player.score = temp_score
                enemy_list = world.character_list
                score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_image, True)
                item_group.add(score_coin)

                # Add the items from the level data
                for item in world.items_list:
                    item_group.add(item)

            # # Show the intro
            if start_intro:
                if intro_fade.fade():
                    start_intro = False
                    # Reset fade counter
                    intro_fade.fade_counter = 0

            # Show the death screen
            if not player.alive:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                if dead_fade.fade():
                    # Restart Button
                    if restart_button.draw(screen):
                        dead_fade.fade_counter = 0
                        start_intro = True
                        world_data = reset_level(
                            damage_group, arrow_group, item_group, fireball_group
                        )
                        # Load level data
                        with open(
                            f"levels/level{level}_data.csv", newline=""
                        ) as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)

                        world = World()
                        world.process_data(
                            world_data,
                            tile_images,
                            items_images_list,
                            master_animation_list,
                        )
                        temp_score = player.score
                        player = world.player
                        player.score = temp_score
                        enemy_list = world.character_list
                        score_coin = Item(
                            constants.SCREEN_WIDTH - 115, 23, 0, coin_image, True
                        )
                        item_group.add(score_coin)

                        # Add the items from the level data
                        for item in world.items_list:
                            item_group.add(item)

        # Update the screen
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
