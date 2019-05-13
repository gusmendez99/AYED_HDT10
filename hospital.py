# Universidad del Valle de Guatemala
# Algoritmos y Estructura de Datos - HDT10
# Gustavo Mendez - 18500
# Roberto Figueroa - 18306
# Luis Urbina - 18473
# Archivo: hospital.py
# Fecha: 12/05/2019
# Desc: Modulo que se encarga de la conexion a Neo4J, para la creacion de relaciones entre medicina, paciente y doctor

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
import sys

driver = GraphDatabase("http://localhost:7474",
                       username="neo4j", password="1234")

patients = driver.labels.create("Patient")
doctors = driver.labels.create("Doctor")
drugs = driver.labels.create("Drug")

# MAIN FUNCION FOR ADD A VISIT


def registerMedicalVisit(patientName, doctorName, drugName, initDate, endDate, dose):
    addDrug(drugName, initDate, endDate, dose)
    linkPatientWithDoctor(patientName, doctorName)
    linkPatientWithDrug(patientName, drugName)
    linkDoctorWithDrug(doctorName, drugName)

# SEARCHS


# filter doctors by specialty, returns a list of doctor names
def filterDoctorBySpecialty(specialty):
    doctors = []
    query = "MATCH (d:Doctor) WHERE d.specialty = \"{0}\" RETURN d".format(
        specialty)
    results = driver.query(query, returns=(client.Node))

    for node in results:
        doctors.append(node[0]["name"])  # adds doctor name

    return doctors


# returns a list of known people (another patients) by current patient
def getKnownPeopleByPatient(patientName):
    knownPeople = []
    query = 'MATCH (p:Patient)-[r:KNOWS]->(u:Patient) WHERE p.name=\"{0}\" RETURN p, type(r), u'.format(
        patientName)
    results = driver.query(query, returns=(client.Node, str, client.Node))

    for node in results:
        knownPeople.append(node[2]["name"])  # adds known patient name

    return knownPeople

# NODES - CREATE


def addPatient(name, phone):
    nodePatient = driver.nodes.create(name=name, phone=phone)
    patients.add(nodePatient)
    return nodePatient


def addDoctor(name, phone, collegiateCode, specialty):
    nodeDoctor = driver.nodes.create(
        name=name, phone=phone, collegiateCode=collegiateCode, specialty=specialty)
    doctors.add(nodeDoctor)
    return nodeDoctor


def addDrug(name, initDate, endDate, dose):
    drugNode = driver.nodes.create(
        name=name, initDate=initDate, endDate=endDate, dose=dose)
    drugs.add(drugNode)
    return drugNode


# RELATIONS - MAIN RELATIONSHIPS
def linkPatientWithDoctor(patientName, doctorName):
    query = "MATCH (p:Patient), (d:Doctor) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(
        patientName, doctorName)
    results = driver.query(query, returns=(client.Node, client.Node))
    for node in results:
        myPatient = node[0]
        myDoctor = node[1]
        myPatient.relationships.create("VISITS", myDoctor)


def linkPatientWithDrug(patientName, drugName):
    query = "MATCH (p:Patient), (d:Drug) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(
        patientName, drugName)
    results = driver.query(query, returns=(client.Node, client.Node))
    for node in results:
        myPatient = node[0]
        myDrug = node[1]
        myPatient.relationships.create("TAKES", myDrug)


def linkDoctorWithDrug(doctorName, drugName):
    queryDoctors = "MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d".format(
        doctorName)
    results = driver.query(queryDoctors, returns=(client.Node))
    for node in results:
        myDoctor = node[0]

    queryDrugs = "MATCH (d:Drug) WHERE d.name=\"{0}\" RETURN d".format(
        drugName)
    results = driver.query(queryDrugs, returns=(client.Node))
    for node in results:
        myDrug = node[0]
        myDoctor.relationships.create("PRESCRIBES", myDrug)


# RELATIONS - SECONDARY RELATIONSHIPS
def linkPatientWithPatient(patientName1, patientName2):
    queryPatient1 = 'MATCH (p:Patient) WHERE p.name=\"{0}\" RETURN p'.format(
        patientName1)
    results = driver.query(queryPatient1, returns=(client.Node))

    for node in results:
        myPatient1 = node[0]

    queryPatient2 = 'MATCH (p:Patient) WHERE p.name=\"{0}\" RETURN p'.format(
        patientName2)
    results = driver.query(queryPatient2, returns=(client.Node))

    for node in results:
        myPatient2 = node[0]
        myPatient1.relationships.create("KNOWS", myPatient2)


def linkDoctorWithPatient(doctorName, patientName):
    query = 'MATCH (p:Paciente) WHERE p.name= \"{0}\" RETURN p'.format(
        patientName)
    results = driver.query(query, returns=(client.Node))

    for node in results:
        myPatient = node[0]

    query = 'MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d'.format(doctorName)
    results = driver.query(query, returns=(client.Node))
    for node in results:
        myDoctor = node[0]
        myDoctor.relationships.create("KNOWS", myPatient)


def linkDoctorWithDoctor(doctorName1, doctorName2):
    query = 'MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d'.format(
        doctorName1)
    results = driver.query(query, returns=(client.Node))
    for node in results:
        myDoctor1 = node[0]

    query = 'MATCH (d:Doctor) WHERE d.name=\"{0}\" RETURN d'.format(
        doctorName2)
    results = driver.query(query, returns=(client.Node))
    for node in results:
        myDoctor2 = node[0]

    myDoctor1.relationships.create("KNOWS", myDoctor2)


# RECOMMENDATION OF FRIENDS BY KNOWN DOCTOR SPECIALTY 
def getDoctorRecommendationByKnownPeople(patientName, specialty):
    # Initialize lists
    doctorKnownPeopleList, doctorsBySpecialtyList, friendsKnownPeopleList = []

    recommendationDoctorList = []  # Recommended doctors

    knownPeopleList = getKnownPeopleByPatient(patientName)
    doctorsBySpecialtyList = filterDoctorBySpecialty(specialty)

	# If currPatient knows people...
    if (knownPeopleList != None):
        for patientName in knownPeopleList:
            query = 'MATCH (p:Patient)-[r:KNOWS]->(u:Patient) WHERE p.name=\"{0}\" RETURN u'.format(
                patientName)
            results = driver.query(query, returns=(client.Node))

            for friendKnownPerson in results:
                friendsKnownPeopleList.append(friendKnownPerson[0]["name"])

        # Filter doctor by specialty, and match if a current patient friend has visited
        for i in range(len(doctorsBySpecialtyList)):
            for j in range(len(doctorKnownPeopleList)):
                query = "MATCH (p:Paciente)-[r:VISITS]->(d:Doctor) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(
                    doctorKnownPeopleList[j], doctors[i])

                results = driver.query(
                    query, returns=(client.Node, client.Node))
                for node in results:
                    recommendationDoctorList.append(node[1]["name"])

        # If doctor has been visited by friends of current patient friends
        for i in range(len(doctorsBySpecialtyList)):
            for j in range(len(friendsKnownPeopleList)):
                query = "MATCH (p:Paciente)-[r:VISITS]->(d:Doctor) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(
                    friendsKnownPeopleList[j], doctorsBySpecialtyList[i])

                results = driver.query(
                    query, returns=(client.Node, client.Node))
                for node in results:
                    recommendationDoctorList.append(node[1]["name"])

        return recommendationDoctorList

# RECOMMENDATION BETWEEN DOCTORS
def getDoctorRecommendationByKnownDoctor(specialty, doctorName):

	recommendationDoctorList = []
	query = 'MATCH (d:Doctor)-[r:KNOWS]->(o:Doctor) WHERE d.specialty = \"{0}\" AND d.name = \"{1}\" RETURN d, type(r), o'.format(specialty, doctorName)

	results = driver.query(query, returns=(client.Node, str, client.Node))
	for node in results:        
		recommendationDoctorList.append(node[2]["name"])

		recommendedDoctor = node[2]["name"]
        # Get doctor friends of recommended doctor
		newQuery = 'MATCH (d:Doctor)-[r:KNOWS]->(o:Doctor) WHERE d.specialty = \"{0}\" AND d.name = \"{1}\" RETURN d, type(r), o'.format(specialty, recommendedDoctor)

		newResults = driver.query(newQuery, returns=(client.Node, str, client.Node))

		for node in newResults:
			if (node[2]["name"] != ""):
				recommendationDoctorList.append(node[2]["name"])
	
	return recommendationDoctorList

#UTILS
def validateNumber(variable): 
    try:
        #Try cast
        int(variable)
        return True
    except ValueError:        
        return False

def isOptionInRange(x, a, b):
    #Validates range
    if(x >= a and x <= b) or (x <= a and x >= b):
        return True
    return False