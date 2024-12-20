from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Enum
from . import db 
import enum

# Define roles
class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

# Define statuses 
class TicketStatus(enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"

# Define priorities 
class TicketPriority(enum.Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for the user
    email = db.Column(db.String(150), unique=True) # User's email
    password = db.Column(db.String(150)) # User's hashed password
    full_name = db.Column(db.String(150))  # Full name of the user
    job_title = db.Column(db.String(150))  # job title for context
    role = db.Column(db.String(10), default="user")  # "user" or "admin"
    tickets = db.relationship('Ticket', backref='creator', lazy=True)  # Connect tickets to users

    def is_admin(self):
        """Check if the user is an admin."""
        return self.role == UserRole.ADMIN
    
    def __str__(self):
        return f"{self.full_name} ({self.email}) - Role: {self.role.value}"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # Title of the ticket
    description = db.Column(db.Text, nullable=False)  # Details about the issue or task
    priority = db.Column(db.String(10), nullable=False) # Priority level
    status = db.Column(db.String(50), default="Open")  # Default status is "Open"
    assigned_to = db.Column(db.String(100), nullable=True)  # Name or ID of the person assigned to the ticket
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # ID of the user who created the ticket
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())  # Timestamp for when the ticket was created

    def __str__(self):
        return f"Ticket '{self.title}' - {self.priority.value} Priority - Status: {self.status.value}"
