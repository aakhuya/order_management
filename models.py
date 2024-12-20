from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}')"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="orders")

    def __repr__(self):
        return f"Order(id={self.id}, description='{self.description}', amount={self.amount}, customer_id={self.customer_id})"