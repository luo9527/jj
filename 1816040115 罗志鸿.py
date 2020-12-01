#我的主要功能是游戏开始，按下任意键就运行游戏
#期间按下ESC键就自动退出游戏
#游戏期间长按空格键就可以手动加速，松开空格键就恢复加速前的速度
#而且速度还会随着蛇身体的长度增加而增加。每吃一个食物
#界面右上方就会显现分数，左上方就会显现当前速度
#游戏结束时会有计分排行榜，游戏结束后会上传分数到文本，并显现在屏幕
#一旦你按下TAB键就会清空排行榜数据
# 下面这个是初级排行榜的代码
#因为这个下次运行无法保存排行榜记录，所以我又重新弄了一个可以保存记录的
'''
jj=[0,0,0]

def Ranking():
    
    global score,jj

    if score>jj[2]:
      jj[2]=score
    if score>jj[1]:
      t=jj[2]
      jj[2]=jj[1]
      jj[1]=t
    if score>jj[0]:
      t=jj[0]
      jj[0]=jj[1]
      jj[1]=t
      
    font = pygame.font.SysFont(None, 40)
    font1 = pygame.font.SysFont('simsunnsimsun', 40)
    for i in range(3):
      score_str = "{:,}".format(jj[i])
      tip = font.render('TOP%d: '%(i+1)+ score_str, True, goldColor)
      playSurface.blit(tip, (500, 50+i*40))
    
    pygame.display.update()

# 排行榜单到这结束

'''


import pygame,sys,random, time       # 首先定义四个本代码需要用到的库(游戏库，退出函数，随机库,时间库)
from pygame.locals import *     # 调用pygame库里的函数


#定义颜色变量
redColor = pygame.Color(255,0,0)    # 食物的颜色
blackColor = pygame.Color(120,70,100)   # 背景颜色
bColor = pygame.Color(0,0,0)
buleColor = pygame.Color(0,0,255)    # 蛇的颜色
greyColor = pygame.Color(150,150,150)
DARKGRAY = pygame.Color(40,40,40)
goldColor = pygame.Color(255,215,0)

# 此处开始是积分榜代码

jj=[0,0,0]
new_data=[]
data=0
try:
  with open('ranking.txt') as f:
    data=f.read()
    data=data.split()
except:
  print('yashilani')
if data != 0:
  for i in data:
    new_data.append(int(i))
    jj=new_data

def Ranking():
    global score,jj
    if score>jj[2]:
      jj[2]=score
    if score>jj[1]:
      t=jj[2]
      jj[2]=jj[1]
      jj[1]=t
    if score>jj[0]:
      t=jj[0]
      jj[0]=jj[1]
      jj[1]=t
      
    font = pygame.font.SysFont(None, 40)
    font1 = pygame.font.SysFont('simsunnsimsun', 40)
    f=open('ranking.txt','w')
    f.truncate()
    for i in range(3):
      a=str(jj[i])    
      f.write(a)
      f.write(' ')
      score_str = "{:,}".format(jj[i])
      tip = font.render('TOP%d: '%(i+1)+ score_str, True, goldColor)
      playSurface.blit(tip, (500, 50+i*50))
    
    pygame.display.update()

# 积分榜单到这结束
    
# 以下为绘制方格网所需的
Window_Width = 640

Window_Height = 480

Cell_Size = 20  

def drawGrid():     # 定义一个函数实现在游戏背景画方格，显得游戏效果更佳

    for x in range(0, Window_Width, Cell_Size):  # 画垂直线

        pygame.draw.line(playSurface, DARKGRAY, (x, 0), (x, Window_Height))

    for y in range(0, Window_Height, Cell_Size):  # 画水平线

        pygame.draw.line(playSurface, DARKGRAY, (0, y), (Window_Width, y))
        
# 绘制方格网到这结束

def draw_score(): # 绘制分数函数
    global score
    score=len(snakebody)-3
    font = pygame.font.SysFont(None, 40)
    score_str = "{:,}".format(score)
    score_image = font.render('Score: ' + score_str, True,goldColor )
    score_rect = score_image.get_rect()
    score_rect.topleft = (Window_Width - 200, 10)
    playSurface.blit(score_image, score_rect)
    pygame.display.update()

def draw_speed(): # 绘制分数函数 
    font = pygame.font.SysFont(None, 40)
    speed_str = "{:,}".format(speed)
    speed_image = font.render('Speed: ' + speed_str, True,goldColor)
    speed_rect = speed_image.get_rect()
    speed_rect.topleft = (100, 10)
    playSurface.blit(speed_image, speed_rect)
    pygame.display.update()

def drawPressKeyMsg():  #开始界面右下方的提示文字
    pressKeySurf = BASICFONT.render('Press any key to play.', True, buleColor)
    pressKeySurft= BASICFONT.render('Press space to speed_up.', True, goldColor)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRectt = pressKeySurft.get_rect()
    pressKeyRect.topleft = (Window_Width - 250, Window_Height  - 50)
    pressKeyRectt.topleft = (Window_Width - 250, Window_Height  - 30)
    playSurface.blit(pressKeySurf, pressKeyRect)
    playSurface.blit(pressKeySurft, pressKeyRectt)

def drawPressKeyMsgs():  #结束界面右下方的提示文字
    pressKeySurf = BASICFONT.render('Press any key to tryagain.', True, redColor)
    pressKeySurft= BASICFONT.render('Press esc to quit.', True, buleColor)
    pressKeySurftt= BASICFONT.render('Press tab to clear the data.', True, goldColor)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRectt = pressKeySurft.get_rect()
    pressKeyRecttt = pressKeySurft.get_rect()
    pressKeyRect.topleft = (Window_Width - 250, Window_Height  - 60)
    pressKeyRectt.topleft = (Window_Width - 250, Window_Height  - 40)
    pressKeyRecttt.topleft = (Window_Width - 250, Window_Height  - 20)
    playSurface.blit(pressKeySurf, pressKeyRect)  
    playSurface.blit(pressKeySurft, pressKeyRectt)
    playSurface.blit(pressKeySurftt, pressKeyRecttt)


def checkForKeyPress(): # 判断函数，如果按ESCAPE则退出游戏，按下TAB则清空积分榜数据
    global jj

    if len(pygame.event.get(QUIT)) > 0:

        pygame.quit()
        sys.exit()

    keyUpEvents = pygame.event.get(KEYUP)

    if len(keyUpEvents) == 0:

        return None

    if keyUpEvents[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
        
    if keyUpEvents[0].key == K_TAB:
        jj=[0,0,0]
        

    return keyUpEvents[0].key


def gameStart():#开始界面
    
    playSurface.fill(bColor)
    
    titleFont = pygame.font.Font('freesansbold.ttf', 40)
    
    titleSurf = titleFont.render('COME ON,MEN', True, redColor)
    
    titleRect = titleSurf.get_rect()
    titleRect.center = (Window_Width / 2, Window_Height  / 2)
    playSurface.blit(titleSurf, titleRect)
        
    drawPressKeyMsg()
    
    pygame.display.update()
    
    while True:
        
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def gameOver(): #结束界面

    #playSurface.fill(greyColor)
    
    titleFont = pygame.font.Font('freesansbold.ttf', 40) #默认字体类型
    
    titleSurf = titleFont.render('Game Over', True, goldColor)
    
    titleRect = titleSurf.get_rect()  
    titleRect.center = (Window_Width / 2, Window_Height  / 2)

    playSurface.blit(titleSurf, titleRect)
        
    drawPressKeyMsgs()
    
    pygame.display.update()

    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE: # 按EAC终止程序
            pygame.quit()
            sys.exit() # 终止程序
          else:
            return  main()# 结束此函数, 重新开始游戏

    return 


#定义主函数
def main():
    global playSurface,BASICFONT,speed_up,speed,snakebody,score,Window_Width
    a=0
    pygame.init()       # 初始化游戏
    fpsClock = pygame.time.Clock()      # 时钟变量
    playSurface = pygame.display.set_mode((640,480))       # 在这里我设置了一个长为640，宽为480的一个图形界面
    pygame.display.set_caption('蛇蛇大作战')     # 该处为图形标题
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18) #默认字体类型
    gameStart()
    snakeposition = [100,100]        # 初始化蛇的位置
    snakebody = [[100,100],[80,100],[60,100]]      # 定义蛇的身体长度
    targetposition =[300,300]       # 初始化食物的位置
    # 接下来我以用‘targetflag=1’作为判断食物没有被吃掉，‘targetflag=0’则被吃掉
    targetflag = 1

    direction ='right'      # 初始化蛇的行进方向（右边）
    changeDirection = direction  # 改变反向
    score = 0 #初始化分数
    speed = 10
    while True:
        
        for event in pygame.event.get():    # 从队列中获取事件
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            

            if event.type == KEYDOWN:     # 判断按下键盘事件
                if event.key == K_RIGHT:
                    changeDirection = 'right'       # 按键盘右键就判定改变蛇的方向为右
                if event.key == K_LEFT:
                    changeDirection = 'left'        # 按键盘左键就判定改变蛇的方向为左
                if event.key == K_UP:
                    changeDirection = 'up'          # 按键盘上键就判定改变蛇的方向为上
                if event.key == K_DOWN:
                    changeDirection = 'down'        # 按键盘下键就判定改变蛇的方向为下
                
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))     #按下esc则退出游戏  pygame.event.post()--放置一个新的事件到队列中,pygame.event.Event()--创建一个新的事件对象
                if event.key == K_SPACE:    # 按下空格键就判定速度加10 
                    a += 20
                
            if  event.type == KEYUP:      # 判断松开键盘事件
                if event.key == K_SPACE:    #松开键盘就实现恢复原来的速度
                    a -= 20
                
            
        # 确定方向 (根据前面的判定确定并执行改变方向)
        if changeDirection == 'right' and  direction != 'left':
            direction = changeDirection
            
        if changeDirection == 'left' and  direction != 'right':
            direction = changeDirection

        if changeDirection == 'up' and  direction != 'down':
            direction = changeDirection

        if changeDirection == 'down' and  direction != 'up':
            direction = changeDirection

        # 根据方向移动蛇头的坐标
        if direction == 'right':
            snakeposition[0] += 20

        if direction == 'left':   
            snakeposition[0] -= 20

        if direction == 'up':   
            snakeposition[1] -= 20

        if direction == 'down':   
            snakeposition[1] += 20
            
        
        
        
        snakebody.insert(0,list(snakeposition))     # 将蛇头的位置加入列表中

        if snakeposition[0] == targetposition[0] and  snakeposition[1] == targetposition[1]:
            targetflag = 0                          # 当蛇头与食物重合时，我认定蛇吃掉了食物，然后将食物数量归零

        else:
            snakebody.pop()                     # 清除蛇走过的区域
                        


        if targetflag == 0:                         # 食物归零后，在规定范围内生成新的食物
            x = random.randrange(1,32)
            y = random.randrange(1,24)
            targetposition = [int(x*20),int(y*20)]
            targetflag = 1
        playSurface.fill(blackColor)                # 填充背景颜色为黑色
        
        drawGrid()      #调用前面的绘制地图函数
        
        for position in snakebody:                  #画出蛇与食物
            pygame.draw.rect(playSurface,buleColor,Rect(position[0],position[1],20,20))
            pygame.draw.rect(playSurface,redColor,Rect(targetposition[0],targetposition[1],20,20))
        #参数Surface: 指定一个Surface编辑区，并在该区域绘制所需界面
        #参数Color: 规定颜色
        #参数Rect: 返回一个矩形（（x, y），（width,height））
        #参数width: 表示线条的粗细，width = 0,则填充为实心， width = 1，则为空心
        pygame.display.flip()       # 更新并显示到屏幕上

        if snakeposition[0] > 620 or snakeposition[0] < 0:
            Ranking()
            gameOver()

        elif snakeposition[1] > 460 or snakeposition[1] < 0:
            Ranking()
            gameOver()



        
        if len(snakebody) < 40:             # 在这我设置当蛇吃到食物后随身体的长度的增加，行进速度也增加
              speed = 2 + len(snakebody)+a // 4 
        
        draw_score()
        draw_speed()
        fpsClock.tick(speed)                # 让蛇以speed的帧率运行
        
        
if __name__== '__main__':
   main()

        
                
            
            

    













            
