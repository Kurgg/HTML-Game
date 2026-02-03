import random
import sys
import pygame


WIDTH = 960
HEIGHT = 540
BG_COLOR = (10, 10, 20)
PLAYER_COLOR = (100, 220, 255)
ENEMY_COLOR = (255, 100, 120)
TEXT_COLOR = (240, 240, 255)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 36, 36)
        self.speed = 240
        self.max_health = 100
        self.health = self.max_health

    def update(self, dt, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        length = (dx * dx + dy * dy) ** 0.5 or 1
        self.rect.x += int((dx / length) * self.speed * dt)
        self.rect.y += int((dy / length) * self.speed * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def render(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
        self._draw_health_bar(surface, self.rect.topleft, self.health, self.max_health)

    @staticmethod
    def _draw_health_bar(surface, pos, health, max_health):
        bar_width = 40
        bar_height = 6
        x, y = pos
        pygame.draw.rect(surface, (40, 40, 60), (x, y - 10, bar_width, bar_height))
        fill = int(bar_width * max(health, 0) / max_health)
        pygame.draw.rect(surface, (80, 220, 120), (x, y - 10, fill, bar_height))


class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocity = pygame.Vector2(-speed, 0)
        self.max_health = 30
        self.health = self.max_health

    def update(self, dt):
        self.rect.x += int(self.velocity.x * dt)

    def render(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)
        self._draw_health_bar(surface, self.rect.topleft, self.health, self.max_health)

    @staticmethod
    def _draw_health_bar(surface, pos, health, max_health):
        bar_width = 36
        bar_height = 5
        x, y = pos
        pygame.draw.rect(surface, (40, 40, 60), (x, y - 9, bar_width, bar_height))
        fill = int(bar_width * max(health, 0) / max_health)
        pygame.draw.rect(surface, (255, 170, 60), (x, y - 9, fill, bar_height))


def spawn_enemy():
    y = random.randint(40, HEIGHT - 40)
    speed = random.randint(90, 140)
    return Enemy(WIDTH + 40, y, speed)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Arena")
    clock = pygame.time.Clock()

    player = Player(60, HEIGHT // 2)
    enemies = []
    spawn_timer = 0.0
    running = True

    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(dt, keys)

        spawn_timer -= dt
        if spawn_timer <= 0:
            enemies.append(spawn_enemy())
            spawn_timer = 1.2

        for enemy in enemies:
            enemy.update(dt)

        for enemy in enemies[:]:
            if enemy.rect.right < 0:
                enemies.remove(enemy)

        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                player.health -= 10 * dt
                enemy.health -= 20 * dt
                if enemy.health <= 0:
                    enemies.remove(enemy)

        if player.health <= 0:
            running = False

        screen.fill(BG_COLOR)
        player.render(screen)
        for enemy in enemies:
            enemy.render(screen)

        health_text = f"Player Health: {int(max(player.health, 0))}/{player.max_health}"
        label = pygame.font.SysFont(None, 24).render(health_text, True, TEXT_COLOR)
        screen.blit(label, (20, 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
