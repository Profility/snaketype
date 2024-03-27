import curses
import time
import math
import random
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="SnakeType",
        description="All snaketype command-line arguments"
    )

    parser.add_argument(
        "-a",
        "--amount",
        metavar="AMOUNT OF WORDS",
        default=25,
        type=int,
        help="Amount of words to type"
    )

    parser.add_argument(
        "-f",
        "--filename",
        metavar="FILENAME",
        default="words.txt",
        type=str,
        help="Name of the wordlist file"
    )

    return parser.parse_args()

def getWords():
    with open(f"words.txt", "r") as words:
        lines = words.readlines()
        wordlist = [line.strip() for line in lines]
        return str(' '.join(random.sample(wordlist, parse_arguments().amount)))

def main(screen):

    # Setup
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Correct
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Wrong

    curses.curs_set(0)

    typedText = []
    texty, textx = 1, 0
    wordText = getWords()
    startTime = time.time()

    screen.keypad(True)
    screen.clear()

    screen.addstr(texty, textx, wordText)
    screen.refresh()

    # WPM Loop
    while True:
        maxyx = screen.getmaxyx()

        elapsedTime = math.floor(max(time.time() - startTime, 1))
        wordsPerMinute = round(len(typedText) / (elapsedTime / 60) / 5)

        screen.addstr(0,0, f"Elapsed Time: {elapsedTime} | WPM: {wordsPerMinute}")

        # When finished
        if ''.join(typedText) == wordText: 
            print(f"you finished typing!\n\ntime: {elapsedTime}\nwpm: {wordsPerMinute}")
            break

        key = screen.getch()

        # If CTRL+Q pressed
        if key == 17 or key == 27 or key == 3:
            break

        # Handling resizing
        elif key == curses.KEY_RESIZE:
            curses.resize_term()
            continue

        # If any key pressed other than backspace
        elif key != 8:
            typedText.append(chr(key))

            # Compare typed text with target text
            for i, c in enumerate(typedText):
                textColor = curses.color_pair(1)
                if c != wordText[i]: # If typed character doesn't match target
                    textColor = curses.color_pair(2)
                else: # If typed character matches target
                    textColor = curses.color_pair(1)

            # If end of line is reached, go to next line
            if textx >= maxyx[1]:
                texty = texty + 1
                textx = 0
                
            screen.addstr(texty, textx, wordText[i], textColor) # Print characters with appropriate color
            textx = textx + 1
        
        # If BACKSPACE is pressed
        elif key == 8:
            if len(typedText) > 0:
                typedText.pop()
                screen.addstr(texty, textx-1, wordText[len(typedText)])
                textx = textx - 1

        screen.refresh()
            
curses.wrapper(main)