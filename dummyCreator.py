#Here we're gonna add dummy data, just for tests

from hospital import *

#Agrega doctores al grafo

d1 = addDoctor("Juan","25841644","5021","Cardiologo")
addDoctor("Carlos","57875435","3301","Dermatologo")
addDoctor("Pedro","97895456","2255","Otorrinolaringologo")
addDoctor("Diego","78250828","5566","Neurocirijano")
addDoctor("Francisco","47345855","6699","Anestiologo")
addDoctor("Michael","82185063","5584","Cirujano")
addDoctor("Saul","25841644","6551","Urologia")
addDoctor("Luis","40435145","8874","Ginecologo")
addDoctor("Jose","40435145","8874","Oncologo")


#Agrega pacientes al grafo

addPatient("Steven","68946194")
addPatient("Maria","29193929")
addPatient("Zonia","45558785")
addPatient("Ines","49026128")
addPatient("Adrian","97546498")
addPatient("Ian","68777789")
addPatient("Justin","79314502")


#Crea relaciones entre pacientes y doctores


registerMedicalVisit("Steven","Juan","Alka-Seltzer","1 c/d 7 hrs")
registerMedicalVisit("Maria","Carlos","Panadol","3 c/d 7 hrs")
registerMedicalVisit("Zonia","Pedro","Amoxicilina","2 c/d 7 hrs")
registerMedicalVisit("Ines","Diego","Aspirina","3 c/d 7 hrs")
registerMedicalVisit("Adrian","Francisco","Paracetamol","1 c/d 12 hrs")
registerMedicalVisit("Ian","Michael","Acetazolamida","1 c/d 12 hrs")
registerMedicalVisit("Justin","Saul","Acetilcisteína","4 c/d 12 hrs")

#Crea relaciones entre pacientes


linkPatientWithPatient("Steven","Maria")
linkPatientWithPatient("Zonia","Ines")
linkPatientWithPatient("Adrian","Ian")
linkPatientWithPatient("Ian","Justin")
linkPatientWithPatient("Ian","Ines")
linkPatientWithPatient("Zonia","Maria")

#Crea relaciones entre doctores

linkDoctorWithDoctor("Juan","Carlos")
linkDoctorWithDoctor("Pedro","Diego")
linkDoctorWithDoctor("Francisco","Michael")
linkDoctorWithDoctor("Saul","Jose")
linkDoctorWithDoctor("Luis","Michael")
linkDoctorWithDoctor("Luis","Juan")


#Crea relaciones entre doctores y pacientes


linkPatientWithDoctor("Steven","Carlos")
linkPatientWithDoctor("Steven","Diego")
linkPatientWithDoctor("Zonia","Saul")
linkPatientWithDoctor("Zonia","Francisco")
linkPatientWithDoctor("Zonia","Carlos")
linkPatientWithDoctor("Adrian","Jose")
linkPatientWithDoctor("Ian","Luis")
linkPatientWithDoctor("Justin","Michael")
linkPatientWithDoctor("Justin","Luis")
linkPatientWithDoctor("Justin","Juan")


print("Dummy data added successfully, now run main.py ...")
