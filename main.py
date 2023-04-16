from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
import random
import time
import sys, os

global length
bomb_x = ""
bomb_y = ""
delays = [0.07, 0.03, 0.08, 0.07, 0.5]
long_words = True
instant_typing = True
pyautogui.PAUSE = 0
used_words = []

with open('wordlist.txt') as word_file:
    valid_words = set(word_file.read().split())

def release(key):
    global bomb_x, bomb_y, length, used_words
    if key == Key.f8:
        try:
            bomb_x, bomb_y = pyautogui.position()
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    if key == Key.f4:
        try:
            pyautogui.click(x=bomb_x, y=bomb_y, clicks=2)
            with pyautogui.hold('ctrl'):
                pyautogui.press(['c'])
            pyautogui.click(x=bomb_x - 100, y=bomb_y)
            time.sleep(0.1)
            syllabe = pyperclip.paste()
            final = syllabe.lower().strip()
            pyperclip.copy('')
            found_words = []
            time.sleep(0.1)
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

            while final_word in used_words:
                if len(used_words) == arrsize:
                    print("All words have been used.")
                    return True
                choice = random.randint(0, arrsize - 1)
                final_word = found_words[choice].strip('"').strip(':').strip('"')

            used_words.append(final_word)

            if instant_typing:
                pyperclip.copy(f'{final_word}')
                with pyautogui.hold('ctrl'):
                    pyautogui.press(['v'])
            else:
                for w in final_word:
                    delay = random.choice(delays)
                    pyautogui.write(w, delay)
            time.sleep(0.1)
            pyautogui.press('enter')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            return True


with Listener(on_release=release) as listener:
    listener.join()
