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

#Agrega pacientes al grafo

addPatient("Steven","68946194")
addPatient("Maria","29193929")
addPatient("Zonia","45558785")
addPatient("Ines","49026128")


#Crea relaciones
registerMedicalVisit("Steven","Juan","Alka-Seltzer","1 c/d 7 hrs")
registerMedicalVisit("Maria","Carlos","Panadol","3 c/d 7 hrs")
registerMedicalVisit("Zonia","Francisco","Amoxicilina","2 c/d 7 hrs")



