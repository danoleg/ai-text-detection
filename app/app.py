import iris
from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_material import Material
from helpers.text import describe_text


app = Flask(__name__)
Material(app)

app.config['iris_host'] = ""
app.config['iris_port'] = 1972
app.config['iris_namespace'] = "USER"
app.config['iris_username'] = "SQLAdmin"
app.config['iris_password'] = ""
app.config['connection'] = None


@app.route('/')
def index():
    return redirect('/config')


@app.route('/config', methods=['GET', 'POST'])
def config():

    data = {
        "hostname": app.config['iris_host'],
        "port": int(app.config['iris_port']),
        "user": app.config['iris_namespace'],
        "namespace": app.config['iris_username'],
        "password": app.config['iris_password']
    }

    if request.method == 'POST':
        app.config['iris_host'] = request.form['hostname']
        app.config['iris_port'] = request.form['port']
        app.config['iris_namespace'] = request.form['user']
        app.config['iris_username'] = request.form['namespace']
        app.config['iris_password'] = request.form['password']

        try:

            app.config['connection'] = conn = iris.connect(
                app.config['iris_host'],
                int(app.config['iris_port']),
                app.config['iris_namespace'],
                app.config['iris_username'],
                app.config['iris_password']
            )

            cur = conn.cursor()

            cur.execute("""DROP TABLE IF EXISTS Texts""")

            cur.execute("""CREATE TABLE IF NOT EXISTS Texts (
                        label VARCHAR(16),
                        char_count FLOAT,
                        word_count FLOAT,
                        avg_word_length FLOAT,
                        sentence_count FLOAT,
                        avg_sentence_length FLOAT,
                        unique_word_count FLOAT,
                        stop_word_count FLOAT,
                        unique_word_ratio FLOAT,
                        punc_count FLOAT,
                        punc_ratio FLOAT,
                        question_count FLOAT,
                        exclamation_count FLOAT,
                        digit_count FLOAT,
                        capital_count FLOAT,
                        repeat_word_count FLOAT,
                        unique_bigram_count FLOAT,
                        unique_trigram_count FLOAT,
                        unique_fourgram_count FLOAT
                    )""")
            cur.close()

            return redirect('/text-processing')
        except Exception as e:
            return str(e)

    return render_template('config.html', data=data)


@app.route('/text-processing', methods=['GET', 'POST'])
def text_processing():

    conn = app.config['connection']
    prediction_text_source_value = None
    prediction_text_source_probability = None
    text = ''

    if not conn:
        return redirect('/')

    if request.method == 'POST':
        text = request.form['text']
        text_data = describe_text(text)
        timestamp = int(round(datetime.now().timestamp()))

        insert_query = f"""INSERT INTO Texts VALUES 
        ('w{str(timestamp)[5:]}',
        {text_data['char_count']},
        {text_data['word_count']},
        {text_data['avg_word_length']},
        {text_data['sentence_count']},
        {text_data['avg_sentence_length']},
        {text_data['unique_word_count']},
        {text_data['stop_word_count']},
        {text_data['unique_word_ratio']},
        {text_data['punc_count']},
        {text_data['punc_ratio']},
        {text_data['question_count']},
        {text_data['exclamation_count']},
        {text_data['digit_count']},
        {text_data['capital_count']},
        {text_data['repeat_word_count']},
        {text_data['unique_bigram_count']},
        {text_data['unique_trigram_count']},
        {text_data['unique_fourgram_count']}
        )
        """

        cur = conn.cursor()
        cur.execute(insert_query)
        cur.execute("""SELECT 
              TOP(1)
              PREDICT(TextModel use TextTrainedModel) as prediction, 
              PROBABILITY(TextModel use TextTrainedModel for 'ai') as probability_label
            FROM 
            SQLUser.Texts order by label DESC""")
        prediction = cur.fetchall()
        cur.close()

        prediction_text_source_value = prediction[0][0]
        prediction_text_source_probability = round(round(float(prediction[0][1]), 2) * 100, 2)
        if prediction_text_source_value == 'human':
            prediction_text_source_probability = 100-prediction_text_source_probability

        print(prediction[0], flush=True)

    return render_template(
        'predict.html',
        text=text,
        prediction_text_source_value=prediction_text_source_value,
        prediction_text_source_probability=prediction_text_source_probability
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8010)
