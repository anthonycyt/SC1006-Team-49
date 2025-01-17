# 2006-TDDB-49
# SC2006 - Software Engineering || NTUFoodie : By Students For Students
## About

Welcome to the official repository for NTUFoodie made for our SC2006 Project (Team 49)! 

<br />
<div align="center">
    <img width="70%" alt="NTUFoodie Page" src="https://github.com/user-attachments/assets/7fe27f90-dc8b-48ba-9e06-a66dd9f104e4">
</div>
<br />

**NTUFoodie** is a student-centered initiative aimed at helping university students to discover cost-efficient yet tasty meals through reviews made by others as a guide. This web based application not only minimizes food waste but also ensures that nutritious meals are made available
to every university student without breaking the bank! As students ourselves we understand deeply how hard it is to be able to find budget meals in order to save money, hence NTUFoodie was built from the genuine desire to support our fellow students in saving money!  

This project is an application of software engineering best practices and design patterns in order to ensure high reliability, performance, and extensibility for future enhancements. 

  
## Contributors 

| Name                          | GitHub Account                                       |
|-------------------------------|------------------------------------------------------|
| Anthony Chua Yong Tai (Leader)| [anthonycyt](https://github.com/anthonycyt)          |            
| Ho King Hei                   | [khey0](https://github.com/khey0)                    |
| Khoo Qian Yee                 | [erinarin034](https://github.com/erinarin034)        | 
| Rachel Lim Lin                | [uwubrain](https://github.com/uwubrain)              | 
| Muhammad Wisnu Darmawan       | [abangwizzz](https://github.com/abangwizzz)          |

  
## Table of Content
  
<details>
<summary>Demo Video</summary>
<br>
Youtube link for higher definition: https://www.youtube.com/watch?v=qMXj91_hbos

https://github.com/user-attachments/assets/f2618c64-f73e-4910-a492-1dffd1a67084



</details>

<details>
<summary>Diagrams</summary>
<br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/Sequence%20Diagrams" style="text-decoration: underline;">
    Sequence Diagrams 
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/Class%20Diagram.pdf" style="text-decoration: underline;">
    Class Diagram
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/System%20Architecture.pdf" style="text-decoration: underline;">
    Complete System Architecture
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/Complete%20Use%20Case%20Diagram%20.png" style="text-decoration: underline;">
    Complete Use Case Diagram
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/Dialog%20Maps" style="text-decoration: underline;">
    Dialog Maps
</a><br>
</details>  

<details>
<summary>Supporting Documents</summary>
    <br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/Complete%20Use%20Case%20Description%20(Ver%202.2).doc" style="text-decoration: underline;">
    Use Case Description
</a><br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/NTUFoodie_TDDB_Team%2049_SRS.pdf" style="text-decoration: underline;">
    SRS Document
</a><br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/NTUFoodie%20UI%20Mockup.pdf" style="text-decoration: underline;">
    UI Mockup
</a><br>
    <br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/SC2006%20Demo%20Video.mov" style="text-decoration: underline;">
    Demo Video(Compressed)
</a><br>
</details>

## How to Run
**DO NOTE that an .env file is required within the NTUFoodie folder, which can be asked for from any group members of this project!**

## MacOS
1. Clone the GitHub repo/ Download the GitHub Repo onto VSCode
   ```bash
    cd "Lab 4 Deliverables"
    cd NTUFoodie
    ```
2. Bypass the execution policy temporarily Activate the virtual environment
   ```bash
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
3. Activate the virtual environment
   ```bash
    source venv/bin/activate
    ```
4. Run the server
    ```bash
    python manage.py runserver
    ```  
    And you are ready to start using the NTUFoodie! The server application will be running on http://127.0.0.1:8000/.
   
## Windows
1. Clone the GitHub repo/ Download the GitHub Repo onto VSCode
   ```bash
    cd "Lab 4 Deliverables"
    cd NTUFoodie
    ```
2. Bypass the execution policy temporarily Activate the virtual environment
   ```bash
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
3. Activate the virtual environment
   ```bash
    .\venv\bin\Activate.ps1
    ```
4. Run the server
    ```bash
    python manage.py runserver
    ```

## Pre-configured Users 
| Role       | Username       | Password       |
| :------------- |:-------------| :-----|
| Consumer      | testuser      | testpassword |
| Store Owner  | teststoreowner| testpassword |
| Admin         | anthony       | testpassword |

## App Design

## Overview of the System
<br />
<div align="center">
    <img width="50%" alt="Complete System Archi" src="https://github.com/anthonycyt/SC1006-Team-49/blob/main/Lab%205%20Deliverables/Supporting%20Documents%20and%20Diagrams/System%20Architecture.pdf">
</div>
<br />


## Frontend
The frontend mainly consists of each interface dedicated to a specific type of user, designed with distinct functionalities following our class diagrams. You will find more detailed design documents for each interface in the <code>template/NTUFoodieApp</code> directory.

* **Admin UI:** This interface is designed for administrators to manage NTUFoodie’s content, including user management, food listing approvals, and report moderation.

* **Consumer UI:** The consumer interface allows users to explore food listings, add reviews, and navigate to food locations. It’s tailored to be visually engaging and easy to navigate, helping users find budget-friendly meals quickly.

* **StoreOwner UI:** For users managing food listings, this interface includes options to create, update, and manage food listings. Store owners can easily keep their listings up-to-date and highlight any discounts or deals available.

**Supporting Directories and Assets:**
<code>static/images</code> contains all images used throughout NTUFoodie, enhancing the visual appeal of each page. Images are carefully selected to make the app engaging and user-friendly. Some HTML files include inline JavaScript using <code><script></code> tags to enhance user interaction and their overall experience with the web-app.


## Backend
The backend uses *SQLite3* as the database, which is lightweight and suitable for local development and smaller-scale applications. It is used to store various data types such as food listings, user details, reviews, and food discounts.

Authentication and authorization are handled via Django’s built-in user authentication system, which is extended to implement role-based access control (Admin, Consumer, Store Owner).
The backend ensures the consistency and integrity of the application by implementing business rules, such as:  

* **StoreOwner:** Only users with a "StoreOwner" role can create or update food listings.

* **Admin:** Admins have full access to manage all content, including approving food listings, moderating reviews, and managing user roles. These functions can't be accessed by Store Owners and Consumers
  
* **Consumer:** Consumers can browse food listings, view reviews, and add their own reviews.

All python files about the logic behind the web-app can be found withint the <code>/NTUFoodieApp</code> file.

## Design Patterns Used  

* Observer Pattern <code>For notifying users through notifications</code>  
* SOLID Design Principles <code>Following mainly SRP</code>

  
## External API(s) Used
* Mapbox APIS = https://www.mapbox.com/maps/streets
  - Geocoding
  - Get Directions
  - Live location




