from flask import Flask, session, request, redirect, url_for
from db_scripts import get_question_after, get_quises
def start_quis(quiz_id):
    '''crea los valores deseados en el diccionario session'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
 
def end_quiz():
    session.clear()
 
def quiz_form():
    '''la función obtiene una lista de cuestionarios de la base de datos y crea un formulario con una lista desplegable'''
    html_beg = '''<html><body><h2>Elija un cuestionario:</h2><form method="post" action="index"><select name="quiz">'''
    frm_submit = '''<p><input type="submit" value="Seleccionar"> </p>'''
 
    html_end = '''</select>''' + frm_submit + '''</form></body></html>'''
    options = ''' '''
    q_list = get_quises()
    for id, name in q_list:
        option_line = ('''<option value="''' +
                        str(id) + '''">''' +
                        str(name) + '''</option>
                      ''')
        options = options + option_line
    return html_beg + options + html_end
       
def index():
    '''Primera página: si vino con una solicitud GET, entonces elegir un cuestionario, 
    si fue POST, entonces recordar el ID del cuestionario y enviarlo a las preguntas'''
    if request.method == 'GET':
        # el cuestionario no está seleccionado, restablecer el id del cuestionario y mostrar el formulario de selección
        start_quis(-1)
        return quiz_form()
    else:
        # ¡se recibieron datos adicionales en la solicitud! Usarlos:
        quest_id = request.form.get('quiz') # número de cuestionario seleccionado
        start_quis(quest_id)
        return redirect(url_for('test'))
 
def test():
    '''devuelve la página de la pregunta'''
    # ¿qué ocurriría si un usuario sin elegir un cuestionario fuera directo a la dirección '/test'? 
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        # todavía hay una versión antigua de la función:
        result = get_question_after(session['last_question'], session['quiz'])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            session['last_question'] = result[0]
            # si hemos enseñado a la base de datos a devolver Row o dict, entonces no debemos escribir result[0] y en su lugar escribimos result['id']
            return '<h1>' + str(session['quiz']) + '<br>' + str(result) + '</h1>'
 
def result():
    end_quiz()
    return "¡eso es todo!"
 
# Crear un objeto de aplicación web:
app = Flask(__name__)  
app.add_url_rule('/', 'index', index) # crea una regla para la URL '/'
app.add_url_rule('/index', 'index', index, methods=['post', 'get']) # regla para '/index'
app.add_url_rule('/test', 'test', test) # crea una regla para la URL '/test'
app.add_url_rule('/result', 'result', result) # crea una regla para la URL '/test'
# Establecer la clave de encriptación:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
 
if __name__ == "__main__":
    # Iniciar el servidor web:
    app.run()
