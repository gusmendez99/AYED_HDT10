# Universidad del Valle de Guatemala
# Algoritmos y Estructura de Datos - HDT10
# Gustavo Mendez - 18500
# Roberto Figueroa - 18306
# Luis Urbina - 18473
# Archivo: main.py
# Fecha: 12/05/2019
# Desc: Main, desplegando menu principal para manejo de relaciones de una clinica entre pacientes, doctor y medicina

from hospital import *

print("BIENVENIDO AL PROGRAMA QUE OPTIMIZA LOS ASIENTOS DE LA BODA!\n")
option = 1

while(option != 4):
    print("""
    ***********************
    Elija una opcion:
    1. Agregar un doctor
    2. Ingresar un paciente
    3. Ingresar visita de un paciente a un doctor
    4. Obtener doctores por especialidad
    5. Ingresar que un paciente conoce a otro paciente.
    6. Obtener recomendacion de doctores que conocen mis conocidos(otros pacientes) 
    7. Obtener recomendacion de doctores por mi doctor, y por especialidad
    8. Salir
    ***********************
    """)
    option = input("> ")
    if(validateNumber(option)):
        option = int(option)
        #Check if option is in range
        validRange = isOptionInRange(option, 1, 8)
        if(validRange):
            if(option == 1): #Add Doctor
                print("Not implemented yet")

            elif(option == 2): #Add Patient
                print("Not implemented yet")

            elif(option == 3): #Add Visit
                print("Not implemented yet")
            
            elif(option == 4): #Get doctors by specialty
                print("Not implemented yet")

            elif(option == 5): #Add relationship between patients
                print("Not implemented yet")

            elif(option == 6): #Get First doctor recommendation
                print("Not implemented yet")

            elif(option == 7): #Get Second doctor recommendation
                print("Not implemented yet")
                
            elif(option == 8): #Exit
                print("Saliendo...")
    else:
        print("El valor ingresado no es un numero, intente de nuevo...")
