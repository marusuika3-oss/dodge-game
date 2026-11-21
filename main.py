
import pygame
import random

#pygameを初期化して、画面更新の速さを管理する
#pygameはimportしたあとinitで有効化する
pygame.init()

#pygame~Clockの新しいインスタンスclockを作る　後で使う
clock = pygame.time.Clock()

#800*600のゲーム画面をつくる
#画面をつくり、返されたsurfaceオブジェクト（画像を入れるための入れ物）をscreenに入れる
#screenを使うことで描写を処理
screen = pygame.display.set_mode((800, 600))

#ウィンドウに表示される文字を設定
pygame.display.set_caption("障害物よけゲーム")
#フォントを指定　関数をよんでfont に返す
font = pygame.font.SysFont(None, 64)
score_font = pygame.font.SysFont(None, 36)

#ゲームの状態
running = True
game_over = False
paused = False

#プレイヤーと障害物の初期設定
player_x = 380
#リストの中に二つの辞書 obstacle["y"]= 0 or -250
obstacles = [
    {"x": random.randint(0, 680), "y": 0},
    {"x": random.randint(0, 680), "y": -250}
]
#障害物のスピード
obstacle_speed = 12

#現在のスコアと、これまでの最高スコアの初期設定
score = 0
best_score = 0

#メインループ：ゲームが終了するまで毎フレーム実行する
while running:
    #各キーが押されているかチェックする
    keys = pygame.key.get_pressed()
    
    #ゲームオーバーでも一時停止でもなければ、ゲームを進める
    if not game_over and not paused:
        
        #左右キーを押している間、プレイヤーをうごかす
        #pygame.K_□　キー□が押されていればtrue 大体のキーはこれだけで行ける
        if keys[pygame.K_LEFT]:
            player_x -= 10
        if keys[pygame.K_RIGHT]:
            player_x += 10
            
        #プレイヤーが画面の外へ出ないようにする
        if player_x < 0:
            player_x = 0
        if player_x > 760:
            player_x = 760
        
        #障害物をしたに移動する
        for obstacle in obstacles:
            obstacle["y"] += obstacle_speed

            #画面下に出た時に、障害物を上に戻す　スコアも加算
            if obstacle["y"] > 600:
                obstacle["y"] = -240
                obstacle["x"] = random.randint(0, 680)
                score += 1
                #比べて必要な方を取る
                best_score = max(best_score, score)
                obstacle_speed = min(12 + score * 0.3, 16)
    
    #プレイヤーと消費設定の当たり判定
    #pygame.Rect関数を呼び出してplayer_rectにいれる
    player_rect = pygame.Rect(player_x, 500, 40, 40)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], 120, 240)

        #プレイヤーが障害物にあたったか調べる
        if player_rect.colliderect(obstacle_rect):
            game_over = True
    
    #キーボードやウィンドウを閉じる操作を処理する
    #pygameが受け取ったイベントをとりだしていく
    for event in pygame.event.get():
        
        #イベントの種類がウィンドウを閉じるならば
        if event.type == pygame.QUIT:
            running = False
        #イベントの種類がキーが押されるならば
        if event.type == pygame.KEYDOWN:
            
            #ゲームオーバー後にRキーをおすと、ゲームをリセット
            if event.key == pygame.K_r and game_over:
                player_x = 380
                obstacles = [
                {"x": random.randint(0, 680), "y": 0},
                {"x": random.randint(0, 680), "y": -250}
                ]
                obstacle_speed = 12
                score = 0
                game_over = False
            
            #Pキーを押すたびに一時停止と再開を切り替える
            if event.key == pygame.K_p and not game_over:
                paused = not paused

    #プレイヤー、障害物、スコアを画面に書く
    screen.fill((30, 30, 40))

    # プレイヤーを描画する
    pygame.draw.rect(screen, (50, 200, 100), (player_x, 500, 40, 40))
    for obstacle in obstacles:
        pygame.draw.rect(screen, (220, 70, 70),
            (obstacle["x"], obstacle["y"], 120, 240))

    #ゲームオーバー時のメッセージを表示する
    if game_over:
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (280, 250))
        restart_text = score_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (280, 320))
    
    #一時停止中のメッセージを表示する
    if paused and not game_over:
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (300, 250)) 
    
    #現在のスコアと最高スコアを表示する
    #f"{}"
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    best_text = score_font.render(f"Best: {best_score}", True, (255, 255, 255))
    screen.blit(best_text, (10, 40))    
    
    
    #スクリーンの内容をウィンドウに表示
    pygame.display.flip()
    
    #インスタンスclockに60を入れる　一秒間に更新を（）回行う
    #ゲームの更新速度を最大60フレームにする
    clock.tick(60)

pygame.quit()

#if a :  a = true なら適用　
#for obstacle  in ob~s
#
#
#
#
#
#
#