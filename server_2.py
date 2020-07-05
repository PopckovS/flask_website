#! /usr/bin/python3

from flask import Flask, url_for, request, render_template, \
    redirect, abort, flash, make_response
# from werkzeug import secure_filename

app = Flask(__name__)

# Пока не знаю что это за чтука, но без нее flash сообщения не работают
app.secret_key = 'some_secret'

STYLE_PATH = 'style/'


# Метод выводит главное меню
def get_main_menu():
    '''Стандартное главное меню'''
    file = open('templates/main_menu.html', 'r')
    return file.read()


# Метод выводит форму для отправки
def show_form_login():
    file = open('templates/form.html', 'r')
    return file.read()


# Метод возвращает параметры запросса
def form_login_check():
    return str(request.form)


# Метод выводит форму отправки, или обрабатывает отправленную форму
@app.route('/login', methods=['POST', 'GET'])
def page_login():
    param = ''
    if request.method == 'GET':
        param = show_form_login()
    elif request.method == 'POST':
        param = form_login_check()

    result = get_main_menu() + param
    return result


def style_main():
    # return STYLE_PATH + 'main.css'
    return 'style/main.css'


@app.route("/<path:any>")
def page_not_found(any):
    header = get_main_menu() + '<h1>Страница не найдена !</h1>'
    return header


@app.route("/")
def page_index():
    return render_template('index.html',
                           menu=get_main_menu(),
                           style_main=style_main(),
                           header='Главная страница')


@app.route("/help")
def page_help():
    return render_template('help.html', menu=get_main_menu())


@app.route("/user/<username>")
def page_user(username):
    header = '<h1>Hello {name}</h1>'.format(name=username)
    header += get_main_menu()
    return header


@app.route("/args")
def page_args():
    '''Страница для отображения GET параметров из URL'''
    params = request.args
    result = get_main_menu() + str(params)
    return result



@app.route('/document-upload', methods=['GET', 'POST'])
def page_upload_file():
    return render_template('document_upload.html', menu=get_main_menu())



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file_1']
        file.save('uploads/' + file.filename)
        # file.save('uploads/' + secure_filename(file.filename))

        # После загрузки файла на сервер, выводим flash сообщение о успешной загрузки
        flash('Файл {file} успешно загружен'.format(file=file.filename))
    return redirect('document-upload')


@app.route('/errors')
def page_about_errors():
    '''Страница с общим пояснением о обработке ошибок во Flask.'''
    return render_template('errors.html', menu=get_main_menu())


@app.route('/errors/<error>')
def page_of_errors_examples(error):
    '''Метод перенаправляет на стр.ошибок которая указана в GET параметре'''
    abort(int(error))


# @app.route('/flash/<name>', methods=['GET', 'POST'])
@app.route('/flash/<name>')
def page_flash(name):
    flash('You were successfully logged as = ' + name)
    return render_template('flash.html', menu=get_main_menu())


@app.route('/response', methods=['POST', 'GET'])
def page_response():
    '''make_response Получаем ответ до завершения функции.

    1 - аргумент render_template() с шаблоном, и переданными в него данными для шаблонизатора
    2 - аргумент это статус ответа
    Таким образом мы получаем обьект http ответа, и имееем возможность изменять его до возвращения.
    '''

    response = make_response(render_template('response.html', menu=get_main_menu()), 200)

    print('============= начало ответа =============')
    print(response)
    print('============= конец ответа =============')

    return response
    # return render_template('response.html', menu=get_main_menu())






# Запуск всего приложения, в случае если приложение запущено как основное, а не модуль
if __name__ == "__main__":
    app.run(debug=True, port=5000) #запустить на порту 5000








'''
Вопросы для разбора:
WSGI приложение 
'User %s' % username
Werkzeug
обработка специальных (escape-) последовательностей (escaping)



Различные модули из Flask:
1) url_for - динамич генерация url для функция
2) request - работа с http GET, POST ...
3) render_template - Работа с шаблонами




Сайт нужно каждый раз перезагружать, debug=True это укажет что сервер 
работает в режиме  дебага, и будет перезагруж автоматически. И мы получим
сообщение "Debugger is active!".

Изначально сайт открыт локально, установив host='0.0.0.0' можно его расшарить.
    app.run(host='0.0.0.0', port=5000)
    
При указании пути в роуте, можно указыать динамические переменные, которые
надо передавть в метод в виде аргументов, также можно указывать тип этих аргументов:
Число      <int:post_id>     
Десятичное <float:number>    
Как стандартное но принимает в себя слеши <path:long_url_path>    

Модуль Werkzeug определяет правила работы с url во Flask.

url_for функция создает сложные url для функции обработчика, по сути это заменяется 
прсото созданием жестких ссылок.

methods=['GET', 'POST'] можно указывать что метод принимает,несколько методов.
from flask import request импортируя методы можно определять, какой тип именно сейчас
работает.   request.method == 'POST'  request.method == 'GET'


request, session и g 1 , а также
к функции get_flashed_messages().
'''



