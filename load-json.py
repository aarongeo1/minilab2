from pymongo import MongoClient
import json
import subprocess


def connect(jfile,port = ""):
    client = MongoClient(port)
    db = client["291db"]
    collection = db["dblp"]
    p = subprocess.Popen("mongoimport --db 291db --collection dblp --drop --file ./{}".format(jfile), stdout=subprocess.PIPE, shell=True)
    


if __name__ == "__main__":
    jfile = input("Enter the json file")
    port = input("Ënter the post number")
    connect(jfile,port)
