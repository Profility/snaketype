import curses
import time
import math
import random
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="SnakeType", description="All snaketype command-line arguments"
    )

    parser.add_argument(
        "-f",
        "--filename",
        metavar="FILENAME",
        default="words.txt",
        type=str,
        help="Name of the wordlist file",
    )

    parser.add_argument(
        "-a",
        "--amount",
        metavar="AMOUNT OF WORDS",
        type=int,
        help="Amount of words to type",
    )

    return parser.parse_args()


def getWords():
    args = parse_arguments()
    try:
        with open(args.filename, "r") as words:
            lines = words.readlines()
            wordlist = [line.strip() for line in lines]

            if not args.amount:
                args.amount = len(wordlist)

            return str(" ".join(random.sample(wordlist, args.amount)))
    except Exception as e:
        return f"Failed to get words: {e}"


def compareCharacters(typedChar, targetChar):
    textColor = curses.color_pair(1)
    if typedChar != targetChar:  # If typed character doesn't match target
        textColor = curses.color_pair(2)
    else:  # If typed character matches target
        textColor = curses.color_pair(1)

    return textColor


def main(screen):

    # Setup
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Correct
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)  # Wrong

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

        screen.addstr(0, 0, f"Elapsed Time: {elapsedTime} | WPM: {wordsPerMinute}")

        # When finished
        if "".join(typedText) == wordText:
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

            # If end of line is reached, go to next line
            if textx >= maxyx[1]:
                texty = texty + 1
                textx = 0

            # Compare typed text with target text
            for i, c in enumerate(typedText):
                screen.addstr(
                    texty, textx, wordText[i], compareCharacters(c, wordText[i])
                )  # Print characters with appropriate color

            textx = textx + 1

        # If BACKSPACE is pressed
        elif key == 8:
            if len(typedText) > 0:
                typedText.pop()
                screen.addstr(texty, textx - 1, wordText[len(typedText)])
                textx = textx - 1

        screen.refresh()


curses.wrapper(main)
