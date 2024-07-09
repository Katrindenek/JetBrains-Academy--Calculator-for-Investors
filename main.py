import csv
import os

from sqlalchemy import Column, String, Float
from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class MainMenu:
    text = "MAIN MENU\n0 Exit\n1 CRUD operations\n2 Show top ten companies by criteria\nEnter an option:"

    def __init__(self, sql_engine):
        self.options = {
            "0": self.exit,
            "1": self.crud_menu,
            "2": self.show_top_ten,
        }
        self.should_exit = False
        self.engine = sql_engine

    def display(self):
        while not self.should_exit:
            print(self.text)
            choice = input()
            if choice in self.options:
                self.options[choice]()
            else:
                print("Invalid option!")

    def exit(self):
        self.should_exit = True
        print("Have a nice day!")

    def crud_menu(self):
        crud_menu = CrudMenu(self.engine)
        crud_menu.display()

    def show_top_ten(self):
        show_top_ten = ShowTopTenMenu(self.engine)
        show_top_ten.display()


class CrudMenu(MainMenu):
    text = ("CRUD MENU\n0 Back\n1 Create a company\n2 Read a company\n3 Update a company\n4 Delete a company\n5 List "
            "all companies\n\nEnter an option:")

    def __init__(self, sql_engine):
        super().__init__(sql_engine)
        self.options = {
            "0": self.back,
            "1": self.create_company,
            "2": self.read_company,
            "3": self.update_company,
            "4": self.delete_company,
            "5": self.list_companies,
        }
        self.should_exit = False

    def display(self):
        while not self.should_exit:
            print(self.text)
            choice = input()
            if choice in self.options:
                self.options[choice]()
            else:
                self.should_exit = True
                print("Invalid option!")

    def back(self):
        self.should_exit = True

    def create_company(self):
        print("Enter ticker (in the format 'MOON'):")
        ticker = input()
        print("Enter company (in the format 'Moon Corp'):")
        company = input()
        print("Enter industries (in the format 'Technology'):")
        industries = input()
        print("Enter ebitda (in the format '987654321'):")
        ebitda = input()
        print("Enter sales (in the format '987654321'):")
        sales = input()
        print("Enter net profit (in the format '987654321'):")
        net_profit = input()
        print("Enter market price (in the format '987654321'):")
        market_price = input()
        print("Enter net debt (in the format '987654321'):")
        net_debt = input()
        print("Enter assets (in the format '987654321'):")
        assets = input()
        print("Enter equity (in the format '987654321'):")
        equity = input()
        print("Enter cash equivalents (in the format '987654321'):")
        cash_equivalents = input()
        print("Enter liabilities (in the format '987654321'):")
        liabilities = input()
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            company = Company(ticker=ticker, name=company, sector=industries)
            session.add(company)
            financial = Financial(ticker=company.ticker, ebitda=ebitda, sales=sales, net_profit=net_profit,
                                  market_price=market_price, net_debt=net_debt, assets=assets, equity=equity,
                                  cash_equivalents=cash_equivalents, liabilities=liabilities)
            session.add(financial)
            session.commit()
            session.close()
        finally:
            print("Company created successfully!")
            self.back()

    def read_company(self):
        print("Enter company name:")
        company_name = input()
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            companies = session.query(Company).filter(Company.name.ilike(f'%{company_name}%')).all()
            if companies:
                for i, company in enumerate(companies):
                    print(f"{i} {company.name}")

                print("Enter company number:")
                company_number = int(input())
                company_ticker = companies[company_number].ticker
                print(company_ticker, companies[company_number].name)
                financial = session.query(Financial).filter(Financial.ticker == company_ticker).first()
                print("P/E =", round(financial.market_price / financial.net_profit, 2) if financial.net_profit else None)
                print("P/S =", round(financial.market_price / financial.sales, 2) if financial.sales else None)
                print("P/B =", round(financial.market_price / financial.assets, 2) if financial.assets else None)
                print("ND/EBITDA =", round(financial.net_debt / financial.ebitda, 2) if financial.ebitda else None)
                print("ROE =", round(financial.net_profit / financial.equity, 2) if financial.equity else None)
                print("ROA =", round(financial.net_profit / financial.assets, 2) if financial.assets else None)
                print("L/A =", round(financial.liabilities / financial.assets, 2) if financial.assets else None)
            else:
                print("Company not found!")
            session.commit()
            session.close()
        finally:
            self.back()

    def update_company(self):
        print("Enter company name:")
        company_name = input()
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            companies = session.query(Company).filter(Company.name.ilike(f'%{company_name}%')).all()
            if companies:
                for i, company in enumerate(companies):
                    print(f"{i} {company.name}")

                print("Enter company number:")
                company_number = int(input())
                company_ticker = companies[company_number].ticker
                print("Enter ebitda (in the format '987654321'):")
                ebitda = input()
                print("Enter sales (in the format '987654321'):")
                sales = input()
                print("Enter net profit (in the format '987654321'):")
                net_profit = input()
                print("Enter market price (in the format '987654321'):")
                market_price = input()
                print("Enter net debt (in the format '987654321'):")
                net_debt = input()
                print("Enter assets (in the format '987654321'):")
                assets = input()
                print("Enter equity (in the format '987654321'):")
                equity = input()
                print("Enter cash equivalents (in the format '987654321'):")
                cash_equivalents = input()
                print("Enter liabilities (in the format '987654321'):")
                liabilities = input()

                stmt = update(Financial)\
                    .where(Financial.ticker == company_ticker)\
                    .values(ebitda=ebitda, sales=sales, net_profit=net_profit,
                            market_price=market_price, net_debt=net_debt,
                            assets=assets, equity=equity, cash_equivalents=cash_equivalents,
                            liabilities=liabilities)

                session.execute(stmt)
                print("Company updated successfully!")
            else:
                print("Company not found!")
            session.commit()
            session.close()
        finally:
            self.back()

    def delete_company(self):
        print("Enter company name:")
        company_name = input()
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            companies = session.query(Company).filter(Company.name.ilike(f'%{company_name}%')).all()
            if companies:
                for i, company in enumerate(companies):
                    print(f"{i} {company.name}")

                print("Enter company number:")
                company_number = int(input())
                company_ticker = companies[company_number].ticker
                stmt1 = delete(Financial).where(Financial.ticker == company_ticker)
                stmt2 = delete(Company).where(Company.ticker == company_ticker)
                session.execute(stmt1)
                session.execute(stmt2)
                print("Company deleted successfully!")
            else:
                print("Company not found!")
            session.commit()
            session.close()
        finally:
            self.back()

    def list_companies(self):
        print("COMPANY LIST")
        Session = sessionmaker(bind=self.engine)
        session = Session()
        companies = session.query(Company).order_by(Company.ticker).all()
        for company in companies:
            print(company.ticker, company.name, company.sector)
        session.commit()
        session.close()
        self.back()


class ShowTopTenMenu(MainMenu):
    text = "TOP TEN MENU\n0 Back\n1 List by ND/EBITDA\n2 List by ROE\n3 List by ROA\n\nEnter an option:"

    def __init__(self, sql_engine):
        super().__init__(sql_engine)
        self.options = {
            "0": self.back,
            "1": self.list_by_ndebitda,
            "2": self.list_by_roe,
            "3": self.list_by_roa,
        }
        self.should_exit = False

    def display(self):
        while not self.should_exit:
            print(self.text)
            choice = input()
            if choice in self.options:
                self.options[choice]()
            else:
                self.should_exit = True
                print("Invalid option!")

    def back(self):
        self.should_exit = True

    def list_by_ndebitda(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        companies = session.query(Financial).order_by(Financial.net_debt / Financial.ebitda).all()
        print('TICKER', 'ND/EBITDA')
        for i in range(1, 11):
            print(companies[-i].ticker, (round(companies[-i].net_debt / companies[-i].ebitda, 2)
                                        if companies[-i].ebitda else None))
        session.commit()
        session.close()
        self.back()

    def list_by_roe(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        companies = session.query(Financial).order_by(Financial.net_profit / Financial.equity).all()
        print('TICKER', 'ROE')
        for i in range(1, 11):
            print(companies[-i].ticker, (round(companies[-i].net_profit / companies[-i].equity, 2)
                                         if companies[-i].equity else None))
        session.commit()
        session.close()
        self.back()

    def list_by_roa(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        companies = session.query(Financial).order_by(Financial.net_profit / Financial.assets).all()
        print('TICKER', 'ROA')
        for i in range(1, 11):
            print(companies[-i].ticker, (round(companies[-i].net_profit / companies[-i].assets, 2)
                                         if companies[-i].assets else None))
        session.commit()
        session.close()
        self.back()


class Company(Base):
    __tablename__ = 'companies'
    ticker = Column(String(5), primary_key=True, nullable=False)
    name = Column(String(50))
    sector = Column(String(50))


class Financial(Base):
    __tablename__ = 'financial'
    ticker = Column(String(5), primary_key=True, nullable=False)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


def load_data(csv_file, **columns):
    with open(csv_file, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            yield {column: row[column] for column in columns}


if __name__ == '__main__':
    engine = create_engine('sqlite:///investor.db')
    if not os.path.exists("investor.db"):
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        with open("companies.csv", "r", newline="") as companies_file:
            reader = csv.DictReader(companies_file, delimiter=",")
            for row in reader:
                company = Company(ticker=row.get("ticker"), name=row.get("name"), sector=row.get("sector"))
                session.add(company)
            session.commit()

        Session = sessionmaker(bind=engine)
        session = Session()
        with open("financial.csv", "r", newline="") as financial_file:
            reader = csv.DictReader(financial_file, delimiter=",")
            for row in reader:
                for column, value in row.items():
                    if value == '':
                        row[column] = None
                financial = Financial(ticker=row.get("ticker"), ebitda=row.get("ebitda"), sales=row.get("sales"),
                                      net_profit=row.get("net_profit"), market_price=row.get("market_price"),
                                      net_debt=row.get("net_debt"), assets=row.get("assets"),
                                      equity=row.get("equity"), cash_equivalents=row.get("cash_equivalents"),
                                      liabilities=row.get("liabilities"))
                session.add(financial)
            session.commit()
            session.close()

        # print("Database created successfully!")

    print("Welcome to the Investor Program!")
    main_menu = MainMenu(engine)
    main_menu.display()
