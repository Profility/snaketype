import curses
import time
import math
import random
import json

def getWords():
    with open('wordlist.json', 'r') as list:
        return str(' '.join(random.sample(json.load(list), 15)))

def main(screen):

    # Setup
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Correct
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Wrong

    curses.curs_set(0)

    wordText = getWords()
    typedText = []
    startTime = time.time()

    screen.keypad(True)
    screen.clear()

    screen.addstr(wordText)
    screen.refresh()

    # WPM Loop
    while True:
        elapsedTime = math.floor(max(time.time() - startTime, 1))
        wordsPerMinute = round(len(typedText) / (elapsedTime / 60) / 5)

        if ''.join(typedText) == wordText: # Break when typedtext is equal to wordtext
            print(f'Finished!\nElapsed Time: {elapsedTime}s\nWPM: {wordsPerMinute}')
            break

        key = screen.getch()

        # If CTRL+Q pressed
        if key == 17 or key == 27:
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

                screen.addstr(0, i, wordText[i], textColor) # Print characters with appropriate color
        
        # If BACKSPACE is pressed
        elif key == 8:
            if len(typedText) > 0:
                length = len(typedText) - 1
                typedText.pop()
                screen.move(0, length)
                screen.addstr(0, len(typedText), wordText[len(typedText)])

        screen.refresh()
            
curses.wrapper(main)