from manage_sheets import alph, GoogleSheet
from os import system
from term_avanzada import coloredPrint, tcolor, getShSize
from time import ctime, time


# In this proyect the following standarization would be followed: 
#       Objects   = PascalCase
#       Functions = camelCase
#       Variables = snake_case

# And also, please check the use of the keys.json file

# Creation of the Object from the class GoogleSheets:
HojaCalculo = GoogleSheet()

# Bash specific routine to get the terminal size, and OS specifications
term_size = getShSize()[1]
clear_message = "clear"

# Action of the user, made global to be appliable in every sub-menu
choice = ""

# Functionality functions
def errorMessage(): 
    system(clear_message)
    coloredPrint("- Error - ".center, tcolor.FAIL)
    choice = input("Volver al menu (ok): ")


def contained(str, substr): 
    if substr in str: return True
    else: return False


def findValue(value="Malik", hoja="Stock"): 
    range_values = HojaCalculo.findRangeValues(hoja)
    values = HojaCalculo.returnRangeValues(hoja, f"A1:{range_values}")
    for row in range(len(values)):
        for column in range(len(values[0])):
            if values[row][column].find(value)>-1:
                return f"{hoja}!{alph[column]}{row+1}"
    return None


def filterValue():
    names = HojaCalculo.returnColumn("Stock", "B2:B150")
    aux_names = names
        
    while True: 
        coloredPrint("\nIngrese palabra clave o nombre del producto. ", tcolor.CYAN)
        choice = input(": ")
        
        aux_names = list(filter(lambda name: name.__contains__(choice), aux_names))
        
        if len(aux_names) == 0:
            coloredPrint("- No hubo resultados -".center(term_size), tcolor.FAIL)
            aux_names = names
        
        elif len(aux_names) == 1: 
            return aux_names[0]
        
        else: 
            coloredPrint("\nSe redujo la lista a los siguientes elementos:", tcolor.GREEN)
            for name in aux_names: 
                coloredPrint("\t> "+name, tcolor.BOLD)


def filterProcess():

    models = HojaCalculo.returnColumn("Production", "A2:A150")
    quantity = HojaCalculo.returnColumn("Production", "B2:B150")
    due = HojaCalculo.returnColumn("Production", "O2:O150")
 
    for i in range(len(models)): 
        coloredPrint(f"{i+1} - {models[i]}  {quantity[i]}  {due[i]}", tcolor.BOLD)
        
    num = int(input("\nNúmero de proceso a actualizar: "))+1
    
    return [num, models[num-2]]

#Modular functions - Actual actions for the user
def editStock(): 
    try: 
        system(clear_message)
        coloredPrint("-Edición del Stock-".center(term_size), tcolor.REVERSE)
        
        names = HojaCalculo.returnColumn("Stock", "B2:B150")
        codes = HojaCalculo.returnColumn("Stock")
        new_quantity = 0
    
        
        index = names.index(filterValue()) 
        system(clear_message)
                   
        coloredPrint("El nuevo producto es: ", tcolor.BLUE)
        coloredPrint("Código:          " + codes[index], tcolor.PURPLE)
        coloredPrint("Nombre:          " + names[index], tcolor.PURPLE)
        coloredPrint("Cantidad Actual: " + HojaCalculo.returnValue("Stock", f"C{index+2}"), tcolor.PURPLE)
        new_quantity = int(input("Nueva cantidad:  "))
        
        choice = input("Confirmar (s/n): ").lower()
        if choice.__contains__("s"): 
            HojaCalculo.setSingleValue(new_quantity, f"C{index+2}", "Stock")
            coloredPrint("- Operación Exitosa - ".center(term_size), tcolor.GREEN)
            choice = input("Volver al menu (ok): ")
            
        else: 
            coloredPrint("- Operación Cancelada - ".center(term_size), tcolor.GREY)
            choice = input("Volver al menu (ok): ")
    
    except: 
        errorMessage()


def totalValues(): 
    try: 
        range_y = HojaCalculo.findY()
        range_x = alph.find(HojaCalculo.findX())
        
        values = HojaCalculo.returnRow("Stock", f"{alph[range_x-1]}{range_y+2}:Z{range_y+2}")
        
        system(clear_message)
        coloredPrint("- Valores de equilibrio de la compañía - ".center(term_size), tcolor.REVERSE)
        coloredPrint("\nCosto total del stock: "+values[0], tcolor.CYAN)
        coloredPrint("Precio total del stock: "+values[1], tcolor.CYAN)
        
        choice = input("Volver al menu (ok): ")
    except: 
        errorMessage()

    
def updateProcess(): 
    try:
        system(clear_message)
        coloredPrint("- Actualizar Proceso -".center(term_size), tcolor.REVERSE)
        
        data = filterProcess()
        
        progress = int(input("Progreso Actual (1-10): "))
        
        if progress == 10: 
            index = HojaCalculo.returnColumn("Stock", "B2:B150").index(data[1])
            quantity = int(HojaCalculo.returnValue("Production", f"B{data[0]}"))
            previous_q = int(HojaCalculo.returnValue("Stock", f"C{index}"))
            
            coloredPrint("La nueva cantidad de "+data[1]+" es "+str(quantity+previous_q), tcolor.CYAN)
            choice = input("Confirmar (s/n): ").lower()
            if choice.__contains__("s"):
                HojaCalculo.setSingleValue(quantity+previous_q, f"C{index}", "Stock")
                HojaCalculo.deleteRow(data[0], "Production")
                HojaCalculo.moveRangeValues("Production", f"A{data[0]+1}:O150", 0, -1)
                coloredPrint("-Operación Exitosa-".center(term_size), tcolor.GREEN)
                
            else: 
                coloredPrint("-Operación Cancelada-".center(term_size), tcolor.FAIL)
        else: 
            choice = input("Confirmar (s/n): ").lower()
            if choice.__contains__("s"):
                graph = ["#" for i in range(progress)] + ["" for i in range(10-progress)]
                HojaCalculo.setRangeValues([graph], "Production", f"D{data[0]}:M{data[0]}")
                HojaCalculo.setSingleValue(str(progress*10)+"%", f"N{data[0]}", "Production")
                coloredPrint("-Operación exitosa-".center(term_size), tcolor.GREEN)
                
            else: coloredPrint("-Operación cancelada-".center(term_size), tcolor.FAIL)
            
        choice = input("Volver al menu (ok): ")
    
    except: 
        errorMessage()


def newProcess(): 
    try:
        system(clear_message)
        coloredPrint("-Nueva Producción-".center(term_size)+"\n", tcolor.REVERSE)
        
        name = filterValue()
        system(clear_message)
        coloredPrint("Nombre: "+name, tcolor.CYAN)
        quantity = input("Número de productos a producir: ")
        date = ctime()
        due = ctime(time() + int(input("Número de días para realizar la producción: "))*86400)
        progress = input("Progreso porcentual(1-10): ")
        
        date_0 = date[:11] + date[20:]
        date_1 = due[:11] + due[20:]
        
        coloredPrint("El nuevo proceso de producción es entonces: ", tcolor.CYAN)
        coloredPrint("Modelo:                 "+name, tcolor.CYAN)
        coloredPrint("Cantidad:               "+quantity, tcolor.CYAN)
        coloredPrint("Para finalizar:         "+date_1, tcolor.CYAN)
        coloredPrint("Con progreso actual de: "+str(int(progress)*10)+"%", tcolor.CYAN )
        choice = input("Confirmar (s/n): ").lower()
        
        graph = ["#" for i in range(int(progress))] + ["" for i in range(10-int(progress))]
        data = [name, quantity, date_0, str(int(progress)*10)+"%", date_1]
        
        if choice.__contains__("s"): 
            y = HojaCalculo.findY("Production") + 1
            HojaCalculo.setRangeValues([data[:3]], "Production", f"A{y}:C{y}")
            HojaCalculo.setRangeValues([graph], "Production", f"D{y}:M{y}")
            HojaCalculo.setRangeValues([data[3:]], "Production", f"N{y}:O{y}")
            coloredPrint("-Operación Exitosa-".center(term_size), tcolor.GREEN)
            
        else: 
            coloredPrint("-Operación Cancelada-".center(term_size), tcolor.FAIL)
            
        choice = input("Volver al menu (ok): ")
        
    except: 
        errorMessage()
    
    
def delProcess():
    try:
        system(clear_message)
        coloredPrint("- Eliminar proceso -".center(term_size), tcolor.REVERSE)
        
        data = filterProcess()
        process = HojaCalculo.returnRow("Production", f"A{data[0]}:Z{data[0]}")[:3]
        
        coloredPrint("Se eliminará el proceso: ", tcolor.BLUE)
        coloredPrint(" | ".join(process), tcolor.BOLD)
        choice = input("Confirmar (s/n): ").lower()
        if choice.__contains__("s"): 
            HojaCalculo.deleteRow(data[0], "Production")
            HojaCalculo.moveRangeValues("Production", f"A{data[0]+1}:O150", 0, -1)
            coloredPrint("- Operación Exitosa -".center(term_size), tcolor.GREEN)
        else: 
            coloredPrint("- Operación Cancelada -".center(term_size), tcolor.FAIL)
        
        choice = input("Volver al menu (ok): ")
        
    except:
        errorMessage()


def newSale(): 
    system(clear_message)
    coloredPrint("- Nueva Venta -".center(term_size), tcolor.REVERSE)
    coloredPrint("\nCliente: ", tcolor.CYAN)
    
    choice = input("\nNuevo o Preexistente (n/p): ").lower()
    
    client = ""
    models = []
    ids = []
    prices = []
    quantities = []
    
    # Selection of the Client
    if choice.__contains__("n"): 
        addClient()
        clients = HojaCalculo.returnColumn("Clientes", "A2:A150")
        client = clients[len(clients)-1]
        
    elif choice.__contains__("p"): 
        clients = HojaCalculo.returnColumn("Clientes", "A2:A150")
        for i in range(len(clients)): 
            coloredPrint(f"{i+1} - {clients[i]}", tcolor.BOLD)
        num = int(input("\nNúmero del Cliente: "))
        client = clients[num-1]
     
    # Creation of list of products   
    while True: 
        model = filterValue()
        ind = HojaCalculo.returnColumn("Stock", "B2:B150").index(model)
        coloredPrint("\nProducto seleccionado "+ model, tcolor.CYAN)
        quantity = int(input("\nCantidad de productos: "))
        choice = input("Confirmar (s/n): ")
        if choice.__contains__("s"): 
            models.append(model)
            ids.append(HojaCalculo.returnValue("Stock", f"A{ind+1}"))
            prices.append(HojaCalculo.returnValue("Stock", f"E{ind+1}"))
            quantities.append(quantity)
            
        else: coloredPrint("- Producto Cancelado -".center(term_size), tcolor.FAIL)
        
        choice = input("¿Agregar más productos? (s/n): ").lower()
        if choice.__contains__("s"): continue
        else: break
    
    array = []
    for i in range(len(models)): 
        array.append([ids[i], models[i], prices[i], quantities[i]])
    
    #Final Date
    due = ctime(time() + int(input("Número de días para la entrega: "))*86400)
    date = due[:11] + due[20:]
    
    #Final Confirmation
    system(clear_message)
    coloredPrint("Se tienen los siguientes datos: ", tcolor.BOLD)
    coloredPrint("Cliente: "+ client, tcolor.CYAN)
    coloredPrint("Fecha de entrega: "+date, tcolor.CYAN)
    coloredPrint("Lista de productos y cantidades: ", tcolor.BLUE)
    for i in range(len(array)): 
        coloredPrint("\tProducto: "+array[i][1]+"| Cantidad: "+str(array[i][3]), tcolor.BOLD)
        
    choice = input("Confirmar (s/n): ").lower()
    if choice.__contains__("s"): 
        y = len(HojaCalculo.returnColumn("Ventas", f"C2:C150"))+2
        HojaCalculo.setRangeValues([[client, date]], "Ventas", f"A{y}:B{y}")
        HojaCalculo.setRangeValues(array, "Ventas", f"C{y}:F{y+len(array)}")
        coloredPrint("- Operación Exitosa -".center(term_size), tcolor.GREEN)
        
    else: 
        coloredPrint("- Operación Cancelada -".center(term_size), tcolor.FAIL)
    
    choice = input("Volver al menu (ok): ")
    

def endSale(): 
    system(clear_message)
    coloredPrint("- Generar Ticket -".center(term_size), tcolor.REVERSE)
    
    coloredPrint("Seleccionar una venta: ", tcolor.CYAN)
    
    clients = list(filter(lambda name: name != "", HojaCalculo.returnColumn("Ventas", "A2:A150")))
    dates = list(filter(lambda name: name != "", HojaCalculo.returnColumn("Ventas", "B2:B150")))
        
    for i in range(len(clients)):
        coloredPrint(f"{i+1} - Cliente: "+clients[i] + "| Fecha: "+dates[i], tcolor.BOLD)
        
    num = int(input("Número de venta: "))
    
    # Getting the initial index of the sale and the credentias (Client, Date)
    ind_sale = HojaCalculo.returnColumn("Ventas", "A2:A150").index(clients[num-1])+2
    sale_creds = HojaCalculo.returnRangeValues("Ventas", f"A{ind_sale}:B{ind_sale}")[0]
    
    # Getting the ending point of the sale
    if num == len(clients):
       ind_end = len(HojaCalculo.returnColumn("Ventas", "C2:D150"))+1
    
    else: 
        ind_end = HojaCalculo.returnColumn("Ventas", "A2:A150").index(clients[num])+1
    
    # Getting the values of the products
    raw_data = HojaCalculo.returnRangeValues("Ventas", f"C{ind_sale}:F{ind_end}")
    sale_data = []
    
    # Adjust the data to fit in Ticket
    for i in range(len(raw_data)):
        sale_data.append([raw_data[i][1], int(raw_data[i][2][1:-3]), raw_data[i][3]])
    
    system(clear_message)
    coloredPrint("Venta Seleccionada: ", tcolor.BOLD)
    coloredPrint("Cliente: "+sale_creds[0] + "\nFecha: "+sale_creds[1], tcolor.CYAN)
    for i in range(len(sale_data)):
        coloredPrint(f"{i+1} - Producto: {str(sale_data[i][0])} | Cantidad: {str(sale_data[i][2])}", tcolor.BLUE)
        
    choice = input("Confirmar ticket (s/n): ").lower()
    
    if choice.__contains__("s"): 
        #Remove sale from Sale's Sheet
        HojaCalculo.deleteRangeValues("Ventas", f"A{ind_sale}:F{ind_end}")
        HojaCalculo.moveRangeValues("Ventas", f"A{ind_end+1}:F150", 0, ind_sale-ind_end)
        
        # Write sales data on ticket
        HojaCalculo.setRangeValues([[sale_creds[0]]], "Ticket", "C2:D2") #Client
        HojaCalculo.setRangeValues([[sale_creds[1]]], "Ticket", "C3:D3") #Date
        
        HojaCalculo.setRangeValues(sale_data, "Ticket", f"B6:D{len(sale_data)+6}") #Product Data
        
        coloredPrint("- Operación Exitosa -".center(term_size), tcolor.GREEN)
        
    else: 
        coloredPrint("- Operación Cancelada -".center(term_size), tcolor.FAIL)
    
    choice = input("Volver al menu (ok): ")


def addClient():
    system(clear_message)
    coloredPrint("- Añadir Cliente -".center(term_size), tcolor.REVERSE)
    name = input("\nNombre: ")
    phone = int(input("Número Telefónico: "))
    email = input("Dirección de correo electrónico: ")
    adress = input("Dirección para envíos: ")
    
    choice = input("Confirmar datos (s/n): ").lower()
    
    if choice.__contains__("s"): 
            y = HojaCalculo.findY("Clientes") +1 
            HojaCalculo.setRangeValues([[name, phone, email, adress]], "Clientes", f"A{y}:D{y}")
            coloredPrint("- Operación Exitosa -".center(term_size), tcolor.GREEN)
    else: 
        coloredPrint("- Operación Cancelada -".center(term_size), tcolor.FAIL)
    
    choice = input("Volver (ok): ")

    
def removeClient():
    system(clear_message)
    coloredPrint("- Eliminar Cliente -".center(term_size), tcolor.REVERSE)
    print("")
    clients = HojaCalculo.returnColumn("Clientes", "A1:A150")
    for i in range(len(clients)): 
        coloredPrint(f"{i+1} - {clients[i]}", tcolor.BOLD)
    
    num = int(input("\nNúmero del cliente a eliminar: "))
    coloredPrint("\nSe eliminará a "+clients[num-1], tcolor.BLUE)
    choice = input("Confirmar (s/n): ").lower()
    
    if choice.__contains__("s"): 
        HojaCalculo.deleteRow(num, "Clientes")
        HojaCalculo.moveRangeValues("Clientes", f"A{num+1}:D150", 0, -1)
        coloredPrint("- Operación Exitosa -".center(term_size), tcolor.GREEN)
    else: 
        coloredPrint("- Operación Cancelada -".center(term_size), tcolor.FAIL)
    
    choice = input("Volver al menu (ok): ")


def editClients(): 
    
    system(clear_message)
    coloredPrint("- Editar Cartera de Clientes -".center(term_size), tcolor.REVERSE)
    coloredPrint("\n[1] Añadir cliente.", tcolor.CYAN)
    coloredPrint("[2] Eliminar Cliente.", tcolor.BLUE)
    coloredPrint("[menu] Volver al menu.", tcolor.PURPLE)
    choice = input(": ").lower()
    
    try:
        if choice.__contains__("1"): addClient()
            
        elif choice.__contains__("2"): removeClient()
            
        elif choice.__contains__("menu"): pass
        
        else: editClients()
    
    except: errorMessage()   

#   Menus - Differnt action selecters
#   Main menu
def menu(): 
    #Imprimimos el menú de acciones
    system(clear_message) #Puede tener cambios con respecto a que OS se está utilizando
    coloredPrint("Salta Services - Menu".center(term_size), tcolor.REVERSE)
    coloredPrint("\nOpciones disponibles: ", tcolor.BOLD)
    coloredPrint("\t[1] Manejo de Stock.", tcolor.GREEN)
    coloredPrint("\t[2] Control de Producción.", tcolor.CYAN)
    coloredPrint("\t[3] Seguimiento de Ventas.", tcolor.BLUE)
    coloredPrint("\t[menu] Ver los comandos posibles.", tcolor.PURPLE)
    coloredPrint("\t[quit] Leave program.", tcolor.GREY)

#   Focused on Stock sheet and basic operations
def stock(): 
    
    #Imprimimos el menú de acciones
    system(clear_message) #Puede tener cambios con respecto a que OS se está utilizando
    coloredPrint("Salta Services - Stock".center(term_size), tcolor.REVERSE)
    coloredPrint("\nOpciones disponibles: ", tcolor.BOLD)
    coloredPrint("\t[1] Editar cantidad de producto.", tcolor.GREEN)
    coloredPrint("\t[2] Valores totales.", tcolor.CYAN)
    coloredPrint("\t[menu] Volver al Menu Principal.", tcolor.PURPLE)
    
    choice = input(": ").lower()
        
    if choice.__contains__("1"):
        editStock()
        system(clear_message)
        menu()
        
    elif choice.__contains__("2"): 
        totalValues()
        system(clear_message)
        menu()
        
    elif choice.__contains__("menu"): 
        system(clear_message)
        menu()
        
    else: 
        stock() # Recrusion

#   Focused on Production management and effects on Stock
def production():
    #Imprimimos el menú de acciones
    system(clear_message) #Puede tener cambios con respecto a que OS se está utilizando
    coloredPrint("Salta Services - Producción".center(term_size), tcolor.REVERSE)
    coloredPrint("\nOpciones disponibles: ", tcolor.BOLD)
    coloredPrint("\t[1] Actualizar proceso.", tcolor.GREEN)
    coloredPrint("\t[2] Agregar nuevo proceso.", tcolor.CYAN)
    coloredPrint("\t[3] Cancelar proceso.", tcolor.BLUE)
    coloredPrint("\t[menu] Volver al Menu Principal.", tcolor.PURPLE)
    
    choice = input(": ").lower()
        
    if choice.__contains__("1"):
        updateProcess()
        system(clear_message)
        menu()
        
    elif choice.__contains__("2"): 
        newProcess()
        system(clear_message)
        menu()
        
    elif choice.__contains__("3"): 
        delProcess()
        system(clear_message)
        menu()
        
    elif choice.__contains__("menu"): 
        system(clear_message)
        menu()
        
    else: 
        production() # Recrusion

#   Management of Clients and Sales sheets
def sales(): 
    #Imprimimos el menú de acciones
    system(clear_message) #Puede tener cambios con respecto a que OS se está utilizando
    coloredPrint("Salta Services - Ventas".center(term_size), tcolor.REVERSE)
    coloredPrint("\nOpciones disponibles: ", tcolor.BOLD)
    coloredPrint("\t[1] Nueva Venta.", tcolor.GREEN)
    coloredPrint("\t[2] Generar Ticket.", tcolor.CYAN)
    coloredPrint("\t[3] Editar Cartera de Clientes.", tcolor.BLUE)
    coloredPrint("\t[menu] Volver al Menu Principal.", tcolor.PURPLE)
    
    choice = input(": ").lower()
        
    if choice.__contains__("1"):
        newSale()
        system(clear_message)
        menu()
        
    elif choice.__contains__("2"): 
        endSale()
        system(clear_message)
        menu()
        
    elif choice.__contains__("3"): 
        editClients()
        system(clear_message)
        menu()
        
    elif choice.__contains__("menu"): 
        system(clear_message)
        menu()
        
    else: 
        sales() # Recrusion

#   Main loop - Core of the program
def main(): 
    # Starting Point
    system(clear_message)
    menu()
    choice = ""#Acción del usuario - User input

    #Menú de la aplicación - Program menu
    while choice != "quit":
        
        choice = input(": ").lower()
         
        if choice.__contains__("1"):
            stock()
            
        elif choice.__contains__("2"): 
            production()
            
        elif choice.__contains__("3"): 
            sales()
            
        elif choice.__contains__("menu"): 
            menu()
            
        else: 
            coloredPrint("- Entrada no válida -".center(term_size), tcolor.FAIL)

    system(clear_message)
    coloredPrint("Salta Services Off".center(term_size), tcolor.REVERSE)


if __name__ == "__main__": 
    main()


## Ain Bolaños Cortés jqp983