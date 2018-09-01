# -*- coding: utf-8 -*-
#import RPi.GPIO as GPIO
import GPIOmock as GPIO
import threading
import time
import random
import os
from subprocess import call

DEBUG = 4
DEBUG_LEVELS = {1: "[i]", 2: "[e]", 3: "[d]"}

# green, red, blue, yellow
LIGHTS = [33, 37, 35, 31]
BUTTONS = [11, 15, 13, 7]
NOTES = ["E3", "A4", "E4", "Cs4"]

# values you can change that affect game play
speed = 0.25
use_sounds = False

# flags used to signal game status
is_displaying_pattern = False
is_won_current_level = False
is_game_over = False

# game state
current_level = 1
current_step_of_level = 0
pattern = []


def log_print(msg, lvl, clr=False):
    """
    prints msg with log level
    :param msg: msg to print
    :param lvl: log level of message
    :param clr: clear console flag
    """
    if clr:
        os.system('cls' if os.name == 'nt' else 'clear')

    if lvl < DEBUG:
        log_print(DEBUG_LEVELS[lvl], repr(msg))


def play_note(note):
    """
    using Sonic Pi to play a note
    :param note: note to play
    """
    if use_sounds:
        call(["sonic_pi", "play :" + note])

    log_print("Playing Note %s" % note, 3)


def initialize_sonic_pi():
    """
    Initializing Sonic Pi for best performance using web know how
    """
    # call(["sonic_pi", "set_sched_ahead_time! 0"])
    # call(["sonic_pi", "use_debug false"])
    # call(["sonic_pi", "use_synth :pulse"])
    # call(["sonic_pi", "use_bpm 100"])

    log_print("Sonic Pi Initialized", 3)


def initialize_gpio():
    """
    Initializing GPIO pins and setting event handlers
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LIGHTS, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for i in range(4):
        GPIO.add_event_detect(BUTTONS[i], GPIO.FALLING, verify_player_selection, 400 if use_sounds else 250)

    log_print("GPIO Initialized", 3)


def verify_player_selection(channel):
    """
    Event driven check if player was correct
    @Todo add limit to levels

    :param channel: the GPIO channel the event fired on
    """
    global current_step_of_level, current_level, is_won_current_level, is_game_over

    if not is_displaying_pattern and not is_won_current_level and not is_game_over:
        play_note(NOTES[BUTTONS.index(channel)])
        flash_led_for_button(channel)
        if channel == BUTTONS[pattern[current_step_of_level]]:
            current_step_of_level += 1
            if current_step_of_level >= current_level:
                current_level += 1
                is_won_current_level = True
        else:
            is_game_over = True


def flash_led_for_button(button_channel, delay=0.1):
    led = LIGHTS[BUTTONS.index(button_channel)]
    turn_light(led, 1)
    time.sleep(delay)
    turn_light(led, 0)


def add_new_color_to_pattern():
    global is_won_current_level, current_step_of_level
    is_won_current_level = False
    current_step_of_level = 0
    next_color = random.randint(0, 3)
    pattern.append(next_color)


def display_pattern_to_player():
    global is_displaying_pattern
    is_displaying_pattern = True

    reset_lights()

    for i in range(current_level):
        play_note(NOTES[pattern[i]])
        led = LIGHTS[pattern[i]]
        turn_light(led, 1)
        time.sleep(speed)
        turn_light(led, 0)
        time.sleep(speed)

    is_displaying_pattern = False


def wait_for_player_to_repeat_pattern():
    while not is_won_current_level and not is_game_over:
        time.sleep(0.1)


def reset_lights():
    # reset lights
    GPIO.output(LIGHTS, GPIO.LOW)
    log_print("Resetting Lights", 3)


def turn_light(led, state):
    if state:
        GPIO.output(led, GPIO.HIGH)
        log_print("light %d is now on" % led, 3)
    else:
        GPIO.output(led, GPIO.LOW)
        log_print("light %d is now off" % led, 3)


def reset_board_for_new_game():
    global is_displaying_pattern, is_won_current_level, is_game_over
    global current_level, current_step_of_level, pattern
    is_displaying_pattern = False
    is_won_current_level = False
    is_game_over = False
    current_level = 1
    current_step_of_level = 0
    pattern = []
    reset_lights()

    log_print("Begin new round!", 1, True)


def start_game():
    reset_board_for_new_game()

    while True:
        add_new_color_to_pattern()
        display_pattern_to_player()
        wait_for_player_to_repeat_pattern()

        if is_game_over:
            log_print("Game Over! Your max score was {} colors!\n".format(current_level - 1), 1)

            play_again = input("Enter 'Y' to play again, or just press [ENTER] to exit.\n")
            if play_again.lower() != "y":
                log_print("Thanks for playing!", 1)
                break

            reset_board_for_new_game()

        time.sleep(2)


def start_game_monitor():
    log_print("Starting Game Thread", 3)
    t = threading.Thread(target=start_game)
    t.daemon = True
    t.start()
    t.join()


def main():
    try:
        initialize_sonic_pi()
        initialize_gpio()
        start_game_monitor()
    finally:
        # clean GPIO
        log_print("Calling GPIO cleanup", 3)
        GPIO.cleanup()


if __name__ == '__main__':
    main()
