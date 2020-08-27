#!/usr/bin/env python3

from time import sleep
from pynput.keyboard import Key, KeyCode, Listener
from subprocess import Popen

print('TOMATO TIMER', '='*20, sep='\n')

pomodoro_time = 1500
short_break = 300 
long_break = 900
pomodoro = 1

try:
    while True:

        print(f'\nIniciando pomodoro nº {pomodoro} ...\n')
        input('Pressione ENTER para iniciar.')
        while pomodoro_time > 0:
            minutes = str(int(pomodoro_time / 60)).zfill(2)
            seconds = str(pomodoro_time % 60).zfill(2)
            print(f'{minutes}:{seconds}')
            sleep(30)
            pomodoro_time -= 30

        if pomodoro % 4 > 0:
            time_pause = short_break
            message = 'Hora de uma pausa curta!'
        else:
            time_pause = long_break
            message = 'Hora uma pausa longa!'

        # avisa que o pomodoro acabou
        Popen(['aplay', '-q', 'alert.wav'])
        Popen(['notify-send', '-t', '3500', 'TOMATO', message])

        minutes = str(int(time_pause / 60)).zfill(2)
        seconds = str(time_pause % 60).zfill(2)
        print(f'\nPomodoro nº {pomodoro} finalizado. Tire uma pausa de {minutes}:{seconds}!')
        input('Pressione ENTER para continuar.\n')

        while time_pause > 0:
            mins = str(int(time_pause / 60)).zfill(2)
            secs = str(time_pause % 60).zfill(2)
            print(f'{mins}:{secs}')
            sleep(15)
            time_pause -= 15

        # avisa que a pausa acabou
        Popen(['aplay', '-q', 'alert.wav'])
        Popen(['notify-send', '-t', '3500', 'TOMATO', 'Pausa encerrada! Voltando aos trabalhos ...'])

        pomodoro_time = 1500
        pomodoro += 1

except KeyboardInterrupt:
    print('\nPrograma encerrado!', '='*20, sep='\n')

