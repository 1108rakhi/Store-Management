from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    conn.close()
    return result

@router.post("/")
def add_product(name: str, price: float, quantity: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
        (name, price, quantity)
    )
    conn.commit()
    conn.close()
    return {"message": "Product added successfully"}

@router.put("/{product_id}")
def update_product(product_id: int, name: str, price: float, quantity: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s",
        (name, price, quantity, product_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Product updated"}

@router.delete("/{product_id}")
def delete_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    conn.commit()
    conn.close()
    return {"message": "Product deleted"}
