import os
import xml.etree.ElementTree as ET
from typing import Union
import copy
from classes.LinkedList import LinkedList

class ManageXMLs:
    def __init__(self, ruta: str):
        self.ruta = ruta
        self.processed = False

    def __str__(self) -> str:
        return self.ruta
    
    def check_file(self, ruta: str) -> Union[bool, str]:
        if not os.path.exists(ruta):
            return "# ERROR: El archivo no existe"
        
        extension = os.path.splitext(ruta)[1]
        extension_correcta = ".xml"
        
        if extension != extension_correcta:
            return f"# ERROR: Extensión incorrecta. Debe ser {extension_correcta}"
        
        return True
    
    def process_file(self):
        # Genera los datos de entrada
        tree = ET.parse(self.ruta)
        root = tree.getroot()

        for senales_elem in root.findall("senales"):
            for senal_elem in senales_elem.findall("senal"):
                pattern_matrix = None
                rows_pattern_matrix = []
                input_data = {}
                output_data = {}

                input_data["t"] = int(senal_elem.get("t"))
                input_data["a"] = int(senal_elem.get("A"))
                input_data["name"] = senal_elem.get("nombre")

                # Método: generar matriz
                data_matrix = []

                for _ in range(input_data["t"]):
                    row = []
                    for i in range(input_data["a"]):
                        row.append(0)
                    data_matrix.append(row)

                pattern_matrix = copy.deepcopy(data_matrix)

                # Método: llenar matriz con datos del archivo
                for dato_elem in senal_elem.findall("dato"):
                    data_matrix[int(dato_elem.get("t")), int(dato_elem.get("A"))] = dato_elem.text
                    pattern_matrix[int(dato_elem.get("t")), int(dato_elem.get("A"))] = (0 if dato_elem.text == 0 else 1)
                
                input_data["signals_matrix"] = data_matrix

                # Esta lista tiene cada fila de la matriz de patrones en un string convertido, es decir
                # si la primera fila de la matriz se ve así: [1,0,0,1], el dato que se guardará será
                # "1001"
                rows_pattern_matrix = [''.join(map(str,elem)).strip() for elem in pattern_matrix]

                indices_por_elemento = {}

                for idx, elemento in enumerate(rows_pattern_matrix):
                    if elemento in indices_por_elemento:
                        indices_por_elemento[elemento].append(idx)
                    else:
                        indices_por_elemento[elemento] = [idx]

                # Esta lista guarda el índice por tiempo, es decir tiempo(indice) de las filas repetidas de la matriz de patrones
                # Ejemplo: si rows_pattern_matrix tiene la siguiente estructura: ["101","001","101"], filas_repetidas se verá
                # así: [[0,2],[1]]
                filas_repetidas = list(indices_por_elemento.values())
        
                # Generar datos de archivo de salida
                output_data["a"] = input_data["a"]
                output_matrix = []

                for j in filas_repetidas:
                    row = []

                    for amp in range(input_data["a"]):
                        row[0] = j

                        sum_columns_data = 0

                        for k in j:
                            sum_columns_data += input_data["signals_matrix"][k][amp]

                        row.append(sum_columns_data)

                    output_matrix.append(row)
                
                output_data["reduced_signals_matrix"] = output_matrix

