import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
connection_string = st.secrets["connection_string"]
#connection_string = 'mysql+pymysql://root:shymamysql@127.0.0.1:3306/liane_library'

def create_friend(first_name,last_name,email,phone, max_loan=2, notes=None):
    engine = create_engine(connection_string)
    df= pd. DataFrame(
        [[first_name,last_name,email,phone, max_loan, notes]], columns= ["first_name","last_name","email","phone","max_loan", "notes"])
    df.to_sql(
        "friends", if_exists="append", con=connection_string, index=False)
    message = f"Added '{first_name} {last_name}' to 'friends'."
    return message


def create_book(title,author,isbn,genre, comments, is_available, date_added=pd.Timestamp.today().date()):
    engine = create_engine(connection_string)
    if is_available is None:
        is_available = True
# Check for duplicate ISBN before inserting
    if isbn:
        existing = pd.read_sql(
            "SELECT COUNT(*) as count FROM books WHERE isbn = %s",
            con=connection_string,
            params=(isbn,)
        )
        if existing["count"][0] > 0:
            raise ValueError(f"A book with ISBN '{isbn}' already exists in the inventory.")
        
    df = pd. DataFrame(
        [[title,author,isbn,genre, comments, is_available, date_added]], 
        columns= ["title","author","isbn","genre","comments","is_available","date_added"])
    df.to_sql(
        "books", if_exists="append", con=connection_string, index=False)
    message = f"Added '{title}' to 'books'."
    return message

def create_loan(book, friend, loan_status, remarks=None, due_date=None, date_returned=None, date_borrowed=None):
    engine = create_engine(connection_string)
    # Dates
    if date_borrowed is None:
        date_borrowed = pd.Timestamp.today().date()
    else:
        date_borrowed = pd.to_datetime(date_borrowed).date()

    if due_date is None:
        # If no due date is given, automatically default to 14 days from the borrow date
        due_date = date_borrowed + pd.Timedelta(days=14)
    else:
        due_date = pd.to_datetime(due_date).date()

    if date_returned is not None:
        date_returned = pd.to_datetime(date_returned).date()

    # status defaults & validation
    if loan_status is None:
        loan_status = "BORROWED"
    else:
        loan_status = loan_status.upper()

    # validation on borrowed & due dates
    if due_date < date_borrowed:
        raise ValueError(
            f"Validation Error: Due date ({due_date}) cannot be earlier than the borrow date ({date_borrowed})."
        )

    allowed_statuses = {"BORROWED", "RETURNED", "OVERDUE"}
    if loan_status not in allowed_statuses:
        raise ValueError(
            f"Validation Error: Invalid loan status '{loan_status}'. Must be one of {allowed_statuses}."
        )

   
    df = pd.DataFrame(
        [[book["book_id"], friend["friend_id"], date_borrowed, due_date, date_returned, loan_status, remarks]], 
        columns=["book_id", "friend_id", "date_borrowed", "due_date", "date_returned", "loan_status", "remarks"]
    )
    
    df.to_sql("loans", if_exists="append", con=connection_string, index=False)
    
    message = f"Added new book loan on '{date_borrowed}' to 'loans'."
    return message