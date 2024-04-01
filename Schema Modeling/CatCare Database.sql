use 336Homeworks;

DROP TABLE IF EXISTS PetAppointment;
DROP TABLE IF EXISTS NailAppointment;
DROP TABLE IF EXISTS Review;

DROP TABLE IF EXISTS Pet;
DROP TABLE IF EXISTS Customer;

DROP TABLE IF EXISTS Provider;
DROP TABLE IF EXISTS ProviderSchedule;


CREATE TABLE Customer(
	CustomerID INT NOT NULL PRIMARY KEY,
    Username VARCHAR(100),
    Password VARCHAR(64),
    Name VARCHAR(32),
    Address VARCHAR(255),
    Email VARCHAR(64),
    Number BIGINT(10)
);


CREATE TABLE Pet(
	PetID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(64),
    Age INT,
    Species VARCHAR(3),
    Breed VARCHAR(32),
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE ProviderSchedule(
	ScheduleID INT NOT NULL PRIMARY KEY,
    Day DATE,
    StartTime DATETIME,
    EndTime DATETIME
);

CREATE TABLE Provider(
	ProviderID INT NOT NULL PRIMARY KEY,
    Username VARCHAR(100),
    Password VARCHAR(64),
    Name VARCHAR(32),
    Address VARCHAR(255),
    Email VARCHAR(64),
    Number BIGINT(10),
    Industry VARCHAR(64),
    Specialization VARCHAR(64),
    Company VARCHAR(64),
    PriceRate INT,
    Rating INT,
    ScheduleID INT,
    FOREIGN KEY (ScheduleID) REFERENCES ProviderSchedule(ScheduleID)
);

CREATE TABLE Review (
    ReviewID INT NOT NULL PRIMARY KEY,
    ProviderID INT NOT NULL,
    ServiceType VARCHAR(20), 
    Rating INT, 
    Comment TEXT, 
    FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID)
);

CREATE TABLE PetAppointment(
	AppointmentID INT NOT NULL PRIMARY KEY,
    ProviderID INT,
    PetID INT,
    FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID),
    FOREIGN KEY (PetID) REFERENCES Pet(PetID),
    Status VARCHAR(32),
    BorrowDate DATETIME,
    ReturnDate DATETIME
);


CREATE TABLE NailAppointment(
	AppointmentID INT NOT NULL PRIMARY KEY,
    ProviderID INT,
    CustomerID INT,
    FOREIGN KEY (ProviderID) REFERENCES Provider(ProviderID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    Status VARCHAR(32),
    BorrowDate DATETIME,
    ReturnDate DATETIME
);
