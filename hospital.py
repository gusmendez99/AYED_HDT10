#Universidad del valle de Guatemala
#Algoritmos y Estructura de Datos - HDT10
#Gustavo Mendez - 18500
#Archivo: hospital.py
#Fecha: 12/05/2019
#Desc: Modulo que se encarga de la conexion a Neo4J, para la creacion de relaciones entre medicina, paciente y doctor

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
import sys

driver = GraphDatabase("http://localhost:7474", username="neo4j", password="1234")

patients = driver.labels.create("Patient")
doctors = driver.labels.create("Doctor")
drugs = driver.labels.create("Drug")

# MAIN FUNCION FOR ADD A VISIT
def registerMedicalVisit(patientName, doctorName, drugName, initDate, endDate, dose):
    drug = addDrug(drugName, initDate, endDate, dose)
    linkPatientWithDoctor(patientName, doctorName)
    linkPatientWithDrug(patientName, drugName)
    linkDoctorWithDrug(doctorName, drugName)

# SEARCHS
def filterDoctorBySpecialty(specialty): #filter doctors by specialty, returns a list of doctor names
    doctors = []
    query = "MATCH (d:Doctor) WHERE d.specialty = \"{0}\" RETURN d".format(specialty)
    results = driver.query(query, returns=(client.Node))
	
    for node in results:
        doctors.append(node[0]["name"]) #adds doctor name
	
    return doctors

def getKnownPeopleByPatient(patientName): #returns a list of known people (another patients) by current patient
    knownPeople = []
    query = 'MATCH (p:Patient)-[r:KNOWS]->(u:Patient) WHERE p.name=\"{0}\" RETURN p, type(r), u'.format(patientName)
    results = driver.query(query, returns=(client.Node, str, client.Node))
    
    for node in results:
        knownPeople.append(node[2]["name"]) #adds known patient name
    
    return knownPeople

# NODES - CREATE
def addPatient(name, phone):
    nodePatient = driver.nodes.create(name=name, phone=phone)
    patients.add(nodePatient)
    return nodePatient

def addDoctor(name, phone, collegiateCode, specialty):
    nodeDoctor = driver.nodes.create(name=name, phone=phone, collegiateCode=collegiateCode, specialty=specialty)
    doctors.add(nodeDoctor)
    return nodeDoctor

def addDrug(name, initDate, endDate, dose):
    drugNode = driver.nodes.create(name=name, initDate=initDate, endDate=endDate, dose=dose)
    drugs.add(drugNode)
    return drugNode



# RELATIONS - MAIN RELATIONSHIPS
def linkPatientWithDoctor(patientName, doctorName):
    query = "MATCH (p:Patient), (d:Doctor) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(patientName, doctorName)
    results = driver.query(query, returns=(client.Node, client.Node))
    for node in results:
        myPatient = node[0]
        myDoctor = node[1]
        myPatient.relationships.create("VISITS", myDoctor)

def linkPatientWithDrug(patientName, drugName):
    query = "MATCH (p:Patient), (d:Drug) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(patientName, drugName)
    results = driver.query(query, returns=(client.Node, client.Node))
    for node in results:
        myPatient = node[0]
        myDrug = node[1]
        myPatient.relationships.create("TAKES", myDrug)

def linkDoctorWithDrug(doctorName, drugName):
    queryDoctors = "MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d".format(doctorName)
    results = driver.query(queryDoctors,returns=(client.Node))
    for node in results:
        myDoctor = node[0]

    queryDrugs="MATCH (d:Drug) WHERE d.name=\"{0}\" RETURN d".format(drugName)
    results = driver.query(queryDrugs,returns=(client.Node))
    for node in results:
        myDrug = node[0]
        myDoctor.relationships.create("PRESCRIBES", myDrug)


# RELATIONS - SECONDARY RELATIONSHIPS
def linkPatientWithPatient(patientName1, patientName2):
    queryPatient1 ='MATCH (p:Patient) WHERE p.name=\"{0}\" RETURN p'.format(patientName1)
    results = driver.query(queryPatient1,returns=(client.Node))

    for node in results:
        myPatient1 = node[0]

    queryPatient2 ='MATCH (p:Patient) WHERE p.name=\"{0}\" RETURN p'.format(patientName2)
    results = driver.query(queryPatient2,returns=(client.Node))

    for node in results:
        myPatient2 = node[0]
        myPatient1.relationships.create("KNOWS", myPatient2)
  

def linkDoctorWithPatient(doctorName, patientName):
    query ='MATCH (p:Paciente) WHERE p.name= \"{0}\" RETURN p'.format(patientName)
    results = driver.query(query,returns=(client.Node))
    
    for node in results:
        myPatient = node[0]

    query='MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d'.format(doctorName)
    results = driver.query(query,returns=(client.Node))
    for node in results:
        myDoctor = node[0]
        myDoctor.relationships.create("KNOWS", myPatient)
  

def linkDoctorWithDoctor(doctorName1, doctorName2):
    query ='MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d'.format(doctorName1)
    results = driver.query(query,returns=(client.Node))
    for node in results:
        myDoctor1 = node[0]

    query ='MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d'.format(doctorName2)
    results = driver.query(query,returns=(client.Node))
    for node in results:
        myDoctor2=node[0]

    myDoctor1.relationships.create("KNOWS", myDoctor2)




# RECOMMENDATION SYSTEM
