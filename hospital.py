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

# RELATIONS - CREATE
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


