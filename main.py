import curses
import time
import math
import random

wordAmount = 20

def getWords():
    with open("words.txt", "r") as words:
        lines = words.readlines()
        wordlist = [line.strip() for line in lines]
        return str(' '.join(random.sample(wordlist, wordAmount)))

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

    textx = 0
    texty = 0

    screen.addstr(wordText)
    screen.refresh()

    # WPM Loop
    while True:
        screenyx = screen.getmaxyx()

        print(f"s{screen.getmaxyx()[1]} | t{textx}")
        elapsedTime = math.floor(max(time.time() - startTime, 1))
        wordsPerMinute = round(len(typedText) / (elapsedTime / 60) / 5)

        # When finished
        if ''.join(typedText) == wordText: 
            print(f"you finished typing!\n\ntime: {elapsedTime}\nwpm: {wordsPerMinute}")
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
                print(f"i{i}")
                textColor = curses.color_pair(1)
                if c != wordText[i]: # If typed character doesn't match target
                    textColor = curses.color_pair(2)
                else: # If typed character matches target
                    textColor = curses.color_pair(1)

            if textx >= screenyx[1]:
                texty = texty + 1
                textx = 0
                
            screen.addstr(texty, textx, chr(key), textColor) # Print characters with appropriate color
            textx = textx + 1
        
        # If BACKSPACE is pressed
        elif key == 8:
            if len(typedText) > 0:
                length = len(typedText) - 1
                typedText.pop()
                screen.move(texty, length)
                screen.addstr(texty, len(typedText), wordText[len(typedText)])

        screen.refresh()
            
curses.wrapper(main)