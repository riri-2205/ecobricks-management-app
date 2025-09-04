# EcoBricks Management System

This is a full-featured desktop-based DBMS application built using **Python**, **MySQL**, and **PyQt6**. The system is designed to manage plastic donations and eco-friendly construction projects using ecobricks. It was developed as part of the IT252 Database Management Systems course at NITK.
https://www.google.com/imgres?q=kenichi&imgurl=https%3A%2F%2Fimage.tmdb.org%2Ft%2Fp%2Foriginal%2Fjm8fUh70x9WUIg7tMGMTHEmLhI4.jpg&imgrefurl=https%3A%2F%2Fwww.myseries.tv%2Fhistorys-strongest-disciple-kenichi%2F&docid=4jU440zLCB6fAM&tbnid=2Of_d6ZUHR2d2M&vet=12ahUKEwjDp_vOqL6PAxX61jgGHY5UAQUQM3oECFsQAA..i&w=1920&h=1080&hcb=2&ved=2ahUKEwjDp_vOqL6PAxX61jgGHY5UAQUQM3oECFsQAA
---
Poi dengei lanje nee erri puka cumslut oogabooga

## Features

- **User Management**
  - Add and view donators and builders
  - Role-based categorization

- **Inventory Management**
  - Track donations of different plastic types by weight
  - View inventory data by plastic type
  - View total ecobricks available

- **Project Management**
  - Add eco-friendly projects and assign weight from the inventory
  - Categorize projects by type and urgency
  - Prioritize projects based on a weighted scoring system using parameters like **Urgency** and **Category**

- **Reward System**
  - Stored procedure calculates reward points for contributors based on their donation history

---

## Technologies Used

| Layer       | Tools/Frameworks |
|-------------|------------------|
| Frontend    | PyQt6            |
| Backend     | Python, MySQL Connector |
| Database    | MySQL            |
| Logic       | SQL Triggers, Stored Procedures |

---

## Project Structure
```bash
├── gui-2.py # Main PyQt6 GUI interface with all tabs
├── db_2.py # Database creation, connection, triggers, procedures
├── requirements.txt # Optional: PyQt6 and mysql-connector
```
---

## Installation

1. Install all dependencies
```bash
   pip install PyQt6 mysql-connector-python
```

2. Use your local MySQL credentials to run MySQL
3. Run the Application
```bash
  python gui-2.py
```

---

## Database Design

The system uses a normalized relational schema:

### Tables:
- **Users** (`user_id`, `name`, `email`, `phone_no`, `role`)
- **Inventory** (`inventory_id`, `user_id`, `weight`, `plastic_type`)
- **Projects** (`project_id`, `project_name`, `user_id`, `weight`, `status`, `category`, `urgency`, `priority_score`)
- **Global_Variables** (`name`, `value`) — for tracking total ecobricks

---

## Triggers and Procedures

### Triggers:
- Automatically updates `Global_Variables.total_ecobricks` when new inventory is added
- Assigns inventory to **highest-priority project** upon inventory entry

### Stored Procedure:
```sql
CALL reward_points(user_id, @points);
```

---

### Future Improvements 
- Add authentication system for role-based login (Admin, Donator, Builder)
- Add visual charts (e.g., donation analytics using matplotlib)
- Export reports as PDF/CSV
- Add history/logging for audit trails

---

## Author

Developed by Rithika S, Aranganathan S, Agrima Singh  
As part of the DBMS course (IT252) at NITK

---

## License

This project is open-source and available under the MIT License.
