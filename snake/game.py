from classes import Env, HumanSnake, AISnake, Game

N = 3
num = 500000
alpha = 1

s = HumanSnake()
s = AISnake(N,alpha)

game = Game(s,N,num,print_every=5000)

game.train()
game.play()
