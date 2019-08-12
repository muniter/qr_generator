from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, SubmitField,  validators


class ScanForm(FlaskForm):
    codigo = IntegerField('Código de Barra', render_kw={'autofocus': True})
    enviar = SubmitField('Comprobar')
