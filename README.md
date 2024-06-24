# HealthCare 🏥
HealthCare is a Hospital Management System, which offers a comprehensive software solution designed to streamline the administrative, financial, and clinical operations of a hospital. It integrates various functionalities such as patient registration, appointment scheduling, billing, medical records management, and more, to enhance the efficiency and effectiveness of healthcare delivery.

## System Entities 🥼
- Patient
- Doctor
- Head Doctor
- Nurse
- Head Nurse
- Pharmacist
- Human resources

## Features 🚀
- **Verification Codes and Two-Step Authentication:**
    - Enhancing the security of user accounts by requiring an additional verification step during login. This module helps protect user accounts from unauthorized access by sending a verification code to the user's email address during the authentication process. 
    - Integrating with an email service to send verification codes to users.
    - Implementing the two-step authentication flow to enhance account security.
    - Customized email templates for verification codes.

- **Human Resources:**
    - Manages hospital staff, recruitment, and performance. This module ensures that the hospital operates smoothly by maintaining a well-organized and motivated workforce.
    - Responsible for managing `users` and `employees` entities.
    - The relationship between `users` and `employees` is One-to-One(1-1), so each employee has only one user account.

- **Patient Capabilities:**
    - Register and Login: Validate and register user accounts.
    - Clinic Reservations: Book appointments and view the reservation queue.
    - Manage Reservations: View, update, and delete current reservations; access reservation history.
    - Medical Records: Upload and view medical records.

- **Doctor Capabilities:**
    - Clinic Management: List all clinics, view working hours, and update clinic status.
    - Case and Patient Management: Access current cases, view patient details, and medical records.
    - Room Management: View, update, and add room details.
    - Call Management: List, create, and update calls within the system.

- **Nurse Capabilities:**
    - Patient and Clinic Management: Retrieve user IDs, view clinic patients, and access patient details.
    - Room Management: View, update, and add room details.
    - Call Management: List, view, create, and update calls.

- **Pharmacist:**
    - Responsible for managing the hospital's pharmaceutical inventory, prescriptions and orders. This module ensures that the hospital's pharmacy operates efficiently and that patients receive their medications on time.
    - Managing prescriptions issued by doctors, including verification, dispensing medications, and maintaining records.
    - Keeping track of the pharmaceutical inventory, including stock levels.
    - Handling orders for medications and supplies, ensuring timely procurement and delivery.
    - The relationship between `medication` and `medication_categories` is Many-to-Many(M-M), so each medication has many medication categories and vice versa.
    - The relationship between `prescription` and `prescription_items` is Many-to-Many(M-M), so each prescription has many items (medicines) and vice versa.

- **Billing and Payments:**
    - Responsible for managing patient payments, processing credit card transactions and handling invoices.
    - Handling patient payments for services rendered, including credit card transactions.
    - Storing and managing credit card information securely.
    - Verify card details and handle authorization errors.
    - The relationship between `users` and `credit_cards` is One-to-Many(1-M), so each user can have multiple credit cards between each credit card can only belongs to a single user.

- **Real-Time Communication Chat:**
    - Responsible for facilitating real-time interactions between hospital staff, patients, and other stakeholders. This module supports chat messaging to enhance communication and collaboration within the hospital.
    - Instant text communication between users.
    - Secure storage and retrieval of messages with a One-on-one messaging.

## Technologies Used ⚙️
- **Backend:**
    - Django - Web framework for building the server-side logic
    - Django REST framework - Toolkit for building Web APIs
- **Database:**
    - PostgreSQL - Relational database management system
    - SQLite - Lightweight database used for local development
- **Data Population:**
    - Faker - Library for generating fake data
    - Python scripts for automated data population
- **Real-Time Communication:**
    - WebSocket - Protocol for real-time communication
    - Daphne - ASGI server for handling HTTP, HTTP2, and WebSocket protocols
    - ASGI - Asynchronous server gateway interface for handling asynchronous requests
- **Caching:**
    - Channels Redis - Channel layers that use Redis as a backing store
- **Containerization:**
    - DockerHub - Platform for developing, shipping, and running applications in containers
    - Docker – Software tool that is used to create, deploy and manage virtualized application containers on a common operating system (OS), with an ecosystem of allied tools
- **Deployment:**
    - AWS - Cloud platform from amazon for deploying and hosting web applications (we used t3.micro instance which is sometimes used in big corporations also aligned with best practicing while deploying as we connected to the instance throw ssh connection and used DockerHub)
    - Render - Cloud platform for deploying and hosting web applications
    - Railway - Cloud platform for building, shipping, and monitoring applications

## ER Diagram 🗃️
Here is HealthCare Entity-Relationship diagram
<div align="center">
  <a href="https://drive.google.com/file/d/12yLHMj6asLafd-rBsgR-EDg-U5gkEgK5/view?usp=sharing" target="_blank">
      <img src="https://drive.google.com/uc?id=1HgFwzFlk39phcAD4p8jIEX8leaVgL7-D"/>
  </a>
</div>

## API Documentation 📜
- **Swagger Documentation:**
  - Access the Swagger documentation [*here*](https://gp-mvz0.onrender.com/swagger/).
- **Postman Collection:**
  - Access the Postman collection [*here*](https://documenter.getpostman.com/view/23656997/2sA35G3MtP).

## Front-End Repository 🖌️
The front-end code for this project is developed using Android Native and can be found in the following repository:
[*Front-End Repository*](https://github.com/ALiyASSER0/Health_Care).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

