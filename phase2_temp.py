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
    s_article_input = input('\nEnter one or more keywords to search articles(separated by space) : ')
    s_article_list = list(s_article_input.split(" "))
    l1 = []
    j=1
    print("\n")
    for i in s_article_list:
        rgx = {"$regex":i,"$options":"i"}
        val = collection.aggregate([
            {"$match":{"$or":[{"title":rgx},{"authors":rgx},{"abstract":rgx},{"venue":rgx},{"year":intify(i)}]}},
            {"$project":{"id":1,"title":1,"year":1,"venue":1,"_id":0}}
        ])
        for k in val:
            if k not in l1:
                print(j,"\t", k, "\n")
                l1.append(k)
                j += 1

    send = input("If you wish to select a article then enter article number else enter 'n' : ")
    if send == "n":
        return
    elif send.isdigit() == True:
        send = int(send)
        article = l1[send-1]
        val = collection.find({"title":article["title"]})
        for i in val:
            print(i)
            article = i
        print("\n -----References------\n")
        for j in i["references"]:
            val = collection.aggregate([
            {"$match":{"id":j}},
            {"$project":{"id":1,"title":1,"year":1,"_id":0}}
            ])
            for k in val:
                print(k,"\n")
    else:
        return
    
def search_authors():
    print('\n-----Search authors-----\n')
    s_author_input = input('Enter a keyword to search authors : ')
    a_list = []
    rgx = {"$regex":s_author_input,"$options":"i"}
    val = collection.aggregate([
            {"$match":{"authors":rgx}},
            {"$project":{"authors":1}}
        ])
    numbering = 1
    inp = s_author_input.lower()
    a_dic = {}
    a_list = []
    for i in val:
        l1 = i["authors"]
        for j in l1:
            if j not in a_dic and inp in j.lower():
                a_dic[j] = 1
                a_list.append(j)
            elif j in a_dic and inp in j.lower():
                a_dic[j] = a_dic[j] + 1
            else:
                continue
    for i in a_dic:
        print(numbering,".\t","author : ", i, ", number of publications : ", a_dic[i])
        numbering += 1
    # for i in val:
    #     l1 = i["authors"]
    #     for j in l1:
    #         if j not in a_list:
    #             author = j.lower()
    #             if inp in author:
    #                 a_list.append(j)
    #                 co = collection.aggregate([
    #                 {"$match": {"authors":j}},
    #                 {"$group": {"_id":"$authors","num_publications":{"$sum": 1}}},
    #                 {"$project":{"authors":"$_id","num_publications":1,"_id":0}}
    #                 ])
    #                 co = 0
    #                 for i in val:
    #                     co += 1
    #                 print(numbering,".\t","author : ", j, ", number of publications : ", co)
    #                 numbering += 1
    #             else:
    #                 continue
    #         else:
    #             continue
    send = input("If you wish to select a author then enter author number else enter 'n' : ")
    if send == "n":
        return
    elif send.isdigit() == True:
        send = int(send)
        au = a_list[send-1]
        val = collection.aggregate([
                {"$match": {"authors":au}},
                {"$sort":{"year":-1}},
                {"$project":{"title":1,"year":1,"venue":1,"_id":0}}
                ])
        for i in val:
            print(i)
    else:
        return

    
    
def list_venues():
    while(True):
        print('\n-----List venues-----\n')
        n = input('Enter a number to see of top venues : ')

        if n.isdigit() == True:
            a_dic = {}
            a_list =[]
            l1 = []
            val = collection.aggregate([
                {"$group": {"_id":"$venue","num_of":{"$sum": 1}}},
                {"$project":{"venue":"$_id","num_of":1,"_id":0}}
                ])
            for i in val:
                a_dic[i["venue"]] = i["num_of"]
                a_list.append(i["venue"])
            val1 = collection.aggregate([
                {"$lookup":{"from":"dblp","localField":"id","foreignField":"references","as": "citeds"}},
                {"$unwind": "$citeds"},
                {"$match":{"venue":{"$ne":""}}},
                {"$group": {"_id":"$venue","unique":{"$addToSet": "$citeds.id"}}},
                {"$project":{"num_of_ref":{"$size":"$unique"}}},
                {"$sort":{"num_of_ref":-1}},
                {"$limit":int(n)}
            ])
            for i in val1:
                l1.append([i["_id"],i["num_of_ref"]])
            i = 0
            no_r = 0
            while i < len(l1) and no_r < int(n):
                print("Venue : ",l1[i][0],"   no of articles : ",a_dic[l1[i][0]],"    no of references : ",l1[i][1])
                a_list.remove(l1[i][0])
                i += 1
                no_r += 1
            i = 0
            while i < len(a_list) and no_r < int(n):
                print("Venue : ",a_list[i],"   no of articles : ",a_dic[a_list[i]],"    no of references : ",0) 
                i += 1
                no_r += 1  
            break
        else:
            print("Not a number , Try Again")
        
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
            data_dict = { "id": id_input, "title": title_input, "authors": author_list,"year": year_input,"abstract": None,"venue": None,"references": [],"n_citations": 0}
            collection.insert_one(data_dict)
            show = list(collection.find({"id" : { "$eq" : id_input} }))
            for x in show:
                print(x)
            print('Successfully added.')
            break
    


def main_menu():
    while(True):
        print('\n-----Main menu-----\n')
        m_input = input('1.Search articles\n2.Search authors\n3.List venues\n4.Add articles\n5.terminate the program\n\nEnter your input :  ')
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

