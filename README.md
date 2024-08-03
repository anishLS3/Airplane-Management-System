# Airplane-Management-system
## Project Description

This project involves designing and implementing a database to organize information about all the airplanes stationed and maintained at an airport. The database will manage data related to airplanes, airplane models, technicians, and testing events to ensure the efficient operation and maintenance of the airport's fleet. Below are the detailed specifications for each entity and the relationships between them.

![Image Alt](https://github.com/anishLS3/Airplane-Management-System/blob/d2aa316471f6a9048d8a03642116d8f1c021a3d3/Vimanam.png)

### Entities and Attributes

1. **Airplane**
   - **Registration Number**: A unique identifier for each airplane.
   - **Model Number**: Identifies the specific model of the airplane.

2. **Airplane Model**
   - **Model Number**: A unique identifier for each airplane model.
   - **Capacity**: The seating capacity of the model.
   - **Weight**: The weight of the model.

3. **Technician**
   - **Name**: Full name of the technician.
   - **SSN**: Social Security Number, a unique identifier for each technician.
   - **Address**: Residential address of the technician.
   - **Phone Number**: Contact number of the technician.
   - **Salary**: Monthly or annual salary of the technician.

4. **Expertise**
   - **Technician SSN**: References the technician who has the expertise.
   - **Model Number**: References the airplane model the technician is an expert in.

5. **Test**
   - **Test Number**: A unique identifier for each test.
   - **Name**: The name of the test.
   - **Maximum Score**: The highest possible score for the test.

6. **Testing Event**
   - **Test Number**: References the test being conducted.
   - **Registration Number**: References the airplane being tested.
   - **Technician SSN**: References the technician performing the test.
   - **Date**: Date on which the test was conducted.
   - **Hours Spent**: Number of hours the technician spent performing the test.
   - **Score**: The score the airplane received on the test.

### Relationships

- An **Airplane** is of one specific **Airplane Model**.
- A **Technician** can have expertise in one or more **Airplane Models**.
- A **Technician** can perform multiple **Testing Events**.
- Each **Testing Event** is associated with one **Airplane**, one **Test**, and one **Technician**.

### Database Schema

```sql
CREATE TABLE Airplane (
    registration_number VARCHAR(50) PRIMARY KEY,
    model_number VARCHAR(50) NOT NULL,
    FOREIGN KEY (model_number) REFERENCES Airplane_Model(model_number)
);

CREATE TABLE Airplane_Model (
    model_number VARCHAR(50) PRIMARY KEY,
    capacity INT NOT NULL,
    weight DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Technician (
    ssn CHAR(9) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Expertise (
    technician_ssn CHAR(9),
    model_number VARCHAR(50),
    PRIMARY KEY (technician_ssn, model_number),
    FOREIGN KEY (technician_ssn) REFERENCES Technician(ssn),
    FOREIGN KEY (model_number) REFERENCES Airplane_Model(model_number)
);

CREATE TABLE Test (
    test_number INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    max_score INT NOT NULL
);

CREATE TABLE Testing_Event (
    test_number INT,
    registration_number VARCHAR(50),
    technician_ssn CHAR(9),
    date DATE NOT NULL,
    hours_spent DECIMAL(4, 2) NOT NULL,
    score INT NOT NULL,
    PRIMARY KEY (test_number, registration_number, technician_ssn, date),
    FOREIGN KEY (test_number) REFERENCES Test(test_number),
    FOREIGN KEY (registration_number) REFERENCES Airplane(registration_number),
    FOREIGN KEY (technician_ssn) REFERENCES Technician(ssn)
);
```

### Project Goals

- Efficiently manage and retrieve information about airplanes, models, technicians, and test events.
- Maintain accurate records of the expertise of technicians.
- Track testing events to ensure that all airplanes are maintained in airworthy condition.
- Provide a scalable solution that can accommodate the growth of the airport's operations.

### Getting Started

- Clone the repository: git clone https://github.com/your-username/Airplane-Management-System.git
- Install dependencies: pip install -r requirements.txt
- Run the application: refer instructions.txt
- Access the application at http://localhost:8000.

### Future Enhancements

- Implementing user interfaces for easier data entry and retrieval.
- Developing reports and analytics to monitor maintenance activities and technician performance.
- Integrating with other airport management systems for comprehensive operational management.

### Contribution Guidelines

- Fork the repository and create your branch from `main`.
- Commit messages should be concise and descriptive.
- Ensure that the code adheres to the project's coding standards and conventions.
- Create pull requests for any changes you wish to merge into the main branch.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
