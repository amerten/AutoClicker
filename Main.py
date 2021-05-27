import dungeon_auto_clicker
import forge_auto_clicker
import PySimpleGUI as sg
import threading


def check_args(args):
    try:
        freq = float(args['FREQUENCY'])
        if freq < 0.5:
            return False
        return True
    except:
        return False


if __name__ == "__main__":
    layout = [ [sg.Text('Dungeon (optional):'), sg.Combo(dungeon_auto_clicker.DUNGEONS_LIST, key='DUNGEON')],
            [sg.Text('Frequency [s]:'), sg.Input('5', key='FREQUENCY', size=(10, 1)), sg.Text(key='FREQ_ERROR', size=(20, 1))],
            [sg.Text('Nb runs: '), sg.Input('0', key='NB_RUNS'), sg.Checkbox('Refill', key='REFILL')],
            [sg.Button('Start', key='START'), sg.Button('Stop', key='STOP', disabled=True), sg.Text(key='RUNNING', size=(10, 1))],
            [sg.Text('Forge Auto Sell')],
            [sg.Button('Start', key='START_FORGE'), sg.Button('Stop', key='STOP_FORGE', disabled=True)] ]

    window = sg.Window('Auto Clicker', layout)
    dac = dungeon_auto_clicker.DungeonAutoClicker(window['DUNGEON'])
    fac = forge_auto_clicker.ForgeAutoClicker()

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'START':
            args_ok = check_args(values)
            if not args_ok:
                window['FREQ_ERROR'].update('Invalid frequency', text_color='RED')
            else:
                window['FREQ_ERROR'].update('')
                dac._dungeon = values['DUNGEON']
                ac_nb_runs = 0
                t = threading.Thread(target=dac.run, args=(values,))
                t.start()
                window['START'].update(disabled=True)
                window['STOP'].update(disabled=False)
                window['RUNNING'].update('Running...', text_color='YELLOW')
                window['START_FORGE'].update(disabled=True) 
        elif event == 'STOP':
            window['START'].update(disabled=False)
            window['STOP'].update(disabled=True)
            window['RUNNING'].update('')
            window['START_FORGE'].update(disabled=False)
            dac.terminate()
        elif event == 'START_FORGE':
            window['START'].update(disabled=True)
            window['START_FORGE'].update(disabled=True)
            window['STOP_FORGE'].update(disabled=False)
            fas_t = threading.Thread(target=fac.run)
            fas_t.start()
        elif event == 'STOP_FORGE':
            window['START'].update(disabled=False)
            window['START_FORGE'].update(disabled=False)
            window['STOP_FORGE'].update(disabled=True)
            fac.terminate()

    window.close()
