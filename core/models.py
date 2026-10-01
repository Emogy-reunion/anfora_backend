from core.extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func
from datetime import timezone,date,datetime
import uuid


class BaseModel(db.Model):
    '''
    an abstract model to define fields used by all tables
    it won't be created in the database
    '''
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    modified_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            onupdate=func.now(),
                            nullable=False)

class User(BaseModel):
    '''
    stores the company's authentication data
    '''
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    company_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    admin_firstname = db.Column(db.String(255), nullable=False)
    admin_lastname = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, password=None, **kwargs):
        super().__init__(**kwargs)

        if password:
            self.password = password

    @property
    def password(self):
        raise AttributeError("Password is write-only and cannot be read.")

    @password.setter
    def password(self, plain_text_password):
        # Ensure the hash is stored as a string
        hashed = bcrypt.generate_password_hash(plain_text_password)
        if isinstance(hashed, bytes):
            hashed = hashed.decode('utf-8')
        self.password_hash = hashed

    def verify_password(self, plain_text_password):
        return bcrypt.check_password_hash(self.password_hash, plain_text_password)


class Profile(BaseModel):
    '''
    stores the company's profile information data
    '''
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    logo_url = db.Column(db.String(255), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    default_currency = db.Column(db.String(3), nullable=False)

    website = db.Column(db.String(255), nullable=True)
    legal_business_name = db.Column(db.String(255), nullable=True)
    tax_identification_number = db.Column(db.String(100), nullable=True)
    default_payment_terms = db.Column(db.Integer, default=30, nullable=False)
    default_notes = db.Column(db.Text, nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    address_line2 = db.Column(db.String(255), nullable=True)
    


class CostSheet(db.Model):
    __tablename__ = "cost_sheets"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), default="Safari Expedition Package")
    client_id = db.Column(db.Integer, nullable=True) 
    
    total_cost_price = db.Column(db.Float, nullable=False)
    markup_percentage = db.Column(db.Float, nullable=False)
    target_profit = db.Column(db.Float, nullable=False)
    suggested_selling_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Draft")

    
    items = db.relationship(
        "CostItem", 
        back_populates="cost_sheet", 
        cascade="all, delete-orphan"
    )


class CostItem(db.Model):
    __tablename__ = "cost_items"

    id = db.Column(db.Integer, primary_key=True)
    cost_sheet_id = db.Column(db.Integer, db.ForeignKey("cost_sheets.id"), nullable=False)
    
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    
    cost_sheet = db.relationship("CostSheet", back_populates="items")
    
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100), unique=True, nullable=False)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=True) 
    client_id = db.Column(db.Integer, nullable=False) 
    
    status = db.Column(db.String(50), default="Unpaid")
    issue_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, default=0.0)
    balance_due = db.Column(db.Float, nullable=False)
    
    notes = db.Column(db.Text, nullable=True)

    
    items = db.relationship(
        "InvoiceItem", 
        back_populates="invoice", 
        cascade="all, delete-orphan"
    )


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    
    invoice = db.relationship("Invoice", back_populates="items")
class Quotation(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)
    quotation_number = db.Column(db.String(100), unique=True, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)  # Adjust to match your client/user reference if needed
    
    expiry_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default="Draft")
    
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    notes = db.Column(db.Text, nullable=True)

    
    items = db.relationship(
        "QuotationItem", 
        back_populates="quotation", 
        cascade="all, delete-orphan"
    )

    
    invoices = db.relationship("Invoice", backref="quotation", lazy=True)


class QuotationItem(db.Model):
    __tablename__ = "quotation_items"

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=False)
    
    description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    
    quotation = db.relationship("Quotation", back_populates="items")
    
class GeneratedLetter(db.Model):
    __tablename__ = "generated_letters"

    id = db.Column(db.Integer, primary_key=True)
    letter_type = db.Column(db.String(100), nullable=False)
    recipient_email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default="Generated")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Itinerary(db.Model):
    __tablename__ = "itineraries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default="Safari Expedition Itinerary")
    client_id = db.Column(db.Integer, nullable=True)
    cost_sheet_id = db.Column(db.Integer, db.ForeignKey("cost_sheets.id"), nullable=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=True)
    
    duration_days = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(50), default="Draft")
    notes = db.Column(db.Text, nullable=True)

    
    days = db.relationship(
        "ItineraryDay", 
        back_populates="itinerary", 
        cascade="all, delete-orphan",
        order_by="ItineraryDay.day_number"
    )


class ItineraryDay(db.Model):
    __tablename__ = "itinerary_days"

    id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)
    
    day_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    accommodation = db.Column(db.String(255), nullable=True)
    meals = db.Column(db.String(100), nullable=True) 

    
    itinerary = db.relationship("Itinerary", back_populates="days")
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(100), unique=True, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    
    # Optional foreign key ties to your workflow documents
    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=True)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    num_adults = db.Column(db.Integer, default=1)
    num_children = db.Column(db.Integer, default=0)
    
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(50), default="Pending")  # e.g., Pending, Confirmed, Completed, Cancelled
    notes = db.Column(db.Text, nullable=True)
    
class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)  
    contact_person = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    payment_terms = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    
    services = db.relationship(
        "SupplierServiceItem", 
        back_populates="supplier", 
        cascade="all, delete-orphan"
    )


class SupplierServiceItem(db.Model):
    __tablename__ = "supplier_service_items"

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    
    item_name = db.Column(db.String(255), nullable=False)  
    description = db.Column(db.Text, nullable=True)
    unit_cost = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="USD")

    
    supplier = db.relationship("Supplier", back_populates="services")