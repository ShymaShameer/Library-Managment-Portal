import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
connection_string = st.secrets["connection_string"]

#connection_string = 'mysql+pymysql://root:shymamysql@127.0.0.1:3306/liane_library'

# DELETE FRIEND
def delete_friend(friend_id):
    engine = create_engine(connection_string)
    query = text("""
        DELETE FROM friends
        WHERE friend_id = :friend_id
    """)

    with engine.begin() as conn:
        res = conn.execute(query, {"friend_id": friend_id})
        #  if the friend ID didn't exist in the database
        if res.rowcount == 0:
            raise ValueError(f"No friend found with ID {friend_id}.")
            
    return f"Successfully deleted Friend ID {friend_id} from the directory."


# DELETE BOOK
def delete_book(book_id):
    engine = create_engine(connection_string)

# to block deletion if the book has any loan history
    check_query = text("""
        SELECT COUNT(*) as total_loans
        FROM loans
        WHERE book_id = :book_id
    
    """)
    
    query = text("""
        DELETE FROM books
        WHERE book_id = :book_id
    """)

    with engine.begin() as conn:
# to check if book is borrowed
        result = conn.execute(check_query, {"book_id": book_id}).fetchone()
        
        if result[0] > 0:
            raise ValueError(f"Book ID {book_id} cannot be deleted because it is currently borrowed or has a loan history.")

        res = conn.execute(query, {"book_id": book_id})
        #  if the book ID didn't exist in the database
        if res.rowcount == 0:
            raise ValueError(f"No book found with ID {book_id}.")
            
    return f"Successfully deleted Book ID {book_id} from inventory."


# DELETE LOAN
def delete_loan(loan_id):
    engine = create_engine(connection_string)
    query = text("""
        DELETE FROM loans
        WHERE loan_id = :loan_id
    """)

    with engine.begin() as conn:
        res= conn.execute(query, {"loan_id": loan_id})
        #  if the loan ID didn't exist in the database
        if res.rowcount == 0:
            raise ValueError(f"No loan found with ID {loan_id}.")
            
    return f"Successfully deleted Loan ID {loan_id} from the register."