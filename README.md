# Clasificador de Correos Inteligente

Este proyecto es una aplicación web que permite visualizar y clasificar automáticamente correos electrónicos usando modelos de lenguaje entrenados con Transformers. El sistema identifica el **sentimiento**, la **prioridad** y la **categoría** de cada correo recibido, y los presenta en una interfaz web clara e interactiva.

Está diseñado como un proyecto académico que combina ingeniería de software, procesamiento de lenguaje natural (NLP) y consumo seguro de APIs externas (Gmail).


## Arquitectura general

```
┌──────────────────────────────┐
│  Usuario final (navegador)   │
└────────────┬─────────────────┘
             │
             ▼
    Flask + Tailwind (UI)
             │
             ▼
       Lógica del backend
             │
             ▼
   API de Gmail (lectura segura)
             │
             ▼
   Modelos Hugging Face (3 clasificadores)
             │
             ▼
     Resultados interpretables
```

---

## Demostración



---

## Modelos de clasificación

Este proyecto utiliza **tres modelos** entrenados con Transformers y alojados públicamente en Hugging Face. Cada uno de ellos cumple una función específica en la clasificación del correo:

- [`sentiment-model-mailclassifier`](https://huggingface.co/aaronmena02/sentiment-model-mailclassifier): analiza si el contenido es positivo, negativo o neutro.
- [`priority-model-mailclassifier`](https://huggingface.co/aaronmena02/priority-model-mailclassifier): estima si el correo tiene prioridad alta, media o baja.
- [`category-model-mailclassifier`](https://huggingface.co/aaronmena02/category-model-mailclassifier): clasifica el tipo de mensaje (solicitud, comercial, queja, otro).

Todos los modelos están basados en **RoBERTa** y limitados a **130 tokens** de entrada para asegurar compatibilidad y eficiencia.

---

## Cómo ejecutar el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/mail-classifier.git
cd mail-classifier
```

### 2. Crea un entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura las credenciales de Gmail

1. Ve a [Google Cloud Console](https://console.cloud.google.com/).
2. Crea un nuevo proyecto.
3. Habilita la **Gmail API**.
4. Crea credenciales de tipo **OAuth 2.0 (Escritorio)**.
5. Descarga el archivo `credentials.json` y colócalo en la raíz del proyecto.

### 5. Ejecuta la aplicación

```bash
python app.py
```

La primera vez se abrirá una ventana del navegador para autenticar tu cuenta de Gmail. Se guardará un archivo `token.json` para futuros accesos automáticos.

---

## Limitaciones de acceso

Este proyecto **no está verificado ni desplegado en producción**. Por lo tanto:

- Solo puedes usar la app con cuentas registradas como testers en Google Cloud Console.
- Si otra persona intenta autenticarse, verá un error `403: access_denied`.

Esto es una medida deliberada ya que se trata de un **proyecto académico de demostración** y no un producto de uso público.

---

## Tecnologías utilizadas

- **Python 3.11+**
- **Flask** como framework web
- **Hugging Face Transformers** para modelos de clasificación
- **Torch** para inferencia de modelos
- **Gmail API + OAuth 2.0** para acceso a correos
- **Tailwind CSS** para diseño de la interfaz
- **JavaScript** para interactividad en el frontend

---

## Aprendizajes y objetivos

Este proyecto fue desarrollado como parte de una formación especializada en Inteligencia Artificial aplicada. Los principales objetivos de aprendizaje fueron:

- Integrar modelos de lenguaje en aplicaciones web funcionales.
- Gestionar autenticación segura con APIs externas como Gmail.
- Diseñar una arquitectura modular entre backend, frontend y lógica de modelos.
- Aplicar principios de eficiencia en el uso de modelos Transformer para entornos reales.