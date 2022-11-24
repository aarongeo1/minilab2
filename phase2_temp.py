from pymongo import MongoClient

db = None
collection = None

def connect(port = "27017"):
    global collection
    client = MongoClient("mongodb://localhost:{}".format(port))
    db = client["291db"]
    collection = db["dblp"]

def intify(s):
    if s.isdigit() == True:
        return int(s)
    else:
        return s

def search_article():
    global collection
    print('\n-----Search article-----\n')
    s_article_input = input('Enter one ore more keywords to search articles(separated by space) : ')
    s_article_list = list(s_article_input.split(" "))
    l1 = []
    for i in s_article_list:
        rgx = {"$regex":i,"$options":"i"}
        val = collection.aggregate([
            {"$match":{"$or":[{"title":rgx},{"authors":rgx},{"abstract":rgx},{"venue":rgx},{"year":intify(i)}]}},
            {"$project":{"id":1,"title":1,"year":1,"venue":1,"_id":0}}
        ])
        l1.append(val)
    for i in l1:
        for j in i:
            print(j)
    
    
    
def search_authors():
    print('\n-----Search authors-----\n')
    s_author_input = input('Enter a keyword to search authors : ')
    
    
    
def list_venues():
    while(True):
        print('\n-----List venues-----\n')
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
    while(True):
        print('\n-----Add article-----\n')
        id_input = input('Enter the id (Must be unique) : ')
        title_input = input('Enter the title : ')
        author_input = input('Enter the one or more authors(separeted by space) : ')
        author_list = list(author_input.split(" "))
        year_input = input('Enter the year : ')
        
        
        exist = list(collection.find({"id" : { "$eq" : id_input} }))
        
        if((exist) or (id_input == "") or (title_input == "") or (author_input == "") or (year_input == "")):
            
            print('Wrong input. Either id is not unique or some of the input is blank. try again...')
        else:
            print('Successfully added.')
            break
    


def main_menu():
    while(True):
        print('\n-----Main menu-----\n')
        m_input = input('1.Seach articles\n2.Search authors\n3.List venues\n4.Add articles\n5.terminate the program\n\nEnter your input :  ')
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
