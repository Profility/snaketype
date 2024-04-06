import curses
import time
import math
import random
import argparse

class SnakeType:
    def __init__(self):
        self.typedText = []
        self.texty, self.textx = 1, 0
        self.wordText = self.getWords()
        self.startTime = time.time()

        curses.wrapper(self.main)
        pass

    def parse_arguments(self):
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


    def getWords(self):
        args = self.parse_arguments()
        try:
            with open(args.filename, "r") as words:
                lines = words.readlines()
                wordlist = [line.strip() for line in lines]

                if not args.amount:
                    args.amount = len(wordlist)

                return str(" ".join(random.sample(wordlist, args.amount)))
        except Exception as e:
            return f"Failed to get words: {e}"


    def compareCharacters(self, typedChar, targetChar):
        textColor = curses.color_pair(1)
        if typedChar != targetChar:  # If typed character doesn't match target
            textColor = curses.color_pair(2)
        else:  # If typed character matches target
            textColor = curses.color_pair(1)

        return textColor


    def main(self, screen):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Correct
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)  # Wrong
        curses.curs_set(0)

        screen.keypad(True)
        screen.clear()
        screen.addstr(self.texty, self.textx, self.wordText)
        screen.refresh()

        # WPM Loop
        while True:
            maxyx = screen.getmaxyx()

            elapsedTime = math.floor(max(time.time() - self.startTime, 1))
            wordsPerMinute = round(len(self.typedText) / (elapsedTime / 60) / 5)

            screen.addstr(0, 0, f"Elapsed Time: {elapsedTime} | WPM: {wordsPerMinute}")

            # When finished
            if "".join(self.typedText) == self.wordText:
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
                self.typedText.append(chr(key))

                # If end of line is reached, go to next line
                if self.textx >= maxyx[1]:
                    self.texty = self.texty + 1
                    self.textx = 0

                # Compare typed text with target text
                for i, c in enumerate(self.typedText):
                    screen.addstr(
                        self.texty, self.textx, self.wordText[i], self.compareCharacters(c, self.wordText[i])
                    )  # Print characters with appropriate color

                self.textx = self.textx + 1

            # If BACKSPACE is pressed
            elif key == 8:
                if len(self.typedText) > 0:
                    self.typedText.pop()
                    screen.addstr(self.texty, self.textx - 1, self.wordText[len(self.typedText)])
                    self.textx = self.textx - 1

            screen.refresh()

if __name__ == "__main__":
    SnakeType()