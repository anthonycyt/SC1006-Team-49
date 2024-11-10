# SC2006 - Software Engineering || NTUFoodie : The Future For Students

## About

Welcome to the official repository for NTUFoodie made for our SC2006 Project (Team 49)! 

<br />
<div align="center">
    <img width="679" alt="NTUFoodie Page" src="https://github.com/user-attachments/assets/7fe27f90-dc8b-48ba-9e06-a66dd9f104e4">
</div>
<br />

NTUFoodie is a student-centered initiative aimed at helping university students to discover cost-efficient meals through reviews made by others as a guide. This web based application not only minimizes food waste but also ensures that nutritious meals are made available
to every university student without breaking the bank! As we ourselves are students we understand deeply how hard it is to be able to find budget meals in order to save money, hence NTUFoodie was built from a genuine desire to support our fellow students in saving money!

This project applied software engineering best practices and design patterns in order to ensure high reliability, performance, and extensibility for future enhancements.
___
  
## Contributors 
- @anthony
- @kinghey
- @wiz
- @uwubrain 
- @erinarin034
## Table of Content

<details>
<summary>Demo Video</summary>
<br>
Youtube link: https://www.youtube.com/watch?v=qMXj91_hbos
    
https://github.com/user-attachments/assets/2c262736-b806-4fea-b276-805098b2d2d5

</details>

<details>
<summary>Diagrams</summary>
<br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables/Sequence%20Diagrams" style="text-decoration: underline;">
    Sequence Diagrams
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Class Diagram
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Complete System Architecture
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Use Case Model
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Dialog Map
</a><br>
<br>
</details>  

<details>
<summary>Supporting Documents</summary>
<br>
<br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables/Sequence%20Diagrams" style="text-decoration: underline;">
    Sequence Diagrams
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Class Diagram
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Complete System Architecture
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Use Case Model
</a>
    <br><br>
<a href="https://github.com/anthonycyt/SC1006-Team-49/tree/main/Lab%203%20Deliverables" style="text-decoration: underline;">
    Dialog Map
</a><br>
<br>
</details>


## How to Run
*Do NOTE that a .env file is required within the NTUFoodie folder, which can be asked for from any group members of this project!  

### MacOS
1. Clone the GitHub repo/ Download the GitHub Repo onto VSCode
   ```bash
    cd "Lab 4 Deliverable"/NTUFoodie
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
### Windows
1. Clone the GitHub repo/ Download the GitHub Repo onto VSCode
   ```bash
    cd "Lab 4 Deliverable"/NTUFoodie
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
| Store Owener  | teststoreowner| testpassword |
| Admin         | anthony       | testpassword |

## App Design
### Fronted
The frontend mainly consists of each interface dedicated to a specific type of user, designed with distinct functionalities following our class diagrams. You will find more detailed design documents for each interface in the <code>template/NTUFoodieApp</code> directory.

* Admin UI: This interface is designed for administrators to manage NTUFoodie’s content, including user management, food listing approvals, and report moderation.

* Consumer UI: The consumer interface allows users to explore food listings, add reviews, and navigate to food locations. It’s tailored to be visually engaging and easy to navigate, helping users find budget-friendly meals quickly.

* StoreOwner UI: For users managing food listings, this interface includes options to create, update, and manage food listings. Store owners can easily keep their listings up-to-date and highlight any discounts or deals available.

**Supporting Directories and Assets:**
<code>static/images</code> contains all images used throughout NTUFoodie, enhancing the visual appeal of each page. Images are carefully selected to make the app engaging and user-friendly. Some HTML files include inline JavaScript using <code><script></code> tags to enhance user interaction and their overall experience with the web-app.

### Backend
Backend mainly consists of the database and linkings of each page to store data into the database using SQLite3

### Design Patterns Used
* Stratergy & Factory Pattern
* Observer Pattern

  
## External API(s) Used
* Mapbox APIS
  - Geocoding
  - Get Directions
  - Live location


