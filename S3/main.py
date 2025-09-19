import os
import subprocess
import boto3
from dotenv import load_dotenv

# 1) Cargar variables desde .env ubicado dentro de ./S3
ENV_PATH = os.path.abspath("./conferencia_archivos_2025/S3/.env")
loaded = load_dotenv(dotenv_path=ENV_PATH)

# 2) Obtener credenciales desde variables de entorno
aws_access_key_id = os.getenv("ACCESS_ID")
aws_secret_access_key = os.getenv("SECRET_ID")

# Verificación útil al depurar (puedes borrar estos prints luego)
print("dotenv loaded?", loaded, "path:", ENV_PATH)
print("ACCESS_ID cargado?", bool(aws_access_key_id))
print("SECRET_ID cargado?", bool(aws_secret_access_key))

if not aws_access_key_id or not aws_secret_access_key:
    raise RuntimeError("Faltan ACCESS_ID o SECRET_ID en variables de entorno/.env")

# 3) Rutas absolutas de archivos
archivo_dot = os.path.abspath("./conferencia_archivos_2025/S3/reporte.dot")
archivo_jpg = os.path.abspath("./conferencia_archivos_2025/S3/reporte.jpg")
bucket_name = "ejemplo-clase-mia-2025"

# 4) Generar la imagen con Graphviz (dot)
subprocess.run(["dot", "-Tjpg", archivo_dot, "-o", archivo_jpg], check=True)
print(f"Se ha creado el archivo {archivo_jpg}")

# 5) Crear cliente S3 con las credenciales cargadas
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# 6) Subir el archivo al bucket usando solo el nombre como key
key = os.path.basename(archivo_jpg)  # "reporte.jpg"
s3.upload_file(archivo_jpg, bucket_name, key)
print(f"Se ha subido {key} a {bucket_name}")