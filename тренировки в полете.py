from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/training/<prof>')
def index(prof):
    title1 = "Миссия Колонизация Марса"
    title2 = "И на Марсе будут яблони цвести!"
    if prof == 'инженер' or prof == 'строитель':
        a = 'Инженерные тренажеры'
    else:
        a = 'Научные симуляторы'
    return render_template('Mars.html', title=prof, title1=title1,
                           title2=title2, workout=a,
                           picture=url_for('static', filename='img/MARS2.png'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
