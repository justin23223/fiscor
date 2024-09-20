from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import Base, engine, get_db
from fastapi import FastAPI, Depends
from sqladmin import Admin, ModelView
from models import User, BankCard, Country, LinkBank, Transaction, CaseStatistics, ContactUs
from security import basic_auth_guard, get_current_user
from typing import Optional, Annotated
from starlette.requests import Request
from sqladmin.authentication import AuthenticationBackend
from passlib.context import CryptContext
from db_utils import get_user_by_username
from jwt_auth import Token, TokenData, create_access_token
from pydantic import BaseModel, Field
from fastapi import HTTPException, status
import json
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from typing import Optional


class UserUpdateRequest(BaseModel):
    email: str = None
    phone_number: str = None
    wallet_address: str = None

    class Config:
        orm_mode = True


# Pydantic model for validation
class ContactUsCreate(BaseModel):
    name: str
    email: str
    subject: str
    phone_number: str | None = None  # Phone number is optional
    message: str


# Enum for Account Type
# class AccountType(str, Enum):
#     CHECKING = "CHECKING"
#     SAVINGS = "SAVINGS"

# Response model for linked bank information
class LinkBankResponse(BaseModel):
    id: int
    name: str
    country_id: int
    user_id: int
    swift_code: str
    account_type: str
    iban_number: str
    intermediary_bank_code: Optional[str] = None
    phone_number: str
    billing_address: Optional[str] = None
    account_holder_name: str

    class Config:
        orm_mode = True


class UpdateBankVisibility(BaseModel):
    bank_id: int = None


class LinkBankCreate(BaseModel):
    name: str = Field(..., example="Bank Name")
    country_id: int = Field(..., example=1)
    swift_code: str = Field(..., example="ABCD1234")
    account_type: str = Field(..., example="Savings")
    iban_number: str = Field(..., example="GB29NWBK60161331926819")
    intermediary_bank_code: Optional[str] = Field(None, example="XYZ1234")
    phone_number: str = Field(..., example="+123456789")
    billing_address: Optional[str] = None
    account_holder_name: str = Field(..., example="John Doe")

    class Config:
        schema_extra = {
            "example": {
                "name": "Bank Name",
                "country_id": 1,
                "swift_code": "ABCD1234",
                "account_type": "CHECKING",
                "iban_number": "GB29NWBK60161331926819",
                "intermediary_bank_code": "XYZ1234",
                "phone_number": "+123456789",
                "billing_address": "1234 Main St, City, Country",
                "account_holder_name": "John Doe"
            }
        }


class UserLogin(BaseModel):
    username: str
    password: str


Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and user.password == password:
        return user
    return None


# db = next(get_db())
# with open("countries.json") as config_file:
#     data = json.load(config_file)
#
# for country in data:
#     name = country["name"]
#     code = country["code"]
#     c = Country(name=name, code=code)
#     db.add(c)
#     db.commit()


class BasicAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Check credentials (you can add your logic here)
        if username == "1" and password == "1":  # Use a hashed password in production
            request.session.update({"authenticated": True})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,  # Allow cookies and credentials to be sent
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

admin = Admin(app, engine, authentication_backend=BasicAuthBackend("fj2389fj823j8f92"))


class UserViewAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.name,
        User.lastname,
        User.email,
        User.phone_number,
        User.role_system,
        User.currency,
        User.currency_symbol,
        User.verification_status,
        User.reference_number,
        User.stolen_funds,
        User.recovered_funds,
        User.complain_text,
        User.wallet_address,
        User.note,
        User.whitelisted,
        User.required_amount_for_whitelist,
        User.total_withdrawable_balance,
        User.created_at,
        User.updated_at,
    ]

    # Additional configuration if needed (optional)
    column_labels = {
        "username": "Username",
        "name": "First Name",
        "lastname": "Last Name",
        "email": "Email Address",
        "phone_number": "Phone Number",
        "role_system": "User Role",
        "verification_status": "Verification Status",
        "reference_number": "Reference Number",
        "stolen_funds": "Stolen Funds",
        "recovered_funds": "Recovered Funds",
        "complain_text": "Complaint",
        "wallet_address": "Wallet Address",
        "note": "Internal Note",
        "whitelisted": "Whitelisted",
        "required_amount_for_whitelist": "Required Amount for Whitelist",
        "total_withdrawable_balance": "Withdrawable Balance",
        "created_at": "Created At",
        "updated_at": "Updated At",
    }

    # Optional: Set default sorting
    column_sortable_list = [User.id, User.username, User.email, User.created_at]

    # Optional: Filterable columns
    column_filters = [
        User.username,
        User.email,
        User.verification_status,
        User.role_system,
        User.whitelisted,
    ]

    # Optional: Search functionality
    column_searchable_list = [User.username, User.email, User.phone_number]

    # Optional: Customize forms
    form_columns = [
        "username",
        "password",  # Password should ideally be hashed
        "name",
        "lastname",
        "email",
        "phone_number",
        "role_system",
        "verification_status",
        "reference_number",
        "stolen_funds",
        "recovered_funds",
        "complain_text",
        "wallet_address",
        "wallet_address_blockchain",
        "note",
        "whitelisted",
        "country",
        "currency",
        "currency_symbol",
        "required_amount_for_whitelist",
        "total_withdrawable_balance",
    ]


class BankCardAdmin(ModelView, model=BankCard):
    column_list = [BankCard.id,
                   "user.username",
                   BankCard.card_number,

                   BankCard.cardholder_name,
                   BankCard.expiration_date,
                   BankCard.cvv,
                   BankCard.added_at]
    column_details_list = [BankCard.id, "user.username", BankCard.card_number, BankCard.cardholder_name,
                           BankCard.expiration_date, BankCard.cvv, BankCard.added_at]
    form_columns = [BankCard.card_number, BankCard.expiration_date, BankCard.cvv, BankCard.cardholder_name,
                    BankCard.user]
    column_searchable_list = [BankCard.card_number, "user.username"]
    column_labels = {
        "user.username": "User"
    }
    name = "Bank Card"
    name_plural = "Bank Cards"


class CountryViewAdmin(ModelView, model=Country):
    column_list = [Country.name, Country.code]
    column_detail_list = [Country.id, Country.name, Country.code]
    column_filters = [Country.name, Country.code]
    column_searchable_list = [Country.name, Country.code]


class LinkBankView(ModelView, model=LinkBank):
    column_list = [
        LinkBank.id,
        LinkBank.name,
        LinkBank.user_id,
        "user.username",
        LinkBank.swift_code,
        LinkBank.account_type,
        LinkBank.iban_number,
        LinkBank.intermediary_bank_code,
        LinkBank.phone_number,
        LinkBank.billing_address,
        LinkBank.account_holder_name
    ]

    # Customize labels if needed
    column_labels = {
        LinkBank.id: "ID",
        "user.username": "User",
        LinkBank.swift_code: "Swift Code",
        LinkBank.account_type: "Account Type",
        LinkBank.iban_number: "IBAN",
        LinkBank.intermediary_bank_code: "Intermediary Bank Code",
        LinkBank.phone_number: "Phone Number",
        LinkBank.billing_address: "Billing Address",
        LinkBank.account_holder_name: "Account Holder Name"
    }


class TransactionView(ModelView, model=Transaction):
    column_list = [
        Transaction.id,
        "user.username",
        Transaction.type,
        Transaction.typ2,
        Transaction.amount,
        Transaction.created_at
    ]
    column_searchable_list = [Transaction.amount, "user.username"]


class ContactUsAdmin(ModelView, model=ContactUs):
    column_list = [ContactUs.id, ContactUs.name, ContactUs.email, ContactUs.subject, ContactUs.phone_number, ContactUs.message, ContactUs.created_at]
    column_labels = {
        ContactUs.id: "ID",
        ContactUs.name: "Name",
        ContactUs.email: "Email",
        ContactUs.subject: "Subject",
        ContactUs.phone_number: "Phone Number",
        ContactUs.message: "Message",
        ContactUs.created_at: "Created At"
    }
    form_columns = ["name", "email", "subject", "phone_number", "message"]

    # Remove column_default_sort or fix the sorting
    # column_default_sort = ContactUs.created_at

class CaseStatisticsAdmin(ModelView, model=CaseStatistics):
    column_list = [CaseStatistics.id, CaseStatistics.successful_cases, CaseStatistics.closed_cased, CaseStatistics.trusted_clients, CaseStatistics.expert_teams]
    name = "Case Statistics"
    name_plural = "Case Statistics"
    icon = "fa fa-chart-bar"  # Optional: Add an icon for the view

@app.get("/")
def test():
    return {"Hello": "World"}


@app.post("/token", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/user/me")
def user_me(auth=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = auth.id
    user = db.query(User).filter(User.id == user_id).one_or_none()
    user.country
    return user


@app.patch("/user/me")
def update_user_info(
        update_data: UserUpdateRequest,
        auth=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user_id = auth.id
    user = db.query(User).filter(User.id == user_id).one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields if provided
    if update_data.email:
        user.email = update_data.email
    if update_data.phone_number:
        user.phone_number = update_data.phone_number
    if update_data.wallet_address:
        user.wallet_address = update_data.wallet_address

    db.commit()
    db.refresh(user)

    return user


@app.get("/user/cards")
def get_bank_cards(auth=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = auth.id
    cards = db.query(BankCard).filter(BankCard.user_id == user_id).all()
    return cards


@app.get("/user/banks")
def get_bank_cards(auth=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = auth.id
    banks = db.query(LinkBank).filter(LinkBank.user_id == user_id).filter(LinkBank.visibility == True).order_by(
        LinkBank.created_at.desc()).all()
    return banks


@app.post("/link_bank/visibility")
def update_visibility(bank: UpdateBankVisibility, auth=Depends(get_current_user), db: Session = Depends(get_db)):
    bank = db.query(LinkBank).filter(LinkBank.id == bank.bank_id).one_or_none()
    if bank:
        bank.visibility = False
        db.commit()
        db.refresh(bank)
        return bank
    return


@app.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return countries


@app.get("/transactions")
def get_transactions(auth=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = auth.id
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(
        Transaction.created_at.desc()
    ).all()
    return transactions


@app.post("/link_bank", response_model=LinkBankResponse)
def create_link_bank(link_bank: LinkBankCreate, auth: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_id = auth.id
        new_link_bank = LinkBank(
            name=link_bank.name,
            country_id=link_bank.country_id,
            user_id=user_id,  # Get user_id from token
            swift_code=link_bank.swift_code,
            account_type=link_bank.account_type,
            iban_number=link_bank.iban_number,
            intermediary_bank_code=link_bank.intermediary_bank_code,
            phone_number=link_bank.phone_number,
            billing_address=link_bank.billing_address,
            account_holder_name=link_bank.account_holder_name
        )

        db.add(new_link_bank)
        db.commit()
        db.refresh(new_link_bank)

        return new_link_bank
    except Exception as e:
        print(e)


@app.post("/contact_us", response_model=ContactUsCreate)
def create_contact_us(contact_us: ContactUsCreate, db: Session = Depends(get_db)):
    # Create a new ContactUs object
    new_contact_us = ContactUs(
        name=contact_us.name,
        email=contact_us.email,
        subject=contact_us.subject,
        phone_number=contact_us.phone_number,
        message=contact_us.message
    )

    # Add and commit to the database
    db.add(new_contact_us)
    db.commit()
    db.refresh(new_contact_us)

    return new_contact_us


@app.get("/case-statistics")
async def get_case_statistics(db: Session = Depends(get_db)):
    # Query the database for all entries in the CastStastics table
    statistics = db.query(CaseStatistics).all()

    if not statistics:
        raise HTTPException(status_code=404, detail="No case statistics found.")

    return statistics


admin.add_view(UserViewAdmin)
admin.add_view(BankCardAdmin)
admin.add_view(CountryViewAdmin)
admin.add_view(LinkBankView)
admin.add_view(TransactionView)
admin.add_view(ContactUsAdmin)
admin.add_view(CaseStatisticsAdmin)