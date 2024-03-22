import curses
import random
import time

# TODO:
# Remove delay for the cursor when pressing backspace
# Add support for multiple y-lines
# Add wpm and time elapsed
# Add random words

def main(screen):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Correct
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Wrong

    wordText = 'This is snaketype, a python typing tester.'
    typedText = []
    flag = False

    screen.keypad(True)
    screen.clear()
    screen.addstr(wordText)
    screen.refresh()

    curses.curs_set(0) # Disable cursor

    while True:
        if ''.join(typedText) == wordText: # Break when typedtext is equal to wordtext
            print('Finished!')
            break

        key = screen.getch()
        if key == 17: # If CTRL+Q pressed
            break

        elif key != 8: # If any key pressed
            typedText.append(chr(key))

            # Compare typed text with target text
            for i, c in enumerate(typedText):
                textColor = curses.color_pair(1)
                if c != wordText[i]: # If typed character doesn't match target
                    flag = True
                    textColor = curses.color_pair(2)
                elif flag == False: # If typed character matches target
                    textColor = curses.color_pair(1)

                screen.addstr(0, i, wordText[i], textColor) # Print characters with appropriate color
                #screen.addstr(2, 0, f"Typed: {''.join(typedText)}")

        elif key == 8: # If BACKSPACE is pressed
            if len(typedText) > 0:
                length = len(typedText) - 1
                typedText.pop()
                screen.move(0, length)
                screen.addstr(0, len(typedText), wordText[len(typedText)])
        screen.refresh()
            

curses.wrapper(main)