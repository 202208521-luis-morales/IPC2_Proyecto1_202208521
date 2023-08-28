from classes.LinkedList import LinkedList
from classes.ManageXMLs import ManageXMLs

xmlData = LinkedList()

while(True):
  print("USAC - Segundo Semestre 2023")
  print("Proyecto 1 - IPC2")
  print("Luis Morales - 202208521")
  print("----------------------------")
  print("MENU")
  print("1. Cargar archivo")
  print("2. Procesar archivo")
  print("3. Escribir archivo salida")
  print("4. Mostrar datos del estudiante")
  print("5. Generar gráfica")
  print("6. Salir")
  option = input("Ingrese el número de opción: ")

  if(option == "1"):
    print("\n")
    print("# Ha elegido '1. Cargar archivo'")
    print("\n")
    ruta_archivo = input("Ingrese la ruta del archivo: ")
    new_xmlData = ManageXMLs(ruta_archivo)

    resultado_validacion = new_xmlData.check_file(ruta_archivo)

    if isinstance(resultado_validacion, bool):
        xmlData.append(new_xmlData)
        print("\n")
        print("# Archivo subido con éxito")
        print("\n")
    else:
        print("\n")
        print(resultado_validacion)
        print("\n")

  elif(option == "2"):
    print("\n")
    print("# Ha elegido '2. Procesar el Archivo'")
    print("\n")
    if not xmlData.is_empty():
      xmlData.print_as_list()
      print("\n")
      position_by_user = input("Elija el número del archivo que quiere procesar: ")
      if xmlData.get_elem_by_position(position_by_user) != None:
        xmlData.get_elem_by_position(position_by_user).data.process_file()
        print("\n")
        print("# Archivo procesado con éxito")
        print("\n")
      else:
        print("\n")
        print("# ERROR: El número de archivo es incorrecto")
        print("\n")
    else:
      print("\n")
      print("# ERROR: Primero debes agregar algún archivo")
    
    print("\n")
    # Procesando
  elif(option == "3"):
    print("\n")
    print("# Ha elegido '3. Escribir Archivo de salida'")
    print("\n")
    xmlData.print_as_list()
    print("\n")
    position_by_user = input("Elija el número del archivo que quiere procesar: ")
    output_route = input("Ingrese la ruta donde imprimirá el archivo: ")

    if xmlData.get_elem_by_position(position_by_user) != None:
      xmlData.get_elem_by_position(position_by_user).data.generate_output_xml(output_route)
    else:
      print("\n")
      print("# ERROR: El número de archivo es incorrecto")
      print("\n")

    print("\n")
    print("# Archivo generado correctamente'")
    print("\n")
  elif(option == "4"):
    print("\n")
    print("# Ha elegido '4. Mostrar datos del estudiante'")
    print("\n")
    print("+-----------------------------------+")
    print("| Luis Rodrigo Morales Florián      |")
    print("| 202208521                         |")
    print("| IPC2 Sección B                    |")
    print("| Ingeniería en Ciencias y Sistemas |")
    print("+-----------------------------------+")
    print("\n")
  elif(option == "5"):
    print("\n")
    print("# Ha elegido '5. Generar gráfica'")
    print("\n")
    # Generar gráfica
  elif(option == "6"):
    print("\n")
    print("# ADIOS'")
    break
    # Generar gráfica