import random
import json
from tabulate import tabulate
from datetime import datetime, timedelta

def adding_books(title, author, isbn):
  """
  This function add books in the data base
  """
  try:
    try:
      with open('library.json', 'r') as book_file:
        book_data = json.loads(book_file.read())
    except FileNotFoundError:
      book_data = []  

    new_book = {
      "title": title,
      "author": author,
      "ISBN": isbn,
      "status":"not_borrowed",
    }

    book_data.append(new_book)
    with open('library.json', 'w') as book_file:
      json.dump(book_data, book_file)

    return book_data

  except (IOError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing 'library.json': {e}")
    return []

def adding_user(name, isbn):
    """
    This function adds a user to the database.
    """
    try:
        try:
            with open('user.json', 'r') as user_file:
                user_data = json.loads(user_file.read())
        except FileNotFoundError:
            user_data = []

        current_date = datetime.now().date()
        return_date = (current_date + timedelta(days=15)).strftime('%Y-%m-%d')

        new_user = {
            "name": name,
            "ISBN": isbn,
            "status": "borrowed",
            "borrow_date": str(current_date),
            "return_date": return_date
        }

        user_data.append(new_user)
        with open('user.json', 'w') as user_file:
            json.dump(user_data, user_file)
        update_book_status(isbn)
        return user_data

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing 'user.json': {e}")
        return []

def update_book_status(isbn):
    book_list = view_available_books()
    
    available_books = []
    for book in book_list:
        if int(book['ISBN']) == int(isbn):
            book['status'] = 'borrowed'  
            available_books.append(book)
    
    if available_books:
        print("Status updated to 'borrowed' for the book with ISBN:", isbn)      
        with open('library.json', 'w') as book_file:
            json.dump(book_list, book_file)        
        # headers = ["Book Title", "ISBN", "Status"]
        print(tabulate([list(book.values()) for book in book_list], tablefmt="grid"))
        
    else:
        print("No available books.")
   
def searching_books():
    """
     This function searches for books in the database
    """
    
    print("Search for books by title or author.")
    search_options = ['by title', 'by author']
    book_list = view_available_books()
    
    for index, option in enumerate(search_options, start=1):
        print(f"{index}: {option}")
      
    selected_option = int(input("Enter your search option: "))
    
    if selected_option == 1:
        title = input("Enter your title to search: ")
        print("Searching for books by title ....")
        for book in book_list:
          if title.lower() in book["title"].lower():
            print(f"Book title: 📔 {book['title']}, author: 👵 {book['author']}, ISBN: {book['ISBN']}")
      
    elif selected_option == 2:
        print("Searching for books by author...")
        author = input("Enter your title to search: ")
        print("Searching for books by title ....")
        for book in book_list:
          if author.lower() in book["author"].lower():
            print(f"Book title: 📔 {book['title']}, author: 👵 {book['author']}, ISBN: {book['ISBN']}")
  
    else:
        print("Invalid option. Please select 1 or 2.")

def adding_the_books():
    """
    This function get input from user about the books details
    """
    title = input("Enter the name of the book: ")
    author = input("Enter the name of the author: ")
    isbn = generate_short_number()
    # print('Adding books :: ::',{isbn,title,author})
    
    new_book_data = adding_books(title, author, isbn)
    if new_book_data:
      print("Book added successfully 💖!")
    else:
      print("An error occurred while adding the book 🕵️‍♂️.")
      
def view_available_books():
    """
    This function get the details of books from data base
    """
    try:
        with open('library.json', 'r') as book_file:
            book_data = book_file.read()
        final_books_list = json.loads(book_data)

        return final_books_list
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing 'library.json': {e}")
        return []  
      
def generate_short_number():
  """
  This function generates a random four-digit number between 1000 and 9999 (inclusive).
  """
  number = random.randint(1000, 9999)
  return number

def books_list():
    """
    This function print the list of books 
    """
    print("Here's a list of available books:")
    book_list = view_available_books()
    for list in book_list:
     print(f"Book name: 📔{list['title']}, author 👵: {list['author']}, ISBN: {list['ISBN']}")
  
def borrowing_books():
    print("Number of available books 📔:")
    book_list = view_available_books()
    
    available_books = []
    for book in book_list:
        if book['status'] == 'not_borrowed':
            available_books.append([book['title'], book['author'], book['status'], book['ISBN']])
    
    if available_books:
        headers = ["Book Title", "Author", "Status", "ISBN"]
        print(tabulate(available_books, headers=headers, tablefmt="grid"))
    else:
        print("No available books.")
    book_number = input('which book you want to borrow insert ISBN number :')
    user_name = input('please enter your name :')
    adding_user(user_name,book_number)

def returning_book():
    name = input('provide your name: ')
    try:
        with open('user.json', 'r') as user_file:
            user_data = json.load(user_file)
            found_books = []
            for user_entry in user_data:
                if user_entry.get('name') == name:
                    found_books.append(user_entry)
            if found_books:
                headers = found_books[0].keys()
                rows = [book.values() for book in found_books]
                print(tabulate(rows, headers=headers, tablefmt="grid"))
                isbn = input('which book you want to return give ISBN number:')
                
                
                
            else:
                print("No books found for this user.")
    except FileNotFoundError:
        print("User data file not found.")



def library_facility():
    """
    This is the main function calls on the starting of the page load and works according to the conditions 
    """
    facilities = ["Adding Books", "Viewing Available Books", "Searching for Books",
                  "Borrowing Books", "Returning Books"]

    print("What type of library facility do you need 👮‍♀️?")
    for index, facility in enumerate(facilities):
        print(f"{index + 1}: {facility}")

    choice = input("Enter your choice (number): ")
    try:
        choice = int(choice)
        if choice not in range(1, len(facilities) + 1):
            raise ValueError
    except ValueError:
        print("Invalid choice. Please enter a number between 1 and", len(facilities))
        return 

    if choice == 1:
       adding_the_books()
    elif choice == 2:
       books_list()
    elif choice == 3:
       searching_books()
    elif choice == 4:
        # print("Borrowing book functionality is not implemented yet.")
        borrowing_books()
    elif choice == 5:
        print("Returning book functionality is not implemented yet.")
        returning_book()
    else:
        print("Unexpected error. Please try again.")
      
library_facility()
