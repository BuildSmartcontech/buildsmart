# utils/web_generator.py - Generador de páginas web automáticas

import os
import datetime
import re

class WebGenerator:
    def __init__(self):
        self.carpeta_base = "websites"
        
    def crear_carpeta_negocio(self, negocio_id, negocio_nombre):
        """Crear carpeta para el sitio web del negocio"""
        carpeta = f"{self.carpeta_base}/{negocio_id}"
        os.makedirs(carpeta, exist_ok=True)
        return carpeta
    
    def generar_landing_page(self, negocio_id, negocio_nombre, descripcion, icono):
        """Generar una landing page completa para el negocio"""
        carpeta = self.crear_carpeta_negocio(negocio_id, negocio_nombre)
        
        # Limpiar nombre para URL
        nombre_limpio = re.sub(r'[^a-zA-Z0-9]', '-', negocio_nombre.lower())
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{negocio_nombre}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        .container {{
            max-width: 800px;
            text-align: center;
            background: rgba(255,255,255,0.05);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }}
        .icon {{
            font-size: 5rem;
            margin-bottom: 1rem;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        p {{
            font-size: 1.2rem;
            color: #aaa;
            margin-bottom: 2rem;
            line-height: 1.6;
        }}
        .btn {{
            display: inline-block;
            padding: 1rem 2.5rem;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: transform 0.3s;
        }}
        .btn:hover {{
            transform: scale(1.05);
        }}
        .footer {{
            margin-top: 2rem;
            color: #555;
            font-size: 0.8rem;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #00d2ff;
        }}
        .stat-label {{
            color: #888;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">{icono}</div>
        <h1>{negocio_nombre}</h1>
        <p>{descripcion}</p>
        <div class="stats">
            <div class="stat">
                <div class="stat-number">0</div>
                <div class="stat-label">Proyectos</div>
            </div>
            <div class="stat">
                <div class="stat-number">0</div>
                <div class="stat-label">Clientes</div>
            </div>
            <div class="stat">
                <div class="stat-number">$0</div>
                <div class="stat-label">Ingresos</div>
            </div>
        </div>
        <a href="#" class="btn">🚀 Comenzar</a>
        <div class="footer">
            © {datetime.datetime.now().year} {negocio_nombre} - Creado con BuildSmart Holdings
        </div>
    </div>
</body>
</html>"""
        
        # Guardar archivo
        ruta_html = f"{carpeta}/index.html"
        with open(ruta_html, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return f"websites/{negocio_id}/index.html"
    
    def generar_blog_post(self, negocio_id, titulo, contenido):
        """Generar un post de blog"""
        carpeta = f"{self.carpeta_base}/{negocio_id}/blog"
        os.makedirs(carpeta, exist_ok=True)
        
        nombre_archivo = re.sub(r'[^a-zA-Z0-9]', '-', titulo.lower())
        ruta = f"{carpeta}/{nombre_archivo}.html"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{titulo}</title>
</head>
<body>
    <article>
        <h1>{titulo}</h1>
        <p>{contenido}</p>
    </article>
</body>
</html>"""
        
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return ruta

web_generator = WebGenerator()