<h1 align=center>🐍 SnakeType ⌨</h1>
<p align=center>Typing Test on your Terminal</b>

**SnakeType** is a simple program to test your typing-speed on your terminal.

Make sure you have windows-curses installed, you can do so by running: `pip install windows-curses`

## Usage:
```
python main.py
```
Arguments for snaketype:
- ```-f FILENAME, --filename FILENAME```
Contents of file is used for typing text
-  ```-a AMOUNT OF WORDS, --amount AMOUNT OF WORDS```
Amount of words to type

## TODO:
- [x] Add support for multiple y-lines, word wrapping
- [x] Add wpm and time elapsed
- [x] Add random words
- [x] Fix removing words using BACKSPACE
- [x] Argument/Options Parsing
- [ ] Fix WPM and time calculation