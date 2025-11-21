from procesador_dicom import ProcesadorDICOM

procesador = ProcesadorDICOM()

# 1. Cargar dicoms
carpeta = input("Ingrese la ruta de la carpeta con archivos DICOM: ")
dicoms = procesador.cargar_dicoms(carpeta)

# 2. Extraer metadatos
df = procesador.extraer_metadatos(dicoms)
print(df)

# 3. Calcular intensidad promedio
df = procesador.calcular_intensidad_promedio()
print(df)

# 4. Guardar resultados
procesador.guardar_csv()
