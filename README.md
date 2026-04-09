# Step-by-Step Deployment and Handover Guide:

## 1. Introduction
This guide explains how to set up, run, and maintain the delivery application from scratch. It is written so that another developer, TA, or project handoff team member can understand the system requirements, install the project, and maintain it over time. Docker will be used to run the system consistently across different environments.

## 2. Project Overview 
This project is a delivery application consisting of both backend and frontend components. The backend is built using FastAPI, which supports core features such as user authentication, restaurant and menu management, order processing, delivery assignment, payment handling, and notifications.The frontend provides the user interface for interacting with the system. It communicates with the backend API to display data and perform actions such as browsing restaurants, placing orders, and managing user interactions The system is structured using modular components, including routers, services, schemas,  and data repositories

## 3. Installation Instructions

### 3.1 Prerequisites
Before setting up the project, make sure the following tools are installed on the computer:
- Git
- Docker
- Docker Compose
- Visual Studio Code
- Python 3.x (only required for local development or testing outside Docker)
- node.js and npm

These tools are required to clone the repository, view or edit the code, and run the application in a containerized environment. This setup will run both the backend and frontend services of the application using Docker.

### 3.2 Clone the Repository
Open a terminal  (Command Prompt, PowerShell, or Mac Terminal)

Navigate to the folder where you want to store the project using the cd command. For example: 

cd Desktop

Run the following command to clone the repository 

git clone https://github.com/arynrosh/group-18-gobbl.git

Move into the project folder:

cd group-18-gobbl

This will download the full codebase onto the machine so it can be built and run locally.

Note: The terminal is used to run setup commands. The project can be opened and edited using a code editor such as Visual Studio Code.

### 3.3 Open the Project
Open the folder in your code editor. For example, using Visual Studio Code:

code .

This command opens the current folder (group-18-gobbl) in Visual Studio Code.

Note: If the code command does not work, you can open Visual Studio Code manually and select File → Open Folder, then choose the project directory

### 3.4 Verify Project Files
In your code editor or file explorer, open the project folder (group-18-gobbl).

Confirm that the following project files are present: 
- app/
- app/data/
- frontend/
- requirements.txt
- Dockerfile
- Docker-compose.yml
- requirements.txt

These are required for the application to run correctly. If any of these are missing, the setup may fail, or the application may not run correctly.

### 3.5 Run the System with Docker
This project uses Docker Compose to run both the frontend and backend together.

To build and start the containers, run:

docker compose up --build -d

This command:
- builds the Docker images
- starts the backend service
- starts the frontend service
- runs the system in detached mode

If the containers were already built and you only want to start them again, run:

docker compose up -d

### 3.6 Stop the application

docker compose down

### 3.7 Rebuild after changes 
If major code or dependency changes are made, rebuild the containers with:

docker compose build –no-cache
Docker compose up -d

### 3.8 Access the Application
Once the Docker containers are running successfully. Open a browser and go to http://localhost:8000

To access the FastAPI interactive documentation, go to: http://localhost:8000/docs

Frontend application: http://localhost:5173 or the frontend port specified in docker-compose.yml

This allows users and developers to test endpoints directly through the browser.

## 4. Dependencies
The following tools, libraries, and services are required to run the application.

### 4.1 System Tools
- Docker  
 Used to build and run the application in a containerized environment.
- Docker Compose  
 Used to manage and run multi-container applications.
- Git  
 Used to clone and manage the project repository.
- Visual Studio Code (or any code editor)  
 Used to view and edit project files.
- Python 3.x (optional)  
 Only required for local development or testing outside of Docker.
- Node.js / npm (optional for local frontend development)

### 4.2 Python Dependencies
The backend relies on the following Python packages:
- FastAPI (v0.110.0)  
 Core web framework used to build the API.
- Uvicorn [standard] (v0.29.0)  
 ASGI server is used to run the FastAPI application.
- python-jose [cryptography] (v3.3.0)  
 Used for JWT token creation and authentication.
- python-multipart (v0.0.9)  
 Handles form data in HTTP requests.
- Pytest (v8.1.1)  
 Testing framework used for unit and integration tests.
- pytest-cov (v5.0.0)  
 Used to generate test coverage reports.
- httpx (v0.27.0)  
 HTTP client used for testing API endpoints.

All Python dependencies are listed in the requirements.txt file and are automatically installed when building the Docker container.

### 4.3 Data Storage
JSON-based storage (app/data/)  
Used to store application data such as orders, menus, notifications, and users.

### 4.4 Environment Configuration
The application uses environment variables defined in docker-compose.yml. One important variable is SECRET_KEY, which is passed to the backend service and is used for authentication and security. It is required for signing and verifying authentication tokens

### 4.5 External Services
This application does not use any external APIs or third-party services. Features such as payment processing and notifications are simulated within the system for development and testing purposes.

### 4.6 Frontend Dependencies
The frontend application is located in the frontend/ directory and uses a Node.js-based development environment.

The following tools and libraries are required:
- Node.js (latest LTS version recommended)  
 Used to run the frontend development environment and manage dependencies.
- npm (Node Package Manager)  
 Used to install and manage frontend packages.
- Vite  
 Used as the frontend build tool and development server.
- TypeScript  
 Used for type-safe JavaScript development.
- Tailwind CSS  
 Used for styling the user interface.

All frontend dependencies are defined in the package.json file and can be installed by running npm install inside the frontend/ directory.

## 5. Maintenance Requirements

### 5.1 Account Credentials
The application uses authentication with different user roles (e.g., customers, restaurant owners, drivers, and admins).
User accounts can be created through the application.
Authentication is handled using JWT tokens.
A SECRET_KEY is used to sign and verify authentication tokens.
The SECRET_KEY is defined in docker-compose.yml.
Some test accounts may be stored in app/data/users.json for development purposes.

### 5.2 Data Management
All application data is stored in JSON and CSV files located in the app/data/ directory.

The initial dataset for restaurants and food delivery information was obtained from a kaggle dataset (food_delivery.csv). The dataset was used as a base and then extended by converting relevant information into JSON format with added fields

The application reads and writes to these JSON files during runtime to simulate a database system

These files store users, orders, menus, notifications, and other system data.

The application reads and writes to these files during runtime.

Maintenance considerations:
- Back up the app/data/ folder regularly.
- Avoid editing JSON files while the application is running.
- Make sure there are proper file permissions for read/write access.

### 5.3 Configuration
The system is configured using environment variables defined in docker-compose.yml.

One important configuration variable is:

SECRET_KEY  
Used by the backend service for authentication and security (e.g., signing and verifying tokens)

Other environment variables may include service-specific configuration such as API routing between the frontend and backend.

Maintenance considerations:
- Update environment variables when moving between environments.
- Keep sensitive values secure and do not expose them 
- modifying service definitions
- Restart containers after making configuration changes:

docker-compose down
docker-compose up --build

### 5.4 Frontend Maintenance
Frontend maintenance may involve:
- updating UI components
- changing frontend routes or pages
- updating API request URLs if backend ports or endpoints change
- reinstalling frontend dependencies if package.json changes
- rebuilding containers after frontend code changes

### 5.5 Backend Maintenance
Backend maintenance may involve:
- updating API routes
- modifying service or repository logic
- maintaining schemas and request validation
- updating authentication logic
- checking JSON data consistency
- rerunning tests after changes

### 5.6 External Services
The application does not use external APIs or third-party services. Features such as payment processing and notifications are simulated within the system.

