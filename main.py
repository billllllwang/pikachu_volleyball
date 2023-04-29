# 初始化 Pygame
import pygame
pygame.init()

# 設定視窗大小和初始參數
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 750
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
PLAYER_SPEED = 5
# 設定檢查點
check_p = 1
check_b = 1
check_n = 1
ball_y_original = 50

# 建立遊戲視窗、時間
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Two-Player Volleyball')
clock = pygame.time.Clock()

# 將圖片讀入
BACKGROUND_IMAGE = pygame.image.load("background.png")
PLAYER1_IMAGE = pygame.image.load('pikachu1.png').convert_alpha()
PLAYER2_IMAGE = pygame.image.load('pikachu.png').convert_alpha()
BALL_IMAGE = pygame.image.load('ball.png').convert_alpha()
NET_IMAGE = pygame.image.load('pillar.png').convert_alpha()

# 建立玩家涵式庫
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(50,50))
        self.rect.x = x
        self.rect.y = y

    # 角色移動涵式庫
    def move_player1(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x + PLAYER1_IMAGE.get_width() // 2 > 0:
            self.rect.x -= 8  
        if keys[pygame.K_d] and self.rect.x + PLAYER1_IMAGE.get_width() < WINDOW_WIDTH//2:
            self.rect.x += 8 
        if keys[pygame.K_w] and self.rect.y >= WINDOW_HEIGHT - self.image.get_height():
            self.speed = -28
            self.rect.y -= 28
        if self.rect.y < WINDOW_HEIGHT - self.image.get_height():
            self.speed += 0.9
            self.rect.y += self.speed
    # 角色移動涵式庫
    def move_player2(self):        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > WINDOW_WIDTH//2:
            self.rect.x -= 8 
        if keys[pygame.K_RIGHT] and self.rect.x + PLAYER2_IMAGE.get_width() // 2 < WINDOW_WIDTH:
            self.rect.x += 8
        if keys[pygame.K_UP] and self.rect.y >= WINDOW_HEIGHT - self.image.get_height():
            self.speed = -28
            self.rect.y -= 28
        if self.rect.y < WINDOW_HEIGHT - self.image.get_height():
            self.speed += 0.9
            self.rect.y += self.speed
# 設定球的涵式庫
class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = [-1, 1]

    # 刷新球的位置
    def update(self):
        self.rect.x += BALL_SPEED_X * self.direction[0]
        self.rect.y += BALL_SPEED_Y * self.direction[1]

    # 設定球上下彈的涵式庫
    def bounce_UD(self, ball_rect_x, object_x, ball_speed_x):
        ball_centerx = ball_rect_x + BALL_IMAGE.get_width() // 2
        object_centerx = object_x + PLAYER1_IMAGE.get_width() // 2
        if ball_centerx > object_centerx - PLAYER1_IMAGE.get_width() // 2 and ball_centerx < object_centerx - PLAYER1_IMAGE.get_width() // (10/3):
            ball_speed_x = - 80
        else:
            ball_speed_x = BALL_SPEED_X
        self.direction[1] = -self.direction[1]
        return(ball_speed_x)
    
    # 設定球上下彈的涵式庫
    def bounce_RL(self):
        self.direction[0] = -self.direction[0]
    
    # 設定球在邊界彈的涵式庫
    def boundary(self,check_b):
        if self.rect.x <= 0 or self.rect.x + ball.image.get_width() > WINDOW_WIDTH - 20:
            if check_b == 1:
                self.direction[0] = - self.direction[0]
                check_b = 0
        elif self.rect.y < 0:
            if check_b == 1:
                self.direction[1] = - self.direction[1]
                check_b = 0
        else:
            check_b = 1
        return(check_b)
    
    # 輸出球方向(判定用)
    def output(self):
        return(self.direction)
    
    # 判定球是往上還往下
    def direct(self, ball_y_original):
        delta_y = self.rect.y - ball_y_original
        return(delta_y)
 
# 設定球網的涵式庫
class Net(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 將所有物件套入對應涵式庫
player1 = Player(PLAYER1_IMAGE, 50, WINDOW_HEIGHT - PLAYER1_IMAGE.get_height())
player2 = Player(PLAYER2_IMAGE, WINDOW_WIDTH - 50 - PLAYER2_IMAGE.get_width(),  WINDOW_HEIGHT - PLAYER1_IMAGE.get_height())
ball = Ball(BALL_IMAGE, 50, BALL_IMAGE.get_height() // 2)
net = Net(NET_IMAGE,WINDOW_WIDTH // 2 - NET_IMAGE.get_width() // 2, 400)

# 設定初始分數
player1_score = 0
player2_score = 0

# 設定分數字體
score_font = pygame.font.SysFont(None, 50)


# 主遊戲迴圈
game_running = True
while game_running:
    # 控制活動
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    keys = pygame.key.get_pressed()
    player1.move_player1()
    player2.move_player2()
    check_b = ball.boundary(check_b)
    ball.update()

    # 球的重力加速度
    BALL_SPEED_Y += 0.5 * ball.direction[1]
    
    # 設定殺球和接球
    if pygame.sprite.collide_rect(ball, player2):
        if keys[pygame.K_LEFT] and keys[pygame.K_l]:
            BALL_SPEED_X = 30
            ball.direction[0] = -1
            BALL_SPEED_Y = 7
            ball.direction[1] = 1
            check_p = 0
        if keys[pygame.K_UP] and keys[pygame.K_l]:
            BALL_SPEED_X = 30
            ball.direction[0] = -1
            BALL_SPEED_Y = 25
            ball.direction[1] = -1
            check_p = 0
        if keys[pygame.K_DOWN] and keys[pygame.K_l]:
            BALL_SPEED_X = 20
            ball.direction[0] = -1
            BALL_SPEED_Y = 23
            ball.direction[1] = 1
            check_p = 0
        if check_p == 1:
            if ball.direct(ball_y_original) > 0 and ball.rect.y >= WINDOW_HEIGHT - PLAYER1_IMAGE.get_height():
                ball.direction[1] = -1
                BALL_SPEED_X = 7
                BALL_SPEED_Y = 30
                check_p = 0
            elif ball.direct(ball_y_original) > 0 :
                ball.direction[1] = - ball.direction[1]
                BALL_SPEED_X = 7
                check_p = 0

    elif pygame.sprite.collide_rect(ball, player1):
        if keys[pygame.K_d] and keys[pygame.K_v]:
            BALL_SPEED_X = 30
            ball.direction[0] = 1
            BALL_SPEED_Y = 7
            ball.direction[1] = 1
            check_p = 0
        if keys[pygame.K_w] and keys[pygame.K_v]:
            BALL_SPEED_X = 30
            ball.direction[0] = 1
            BALL_SPEED_Y = 23
            ball.direction[1] = -1
            check_p = 0
        if keys[pygame.K_s] and keys[pygame.K_l]:
            BALL_SPEED_X = 20
            ball.direction[0] = 1
            BALL_SPEED_Y = 11
            ball.direction[1] = 1
            check_p = 0
        if check_p == 1:
            if ball.direct(ball_y_original) > 0 and ball.rect.y >= WINDOW_HEIGHT - PLAYER1_IMAGE.get_height():
                ball.direction[1] = -1
                BALL_SPEED_X = 7
                BALL_SPEED_Y = 30
                check_p = 0
            elif ball.direct(ball_y_original) > 0 :
                ball.direction[1] = - ball.direction[1]
                BALL_SPEED_X = 7
                check_p = 0
    else :
        check_p = 1

    # 設定球與球網的碰撞
    if pygame.sprite.collide_rect(ball, net) and ball.rect.y < 300:
        if check_n == 1 :
            if ball.direct(ball_y_original) > 0:
                ball.direction[1] = -ball.direction[1]
                check_n = 0
            else:
                ball.bounce_RL
    elif pygame.sprite.collide_rect(ball, net) and ball.rect.y > 300: 
        if check_n == 1 :
            ball.bounce_RL()
            check_n = 0
            ball_high = ball.rect.y
    else :
        check_n = 1
    
    # 設定得分系統與下一局球的發球位置
    if ball.rect.y > WINDOW_HEIGHT and ball.rect.x < WINDOW_WIDTH // 2:
        player2_score += 1      
        ball.rect.x = WINDOW_WIDTH - 150 
        ball.rect.y = 50
        player1.rect.x, player1.rect.y = 50, WINDOW_HEIGHT - PLAYER1_IMAGE.get_height()
        player2.rect.x, player2.rect.y =  WINDOW_WIDTH - 50 - PLAYER2_IMAGE.get_width(), WINDOW_HEIGHT - PLAYER1_IMAGE.get_height()
        BALL_SPEED_X = 0
        BALL_SPEED_Y = 0
        game_display.blit(BACKGROUND_IMAGE, (0, 0))
        game_display.blit(net.image, net.rect)
        game_display.blit(player1.image, player1.rect)
        game_display.blit(player2.image, player2.rect)
        game_display.blit(ball.image, ball.rect)
        pygame.display.update()
        pygame.time.delay(1000)

        
    elif ball.rect.y > WINDOW_HEIGHT and ball.rect.x >= WINDOW_WIDTH // 2:
        player1_score += 1
        ball.rect.x = 70 
        ball.rect.y = 50
        player1.rect.x, player1.rect.y = 50, WINDOW_HEIGHT - PLAYER1_IMAGE.get_height()
        player2.rect.x, player2.rect.y =  WINDOW_WIDTH - 50 - PLAYER2_IMAGE.get_width(), WINDOW_HEIGHT - PLAYER1_IMAGE.get_height()
        BALL_SPEED_X = 0
        BALL_SPEED_Y = 0
        game_display.blit(BACKGROUND_IMAGE, (0, 0))
        game_display.blit(net.image, net.rect)
        game_display.blit(player1.image, player1.rect)
        game_display.blit(player2.image, player2.rect)
        game_display.blit(ball.image, ball.rect)
        pygame.display.update()
        pygame.time.delay(1000)
       

    # 將物體畫出在視窗中
    game_display.blit(BACKGROUND_IMAGE, (0, 0))
    game_display.blit(net.image, net.rect)
    game_display.blit(player1.image, player1.rect)
    game_display.blit(player2.image, player2.rect)
    game_display.blit(ball.image, ball.rect)
    score_text = score_font.render(f"{player1_score} - {player2_score}", True, (0,0,0))
    game_display.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 10))
    ball_y_original = ball.rect.y
    
    # 將畫面刷新
    pygame.display.update()

    # 將帧樹設定為60
    clock.tick(60)
