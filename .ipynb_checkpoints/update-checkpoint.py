import pandas as pd
from sqlalchemy import create_engine, text
connection_string = 'mysql+pymysql://root:shymamysql@127.0.0.1:3306/liane_library'

def update_friend(friend_id, first_name=None, last_name= None, email=None, phone=None,notes= None,max_loan= 2):
    engine = create_engine(connection_string)
    updates = []
    params = {"friend_id": friend_id}

    if first_name is not None:
        updates.append("first_name = :first_name")
        params["first_name"] = first_name
        
    if last_name is not None:
        updates.append("last_name = :last_name")
        params["last_name"] = last_name

    if email is not None:
        updates.append("email = :email")
        params["email"] = email

    if phone is not None:
        updates.append("phone = :phone")
        params["phone"] = phone
        
    if max_loan is not None:
        updates.append("max_loan = :max_loan")
        params["max_loan"] = max_loan
        
    if notes is not None:
        updates.append("notes = :notes")
        params["notes"] = notes
        
    if not updates:
        return

    query = text(f"""
        UPDATE friends
        SET {", ".join(updates)}
        WHERE friend_id = :friend_id
    """)
   
    with engine.begin() as conn:
        res = conn.execute(query, params)
        if res.rowcount == 0: raise ValueError(f"No friend found with ID {friend_id}.")
    return f"Successfully Updated Friend ID {friend_id}."
    

    
def update_book(book_id, title=None, author=None, isbn=None, genre=None, comments=None, is_available=None):
    engine = create_engine(connection_string)
    
    # Track the pieces of our SQL SET statement and parameters
    updates = []
    params = {"book_id": book_id}

    # Conditionally build the query based on what the user supplied
    if title is not None and title.strip() != "":
        updates.append("title = :title")
        params["title"] = title

    if author is not None and author.strip() != "":
        updates.append("author = :author")
        params["author"] = author

    if isbn is not None and isbn.strip() != "":
        updates.append("isbn = :isbn")
        params["isbn"] = isbn

    if genre is not None and genre.strip() != "":
        updates.append("genre = :genre")
        params["genre"] = genre

    if comments is not None and comments.strip() != "":
        updates.append("comments = :comments")
        params["comments"] = comments

    if is_available is not None:
        updates.append("is_available = :is_available")
        params["is_available"] = is_available

    # Guard clause: If the user clicked save without altering any inputs, exit early!
    if not updates:
        return "No changes were submitted."

    # Construct the query dynamically using join strings
    query = text(f"""
        UPDATE books
        SET {", ".join(updates)}
        WHERE book_id = :book_id
    """)

    with engine.begin() as conn:
        result = conn.execute(query, params)
        if result.rowcount == 0:
            raise ValueError(f"No book found with ID {book_id}.")
            
    return f"Successfully updated Book ID {book_id}."

def update_loan(
    loan_id,
    book_id=None,
    friend_id=None,
    date_borrowed=None,
    due_date= None,
    date_returned=None,
    loan_status= None,
    remarks= None
):
    engine = create_engine(connection_string)
    updates = []
    params = {"loan_id": loan_id}

    if book_id is not None:
        updates.append("book_id = :book_id")
        params["book_id"] = book_id

    if friend_id is not None:
        updates.append("friend_id = :friend_id")
        params["friend_id"] = friend_id

    if date_borrowed is not None:
        updates.append("date_borrowed = :date_borrowed")
        params["date_borrowed"] = date_borrowed
        
    if due_date is not None:
        updates.append("due_date = :due_date")
        params["due_date"] = due_date
        
    if date_returned is not None:
        updates.append("date_returned = :date_returned")
        params["date_returned"] = date_returned
        
    if loan_status is not None:
        updates.append("loan_status = :loan_status")
        params["loan_status"] = loan_status
        
    if remarks is not None:
        updates.append("remarks = :remarks")
        params["remarks"] = remarks
        
    if not updates:
        raise ValueError("No fields to update.")

    query = text(f"""
        UPDATE loans
        SET {", ".join(updates)}
        WHERE loan_id = :loan_id
    """)

 # --- SYNC is_available IN BOOKS ---
        # If status is RETURNED → mark book as available
        # If status is BORROWED or OVERDUE → mark book as unavailable
    if loan_status is not None:
            if loan_status == "RETURNED":
                conn.execute(text("""
                    UPDATE books SET is_available = 1
                    WHERE book_id = (SELECT book_id FROM loans WHERE loan_id = :loan_id)
                """), {"loan_id": loan_id})
            else:
                conn.execute(text("""
                    UPDATE books SET is_available = 0
                    WHERE book_id = (SELECT book_id FROM loans WHERE loan_id = :loan_id)
                """), {"loan_id": loan_id})
        
        # If date_returned is set but status wasn't changed, still mark as available
    if date_returned is not None and loan_status is None:
            conn.execute(text("""
                UPDATE books SET is_available = 1
                WHERE book_id = (SELECT book_id FROM loans WHERE loan_id = :loan_id)
            """), {"loan_id": loan_id})

    
    
    with engine.begin() as conn:
        res= conn.execute(query, params)
        if res.rowcount == 0: raise ValueError(f"No loan found with ID {loan_id}.")
    return f"Successfully Updated Loan ID {loan_id}."