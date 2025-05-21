#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as tm

#создай окно игры
window = display.set_mode((700, 500))#set_mode функция которая создаёт экран рамезорм 700 на 500 (придаём картежем)
#задай фон сцены
display.set_caption('Шутер')#придаем название окну
background = transform.scale(image.load('fon.jpeg'), (700, 500))#растягиваем и загружаем задний фон (картинку) и ставим ее под размеры окна (700, 500)

clock = time.Clock()#создали игровой таймер
FPS = 60#переменная FPS равна 60

#модуль mixer который позволяет работать с музыкой
mixer.init()#подключение возможности использовать mixer
mixer.music.load('space.ogg')#считали музыку
mixer.music.play()#начать проигрывать музыку
mixer.music.set_volume(0.1)#music.set_wolume(0.5) делает звук в половину тише
gold = mixer.Sound('fire.ogg')#создает экземпляр класса .Sound

class GameSprite(sprite.Sprite):#sprite.Sprite - из библиотеки pygame из модуля sprite ставим класс родитель Sprite
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (w, h))#создаем спрайт и растягиваем его на 65 и 65
        self.speed = player_speed
        self.rect = self.image.get_rect()#все спрайты будут прямоугольные
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):#метод reset нужен для того чтобы спрайт появился на экране
        window.blit(self.image, (self.rect.x, self.rect.y))#на окно window методом blit накладываем картинку self.image и она будет находиться в координатах self.rect.x, self.rect.y

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()#если какая-тот клавиша нажата то в key_pressed лежит True
        #управление первым спрайтом (то  что снизу)
        if key_pressed[K_RIGHT] and self.rect.x < 645:#если нажата стрелочка в право и координаты по иксу меньше 645
            self.rect.x += self.speed#перемещаем его по иксу на столько сколько равна скорость игрока
        if key_pressed[K_LEFT] and self.rect.x > 0:#если нажата стрелочка в лево и координаты по иксу больше 0
            self.rect.x -= self.speed#перемещаем его по иксу на столько сколько равна скорость игрока
        #управление первым спрайтом (то что сверху)
    
    def fire(self):
        bullet = Bullet('kluch.png', self.rect.centerx, self.rect.top, -15, 30, 80)#self.rect.centerx - центральная часть игрока по Х. self.rect.top - верхняя часть игрока (вместе: пули спавняться в центре, сверху игрока)
        bullets.add(bullet)#добавляем в группу спрайта

objects = 0#перменная objects равна 0
died = 0#переменная died равна 0

class Enemy(GameSprite):
    def update(self):
        global objects
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(0, 615)
            self.rect.y = -50
            objects += 1

class Water(GameSprite):
    def update(self):
        global objects
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(0, 615)
            self.rect.y = -50

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()#kill - метод для убивание пулек когда они уходят за экран

monsters = sprite.Group()#создаём группу спрайтов
bullets = sprite.Group()#создаём группу спрайтов
interfere = sprite.Group()#создаём группу спрайтов

for i in range(5):
    enemy = Enemy('rabochiy.png', randint(0, 615), -50, randint(1, 3), 65, 65)
    monsters.add(enemy)#добавляем в группу спрайта

for i in range(3):
    enemy2 = Water('Water.png', randint(0, 615), -50, 3, 35, 65)
    interfere.add(enemy2)#добавляем в группу спрайта

you = Player('machinarium.png', 350, 400, 5, 50, 90)



game = True#переменная game равна true
finish = False#переменная finish равна False если она будет равна True то игрок победил

font.init()#подключение возможности использовать объекты Font
font1 = font.SysFont('Arial', 70)#Установить шрифт / Создание объекта Font с параметрами: шрифт - по умолчанию (None самый первый который стоит в системе компьютера) кегль(размер шрифта) - 70
font2 = font.SysFont('Arial', 30)#Установить шрифт / Создание объекта Font с параметрами: шрифт - по умолчанию (None самый первый который стоит в системе компьютера) кегль(размер шрифта) - 30
win = font1.render('YOU WIN', True, (255, 215, 0))#создать видимую надпись "YOU WIN" желтого цвета (True/False - сглаживать пиксели текста или нет)
lose = font1.render('YOU LOSE', True, (255, 0, 0))#render/рендерить - создавать что-то

num_fire = 0
rel_time = False
oz = 3

while game:#пока game будет True цикл не закончится
    
    for e in event.get():#для каждого события в списке событий совершаемых пользователем (отслеживаем то что нажимает пользователь)
        if e.type == QUIT:#если тип события(e.type) равен нажатие на крестик(QUIT) меняем значение game на false и заканчиваем цикл
            game = False#значение переменной game меняется на False

        if e.type == KEYDOWN:#если кнопка на клавиатуре нажата
            if e.key == K_SPACE:#если на клавиатуре нажат пробел
                if num_fire < 5 and rel_time == False:#если количество выстрелов меньше 5 и перезарядка не идет
                    num_fire += 1
                    you.fire()#пременяем метод fire к игроку
                    #gold.play()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = tm()#зафиксировали время начала перезарядки


    if finish != True:
        window.blit(background, (0, 0))#помещаем фоновую картинку в начало точки координат

        kills = font2.render('Счет:' + str(died), True, (255, 255, 255))#создать видимую надпись "Счет: 0" белого цвета (True/False - сглаживать пиксели текста или нет)
        propusk = font2.render('Пропущено:' + str(objects), True, (255, 255, 255))#создать видимую надпись "Пропущено: 0" белого цвета (True/False - сглаживать пиксели текста или нет)
        

        you.update()#теперь главный герой может двигаться при нажатии на стрелочки
        monsters.update()#теперь все враги в группе могут двигаться автоматически
        bullets.update()#теперь все пули в группе могут двигаться автоматически
        enemy2.update()

        you.reset()#показываем главного героя на экране
        enemy.reset()#показываем врага на экране
        enemy2.reset()
        monsters.draw(window)#отрисовать группу монстров на окне
        bullets.draw(window)#отрисовать группу пуль на окне
        
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprite_list:
            died += 1
            enemy = Enemy('rabochiy.png', randint(0, 615), -50, randint(1, 3), 65, 65)
            monsters.add(enemy)

        if sprite.spritecollide(you, monsters, False) or sprite.spritecollide(you, interfere, False):
            sprite.spritecollide(you, monsters, True)
            sprite.spritecollide(you, interfere, True)
            oz -= 1

        live = font2.render(str(oz), True, (0, 255, 0))#создать видимую надпись "3" зелёного цвета (True/False - сглаживать пиксели текста или нет)
        window.blit(live, (650, 10))


        window.blit(kills, (0, 10))#отрисовываем надпись по верх фона
        window.blit(propusk, (0, 35))#отрисовываем надпись по верх фона

        if rel_time == True:
            new_time = tm()#фиксируем сколько сейчас времени
            if new_time - start < 3:
                relod = font2.render('Wait reload...', True, (255, 0, 0))#создать видимую надпись "Wait reload..." красного цвета (True/False - сглаживать пиксели текста или нет)
                window.blit(relod, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        


        if objects >= 3 or oz <= 0: #если пропущенно 3 врага или враг коснулся игрока (если поставить False то после столкновение враг не пропадет)
            window.blit(lose, (220, 150))#выводим надпись "YOU LOSE"
            finish = True

        if sprite.spritecollide(you, interfere, False):#если враг коснулся игрока (если поставить False то после столкновение враг не пропадет)
            window.blit(lose, (220, 150))#выводим надпись "YOU LOSE"
            finish = True

        if died >= 10:
            window.blit(win, (220, 150))#выводим надпись "YOU WIN"
            finish = True

    display.update()#обновление содержимого экрана (после каждого действия в цикле while экран отображается заново)
    clock.tick(FPS)#указываем частоту работы цикла while за 1 секунду
#создай 2 спрайта и размести их на сцене

#обработай событие «клик по кнопке "Закрыть окно"