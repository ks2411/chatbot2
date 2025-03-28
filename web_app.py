from flask import Flask, render_template, request
from sales_bot import get_seller_answer  # Замените на ваш модуль с логикой бота

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    if request.method == 'POST':
        question = request.form['question']
        answer = get_seller_answer(question)  # Замените на вашу функцию получения ответа
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True)