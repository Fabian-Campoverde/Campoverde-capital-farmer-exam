from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 

db = SQLAlchemy(app)

#Creación del modelo de Cotización
class Cotizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tipo_servicio = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
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

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    form = CotizacionForm()
    if form.validate_on_submit():
        precios = {
            'Constitución de empresa': 1500,
            'Defensa laboral': 2000,
            'Consultoría tributaria': 800
        }

        numero_cotizacion = f"COT-2025-{datetime.utcnow().strftime('%f')}"

        nueva = Cotizacion(
            numero=numero_cotizacion,
            nombre=form.nombre.data,
            email=form.email.data,
            tipo_servicio=form.tipo_servicio.data,
            descripcion=form.descripcion.data,
            precio=precios[form.tipo_servicio.data]
        )

        db.session.add(nueva)
        db.session.commit()

        return jsonify({
            'numero': nueva.numero,
            'nombre': nueva.nombre,
            'precio': nueva.precio,
            'fecha': nueva.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'mensaje': 'Cotización generada exitosamente.'
        })
    return render_template('index.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crear la tabla en la base de datos
    app.run(debug=True)