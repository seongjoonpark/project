import cx_Oracle

def list_orders_by_customer(cursor, customer_id):
    print(f"고객 ID: {customer_id}의 주문 목록")
    sql = """
    SELECT o.order_id, o.order_date, o.total_amount
    FROM Orders o
    WHERE o.customer_id = :customer_id
    """
    cursor.execute(sql, customer_id=customer_id)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("해당 고객의 주문이 없습니다.")
    else:
        for row in rows:
            print(f"주문 ID: {row[0]}, 주문 날짜: {row[1]}, 총 금액: {row[2]}")
    return rows

def order_query():
    try:
        # 데이터베이스 연결
        conn = cx_Oracle.connect(user="이규현", password="ai", dsn="iedb.kangwon.ac.kr")
        cursor = conn.cursor()

        # 고객 ID 입력
        customer_id = int(input("고객 ID를 입력하세요: "))

        # 고객 ID 확인
        cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id = :customer_id", customer_id=customer_id)
        if cursor.fetchone()[0] == 0:
            raise ValueError("고객 ID가 Customers 테이블에 존재하지 않습니다.")

        # 해당 고객의 주문 리스트 출력
        orders = list_orders_by_customer(cursor, customer_id)
        if not orders:
            return  # 주문이 없으면 종료

        # 주문 ID 입력 후 상세 조회
        order_id = int(input("상세 조회할 주문 ID를 입력하세요: "))
        sql = """
        SELECT o.order_date, c.name, od.product_id, p.name, od.quantity, od.price
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        JOIN OrderDetails od ON o.order_id = od.order_id
        JOIN Products p ON od.product_id = p.product_id
        WHERE o.order_id = :order_id AND o.customer_id = :customer_id
        """
        cursor.execute(sql, order_id=order_id, customer_id=customer_id)
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("주어진 주문 ID와 고객 ID에 대한 데이터가 없습니다.")
        else:
            print(f"주문 ID: {order_id}")
            print("주문 날짜:", rows[0][0], "고객 이름:", rows[0][1])
            for row in rows:
                print("제품 ID:", row[2], "제품 이름:", row[3], "수량:", row[4], "가격:", row[5])

    except cx_Oracle.DatabaseError as e:
        print("데이터베이스 오류:", e)
    except ValueError as e:
        print("값 오류:", e)
    finally:
        # 커서와 연결 닫기
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

# 실행
if __name__ == "__main__":
    order_query()
