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
from datetime import datetime
from datetime import timedelta

driver = GraphDatabase("http://localhost:7474", username="neo4j", password="1234")
patients = driver.labels.create("Patient")
doctors = driver.labels.create("Doctor")
drugs = driver.labels.create("Drug")

# MAIN FUNCION FOR ADD A VISIT
# patientName: String name of the patient
# doctorName: String name of the doctor
# drugName: StringName of the drug
# dose: String that represents how many pills the patient has to take

def registerMedicalVisit(patientName, doctorName, drugName, dose):

    #Default: dose for 5 days
    currentDate = datetime.now()
    currDateStr = '{:%Y-%m-%d}'.format(currentDate)
    # set the end of the dose
    endDoseDate = datetime.now() + timedelta(days=5)
    endDateStr = '{:%Y-%m-%d}'.format(endDoseDate)
    # adds a drug with given date
    addDrug(drugName, currDateStr, endDateStr, dose)
    # links a patient with a specific doctor
    linkPatientWithDoctor(patientName, doctorName)
    # links a patient with a speceific drug
    linkPatientWithDrug(patientName, drugName)
    # links a docto with a specific drug
    linkDoctorWithDrug(doctorName, drugName)
    return True

# SEARCHS


# filter doctors by specialty
# param: speciality is the string of the doctor's specialty
# return: list of doctor names
# 
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
    # addPatient adds a patient-type node to the database with a specific name and phone
def addPatient(name, phone):
    nodePatient = driver.nodes.create(name=name, phone=phone)
    patients.add(nodePatient)
    return nodePatient

# addDoctor adds a doctor-type node to the database with given name, phone, collegiateCode, and specialty String
def addDoctor(name, phone, collegiateCode, specialty):
    nodeDoctor = driver.nodes.create(
        name=name, phone=phone, collegiateCode=collegiateCode, specialty=specialty)
    doctors.add(nodeDoctor)
    return nodeDoctor

# addDrug adds a drug-type node to the database with given name, initDate, and dose
def addDrug(name, initDate, endDate, dose):
    drugNode = driver.nodes.create(
        name=name, initDate=initDate, endDate=endDate, dose=dose)
    drugs.add(drugNode)
    return drugNode


# RELATIONS - MAIN RELATIONSHIPS
# makes a match between a patient and a doctor once a medical visit is settled
def linkPatientWithDoctor(patientName, doctorName):
    query = "MATCH (p:Patient), (d:Doctor) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(
        patientName, doctorName)
    results = driver.query(query, returns=(client.Node, client.Node))
    for node in results:
        myPatient = node[0]
        myDoctor = node[1]
        myPatient.relationships.create("VISITS", myDoctor)

# makes a match between a patient and a given drug once a medical visit is settled
def linkPatientWithDrug(patientName, drugName):
    query = "MATCH (p:Patient), (d:Drug) WHERE p.name=\"{0}\" AND d.name=\"{1}\" RETURN p,d".format(
        patientName, drugName)
    results = driver.query(query, returns=(client.Node, client.Node))
    for node in results:
        myPatient = node[0]
        myDrug = node[1]
        myPatient.relationships.create("TAKES", myDrug)

# makes a match between a doctor and a given drug once a medical visit is settled
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
# Links all the patient of a specific patient and creates a relation betwwne both of them
def linkPatientWithPatient(patientName1, patientName2):
    queryPatient1 = 'MATCH (p:Patient) WHERE p.name=\"{0}\" RETURN p'.format(
        patientName1)
    results = driver.query(queryPatient1, returns=(client.Node))

    for node in results:
        myPatient1 = node[0]

    queryPatient2 = 'MATCH (p:Patient) WHERE p.name=\"{0}\" RETURN p'.format(
        patientName2)
    results = driver.query(queryPatient2, returns=(client.Node))

    patientsExist = False

    for node in results:
        patientsExist = True
        myPatient2 = node[0]
        myPatient1.relationships.create("KNOWS", myPatient2)

    return patientsExist

#links a doctor witha specific patient
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

    if(myDoctor1 != None and myDoctor2 != None):
        myDoctor1.relationships.create("KNOWS", myDoctor2)
        return True
    
    return False

    


# RECOMMENDATION OF FRIENDS BY KNOWN DOCTOR SPECIALTY 
def getDoctorRecommendationByKnownPeople(patientName, specialty):
    # Initialize lists
    recommendationDoctorList = []
    
    query = 'MATCH (p:Patient)-[r:VISITS]->(d:Doctor) WHERE p.name=\"{0}\" and d.specialty=\"{1}\" RETURN p, type(r), d'.format(
        patientName, specialty)
    results = driver.query(query, returns=(client.Node, str, client.Node))

    for node in results:
        recommendationDoctorList.append(node[2]["name"])  # adds known patient name
        
    knownPeopleList = getKnownPeopleByPatient(patientName)

	# If currPatient knows people...
    if (knownPeopleList != None and len(knownPeopleList) > 0):
        # Recommendation of firends of current patient
        for currPatientName in knownPeopleList:
            query = 'MATCH (p:Patient)-[r:VISITS]->(d:Doctor) WHERE p.name=\"{0}\" AND d.specialty=\"{1}\" RETURN d'.format(
                currPatientName, specialty)
            results = driver.query(query, returns=(client.Node))

            for doctorVisitedByFriendsOfFriend in results:
                recommendationDoctorList.append(doctorVisitedByFriendsOfFriend[0]["name"])

    
    return recommendationDoctorList

# RECOMMENDATION BETWEEN DOCTORS
def getDoctorRecommendationByKnownDoctor(specialty, doctorName):

	recommendationDoctorList = []
	query = 'MATCH (d:Doctor)-[r:KNOWS]->(o:Doctor) WHERE o.specialty = \"{0}\" AND d.name = \"{1}\" RETURN d, type(r), o'.format(specialty, doctorName)

	results = driver.query(query, returns=(client.Node, str, client.Node))
	for node in results:        
		recommendationDoctorList.append(node[2]["name"])

		recommendedDoctor = node[2]["name"]
        # Get doctor friends of recommended doctor
		newQuery = 'MATCH (d:Doctor)-[r:KNOWS]->(o:Doctor) WHERE o.specialty = \"{0}\" AND d.name = \"{1}\" RETURN d, type(r), o'.format(specialty, recommendedDoctor)

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