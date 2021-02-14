from Pet import *
import threading
import sys
import time
import click
import os


class Stage:
    def __init__(self, row_num=30, col_num=30):
        # self.pixels = [['  ' for c in range(col_num)] for r in range(row_num)]
        # for i in range(row_num):
        #     for j in range(col_num):
        #         if i == 0 or j == 0 or i == row_num - 1 or j == col_num - 1:
        #             self.pixels[i][j] = '██'

        self.items = []
        self.number_of_notifications_shown = 20
        self.notifications = [''] * self.number_of_notifications_shown

    def add_notifications(self, line):
        self.notifications.append(line)
        while len(self.notifications) > self.number_of_notifications_shown:
            self.notifications = self.notifications[1:]
        stage.draw()

    def draw(self, ):
        clear_command_line()
        print('\n'.join(self.notifications + ['\n' + '-' * 20 + '\n']))
        self.prompt()
        
    def prompt(self, ):
        print(f'1 - Show Status  2 - Eat  3 - Drink  4 - Play  '\
              f'5 - Clean  6 - Poop  q - Quit\n')


def user_input(input_buffer_size=1):
    global cmd
    while True:
        cmd = click.getchar()
        # cmd.append(click.getchar())
        # while len(cmd) > input_buffer_size:
        #     cmd = cmd[1:]

def clear_command_line():
    os.system('cls' if os.name == 'nt' else 'clear')

cmd = None
thread_user_input = threading.Thread(target=user_input)
thread_user_input.daemon = True
thread_user_input.start()

stage = Stage()
pet = Cat()
stage.items.append(pet)
pet.stage = stage
stage.add_notifications('Generating a cat')

stage.draw()
while True:
    if cmd == 'q':
        break
    elif cmd == '1':
        stage.add_notifications(f'[Status] {pet}') 
    elif cmd == '2':
        pet.eat()
        stage.add_notifications(f'[Eat]    {pet.__class__.__name__} eats a can of catfood')
    elif cmd == '3':
        pet.drink()
        stage.add_notifications(f'[Drink]  {pet.__class__.__name__} drinks some water')
    elif cmd == '4':
        pass
    elif cmd == '5':
        prev = len(stage.items)
        stage.items = [i for i in stage.items if i != 'poop']
        stage.add_notifications(f'[Clean]  {prev - len(stage.items)} poop cleaned')
    elif cmd == '6':
        pet.poop(forced=True)

    cmd = None

    for i in stage.items:
        if isinstance(i, Pet):
            if i.update() == -1:
                stage.add_notifications(f'[System] will exit in 3 seconds...')
                time.sleep(3)
                sys.exit()
    
    time.sleep(0.1)
