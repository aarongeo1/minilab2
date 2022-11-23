def search_article():  
    print('-----Search article-----')
def search_authors():
    print('-----Search authors-----')
def list_venues():
    print('-----List venues-----')
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
    main_menu()
