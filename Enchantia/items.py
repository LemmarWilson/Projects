import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin=False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type  # 0:coin, 1:health potion
        self.animation_list = (
            animation_list if isinstance(animation_list, list) else [animation_list]
        )
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin

    def update(self, screen_scroll, player, coin_fx, heal_fx):
        # Does not apply to dummy_coin
        if not self.dummy_coin:
            # Reposition the item based on the screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

        # Check if the player collects item
        if self.rect.colliderect(player.rect):
            # Check if item is coin
            if self.item_type == 0:
                player.score += 1
                coin_fx.play()
            elif self.item_type == 1:
                player.health += 10
                heal_fx.play()
                # Ensure player's health is not greater than 100
                if player.health > 100:
                    player.health = 100
            self.kill()

        # Handle animation
        animation_cooldown = 150

        # Update image depending on the current frame
        self.image = self.animation_list[self.frame_index]

        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if the animation has ended
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
