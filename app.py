from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 

db = SQLAlchemy(app)

#Creación del modelo de Cotización
class Cotizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tipo_servicio = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# Crear Formulario con WTForms
class CotizacionForm(FlaskForm):
    nombre = StringField('Nombre del Cliente: ', validators=[DataRequired()])
    email = StringField('Correo Electrónico: ', validators=[DataRequired(), Email()])
    tipo_servicio = SelectField('Tipo de Servicio: ', choices=[
        ('Constitución de empresa', 'Constitución de empresa'),
        ('Defensa laboral', 'Defensa laboral'),
        ('Consultoría tributaria', 'Consultoría tributaria')
    ], validators=[DataRequired()])
    descripcion = TextAreaField('Descripción del caso: ', validators=[DataRequired()])
    submit = SubmitField('Generar Cotización')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crear la tabla en la base de datos
    app.run(debug=True)