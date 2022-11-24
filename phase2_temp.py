from pymongo import MongoClient

db = None
collection = None

def connect(port = "27017"):
    global collection
    client = MongoClient("mongodb://localhost:{}".format(port))
    db = client["291db"]
    collection = db["dblp"]

def search_article():
    global collection
    print('-----Search article-----')
    s_article_input = input('Enter one ore more keywords to search articles(separated by space) : ')
    s_article_list = list(s_article_input.split(" "))
    l1 = []
    for i in s_article_list:
        rgx = {"$regex":i,"$options":"i"}
        val = collection.aggregate([
            {"$match":{"$or":[{"title":rgx},{"authors":rgx},{"abstract":rgx},{"venue":rgx},{"year":rgx}]}},
            {"$project":{"title":1,"year":1,"venue":1}}
        ])
        l1.append(val)
    for i in l1:
        for j in i:
            print(j)
    
    
    
def search_authors():
    print('-----Search authors-----')
    s_author_input = input('Enter a keyword to search authors : ')
    
    
    
def list_venues():
    print('-----List venues-----')
    while(True):
        n = input('Enter a number to see of top venues : ')
        
        err_count = 0 
        for char in n:
            if(ord(char) < 48 or ord(char) > 57):
                err_count = err_count + 1
              
        if(err_count == 0 and int(n) > 0):
            ##code goes here
            break
        else:
            print('Wrong number. Try again...')
    
    
    
def add_article():
    print('-----Add article-----')
    


def main_menu():
    print('-----Main menu-----')
    while(True):
        m_input = input('Enter 1 to Seach articles, 2 to Search authors, 3 to List venues, 4 to Add articles, or 5 to terminate the program : ')
        if(m_input == '1'):
            search_article()
        elif(m_input == '2'):
            search_authors()
        elif(m_input == '3'):
            list_venues()
        elif(m_input == '4'):
            add_article()
        elif(m_input == '5'):
            break
        else:
            print('Wrong input. Try again...')
        
if __name__ == "__main__":
    
    port = input('Enter a port number : ')
    connect(port)
    main_menu()
