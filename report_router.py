from fastapi import APIRouter
from database import get_connection

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/total-sales")
def total_sales():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total) FROM orders")
    result = cursor.fetchone()[0]
    conn.close()
    return {"total_sales": result or 0}


@router.get("/top-products")
def top_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.name, SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.id
        ORDER BY total_sold DESC
        LIMIT 5
    """)
    result = cursor.fetchall()
    conn.close()
    return {"top_products": result}


@router.get("/daily-summary")
def daily_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DATE(created_at) AS order_date, COUNT(*) AS total_orders, SUM(total) AS daily_sales
        FROM orders
        GROUP BY DATE(created_at)
        ORDER BY order_date DESC
    """)
    result = cursor.fetchall()
    conn.close()
    return {"daily_summary": result}
