"""Windows Desktop Clock."""
import os
import PySimpleGUI as sg
import platform
import ctypes
from configparser import ConfigParser
from datetime import datetime

rPath = os.path.dirname(os.path.realpath(__file__))


def main():
    """GUI."""
    settings = ConfigParser()
    settings.read(os.path.join(rPath, 'settings', 'settings.ini'))
    fontSize = int(settings['font']['size'])
    monoFont = (settings['font']['mono'], fontSize)
    bgColor = settings['color']['background']
    fgColor = settings['color']['foreground']
    alpha = float(settings['color']['alpha'])
    wr = float(settings['location']['wr'])
    hr = float(settings['location']['hr'])

    layout = [
        [sg.Text(
            '',
            font=monoFont,
            background_color=bgColor,
            text_color=fgColor,
            justification='center',
            pad=(0, 0),
            key='-time-')],
    ]

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    window = sg.Window(
        'Desktop Clock',
        layout,
        background_color=bgColor,
        alpha_channel=alpha,
        keep_on_top=True,
        no_titlebar=True,
        grab_anywhere=True,
        finalize=True,
        transparent_color=bgColor,
        location=(int(screensize[0] * wr - 180), int(screensize[1] * hr))
    )

    while True:
        event, _ = window.read(10)
        if event == sg.WIN_CLOSED:
            break

        window['-time-'].update(
            datetime.now().strftime('%H:%M:%S')
        )

    window.close()


if __name__ == '__main__':
    if platform.release() == "7":
        ctypes.windll.user32.SetProcessDPIAware()
    elif platform.release() == "8" or platform.release() == "10":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    main()
