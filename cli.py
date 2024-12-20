import sys
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///customers.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    
    orders = relationship("Order", backref="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name={self.name}, email={self.email})>"

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    def __repr__(self):
        return f"<Order(id={self.id}, description={self.description}, amount={self.amount}, customer_id={self.customer_id})>"

def init_db():
    Base.metadata.create_all(engine)
    print("Database Initialized")

def create_customer():
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    customer = Customer(name=name, email=email)
    session.add(customer)
    session.commit()
    print(f"Customer '{name}' created with ID {customer.id}")

def create_order():
    customer_id = int(input("Enter customer ID: "))
    customer = session.get(Customer, customer_id)
    if not customer:
        print(f"Customer with ID {customer_id} does not exist.")
        return
    
    description = input("Enter order description: ")
    amount = int(input("Enter order amount: "))
    order = Order(description=description, amount=amount, customer_id=customer_id)
    session.add(order)
    session.commit()
    print(f"Order '{description}' created for customer ID {customer_id}")

def update_order():
    order_id = int(input("Enter Order ID to update: "))
    order = session.get(Order, order_id)
    if not order:
        print(f"Order with ID {order_id} does not exist.")
        return
    
    order.description = input(f"Enter new description for order (current: {order.description}): ") or order.description
    order.amount = int(input(f"Enter new amount for order (current: {order.amount}): ") or order.amount)
    session.commit()
    print(f"Order ID {order_id} updated successfully")

def delete_order():
    order_id = int(input("Enter Order ID to delete: "))
    order = session.get(Order, order_id)
    if not order:
        print(f"Order with ID {order_id} does not exist.")
        return
    session.delete(order)
    session.commit()
    print(f"Order ID {order_id} deleted successfully.")

def view_orders_by_customer():
    customer_id = int(input("Enter customer ID to view orders: "))
    customer = session.get(Customer, customer_id)
    if not customer:
        print(f"Customer with ID {customer_id} does not exist.")
        return
    
    orders = customer.orders
    if not orders:
        print(f"No orders found for customer with ID {customer_id}.")
        return
    
    print(f"Orders for Customer '{customer.name}' (ID {customer_id}):")
    for order in orders:
        print(order)

def list_customers_and_orders():
    customers = session.query(Customer).all()
    if not customers:
        print("No customers found.")
        return
    for customer in customers:
        print(f"Customer: {customer}")
        for order in customer.orders:
            print(f"  - {order}")

def main_menu():
    while True:
        print("\nWelcome to the Customer-Order Application. What would you like to do?")
        print("1. Create Customer")
        print("2. Create Order for Customer")
        print("3. Update Order")
        print("4. Delete Order")
        print("5. View Orders by Customer")
        print("6. List Customers and their Orders")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_customer()
        elif choice == "2":
            create_order()
        elif choice == "3":
            update_order()
        elif choice == "4":
            delete_order()
        elif choice == "5":
            view_orders_by_customer()
        elif choice == "6":
            list_customers_and_orders()
        elif choice == "7":
            print("Exiting.......")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    init_db()
    main_menu()
