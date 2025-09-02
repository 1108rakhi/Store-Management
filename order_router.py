from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(customer_id: int, items: list[dict]):
    """
    items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Step 1: Create order
        cursor.execute("INSERT INTO orders (customer_id) VALUES (%s)", (customer_id,))
        order_id = cursor.lastrowid

        total_cost = 0

        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]

            # Step 2: Get product price and stock
            cursor.execute("SELECT price, quantity FROM products WHERE id=%s", (product_id,))
            product = cursor.fetchone()

            if not product:
                raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

            if product["quantity"] < quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product_id}")

            # Step 3: Add to order_items
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (order_id, product_id, quantity))

            # Step 4: Reduce product stock
            cursor.execute("""
                UPDATE products SET quantity = quantity - %s WHERE id = %s
            """, (quantity, product_id))

            total_cost += product["price"] * quantity

        # Step 5: Update total in orders table
        cursor.execute("UPDATE orders SET total = %s WHERE id = %s", (total_cost, order_id))

        conn.commit()
        conn.close()
        return {"message": "Order placed", "order_id": order_id, "total": total_cost}

    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    for order in orders:
        cursor.execute("""
            SELECT p.name, oi.quantity 
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order["id"],))
        order["items"] = cursor.fetchall()

    conn.close()
    return orders
