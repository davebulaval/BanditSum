#!/usr/bin/env python
"""
This module aims to provide tools to easily time snippets of codes with color coding.
"""

import functools
from datetime import datetime as dt
from time import time

try:
    from colorama import Fore, Style, init

    init()
except ModuleNotFoundError:
    # Emulate the Fore and Style class of colorama with a class that as an empty string for every attributes.
    class EmptyStringAttrClass:
        def __getattr__(self, attr):
            return ''


    Fore = EmptyStringAttrClass()
    Style = EmptyStringAttrClass()

__author__ = 'Jean-Samuel Leboeuf, Frédérik Paradis'
__date__ = 'May 28th, 2019'


class Timer:
    def __init__(self,
                 display_name=None,
                 datetime_format='%Y-%m-%d %Hh%Mm%Ss',
                 elapsed_time_format='short',
                 main_color='LIGHTYELLOW_EX',
                 exception_exit_color='LIGHTRED_EX',
                 name_color='LIGHTBLUE_EX',
                 time_color='LIGHTCYAN_EX',
                 datetime_color='LIGHTMAGENTA_EX'):

        self.display_name = display_name
        self.start_time = None
        self.elapsed_time = None
        self.datetime_format = datetime_format
        self.elapsed_time_format = elapsed_time_format

        self.main_color = getattr(Fore, main_color)
        self.exception_exit_color = getattr(Fore, exception_exit_color)
        self.name_color = getattr(Fore, name_color)
        self.time_color = getattr(Fore, time_color)
        self.datetime_color = getattr(Fore, datetime_color)

    def __enter__(self):
        self._start_timer()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed_time = time() - self.start_time
        if exc_type:
            self._exception_exit_end_timer()
        else:
            self._normal_exit_end_timer()

    @property
    def func_name(self):
        if self.display_name:  # self.func.__name__ != 'main':
            return f"of '{self.name_color}{self.display_name}{self.main_color}' "
        else:
            return ''

    @property
    def datetime(self):
        if self.datetime_format is None:
            return ''
        else:
            return 'on ' + self.datetime_color + dt.now().strftime(self.datetime_format) + self.main_color

    def format_long_time(self, seconds, period):
        periods = {
            'd': 'day',
            'h': 'hour',
            'm': 'minute',
            's': 'second'
        }

        pluralize = lambda period_value: 's' if period_value > 1 else ''
        format_period_string = periods[period] + pluralize(seconds)
        if period != 's':
            return f"{int(seconds)} {format_period_string}"
        else:
            return f"{seconds:.2f} {format_period_string}"

    def format_short_time(self, seconds, period):
        if period != 's':
            return f"{int(seconds)}{period}"
        else:
            return f"{seconds:.2f}{period}"

    def format_elapsed_time(self, seconds):
        is_long = self.elapsed_time_format == 'long'
        format_time = self.format_long_time if is_long else self.format_short_time
        periods = {
            'd': 60 * 60 * 24,
            'h': 60 * 60,
            'm': 60,
        }

        time_strings = []
        for period_name, period_seconds in periods.items():
            if seconds >= period_seconds:
                period_value, seconds = divmod(seconds, period_seconds)
                time_strings.append(format_time(period_value, period_name))

        time_strings.append(format_time(seconds, 's'))

        return self.time_color + " ".join(time_strings)

    def _start_timer(self):
        self.start_time = time()
        print(self.main_color + f'Execution {self.func_name}started {self.datetime}.\n' + Style.RESET_ALL)

    def _exception_exit_end_timer(self):
        print(self.exception_exit_color +
              '\nExecution terminated after ' +
              self.format_elapsed_time(self.elapsed_time) +
              f'{self.exception_exit_color} {self.datetime}{self.exception_exit_color}.\n' +
              Style.RESET_ALL)

    def _normal_exit_end_timer(self):
        print(self.main_color +
              f'\nExecution {self.func_name}completed in ' +
              self.format_elapsed_time(self.elapsed_time) +
              f'{self.main_color} {self.datetime}.\n' +
              Style.RESET_ALL)


def timed(func=None, *, display_func_name=True, display_name=None, **timer_kwargs):
    if func is None:
        def missing_func_timed(new_func):
            return timed(new_func, **timer_kwargs)

        return missing_func_timed

    if not display_name and display_func_name:
        display_name = func.__name__

    @functools.wraps(func)
    def timed_func(*args, **kwargs):  # args[0] is the reference to 'self' if 'func' is a method.
        with Timer(display_name, **timer_kwargs):
            return func(*args, **kwargs)

    return timed_func


if __name__ == '__main__':
    from time import sleep


    @timed
    def foo():
        sleep(.1)
        print('foo!')


    foo()


    @timed(datetime_format='%Hh%Mm%Ss', display_func_name=False, main_color='WHITE')
    def bar():
        sleep(.1)
        print('bar!')
        raise RuntimeError


    try:
        bar()
    except RuntimeError:
        pass


    class Spam:
        @timed
        def spam(self):
            sleep(.1)
            print('egg!')


    Spam().spam()

    with Timer():
        print('graal')

    with Timer('python', time_color='MAGENTA'):
        print('Python')

    with Timer('python', elapsed_time_format='long', time_color='CYAN') as t:
        print("sleep 1.5 seconds")
        sleep(1.5)
    print(t.elapsed_time)
