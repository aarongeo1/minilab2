from pymongo import MongoClient

def search_article():  
    print('-----Search article-----')
    s_article_input = input('Enter one ore more keywords to search articles(separated by space) : ')
    s_article_list = list(s_article_input.split(" "))
    
    
def search_authors():
    print('-----Search authors-----')
    s_author_input = input('Enter a keyword to search authors : ')
    
    
    
def list_venues():
    print('-----List venues-----')
    n = input('Enter a number to see of top venues : ')
    
    if(int(n) > 0):
        pass
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
    main_menu()
