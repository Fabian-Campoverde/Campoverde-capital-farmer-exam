# 🧾 Sistema de Cotizaciones - Capital & Farmer

Este es un sistema web desarrollado con Flask que permite a usuarios generar cotizaciones legales personalizadas, calculando precios automáticamente y utilizando una IA para analizar el caso y generar propuestas profesionales.

---

## 🚀 Instalación

1. Clona el repositorio:
   git clone https://github.com/Fabian-Campoverde/Campoverde-capital-farmer-exam
   cd tu-repo
Instala las dependencias:
pip install -r requirements.txt
Ejecuta la aplicación:
python app.py
🌐 Uso
Abre tu navegador y accede a: http://localhost:5000

Llena el formulario con:

Nombre

Email

Tipo de servicio

Descripción del caso

Envía el formulario para generar automáticamente:

Una cotización con número, precio y fecha

Un análisis generado por inteligencia artificial que evalúa la complejidad del caso, sugiere ajustes de precio y recomienda servicios adicionales

Se mostrará una página de resultados (result.html) con toda la información, incluyendo la propuesta redactada por IA (Para visualizar los resultados usa http://127.0.0.1:5000/result/id -> cambiar id por el id de la cotización a visualizar)

⚙️ Funcionalidades Implementadas
Generación automática de número de cotización

Cálculo del precio base por tipo de servicio

Análisis del caso con IA (Groq API con modelo LLaMA 3)

Ajuste de precio según complejidad del caso

Recomendaciones personalizadas

Renderizado de resultados en una plantilla HTML

Base de datos SQLite con persistencia de cotizaciones

🧠 API de Inteligencia Artificial Utilizada
Este proyecto utiliza la API de Groq
🔗 https://console.groq.com
Con el modelo LLaMA 3 - 70B para analizar la descripción legal ingresada por el cliente y generar:

Nivel de complejidad del caso (Baja, Media o Alta)

Porcentaje sugerido de ajuste de precio (0%, 25%, 50%)

Servicios adicionales recomendados

Una propuesta profesional redactada para el cliente

📁 Archivos importantes
app.py - Lógica principal del servidor Flask y las rutas

templates/index.html - Formulario de cotización

templates/result.html - Página de resultados con análisis IA

requirements.txt - Dependencias del proyecto

📌 Notas
La base de datos SQLite (database.db) se genera automáticamente en la raíz del proyecto.

Puedes configurar tu API key de Groq directamente en el archivo app.py o usando un .env si implementas python-dotenv.

🧑‍💻 Autor
Fabian Leonardo Campoverde Villanueva
