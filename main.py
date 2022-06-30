from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
import random
from time import sleep

global length
bomb_x = ""
bomb_y = ""
delays = [0.1, 0.03, 0.1, 0.03, 0.3]
long_words = False
instant_typing = False
pyautogui.PAUSE = 0

with open('wordlist.txt') as word_file:
    valid_words = set(word_file.read().split())


def release(key):
    global bomb_x, bomb_y, length
    if key == Key.f8:
        try:
            bomb_x, bomb_y = pyautogui.position()
        except Exception as err:
            print(f"Something went wrong: {err}")
    if key == Key.f4:
        try:
            pyautogui.click(x=bomb_x, y=bomb_y, clicks=2)
            with pyautogui.hold('ctrl'):
                pyautogui.press(['c'])
            pyautogui.click(x=bomb_x - 100, y=bomb_y)
            sleep(0.1)
            syllabe = pyperclip.paste()
            final = syllabe.lower().strip()
            pyperclip.copy('')
            found_words = []
            sleep(0.1)
            for i in valid_words:
                if i.find(final) != -1:
                    found_words.append(i)

            if len(found_words) == 0:
                print("No words were found.")
            length = 0
            arrsize = len(found_words)
            if long_words:
                for i in range(len(found_words)):
                    if len(found_words[i]) > length:
                        length = i
                choice = length
            else:
                choice = random.randint(0, arrsize - 1)
            final_word = found_words[choice].strip('"').strip(':').strip('"')
            if instant_typing:
                pyperclip.copy(f'{final_word}')
                with pyautogui.hold('ctrl'):
                    pyautogui.press(['v'])   
            else:
                for w in final_word:
                    delay = random.choice(delays)
                    pyautogui.write(w, delay)
            sleep(0.1)
            pyautogui.press('enter')
            print(found_words[choice])
        except Exception as err:
            print(f'Something went wrong: {err}')
            return True


with Listener(on_release=release) as listener:
    listener.join()

