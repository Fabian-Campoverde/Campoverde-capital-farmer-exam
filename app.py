import json
import re
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os
from groq import Groq


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 

load_dotenv()

db = SQLAlchemy(app)

# Configuración del cliente Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

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

# Función de análisis con IA
def analizar_con_ia(descripcion, tipo_servicio):
    prompt = f"""
    Analiza este caso legal: {descripcion}
    Tipo de servicio: {tipo_servicio}

    Evalúa:
    1. Complejidad (Baja/Media/Alta)
    2. Ajuste de precio recomendado (0%, 25%, 50%)
    3. Servicios adicionales necesarios
    4. Genera propuesta profesional para cliente (2 a 3 párrafos)
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            
        )
        content = response.choices[0].message.content
        
        return {
            
            'propuesta_texto': extraer_info_desde_texto(content)
        }

    except Exception as e:
        print("Error con IA:", e)
        return {
            'complejidad': 'Desconocida',
            'ajuste_precio': 0,
            'servicios_adicionales': '',
            'propuesta_texto': 'No se pudo generar propuesta.'
        }

#Delimitar la informacion generado por IA
def extraer_info_desde_texto(texto):
    # 1. Extraer complejidad
    complejidad_match = re.search(r'\*\*Complejidad\*\*:\s*(\w+)', texto)
    complejidad = complejidad_match.group(1) if complejidad_match else "Desconocida"

    # 2. Extraer ajuste de precio
    ajuste_match = re.search(r'Ajuste de precio recomendado\*\*:\s*(\d+)%', texto)
    ajuste = int(ajuste_match.group(1)) if ajuste_match else 0

    # 3. Extraer servicios adicionales
    servicios_match = re.search(r'Servicios adicionales necesarios\*\*:\s*(.*?)\n\n', texto, re.DOTALL)
    servicios_adicionales = servicios_match.group(1).strip().replace("\n", " ") if servicios_match else ""

    # 4. Extraer la propuesta completa (desde "**Propuesta Profesional**" hasta el final)
    propuesta_match = re.search(r'\*\*Propuesta Profesional\*\*\n(.*)', texto, re.DOTALL)
    propuesta = propuesta_match.group(1).strip() if propuesta_match else texto

    return json.dumps({
        "complejidad": complejidad,
        "ajuste": ajuste,
        "servicios_adicionales": servicios_adicionales,
        "propuesta": propuesta
    })

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    form = CotizacionForm()
    if form.validate_on_submit():
        # Precios fijos para cada tipo de servicio
        precios = {
            'Constitución de empresa': 1500,
            'Defensa laboral': 2000,
            'Consultoría tributaria': 800
        }

        tipo = form.tipo_servicio.data
        precio_base = precios[tipo]

        # Analizar la descripción del caso con IA
        datos_ia = analizar_con_ia(form.descripcion.data, tipo)
        
        numero_cotizacion = f"COT-2025-{datetime.utcnow().strftime('%f')}"

        # Crear una nueva cotización
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

        # Retorna json con la cotización generada
        return jsonify({
            'numero': nueva.numero,
            'nombre': nueva.nombre,
            'precio': nueva.precio,
            'fecha': nueva.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'mensaje': 'Cotización generada exitosamente.',
            'propuesta_texto':datos_ia['propuesta_texto']
        })
    return render_template('index.html', form=form)

# Ruta para mostrar el resultado de la cotización
@app.route('/result/<int:cotizacion_id>')
def result(cotizacion_id):
    cotizacion = Cotizacion.query.get_or_404(cotizacion_id)
    # Analizar la descripción del caso con IA
    datos_ia = analizar_con_ia(cotizacion.descripcion, cotizacion.tipo_servicio)
    # Extraer resultado en formato JSON
    datos_ia = json.loads(datos_ia['propuesta_texto'])
    return render_template('result.html', cotizacion=cotizacion, ia=datos_ia)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crear la tabla en la base de datos
    app.run(debug=True)