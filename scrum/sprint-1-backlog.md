Sprint 1 Backlog – Backend Implementation

Sprint Duration: February 13, 2026 – March 13, 2026
Sprint Goal:
Implement the foundational backend functionality for user management, menu handling, order processing, delivery assignment, cost calculation, and simulated payment processing. The sprint focuses on ensuring core data models, APIs, and business logic are functional, accurate, and secure, enabling basic system operations for both customers and restaurant owners.

Backend Issues / Tasks
1. User Management & Authentication (HR1)

Task 1.1: Design database tables for Users (customers, restaurant owners), including roles and permissions.

Task 1.2: Implement account creation APIs with input validation (unique username, email, password).

Task 1.3: Implement login authentication API with role-based access control.

Task 1.4: Implement session management / JWT token system for secured authentication.

Task 1.5: Unit tests for authentication and role-based access.


2. Menu Management (HR2)

Task 2.1: Design database tables for Restaurants, Menus, and Menu Items with constraints.

Task 2.2: Implement API to create, update, and delete menu items for a restaurant.

Task 2.3: Implement validation logic to ensure menu items belong to the correct restaurant.

Task 2.4: Implement API to retrieve menu items with filters (availability, category).

Task 2.5: Unit tests for menu creation and validation.


3. Menu & Restaurant Browsing (HR3)

Task 3.1: Implement API to search restaurants by name or cuisine.

Task 3.2: Implement API to search menu items across restaurants.

Task 3.3: Add pagination to API results to handle large datasets.

Task 3.4: Unit tests for search and browsing functionality.


4. Order Management (HR4)

Task 4.1: Design database tables for Orders, Order Items, and Status Tracking.

Task 4.2: Implement API to create, modify, and submit orders (cart system).

Task 4.3: Implement logic to prevent modifications after order completion.

Task 4.4: Implement API to fetch order status for a customer or restaurant.

Task 4.5: Unit tests for order creation, modification, and status updates.


5. Delivery Assignment (HR5)

Task 5.1: Design database tables for Drivers and Delivery Assignments.

Task 5.2: Implement logic to assign deliveries to the nearest available driver.

Task 5.3: Implement APIs for restaurants to assign or reassign delivery drivers.

Task 5.4: Implement APIs to track driver location and status updates.

Task 5.5: Unit tests for delivery assignment and driver tracking.


6. Cost Calculation (HR6)

Task 6.1: Implement logic to calculate total order cost (items + tax + delivery fee).

Task 6.2: Implement APIs to return cost breakdown to customers.

Task 6.3: Unit tests for accurate cost calculations.


7. Payment Processing (Simulated) (HR7)

Task 7.1: Implement simulated payment gateway API to process transactions.

Task 7.2: Implement backend logic to handle payment confirmation/rejection.

Task 7.3: Implement APIs for saving and retrieving customer payment methods.

Task 7.4: Ensure order fulfillment only after successful payment.

Task 7.5: Unit tests for payment processing and order validation.


8. Notifications (HR8)

Task 8.1: Design database structure for notifications (orders, delivery status).

Task 8.2: Implement API for sending notifications to customers and restaurants.

Task 8.3: Implement backend logic for triggering notifications at key order stages.

Task 8.4: Unit tests for notification delivery and logging.


Optional (If Time Permits)

Rating & Reviews (HR9)

Database tables and APIs for adding/retrieving reviews and ratings.


Statistics for System Administrators (HR10)

APIs to compute average delivery times and popular restaurants.


Deliverables for Sprint 1

Database schema for all core backend entities.

Fully functional APIs for user management, menu management, orders, delivery, cost calculation, payment processing, and notifications.

Unit tests covering all implemented backend functionality.

Updated project board with sprint issues tracked and progress logged.
