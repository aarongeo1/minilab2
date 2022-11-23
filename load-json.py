from pymongo import MongoClient
import json
import subprocess
import os


def connect(jfile,port = "27017"):
    client = MongoClient("mongodb://localhost:{}".format(port))
    db = client["291db"]
    collection = db["dblp"]
    os.system("mongoimport --drop --port {} --db 291db --collection dblp  --file ./{}".format(port,jfile))
    


if __name__ == "__main__":
    jfile = input("Enter the json file (INCLUDE .json) : ")
    port = input("Ënter the port number : ")
    connect(jfile,port)
