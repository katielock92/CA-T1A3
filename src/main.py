"""This module contains the main executable for the quiz application.

This module is designed to be used in conjunction with functions.py to
call all expected functions and provide a functional and fun quiz experience.

This app was developed for educational purposes only.

MIT License

Copyright (c) 2023 Katie Lock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time

import colored
import emoji

import functions
import styles

def main():
    functions.welcome()

    functions.login()
    time.sleep

    functions.menu_decision()

    print(
        emoji.emojize(colored.stylize(
            "\n:waving_hand: Thank you for using the Rules Accreditation app!\n", styles.blue_bold
        ))
    )

if __name__ == '__main__':
    main()
