import os
import pygame
#####################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() #초기화 (반드시 필요)

#화면 크기 설정
screen_width = 640  #가로 크기
screen_height = 480 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Project Pang") #게임 이름

# FPS (frame per second)
clock = pygame.time.Clock()
##############################################################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)#############################################################
current_path = os.path.dirname(__file__)        #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")   #images 폴더 위치 반환


#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  #스테이지의 높이 위에 캐릭터를 두기 위해 사용



#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height


#캐릭터 이동 방향
character_to_x = 0


#캐릭터 이동 속도
character_speed = 5


# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]


#무기는 한 번에 여러 발 발사 가능
weapons = []

#무기 이동 속도
weapon_speed = 10

#공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path,"balloon1.png")),
    pygame.image.load(os.path.join(image_path,"balloon2.png")),
    pygame.image.load(os.path.join(image_path,"balloon3.png")),
    pygame.image.load(os.path.join(image_path,"balloon4.png"))]

#공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]  #index 0, 1, 2, 3 에 해당하는 임의의 값,공이 튕겼을때 y 값이 - , x는 속도 동일

#공들 (공들의 정보 리스트로 관리)
balls = []

#최초 발생하는 큰 공 추가 (딕셔너리로 관리)
balls.append({
    "pos_x" : 50,  # 공의 x 좌표 
    "pos_y" : 50,  # 공의 y 좌표 , (50, 50)은 화면 왼쪽 위에 위치
    "img_idx" : 0, # 공의 이미지 인덱스, 현재 처음은 가장 큰 공인 인덱스 0 (공이 나눠지면 0,1,2...)
    "to_x" : 3,  # x축 이동방향 , -3이면 왼쪽으로, 3이면 오른쪽으로 (3은 임의의 값)
    "to_y" : -6, # y축 이동방향, 맨 처음엔 살짝 올라갔다가 내려옴
    "init_spd_y" : ball_speed_y[0]}) # y 최초 속도 , 최초 발생으로 크기가 가장 큰 풍선인 인덱스 0 을 가져옴


#이벤트 루프 (창이 꺼지지 않도록 설정)
running = True #게임이 진행중인가?
while running:
    dt = clock.tick(30)  #게임화면의 초당 프레임 수 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:      #캐릭터를 왼쪽으로
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:   #캐릭터를 오른쪽으로
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:   #무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

# 캐릭터가 1초동안에 100만큼 이동을 해야할 때는
# 10 fps : 1초 동안에 10번 동작 -> 1번에 10만큼 이동 10 * 10 = 100
# 20 fps : 1초 동안 20번 동작 -> 1번에 5만큼 이동  5 * 20 = 100

    #print("fps : " + str(clock.get_fps()))


# 2. 이벤트 처리 (키보드, 마우스 등)####################################################################################################


    
# 3. 게임 캐릭터 위치 정의##################################################################
    character_x_pos += character_to_x

    #캐릭터가 화면 밖으로 나가지 않도록 설정
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width -character_width

    #무기 위치 조정
    #100, 200 -> 180, 160, 140 ...
    #500, 200 -> 180, 160, 140
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]   #무기 위치를 위로


    #천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]   #w[1]은 y좌표, w[1] > 0 천장에 닿지 않은 것 * w[1] < 0 의미는 스크린 밖으로 y좌표가 벗어남


    #공 위치 정의 (공 튀기기)
    for ball_idx, ball_val in enumerate(balls):     #enumerate는 balls 리스트에 있는 것을 가져와서 몇번째 인덱스인지, 해당 인덱스의 값을 출력 
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size   #공마다 사이즈가 다름
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을 때 공 이동 위치 변경 (가로벽에 닿았을 때 반대 쪽으로 튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:  #왼쪽 끝을 벗어나거나 오른쪽 끝을 벗어나면
            ball_val["to_x"] = ball_val["to_x"] * -1   #to_x(현재 가지고 있는 공의 값, x축 이동방향) 이동 방향을 반대쪽으로 바꿔줌

        #세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:   #스테이지에 처음 닿았을 때?
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:   #그 외의 모든 경우에는 속도를 증가 (위에 정의된 처음 속도 -18)
            ball_val["to_y"] += 0.5

        #공 위치 변경 
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

# 4. 충돌 처리 #############################################################################



# 5. 화면에 그리기##########################################################################
    screen.blit(background, (0,0))
 
    #무기가 스테이지 위에서부터 발사
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y) )
    

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))



    pygame.display.update() # 게임화면을 다시 그리기



#pygame 종료
pygame.quit()