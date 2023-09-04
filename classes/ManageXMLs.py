import os
import xml.etree.ElementTree as ET
import copy
import graphviz
import datetime
from typing import Union
from classes.LinkedList import LinkedList

class ManageXMLs:
    def __init__(self, ruta: str):
        self.ruta = ruta
        self.processed = False
        self.signals_data = LinkedList()

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

        if self.processed is False:
            tree = ET.parse(self.ruta)
            root = tree.getroot()

            for senal_elem in root.findall("senal"):
                pattern_matrix = None
                rows_pattern_matrix = []
                input_data = {}
                output_data = {}

                input_data["t"] = int(senal_elem.get("t"))
                input_data["a"] = output_data["a"] = int(senal_elem.get("A"))
                input_data["name"] = output_data["name"] = senal_elem.get("nombre")

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
                    data_matrix[int(dato_elem.get("t"))-1][int(dato_elem.get("A"))-1] = int(dato_elem.text)
                    pattern_matrix[int(dato_elem.get("t"))-1][int(dato_elem.get("A"))-1] = (0 if int(dato_elem.text) == 0 else 1)
                
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
                output_matrix = []

                for j in filas_repetidas:
                    row = {"repeated_rows": j, "times": []}

                    for amp in range(input_data["a"]):
                        sum_columns_data = 0

                        for k in j:
                            sum_columns_data += input_data["signals_matrix"][k][amp]

                        row["times"].append(sum_columns_data)

                    output_matrix.append(row)
                
                output_data["reduced_signals_matrix"] = output_matrix

                self.signals_data.append({"input_data": input_data, "pattern_matrix": pattern_matrix ,"output_data": output_data})
            
            self.processed = True
        else:
            return False

    def generate_output_xml(self, route_to_output: str):
        root = ET.Element("senalesReducidas")
        
        sign_counter = 1
        while self.signals_data.get_elem_by_position(sign_counter) != None:
            sig_dat = self.signals_data.get_elem_by_position(sign_counter)
            outd = sig_dat.data["output_data"]
            senal = ET.SubElement(root, "senal", nombre=outd["name"], A=str(outd["a"]))

            group_counter = 1
            for rdm in outd["reduced_signals_matrix"]:
                group = ET.SubElement(senal, "grupo", g=str(group_counter))
                times = ET.SubElement(group, "tiempos")
                times.text = ','.join(map(str, [(rd+1) for rd in rdm['repeated_rows']]))
                data_group = ET.SubElement(group, "datosGrupo")

                data_counter = 1
                for tm in rdm["times"]:
                    data = ET.SubElement(data_group, "dato", A=str(data_counter))
                    data.text = str(tm)
                    data_counter += 1

                group_counter += 1
            
            sign_counter += 1

        tree = ET.ElementTree(root)
        tree.write(route_to_output, xml_declaration=True, encoding="utf-8")

    def generate_graphs(self):
        self.print_saved_data()
        num_signal = input("Elige el número de señal del que quieres generar gráfica: ")
        alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

        # Método: generar primera gráfica
        dot1 = graphviz.Digraph()
        
        dot1.node("A1", self.signals_data.get_elem_by_position(num_signal).data["input_data"]["name"])
        dot1.node("B1", "t="+str(self.signals_data.get_elem_by_position(num_signal).data["input_data"]["t"]))
        dot1.node("B2", "A="+str(self.signals_data.get_elem_by_position(num_signal).data["input_data"]["a"]))
        dot1.edges([("A1","B1"),("A1","B2")])

        for i in range(self.signals_data.get_elem_by_position(num_signal).data["input_data"]["t"]):
            for j in range(self.signals_data.get_elem_by_position(num_signal).data["input_data"]["a"]):
                node_name = alphabet[i+1] + str(j+3)
                dot1.node(node_name, str(self.signals_data.get_elem_by_position(num_signal).data["input_data"]["signals_matrix"][i][j]))
                
                prev_node_name = alphabet[i] + "1" if i == 0 else alphabet[i] + str(j+3)
                dot1.edge(prev_node_name,node_name)

        new_name = "grafica_1_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dot1.render(new_name, view=True)

        print(f"> Gráfica {new_name} generada con éxito")

        # Método: generar segunda gráfica
        dot2 = graphviz.Digraph()
        
        dot2.node("A1", self.signals_data.get_elem_by_position(num_signal).data["output_data"]["name"])
        dot2.node("B1", "A=" + str(self.signals_data.get_elem_by_position(num_signal).data["output_data"]["a"]))
        dot2.edge("A1","B1")

        alphabet_counter = 0
        for i in self.signals_data.get_elem_by_position(num_signal).data["output_data"]["reduced_signals_matrix"]:
            j_counter = 0

            for j in i["times"]:
                # Agrega los datos del grupo
                if j_counter == 0:
                    node_name = alphabet[alphabet_counter + 1] + str(j_counter + 2)
                    dot2.node(node_name, f"g={alphabet_counter + 1} (t = {','.join(str(row + 1) for row in i['repeated_rows'])})")
                    prev_node_name = alphabet[alphabet_counter] + "1" if alphabet_counter == 0 else alphabet[alphabet_counter] + str(j_counter + 2)
                    dot2.edge(prev_node_name, node_name)
                
                node_name = alphabet[alphabet_counter + 1] + str(j_counter + 3)
                dot2.node(node_name, str(j))
                
                prev_node_name = alphabet[alphabet_counter] + "1" if alphabet_counter == 0 else alphabet[alphabet_counter] + str(j_counter + 3)
                dot2.edge(prev_node_name, node_name)

                j_counter += 1
            
            alphabet_counter += 1

        new_name = "grafica_2_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dot2.render(new_name, view=True)

        print(f"> Gráfica {new_name} generada con éxito")    

    def print_saved_data(self):
        print(self.signals_data.print_as_list())