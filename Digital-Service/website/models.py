from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Provider(db.Model, UserMixin):
    __tablename__ = "Provider"

    # Random IDs or no; integrity error
    ProviderID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(100))
    Password = db.Column(db.VARCHAR(150))
    Name = db.Column(db.VARCHAR(32))
    Industry = db.Column(db.VARCHAR(64))  # pet || nail
    Address = db.Column(db.VARCHAR(255))
    Email = db.Column(db.VARCHAR(64))
    Number = db.Column(db.VARCHAR(12))  # might be better as a string/varchar
    Rating = db.Column(db.Integer)
    PriceRate = db.Column(db.Integer)
    Specialization = db.Column(db.VARCHAR(64))
    Company = db.Column(db.VARCHAR(64))

    Schedules = db.relationship("ProviderSchedule", backref="Provider", lazy=True)
    PetAppointments = db.relationship("PetAppointment", backref="Provider", lazy=True)
    NailAppointments = db.relationship("NailAppointment", backref="Provider", lazy=True)

    def get_id(self):
        return self.Email

    def to_json(self):
        return {
            "id": self.ProviderID,
            "username": self.Username,
            "email": self.Email,
            "industry": self.Industry,
        }


class ProviderSchedule(db.Model):
    __tablename__ = "ProviderSchedule"  # simplifies relationship declarations

    ScheduleID = db.Column(db.Integer, primary_key=True)
    ProviderID = db.Column(db.Integer, db.ForeignKey("Provider.ProviderID"))
    StartTime = db.Column(db.TIME)
    EndTime = db.Column(db.TIME)
    AppointmentDate = db.Column(db.DATE)
    Availability = db.Column(db.Integer)

    def to_json(self):
        return {
            "ScheduleID": self.ScheduleID,
            "Day": self.Day,
            "Start": self.StartTime,
            "End": self.EndTime,
        }


class Customer(db.Model, UserMixin):
    __tablename__ = "Customer"

    CustomerID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(100))
    Password = db.Column(db.VARCHAR(150))
    Name = db.Column(db.VARCHAR(32))
    Address = db.Column(db.VARCHAR(255))  # pet sitting
    Email = db.Column(db.VARCHAR(64))
    Number = db.Column(db.VARCHAR(12))

    NailAppointments = db.relationship("NailAppointment", backref="Customer", lazy=True)
    Pets = db.relationship("Pet", backref="customer", lazy=True)

    # override for login_user
    def get_id(self):
        return self.Email

    def to_json(self):
        return {
            "CustomerID": self.CustomerID,
            "CustomerName": self.Name,
            "CustomerEmail": self.Email,
        }


class Pet(db.Model):
    __tablename__ = "Pet"

    PetID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("Customer.CustomerID"))
    Name = db.Column(db.VARCHAR(64))
    Age = db.Column(db.Integer)
    Species = db.Column(db.VARCHAR(3))
    Breed = db.Column(db.VARCHAR(32))

    Appointments = db.relationship("PetAppointment", backref="Pet", lazy=True)

    def to_json(self):
        return {
            "PetID": self.PetID,
            "CustomerID": self.CustomerID,
            "Name": self.Name,
        }


class PetAppointment(db.Model):
    __tablename__ = "PetAppointment"

    AppointmentID = db.Column(db.Integer, primary_key=True)
    ProviderID = db.Column(db.Integer, db.ForeignKey("Provider.ProviderID"))
    PetID = db.Column(db.Integer, db.ForeignKey("Pet.PetID"))
    Status = db.Column(db.VARCHAR(32))
    BorrowDate = db.Column(db.TIME)
    ReturnDate = db.Column(db.TIME)
    AppDate = db.Column(db.DATE)
    Price = db.Column(db.Integer)

    def to_json(self):
        return {
            "AppointmentID": self.AppointmentID,
            "ProviderID": self.ProviderID,
            "BorrowDate": self.BorrowDate,
            "ReturnDate": self.ReturnDate,
        }


class NailAppointment(db.Model):
    __tablename__ = "NailAppointment"

    AppointmentID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("Customer.CustomerID"))
    ProviderID = db.Column(db.Integer, db.ForeignKey("Provider.ProviderID"))
    # Type = db.Column(db.VARCHAR(15))
    # Comment = db.Column(db.Text)
    Status = db.Column(db.VARCHAR(32))
    StartTime = db.Column(db.TIME)
    EndTime = db.Column(db.TIME)
    AppDate = db.Column(db.DATE)
    Price = db.Column(db.Integer)

    def to_json(self):
        return {
            "AppointmentID": self.AppointmentID,
            "CustomerID": self.CustomerID,
            "ProviderID": self.ProviderID,
            "StartTime": self.StartTime,
            "EndTime": self.EndTime,
        }


