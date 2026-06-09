from random import randint
from flask import Flask, session, redirect, url_for
from SQLM6L4 import get_question_after
def index():
   max_quiz = 3
   # o si el estudiante escribió get_quiz_count(), entonces puede importarlo y especificar:
   # max_quiz = get_quiz_count[0] 
   session['quiz'] = randint(1, max_quiz)
   # o si el estudiante escribió get_quiz_count(), entonces puede importarlo y especificar:
   # session['quiz'] = get_random_quiz_id()
   session['last_question'] = 0
   return '<a href="/test">Test</a>'
def test():
   result = get_question_after(session['last_question'], session['quiz'])
   if result is None or len(result) == 0:
       return redirect(url_for('result'))
   else:
       session['last_question'] = result[0]
       # si hemos enseñado a la base de datos a devolver Row o dict, entonces no debemos escribir result[0] y en su lugar escribimos result['id']
       return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'
def result():
   return "¡eso es todo amigos!"
# Crear un objeto de aplicación web:
app = Flask(__name__) 
app.add_url_rule('/', 'index', index) # crea una regla para la URL '/'
app.add_url_rule('/test', 'test', test) # crea una regla para la URL '/test'
app.add_url_rule('/result', 'result', result) # crea una regla para la URL '/test'
# Establecer la clave de encriptación:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
if __name__ == '__main__':
   # Iniciar el servidor web:
   app.run()
