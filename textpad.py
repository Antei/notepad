import PySimpleGUI as sg
from pathlib import Path

f_name = 'Безымянный'
params = {'font': 'Franklin 42', }

smileys = [
    'веселые', [':)', ':D', 'xD', '<3'],
    'грустные', [':(', 'T_T'],
    'другие', [':3']
]
smileys_events = smileys[1] + smileys[3] + smileys[5]

menu_layout = [
    ['Файл', ['Открыть', 'Сохранить', '---', 'Выход']],
    ['Инструменты', ['Количество слов']],
    ['Вставить', smileys]
]

sg.theme('GrayGrayGray')
layout = [
    [sg.Menu(menu_layout)],
    [sg.Text('Безымянный', key='-DOCNAME-', visible=True)],
    [sg.Multiline(autoscroll=True, expand_y=True, expand_x=True, key='-TEXTFIELD-')],
    [sg.Text('Выражение: '), sg.Input('', key='-EVAL-', expand_x=True), sg.Button('Решить', key='-ENTER-')],
    [sg.Text('Ответ: ', key='-OUTPUT-')]
]

window = sg.Window(f'Simple Textpad', 
                   layout, 
                   size=(800, 600), 
                   resizable=True,
                   )

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Открыть':
        file_path = sg.popup_get_file('Открыть', no_window=True)
        if file_path:
            file = Path(file_path)
            f_name = file_path.split('/')[-1]
            window['-TEXTFIELD-'].update(file.read_text())
            window['-DOCNAME-'].update(file_path.split('/')[-1])

    if event == 'Сохранить':
        file_path = sg.popup_get_file('Сохранить как', no_window=True, save_as=True) + '.txt'
        file = Path(file_path)
        f_name = file_path.split('/')[-1]
        file.write_text(values['-TEXTFIELD-'])
        window['-DOCNAME-'].update(file_path.split('/')[-1])

    if event == 'Выход':
        window.close()

    if event == 'Количество слов':
        full_text = values['-TEXTFIELD-']
        words = [word.strip() for word in full_text.split()]
        word_count = len(words)
        char_count = len(''.join(words))
        sg.popup(f'Количество слов в документе: {word_count}\nКоличество знаков в документе: {char_count}', 
                 no_titlebar=True)

    if event in smileys_events:
        current_text = values['-TEXTFIELD-']
        updated_text = current_text + ' ' + event
        window['-TEXTFIELD-'].update(updated_text)

    if event == '-ENTER-':
        if len(values['-EVAL-'].split()) >= 3: 
            result = eval(values['-EVAL-'])
            window['-OUTPUT-'].update(f'Ответ: {result}')

window.close()