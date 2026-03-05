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

9. Rating & Reviews (HR9) (Optional – If Time Permits)

Task 9.1: Design database tables for Reviews and Ratings

Store rating score, review text, reviewer (customer), restaurant reference

Enforce constraints (one review per customer per order/restaurant)

Task 9.2: Implement API to submit a rating and review for a completed order

Validate that the order is completed

Ensure only customers who placed the order can review

Task 9.3: Implement API to retrieve reviews and average ratings for a restaurant

Support sorting (most recent, highest rating)

Include pagination for large review sets

Task 9.4: Implement validation and moderation rules

Prevent duplicate reviews

Handle empty or invalid rating values

Task 9.5: Unit tests for review creation, validation, and retrieval

10. Statistics for System Administrators (HR10) (Optional – If Time Permits)

Task 10.1: Design data queries or views for administrative statistics

Orders, deliveries, restaurants, and drivers

Time-based aggregations (daily, weekly)

Task 10.2: Implement API to compute average delivery times

Per restaurant

System-wide averages

Task 10.3: Implement API to retrieve popular restaurants

Based on number of orders

Based on average rating (if HR9 implemented)

Task 10.4: Implement access control to restrict statistics APIs to admin users only

Task 10.5: Unit tests for statistics calculations and access control


Deliverables for Sprint 1

Database schema for all core backend entities.

Fully functional APIs for user management, menu management, orders, delivery, cost calculation, payment processing, and notifications.

Unit tests covering all implemented backend functionality.

Updated project board with sprint issues tracked and progress logged.
