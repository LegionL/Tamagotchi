import threading
import time
import click
import sys


def user_input(input_buffer_size=10):
    global cmd
    while True:
        cmd.append(click.getchar())
        while len(cmd) > input_buffer_size:
            cmd = cmd[1:]


cmd = []
thread_user_input = threading.Thread(target=user_input)
thread_user_input.daemon = True
thread_user_input.start()

while True:
    print(cmd)
    if cmd and cmd[-1] == 'q':
        sys.exit()
        break
    # cmd = []
    time.sleep(0.1)
