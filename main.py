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

while(option != 8):
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
                #print("Not implemented yet") 
                doctorName = input("Ingrese el nombre del doctor: ")
                doctorSpecialty = input("Ingrese la especialidad del doctor: ")
                doctorPhone = input("Ingrese el numero de telefono: ")
                doctorCollegiateCode = input("Ingrese el codigo de colegiado: ")                

                if(len(doctorName) > 0 and len(doctorSpecialty) > 0 and len(doctorPhone) > 0 and len(doctorCollegiateCode) > 0
                        and validateNumber(doctorPhone) > 0):
                    if(addDoctor(doctorName, doctorPhone, doctorCollegiateCode, doctorSpecialty) != None):
                        print("Doctor agregado exitosamente")
                else:
                    print("Datos invalidos, intente de nuevo...")
            
            elif(option == 2): #Add Patient
                #print("Not implemented yet") 
                patientName = input("Ingrese el nombre del paciente: ")
                patientPhone = input("Ingrese su numero de telefono: ")           

                if(len(patientName) > 0 and len(patientPhone) > 0 and validateNumber(patientPhone) > 0):
                    if(addPatient(patientName, patientPhone) != None):
                        print("Paciente agregado exitosamente")
                else:
                    print("Datos invalidos, intente de nuevo...")

            elif(option == 3): #Add Visit
                #print("Not implemented yet") 
                patientName = input("Ingrese el nombre del paciente: ")
                doctorName = input("Ingrese el nombre del doctor: ")
                drugName = input("Ingrese el nombre de la medicina: ")
                dose = input("Por default, la dosis se suministra 5 dias, indique la cantidad para un dia: ")                

                if(len(patientName) > 0 and len(doctorName) > 0 and len(drugName) > 0 and len(dose) > 0):
                    if(registerMedicalVisit(patientName, doctorName, drugName, dose)):
                        print("Visita agregada exitosamente")
                else:
                    print("Datos invalidos, intente de nuevo...")
            
            elif(option == 4): #Get doctors by specialty
                #print("Not implemented yet")
                specialty = input("Ingrese la especialidad: ")
                doctors = filterDoctorBySpecialty(specialty)
                if(len(doctors) > 0):
                    print("DOCTORES PARA ESTA ESPECIALIDAD: {0}".format(len(doctors)))
                    print("**************************************")                    
                    for doctor in doctors:
                        print("Doctor: {0}".format(doctor))
                    print("")
                else:
                    print("No se encontraron doctores para esa especialidad, intente de nuevo...")

            elif(option == 5): #Add relationship between patients or doctors
                #print("Not implemented yet")

                optionRelationship = 0
                while(optionRelationship != 3):
                    print("""
                    ***********************
                    Elija una opcion:
                    1. Relacion entre pacientes
                    2. Relacion entre doctores
                    3. Salir
                    ***********************
                    """)

                    secondaryOption = input("> ")
                    if(validateNumber(secondaryOption)):
                        secondaryOption = int(secondaryOption)
                        #Check if option is in range
                        validRange = isOptionInRange(secondaryOption, 1, 3)
                        if(validRange):
                            if(secondaryOption == 1): #Add relationship between patients
                                namePatient1 = input("Ingrese el nombre del paciente que desea relacionar: ")
                                namePatient2 = input("Ingrese el nombre del otro paciente: ")
                                if(linkPatientWithPatient(namePatient1, namePatient2)):
                                    print("Relacion entre pacientes creada exitosamente")
                                else:
                                    print("Ocurrio un error, revisa si los 2 pacientes existen...")
                            
                            elif(secondaryOption == 2): #Add relationship between patients
                                nameDoctor1 = input("Ingrese el nombre del doctor que desea relacionar: ")
                                nameDoctor2 = input("Ingrese el nombre del otro doctor: ")
                                if(linkDoctorWithDoctor(nameDoctor1, nameDoctor2)):
                                    print("Relacion entre pacientes creada exitosamente")
                                else:
                                    print("Ocurrio un error, revisa si los 2 pacientes existen...")
                            elif(secondaryOption == 3):
                                print("Volviendo a menu principal...")
                                optionRelationship = 3
                        
                        else:
                            print("El valor no se encuentra en el rango, prueba de nuevo...")
                    else:
                        print("La entrada no es un numero, intenta de nuevo...")


            elif(option == 6): #Get First doctor recommendation, my doctor has relation with other doctors
                #print("Not implemented yet")
                specialty = input("Sobre qué especialidad espera la recomendación?: ")
                myDoctor = input("Qué doctor desea que le recomiende otros doctores?: ")
                recommendedDoctors = getDoctorRecommendationByKnownDoctor(specialty, myDoctor)
                
                if(len(recommendedDoctors) > 0):
                    print("DOCTORES PARA ESTA ESPECIALIDAD: {0}".format(len(recommendedDoctors)))
                    print("**************************************")
                    for doctor in recommendedDoctors:
                        print("Doctor: {0}".format(doctor))
                    
                    print("")
                else:
                    print("El doctor que ingresaste no tiene recomendaciones para mostrarte ahorita :( ...")

            elif(option == 7): #Get Second doctor recommendation
                #print("Not implemented yet")
                specialty = input("Sobre qué especialidad espera la recomendación?: ")
                myPatientKnown = input("Qué paciente/amigo desea que le recomiende otros doctores?: ")
                recommendedDoctors = getDoctorRecommendationByKnownPeople(myPatientKnown, specialty)
                
                if(len(recommendedDoctors) > 0):
                    print("DOCTORES PARA ESTA ESPECIALIDAD: {0}".format(len(recommendedDoctors)))
                    print("**************************************")
                    for doctor in recommendedDoctors:
                        print("Doctor: {0}".format(doctor))
                    
                    print("")
                else:
                    print("El paciente/amigo que ingresaste no tiene recomendaciones para mostrarte ahorita :( ...")

                
            elif(option == 8): #Exit
                print("Saliendo...")
    else:
        print("El valor ingresado no es un numero, intente de nuevo...")
