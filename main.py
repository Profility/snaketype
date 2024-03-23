import curses
import random
import json

# TODO:
# Remove delay for the cursor when pressing backspace
# Add support for multiple y-lines, word wrapping
# Add wpm and time elapsed
# Add random words /

def getWords():
    with open('wordlist.json', 'r') as list:
        return str(' '.join(random.sample(json.load(list), 15)))

def main(screen):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Correct
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Wrong
    curses.curs_set(0) # Disable cursor

    wordText = getWords()
    wrongFlag = False
    typedText = []

    screen.keypad(True)
    screen.clear()
    screen.addstr(wordText)
    screen.refresh()

    while True:
        if ''.join(typedText) == wordText: # Break when typedtext is equal to wordtext
            print('Finished!')
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
                    wrongFlag = True
                    textColor = curses.color_pair(2)
                elif wrongFlag == False: # If typed character matches target
                    textColor = curses.color_pair(1)

                screen.addstr(0, i, wordText[i], textColor) # Print characters with appropriate color
                #screen.addstr(2, 0, f"Typed: {''.join(typedText)}")
        
        # If BACKSPACE is pressed
        elif key == 8:
            if len(typedText) > 0:
                length = len(typedText) - 1
                typedText.pop()
                screen.move(0, length)
                screen.addstr(0, len(typedText), wordText[len(typedText)])

        screen.refresh()
            
curses.wrapper(main)