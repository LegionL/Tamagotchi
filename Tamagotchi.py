from Pet import Pet, Cat
import threading
import sys
import time
import click
import os


class Stage:
    def __init__(self, row_num=30, col_num=30):
        self.items = []
        self.number_of_notifications_shown = 20
        self.notifications = [''] * self.number_of_notifications_shown

    def add_notifications(self, line):
        self.notifications.append(line)
        while len(self.notifications) > self.number_of_notifications_shown:
            self.notifications = self.notifications[1:]
        self.draw()

    def draw(self, ):
        clear_command_line()
        print('\n'.join(self.notifications + ['\n' + '-' * 20 + '\n']))
        self.prompt()

    def prompt(self, ):
        print('1 - Show Status   2 - Eat   3 - Drink   '
              '4 - Clean   5 - Poop   6 - Sleep   q - Quit\n')


def user_input(input_buffer_size=1):
    global cmd
    while True:
        cmd = click.getchar()


def clear_command_line():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    global cmd
    cmd = None
    thread_user_input = threading.Thread(target=user_input)
    thread_user_input.daemon = True
    thread_user_input.start()

    stage = Stage()
    pet = Cat()
    stage.items.append(pet)
    pet.stage = stage
    stage.add_notifications('[System]  Generating a cat')

    stage.draw()
    while True:
        if cmd == 'q':
            break
        elif cmd == '1':
            stage.add_notifications(f'[Status]  {pet}')
        elif cmd == '2':
            pet.eat()
        elif cmd == '3':
            pet.drink()
        elif cmd == '4':
            prev = len(stage.items)
            stage.items = [i for i in stage.items if i != 'poop']
            stage.add_notifications(
                f'[Clean]   {prev - len(stage.items)} poop cleaned')
        elif cmd == '5':
            pet.poop(forced=True)
        elif cmd == '6':
            pet.sleep()

        cmd = None

        for i in stage.items:
            if isinstance(i, Pet):
                if i.update() == -1:
                    stage.add_notifications(
                        '[System]  will exit in 3 seconds...')
                    time.sleep(3)
                    sys.exit()

        time.sleep(0.1)


if __name__ == '__main__':
    main()
