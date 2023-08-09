from datetime import datetime

from db.conections import Session, get_db
from db.model import Expenses
from fastapi import Depends, FastAPI
from sqlalchemy import func

app = FastAPI()


@app.post("/expenses/", response_model=Expenses)
def create_expense(expense: Expenses, db: Session = Depends(get_db)):
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

# Route to get monthly expenses


@app.get("/expenses/monthly/")
def get_monthly_expenses(month: int, year: int, db: Session = Depends(get_db)):
    expenses = db.query(Expenses).filter(
        Expenses.month == month, Expenses.year == year).all()
    total_expenses = sum(expense.value for expense in expenses)
    return {"total_expenses": total_expenses, "expenses": expenses}

# Route to get yearly expenses


@app.get("/expenses/yearly/")
def get_yearly_expenses(year: int, db: Session = Depends(get_db)):
    from sqlalchemy.sql import func
    result = db.query(Expenses.month, func.sum(Expenses.value).label("total_monthly_expenses"))\
        .filter(Expenses.year == year)\
        .group_by(Expenses.month)\
        .all()
    return [{"month": row[0], "total_expenses": row[1]} for row in result]
