from pynput.keyboard import Listener, Key
import pyautogui
import pyperclip
import random
import time
import sys
import os

bomb_x = ""
bomb_y = ""
delays = [0.03, 0.04, 0.05, 0.06, 0.4]
long_words = True
instant_typing = False
pyautogui.PAUSE = 0
used_words = set()

with open('wordlist.txt') as word_file:
    valid_words = word_file.read().split()

def release(key):
    global bomb_x, bomb_y, used_words
    if key == Key.f8:
        try:
            bomb_x, bomb_y = pyautogui.position()
        except Exception as err:
            print(f"Error getting mouse position: {err}")
    if key == Key.f4:
        try:
            pyautogui.click(x=bomb_x, y=bomb_y, clicks=2)
            with pyautogui.hold('ctrl'):
                pyautogui.press('c')
            pyautogui.click(x=bomb_x - 100, y=bomb_y)
            time.sleep(0.1)
            syllable = pyperclip.paste().lower().strip()
            pyperclip.copy('')
            found_words = [word for word in valid_words if syllable in word]
            
            if not found_words:
                print("No words were found.")
                return

            if long_words:
                found_words.sort(key=len, reverse=True)
            
            final_word = random.choice(found_words)
            while final_word in used_words:
                if len(used_words) == len(found_words):
                    print("All words have been used.")
                    return
                final_word = random.choice(found_words)
            
            used_words.add(final_word)
            
            if instant_typing:
                pyperclip.copy(final_word)
                with pyautogui.hold('ctrl'):
                    pyautogui.press('v')
            else:
                for char in final_word:
                    delay = random.choice(delays)
                    pyautogui.write(char, delay)
            time.sleep(0.1)
            pyautogui.press('enter')
        except Exception as e:
            print(f"Error: {e}")

with Listener(on_release=release) as listener:
    listener.join()
