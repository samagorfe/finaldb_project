# Tech Startup Database Console

A web-based database console built for a fictional tech startup, enabling structured storage, analytics, and operational insights into company data.

 [Click here to open the console](http://127.0.0.1:5000) ← *(replace with live URL if deployed)*

---

## Problem Description

This database was designed for a **tech startup** that collaborates with external vendors, marketing teams, and partner companies. It needed a secure, scalable solution to manage operations, team members, products, and clients.

This project involved:

- Understanding how the system should be used
- Designing the schema and relationships
- Implementing SQL logic and query support
- Debugging diagram assumptions and constraints

---

## Challenges Faced

- Translating ER/EER diagrams into a working schema
- Modeling complex relationships
- Maintaining referential integrity
- Designing a flexible, normalized schema
- Debugging logic for joins, views, and query constraints

---

## Project Questions

**1. Five Rules likely used in the company:**
- A team member cannot supervise more than 10 people.
- Each interview for a candidate must be with a different team member.
- A customer is defined by having at least one active subscription.
- An app must include at least one component.
- A tech partner must be tied to at least one component.

**2. Importance of superclass/subclass relationships:**
> Yes — entities like `UserProfile` can represent Clients, Candidates, or Team Members. Using superclasses prevents duplication and simplifies identity tracking.

**3. Why use a relational DBMS like Oracle?**
> Oracle supports normalization, primary/foreign key constraints, and large-scale transaction safety. It helps enforce business rules at the schema level.

---

## ER Diagram

![ER Diagram](report/ER%20Diagram.png)

---

## EER Diagram

![EER Diagram](report/EER%20Diagram%20from%20Lucidchart%20(2).png)

---

## Assumptions

- All people (employees, candidates, customers) are in one `UserProfile` table.
- A person can have multiple roles.
- Each employee can only have one supervisor.
- A person can apply to many job positions.
- Not all departments have to post job positions.

---


## Logical Design

![Logical Design](report/Logical%20Design.png)

## Dependency Diagram

![Dependency Diagram](report/depdency%20diagram.png)

---

## Relational Schema (Simplified)

<details>
<summary>Click to expand schema</summary>

```sql
USERPROFILE (
  UserProfileID INT PRIMARY KEY,
  Name VARCHAR(100),
  Age INT CHECK (Age < 65),
  Gender VARCHAR(10),
  Address VARCHAR(200)
)

TEAMMEMBER (
  UserProfileID INT PRIMARY KEY,
  Rank VARCHAR(50),
  Title VARCHAR(50),
  FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID)
)

DIVISION (
  DivisionID INT PRIMARY KEY,
  DeptName VARCHAR(100)
)

ROLEPOSTING (
    JobID INT PRIMARY KEY,
    JobDesc VARCHAR(200),
    PostedDate DATE,
    DivisionID INT,
    FOREIGN KEY (DivisionID) REFERENCES DIVISION(DivisionID)
)
APPLICATION (
    UserProfileID INT,
    JobID INT,
    PRIMARY KEY (UserProfileID, JobID),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (JobID) REFERENCES ROLEPOSTING(JobID)
)
INTERVIEW (
    InterviewID INT PRIMARY KEY,
    CandidateID INT,
    InterviewerID INT,
    JobID INT,
    InterviewTime TIMESTAMP,
    Grade INT CHECK (Grade BETWEEN 0 AND 100),
    FOREIGN KEY (CandidateID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (InterviewerID) REFERENCES TEAMMEMBER(UserProfileID),
    FOREIGN KEY (JobID) REFERENCES ROLEPOSTING(JobID)
)
SALARYPAYMENT (
    EmployeeID INT,
    TransactionNo INT,
    PayDate DATE,
    Amount DECIMAL(10,2),
    PRIMARY KEY (EmployeeID, TransactionNo),
    FOREIGN KEY (EmployeeID) REFERENCES TEAMMEMBER(UserProfileID)
)
ASSIGNEDTO (
    UserProfileID INT,
    DivisionID INT,
    PRIMARY KEY (UserProfileID, DivisionID),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (DivisionID) REFERENCES DIVISION(DivisionID)
)
APP (
    AppID INT PRIMARY KEY,
    AppType VARCHAR(50),
    ListPrice DECIMAL(10,2),
    Size VARCHAR(50),
    Weight VARCHAR(50),
    Style VARCHAR(50)
)
COMPONENT (
    ComponentID INT PRIMARY KEY,
    PartName VARCHAR(100),
    Description VARCHAR(200)
)
APPPART (
    AppID INT,
    ComponentID INT,
    Quantity INT,
    PRIMARY KEY (AppID, ComponentID),
    FOREIGN KEY (AppID) REFERENCES APP(AppID),
    FOREIGN KEY (ComponentID) REFERENCES COMPONENT(ComponentID)
)
TECHPARTNER (
    TechPartnerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Address VARCHAR(200),
    AccountNo VARCHAR(50),
    CreditRating INT,
    WebServURL VARCHAR(100)
)
TECHPARTNERPART (
    TechPartnerID INT,
    ComponentID INT,
    UnitType VARCHAR(50),
    PRIMARY KEY (TechPartnerID, ComponentID),
    FOREIGN KEY (TechPartnerID) REFERENCES TECHPARTNER(TechPartnerID),
    FOREIGN KEY (ComponentID) REFERENCES COMPONENT(ComponentID)
)
LAUNCHPLATFORM (
    SiteID INT PRIMARY KEY,
    SiteName VARCHAR(100),
    SiteLocation VARCHAR(100)
)
SUBSCRIPTION (
    SubscriptionID INT PRIMARY KEY,
    SubscriptionsUserProfileID INT,
    CustomerID INT,
    AppID INT,
    SiteID INT,
    FOREIGN KEY (SubscriptionsUserProfileID) REFERENCES TEAMMEMBER(UserProfileID),
    FOREIGN KEY (CustomerID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (AppID) REFERENCES APP(AppID),
    FOREIGN KEY (SiteID) REFERENCES LAUNCHPLATFORM(SiteID)
)
CONTAINS (
    SubscriptionID INT,
    AppID INT,
    PRIMARY KEY (SubscriptionID, AppID),
    FOREIGN KEY (SubscriptionID) REFERENCES SUBSCRIPTION(SubscriptionID),
    FOREIGN KEY (AppID) REFERENCES APP(AppID)
)
WORKSAT (
    UserProfileID INT,
    SiteID INT,
    PRIMARY KEY (UserProfileID, SiteID),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (SiteID) REFERENCES LAUNCHPLATFORM(SiteID)
)
SQL Statements:
CREATE TABLE USERPROFILE (
    UserProfileID INT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT CHECK (Age < 65),
    Gender VARCHAR(10),
    Address VARCHAR(200)
);

CREATE TABLE TEAMMEMBER (
    UserProfileID INT PRIMARY KEY,
    TeamRank VARCHAR(50),
    Title VARCHAR(50),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID)
);

CREATE TABLE DIVISION (
    DivisionID INT PRIMARY KEY,
    DeptName VARCHAR(100)
);

CREATE TABLE ROLEPOSTING (
    JobID INT PRIMARY KEY,
    JobDesc VARCHAR(200),
    PostedDate DATE,
    DivisionID INT,
    FOREIGN KEY (DivisionID) REFERENCES DIVISION(DivisionID)
);

CREATE TABLE APPLICATION (
    UserProfileID INT,
    JobID INT,
    PRIMARY KEY (UserProfileID, JobID),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (JobID) REFERENCES ROLEPOSTING(JobID)
);

CREATE TABLE INTERVIEW (
    InterviewID INT PRIMARY KEY,
    CandidateID INT,
    InterviewerID INT,
    JobID INT,
    InterviewTime TIMESTAMP,
    Grade INT CHECK (Grade BETWEEN 0 AND 100),
    FOREIGN KEY (CandidateID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (InterviewerID) REFERENCES TEAMMEMBER(UserProfileID),
    FOREIGN KEY (JobID) REFERENCES ROLEPOSTING(JobID)
);

CREATE TABLE SALARYPAYMENT (
    EmployeeID INT,
    TransactionNo INT,
    PayDate DATE,
    Amount DECIMAL(10,2),
    PRIMARY KEY (EmployeeID, TransactionNo),
    FOREIGN KEY (EmployeeID) REFERENCES TEAMMEMBER(UserProfileID)
);

CREATE TABLE ASSIGNEDTO (
    UserProfileID INT,
    DivisionID INT,
    PRIMARY KEY (UserProfileID, DivisionID),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (DivisionID) REFERENCES DIVISION(DivisionID)
);

CREATE TABLE APP (
    AppID INT PRIMARY KEY,
    AppType VARCHAR(50),
    ListPrice DECIMAL(10,2),
    Size VARCHAR(50),
    Weight VARCHAR(50),
    Style VARCHAR(50)
);

CREATE TABLE COMPONENT (
    ComponentID INT PRIMARY KEY,
    PartName VARCHAR(100),
    Description VARCHAR(200)
);

CREATE TABLE APPPART (
    AppID INT,
    ComponentID INT,
    Quantity INT,
    PRIMARY KEY (AppID, ComponentID),
    FOREIGN KEY (AppID) REFERENCES APP(AppID),
    FOREIGN KEY (ComponentID) REFERENCES COMPONENT(ComponentID)
);

CREATE TABLE TECHPARTNER (
    TechPartnerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Address VARCHAR(200),
    AccountNo VARCHAR(50),
    CreditRating INT,
    WebServURL VARCHAR(100)
);

CREATE TABLE TECHPARTNERPART (
    TechPartnerID INT,
    ComponentID INT,
    UnitType VARCHAR(50),
    UnitCost DECIMAL(10,2),
    PRIMARY KEY (TechPartnerID, ComponentID),
    FOREIGN KEY (TechPartnerID) REFERENCES TECHPARTNER(TechPartnerID),
    FOREIGN KEY (ComponentID) REFERENCES COMPONENT(ComponentID)
);

CREATE TABLE LAUNCHPLATFORM (
    SiteID INT PRIMARY KEY,
    SiteName VARCHAR(100),
    SiteLocation VARCHAR(100)
);

CREATE TABLE SUBSCRIPTION (
    SubscriptionID INT PRIMARY KEY,
    SubscriptionsUserProfileID INT,
    CustomerID INT,
    AppID INT,
    SiteID INT,
    FOREIGN KEY (SubscriptionsUserProfileID) REFERENCES TEAMMEMBER(UserProfileID),
    FOREIGN KEY (CustomerID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (AppID) REFERENCES APP(AppID),
    FOREIGN KEY (SiteID) REFERENCES LAUNCHPLATFORM(SiteID)
);

CREATE TABLE CONTAINS (
    SubscriptionID INT,
    AppID INT,
    PRIMARY KEY (SubscriptionID, AppID),
    FOREIGN KEY (SubscriptionID) REFERENCES SUBSCRIPTION(SubscriptionID),
    FOREIGN KEY (AppID) REFERENCES APP(AppID)
);

CREATE TABLE WORKSAT (
    UserProfileID INT,
    SiteID INT,
    PRIMARY KEY (UserProfileID, SiteID),
    FOREIGN KEY (UserProfileID) REFERENCES USERPROFILE(UserProfileID),
    FOREIGN KEY (SiteID) REFERENCES LAUNCHPLATFORM(SiteID)
);


INSERT INTO USERPROFILE (UserProfileID, Name, Age, Gender, Address) VALUES
(1, 'Hellen Cole', 28, 'Female', '100 Main St'),
(2, 'John Smith', 35, 'Male', '200 Oak Ave'),
(3, 'Linda Zhao', 30, 'Female', '300 Maple Rd'),
(4, 'Karen West', 31, 'Female', '400 Elm St'),
(5, 'Tom Cruz', 29, 'Male', '500 Pine Blvd');

INSERT INTO TEAMMEMBER (UserProfileID, TeamRank, Title) VALUES
(2, 'Senior', 'Software Engineer'),
(3, 'Lead', 'Product Manager'),
(5, 'Mid', 'Sales Rep');

INSERT INTO DIVISION (DivisionID, DeptName) VALUES
(1, 'Marketing'),
(2, 'Engineering');

INSERT INTO ROLEPOSTING (JobID, JobDesc, PostedDate, DivisionID) VALUES
(11111, 'Marketing Analyst', '2011-01-10', 1),
(12345, 'Backend Developer', '2011-01-15', 2);

INSERT INTO APPLICATION (UserProfileID, JobID) VALUES
(1, 11111),
(4, 12345);

INSERT INTO INTERVIEW (InterviewID, CandidateID, InterviewerID, JobID, InterviewTime, Grade) VALUES
(1, 1, 2, 11111, '2011-01-20 10:00:00', 85),
(2, 1, 3, 11111, '2011-01-22 14:00:00', 90),
(3, 4, 2, 12345, '2011-01-25 09:00:00', 55),
(4, 4, 3, 12345, '2011-01-26 15:00:00', 65);

INSERT INTO SALARYPAYMENT (EmployeeID, TransactionNo, PayDate, Amount) VALUES
(2, 1001, '2024-01-01', 5000.00),
(2, 1002, '2024-02-01', 5100.00),
(3, 2001, '2024-01-01', 6200.00),
(5, 3001, '2024-01-01', 4200.00);

CREATE OR REPLACE VIEW View1 AS
SELECT 
    EmployeeID,
    AVG(Amount) AS AvgMonthlySalary
FROM 
    SALARYPAYMENT
GROUP BY 
    EmployeeID;

CREATE OR REPLACE VIEW View2 AS
SELECT 
    CandidateID,
    JobID,
    COUNT(*) AS RoundsPassed
FROM 
    INTERVIEW
WHERE 
    Grade > 60
GROUP BY 
    CandidateID, JobID;

CREATE OR REPLACE VIEW View3 AS
SELECT 
    A.AppType,
    COUNT(*) AS ItemsSold
FROM 
    SUBSCRIPTION S
JOIN 
    APP A ON S.AppID = A.AppID
GROUP BY 
    A.AppType;

CREATE OR REPLACE VIEW View4 AS
SELECT 
    A.AppID,
    SUM(P.Quantity * T.UnitCost) AS TotalPartCost
FROM 
    APPPART P
JOIN 
    TECHPARTNERPART T ON P.ComponentID = T.ComponentID
JOIN 
    APP A ON P.AppID = A.AppID
GROUP BY 
    A.AppID;

CREATE OR REPLACE VIEW SelectedCandidates AS
SELECT 
    CandidateID,
    JobID,
    COUNT(*) AS RoundsPassed,
    AVG(Grade) AS AvgGrade
FROM 
    INTERVIEW
WHERE 
    Grade > 60
GROUP BY 
    CandidateID, JobID
HAVING 
    COUNT(*) >= 5 AND AVG(Grade) > 70;

SELECT I.InterviewerID, U.Name
FROM INTERVIEW I
JOIN USERPROFILE U ON I.InterviewerID = U.UserProfileID
JOIN USERPROFILE C ON I.CandidateID = C.UserProfileID
WHERE C.Name = 'Hellen Cole' AND I.JobID = 11111;

SELECT R.JobID
FROM ROLEPOSTING R
JOIN DIVISION D ON R.DivisionID = D.DivisionID
WHERE D.DeptName = 'Marketing' AND R.PostedDate BETWEEN '2011-01-01' AND '2011-01-31';

SELECT R.JobID, R.JobDesc
FROM ROLEPOSTING R
LEFT JOIN SelectedCandidates SC ON R.JobID = SC.JobID
WHERE SC.JobID IS NULL AND R.PostedDate <= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);

SELECT T.UserProfileID, U.Name
FROM TEAMMEMBER T
JOIN USERPROFILE U ON T.UserProfileID = U.UserProfileID
JOIN SUBSCRIPTION S ON T.UserProfileID = S.SubscriptionsUserProfileID
JOIN APP A ON S.AppID = A.AppID
WHERE A.ListPrice > 200
GROUP BY T.UserProfileID, U.Name
HAVING COUNT(DISTINCT A.AppType) = (
    SELECT COUNT(DISTINCT AppType) FROM APP WHERE ListPrice > 200
);

SELECT D.DivisionID, D.DeptName
FROM DIVISION D
LEFT JOIN ROLEPOSTING R ON D.DivisionID = R.DivisionID
  AND R.PostedDate BETWEEN '2011-01-01' AND '2011-02-01'
WHERE R.JobID IS NULL;

SELECT U.UserProfileID, U.Name, A.DivisionID
FROM APPLICATION AP
JOIN USERPROFILE U ON AP.UserProfileID = U.UserProfileID
JOIN ASSIGNEDTO A ON U.UserProfileID = A.UserProfileID
WHERE AP.JobID = 12345;

SELECT A.AppType
FROM SUBSCRIPTION S
JOIN APP A ON S.AppID = A.AppID
GROUP BY A.AppType
ORDER BY COUNT(*) DESC
LIMIT 1;

SELECT A.AppType
FROM APP A
JOIN (
    SELECT P.AppID, SUM(P.Quantity * T.UnitCost) AS TotalCost
    FROM APPPART P
    JOIN TECHPARTNERPART T ON P.ComponentID = T.ComponentID
    GROUP BY P.AppID
) AS Cost ON A.AppID = Cost.AppID
ORDER BY (A.ListPrice - Cost.TotalCost) DESC
LIMIT 1;

SELECT A.UserProfileID, U.Name
FROM ASSIGNEDTO A
JOIN USERPROFILE U ON A.UserProfileID = U.UserProfileID
GROUP BY A.UserProfileID, U.Name
HAVING COUNT(DISTINCT A.DivisionID) = (SELECT COUNT(*) FROM DIVISION);

SELECT DISTINCT U.Name, U.Address AS Email
FROM SelectedCandidates SC
JOIN USERPROFILE U ON SC.CandidateID = U.UserProfileID;

SELECT DISTINCT U.Name, U.Address AS Email
FROM SelectedCandidates SC
JOIN USERPROFILE U ON SC.CandidateID = U.UserProfileID;

SELECT T.UserProfileID, U.Name
FROM SALARYPAYMENT S
JOIN TEAMMEMBER T ON S.EmployeeID = T.UserProfileID
JOIN USERPROFILE U ON T.UserProfileID = U.UserProfileID
GROUP BY T.UserProfileID, U.Name
ORDER BY AVG(S.Amount) DESC
LIMIT 1;

SELECT TP.TechPartnerID, TP.Name
FROM TECHPARTNERPART TPP
JOIN COMPONENT C ON TPP.ComponentID = C.ComponentID
JOIN TECHPARTNER TP ON TPP.TechPartnerID = TP.TechPartnerID
JOIN APPPART AP ON C.ComponentID = AP.ComponentID
JOIN APP A ON AP.AppID = A.AppID
WHERE C.PartName = 'Cup'
  AND CAST(REPLACE(A.Weight, 'lb', '') AS DECIMAL) < 4
ORDER BY TPP.UnitCost ASC
LIMIT 1;
