from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/")
def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    conn.close()
    return result

@router.post("/")
def add_customer(name: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
    conn.close()
    return {"message": "Customer added successfully"}

@router.put("/{customer_id}")
def update_customer(customer_id: int, name: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name=%s, email=%s WHERE id=%s", (name, email, customer_id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated"}

@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=%s", (customer_id,))
    conn.commit()
    conn.close()
    return {"message": "Customer deleted"}
