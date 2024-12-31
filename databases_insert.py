import cx_Oracle

def order_input():
    try:
        # 데이터베이스 연결
        conn = cx_Oracle.connect(user="박성준", password="ai", dsn="iedb.kangwon.ac.kr")
        cursor = conn.cursor()

        # 주문 입력
        customer_id = int(input("고객 ID: "))
        order_date = input("주문 날짜 (YYYY-MM-DD): ")
        total_amount = float(input("총 금액: "))

        # 고객 ID 확인
        cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id = :customer_id", customer_id=customer_id)
        if cursor.fetchone()[0] == 0:
            raise ValueError("고객 ID가 Customers 테이블에 존재하지 않습니다.")

        # 주문 생성
        order_sql = """
        INSERT INTO Orders (order_id, customer_id, order_date, total_amount)
        VALUES (order_seq.NEXTVAL, :customer_id, TO_DATE(:order_date, 'YYYY-MM-DD'), :total_amount)
        """
        cursor.execute(order_sql, customer_id=customer_id, order_date=order_date, total_amount=total_amount)

        # 최근 생성된 Order ID 조회
        cursor.execute("SELECT order_seq.CURRVAL FROM dual")
        order_id = cursor.fetchone()[0]
        print(f"주문이 성공적으로 추가되었습니다. 주문 ID: {order_id}")

        # 주문 상세 입력
        while True:
            product_id = int(input("제품 ID: "))
            quantity = int(input("수량: "))
            price = float(input("가격: "))

            # 제품 ID 확인
            cursor.execute("SELECT COUNT(*) FROM Products WHERE product_id = :product_id", product_id=product_id)
            if cursor.fetchone()[0] == 0:
                raise ValueError("제품 ID가 Products 테이블에 존재하지 않습니다.")

            detail_sql = """
            INSERT INTO OrderDetails (detail_id, order_id, product_id, quantity, price)
            VALUES (order_detail_seq.NEXTVAL, order_seq.CURRVAL, :product_id, :quantity, :price)
            """
            cursor.execute(detail_sql, product_id=product_id, quantity=quantity, price=price)
            conn.commit()

            more = input("더 많은 제품을 추가하시겠습니까? (yes/no): ")
            if more.lower() != 'yes':
                break

        print("주문 및 상세 정보가 성공적으로 추가되었습니다!")

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
    order_input()
