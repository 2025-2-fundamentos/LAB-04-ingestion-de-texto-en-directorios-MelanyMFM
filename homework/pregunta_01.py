# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import os
import zipfile
import pandas as pd

def descomprimir_archivo(zip_path, destino):
    """Descomprime un archivo ZIP en la carpeta destino."""
    if not os.path.exists(destino):
        os.makedirs(destino)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destino)

def obtener_ruta_datos(base_path):
    """Verifica y obtiene la ruta correcta de la carpeta de datos extraídos."""
    expected_path = os.path.join(base_path, "train")
    if os.path.isdir(expected_path):
        return base_path
    subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if len(subdirs) == 1:
        return os.path.join(base_path, subdirs[0])
    raise FileNotFoundError("No se encontró la carpeta 'train' en la estructura extraída.")

def procesar_dataset(dataset_path, output_file):
    """Procesa un conjunto de datos y lo guarda en un archivo CSV."""
    registros = []
    for sentiment in ["negative", "positive", "neutral"]:
        sentiment_path = os.path.join(dataset_path, sentiment)
        if not os.path.isdir(sentiment_path):
            raise FileNotFoundError(f"No se encontró la carpeta esperada: {sentiment_path}")
        for filename in sorted(os.listdir(sentiment_path)):
            if filename.endswith(".txt"):
                with open(os.path.join(sentiment_path, filename), "r", encoding="utf-8") as file:
                    registros.append([file.read().strip(), sentiment])
    pd.DataFrame(registros, columns=["phrase", "target"]).to_csv(output_file, index=False, encoding="utf-8")
    print(f"Archivo guardado: {output_file}")

def generar_archivos_csv():
    """Descomprime el archivo ZIP y genera los archivos CSV de train y test."""
    zip_path = os.path.join("files", "input.zip")
    input_folder = os.path.join("files", "input")
    output_folder = os.path.join("files", "output")
    descomprimir_archivo(zip_path, input_folder)
    data_path = obtener_ruta_datos(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for dataset in ["train", "test"]:
        procesar_dataset(os.path.join(data_path, dataset), os.path.join(output_folder, f"{dataset}_dataset.csv"))

def pregunta_01():
    generar_archivos_csv()