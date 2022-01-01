import manage_sheets
import os

def main(): 
    hoja_calculo = manage_sheets.GoogleSheet()
    print(hoja_calculo.return_single_value(hoja="Clientes", range_values =f"A1"))
    print("----Salta Services----")
    print("Usa commando \"help\" para ver las funciones del programa.")

    choose = ""
    print("\nEscoge una acción de las siguientes: ")
    print('''\t1.- Lista de productos. 
        2.- Valor total de los productos. 
        3.- Cambiar Cantidad de producto. 
        4.- Agregar venta.  ''')
    while choose != "quit": 
        
        choose = input(">").lower()

        if choose == "1": 
            lista_productos = hoja_calculo.return_column(column = "B", hoja="Stock")
        
            for i in range(len(lista_productos)): 
                print(f"\t{i+1}.-{str(lista_productos[i][0])}")

        elif choose == "2": 
            valor_total = hoja_calculo.return_single_value(hoja="Stock", range_values="E29")
            print("------------")
            print(f"El precio total en productos es de: {valor_total[0][0]}")

        elif choose == "3": 
            print("------------")
            tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B2:B28")
            for i in range(27): 
                print(f"0{i+1} - {tabla_modelos[i][0]}")
            modelo = input("Código: ")
            if modelo == "01": 
                tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B2:B6")
                row = 2
            elif modelo =="02": 
                tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B8:B9")
                row = 8
            elif modelo =="03": 
                tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B10:B16")
                row = 10
            elif modelo == "04": 
                tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B17:B20")
                row = 17
            elif modelo == "05": 
                tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B21:B26")
                row = 21
            elif modelo =="06": 
                tabla_modelos = hoja_calculo.return_range_values(hoja="Stock", range_values="B27:B28")
                row = 27

            for i in range(len(tabla_modelos)): 
                print(f"{i+1}.- {tabla_modelos[i][0]}")

            modelo = input("Número: ")
            cantidad = int(input("Nueva cantidad de ejemplares: "))
            hoja_calculo.set_single_value(hoja="Stock", range_values=f"C{row+int(modelo)-1}", data=cantidad)
    
        elif choose == "4": 
            nombre = ""
            print("------------")
            
            print("Nueva venta: ")
            entrada = input("Cliente previo?(s/n): ").lower()
            if entrada.__contains__("s"): 
                lista_clientes = hoja_calculo.return_column(column = "A", hoja="Clientes")
        
                for i in range(1, len(lista_clientes)):
                    if lista_clientes[i][0] != "": print(f"\t{i}.-{str(lista_clientes[i][0])}")
                
                numeroCliente = int(input("Numero del cliente: "))
                nombre = hoja_calculo.return_single_value(hoja="Clientes", range_values=f"A{numeroCliente-1}")
            
            else: 
                counter = 1
                print("\t--Añadir nuevo cliente--")
                nombre = str(input("Nombre completo: "))
                entrada = input("Confirmar(s/n): ").lower()
                if entrada.__contains__("s"): 
                    while hoja_calculo.return_single_value(hoja="Clientes", range_values =f"A{counter}") != "": counter+=1
                    hoja_calculo.set_single_value(data =nombre, range_values=f"A{counter}",hoja="Clientes")

                    entrada = input("Número Celular: ")
                    hoja_calculo.set_single_value(data =entrada, range_values=f"B{counter}",hoja="Clientes")

                    email = str(input("Dirección de e-mail: "))
                    hoja_calculo.set_single_value(data =email, range_values=f"C{counter}",hoja="Clientes")
                else: 
                    print("\n\t---Reiniciando Menú---")
                    continue

            print("\tProductos de la venta: ")
            print("Escriba listo para dejar de añadir productos.")
            producto = ""
            counter = 1
            while hoja_calculo.return_single_value(hoja = "Ventas", range_values=f"C{counter}") != "": counter+=1

            hoja_calculo.set_single_value(data = nombre, range_values=f"B{counter}", hoja= "Ventas")

            while producto != "listo": 
                producto = input("Producto: ")
                hoja_calculo.set_single_value(producto, range_values=f"D{counter}", hoja="Ventas")
            
            print("\n---Venta Registrada---\n")          

        elif choose == "help": 
            print("------------\n\n")
            print("\nFunciones: ")
            print('''\t    1.- Lista de productos. 
            2.- Valor total de los productos. 
            3.- Cambiar Cantidad de producto. 
            4.- Agregar venta.\n  
            - ingresa \"quit\" para salir -''')

        elif choose == "clear": os.system("clear")
        
        elif choose == "quit": 
            continue
    
        else: 
            print("\nAy, ocurrió un problema, no te entendí. \nSeleccione una acción: ")
    
    print("\n\n----Salta Services Off----")
    print("Aplication ended...")


if __name__ == "__main__": 
    main()