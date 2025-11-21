import os
import pydicom
import pandas as pd
import numpy as np


class ProcesadorDICOM:

    def __init__(self):
        self.dataframe = pd.DataFrame()

    # --------------------- 1. Cargar archivos DICOM ---------------------
    def cargar_dicoms(self, carpeta):
        """
        Escanea la carpeta, valida archivos DICOM y los carga.
        Devuelve una lista de datasets de pydicom.
        """
        dicoms = []

        for archivo in os.listdir(carpeta):
            ruta = os.path.join(carpeta, archivo)

            if not os.path.isfile(ruta):
                continue

            try:
                ds = pydicom.dcmread(ruta)
                dicoms.append(ds)
            except:
                # No es archivo DICOM válido
                continue

        print(f"Se cargaron {len(dicoms)} archivos DICOM.")
        return dicoms

    # --------------------- 2. Extraer metadatos ---------------------
    def extraer_metadatos(self, lista_dicoms):
        """
        Extrae metadatos requeridos por el taller y los guarda en un DataFrame.
        """

        registros = []

        for ds in lista_dicoms:

            # Se usa getattr() para evitar errores cuando un tag no existe
            paciente_id = getattr(ds, "PatientID", "No disponible")
            paciente_nombre = getattr(ds, "PatientName", "No disponible")
            estudio_uid = getattr(ds, "StudyInstanceUID", "No disponible")
            descripcion = getattr(ds, "StudyDescription", "No disponible")
            fecha = getattr(ds, "StudyDate", "No disponible")
            modalidad = getattr(ds, "Modality", "No disponible")
            filas = getattr(ds, "Rows", "No disponible")
            columnas = getattr(ds, "Columns", "No disponible")

            # Crear un diccionario con todos los datos
            registros.append({
                "PacienteID": paciente_id,
                "PacienteNombre": str(paciente_nombre),
                "EstudioUID": estudio_uid,
                "Descripcion": descripcion,
                "Fecha": fecha,
                "Modalidad": modalidad,
                "Filas": filas,
                "Columnas": columnas,
                "Dataset": ds    # guardamos el objeto para análisis posterior
            })

        self.dataframe = pd.DataFrame(registros)
        print("Metadatos extraídos correctamente.")
        return self.dataframe

    # --------------------- 3. Análisis de imagen ---------------------
    def calcular_intensidad_promedio(self):
        """
        Calcula la intensidad promedio de cada imagen usando pixel_array.
        """

        promedios = []

        for ds in self.dataframe["Dataset"]:
            try:
                matriz = ds.pixel_array
                promedio = np.mean(matriz)
            except:
                promedio = np.nan  # por si algún archivo no tiene imagen

            promedios.append(promedio)

        self.dataframe["IntensidadPromedio"] = promedios
        print("Cálculo de intensidades completado.")
        return self.dataframe

    # --------------------- 4. Exportar ---------------------
    def guardar_csv(self, nombre="resultados_dicoms.csv"):
        self.dataframe.drop(columns=["Dataset"], inplace=True)
        self.dataframe.to_csv(nombre, index=False)
        print(f"Datos guardados en {nombre}.")
