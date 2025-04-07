# Uplift

**Uplift** is a platform designed to centralize all free community resources and connect low-income users with services they might not be aware of—not limited to federal benefits.

---

## 🚀 Prerequisites

Before you begin, make sure the following are installed on your machine:

- A **GitHub account**
- A **Git client** (either terminal-based or GUI like GitHub Desktop or the VSCode Git extension)
- **Visual Studio Code** with the **Python extension**
- A distribution of **Python** (Anaconda or Miniconda is recommended for this course)

---

## 🗂 Codebase Organization

The project consists of **three major components**, each running in its own Docker container:

### 📦 `./app` – Streamlit App

- This is the frontend of the platform.
- Built with **Streamlit**, a Python-based framework for creating simple and interactive web apps.
- This is the main interface for users.

### 🔧 `./api` – Flask REST API

- The backend logic of the application.
- Built using **Flask** and provides REST endpoints to interact with the database.
- Folder structure:
  - `backend/` – where the Flask app and route handlers are set up
  - `server.py` – starts the backend server

### 🗃 `./database-files` – MySQL Database

- Contains SQL scripts that initialize and seed the MySQL database.
- Automatically run when the corresponding Docker container starts.

---

## ⚙️ Project Setup

> **Important:** Always work on a **feature branch** instead of committing directly to `main`.

### 1. Set Up Environment Variables

- Navigate to the `./api` folder.
- Copy `.env.template` and rename it to `.env`.
- Fill in all required values.

---

## 🐳 Using Docker with Taskfile

Ensure Docker is running before using these commands. You can also use **Docker Desktop GUI** for easier management after the first run. This removes the hassle of copy pasting long docker commands every time.

### 📋 View All Available Tasks
```bash
task --list-all
```

### ▶️ Start Containers
```bash
task all:up     # Starts the main app, API, and DB
task test:up    # Starts the test environment
```

### ⏹ Stop Containers
```bash
task all:down   # Stops the main app, API, and DB
task test:down  # Stops the test environment
```

### 🗄 Start Only Database
```bash
task all:db     # Starts only the main DB
task test:db    # Starts only the test DB
```

---

## 🔐 Role-Based Access Control (RBAC)

The app includes a simple Role-Based Access Control (RBAC) system built with Streamlit (without usernames/passwords). Roles determine what pages and features a user can see.

### 👥 Supported Roles

- **Political Strategist**
- **USAID Worker**
- **System Administrator**  
  _(Used for system-level actions like re-training ML models)_

---

## 🧭 Understanding RBAC Implementation

### 1. Sidebar Customization
- Located at: `app/src/.streamlit/config.toml`
- Disables Streamlit’s default sidebar navigation.
- Enables custom role-based navigation.

### 2. Navigation Module
- File: `app/src/modules/nav.py`
- Contains page-link functions grouped by user role.
- Uses `st.sidebar.page_link(...)` to render pages dynamically.

### 3. Home Page Behavior
- File: `app/src/Home.py`
- Displays 3 buttons for user role selection.
- On button click:
  - Updates `st.session_state` with user info
  - Redirects to the role-specific homepage using `st.switch_page(...)`

### 4. Sidebar Links
- Each page calls `SideBarLinks(...)` to load links based on the user’s role.

### 5. Role-Based Page Naming
Pages are grouped and prefixed by role:

| Prefix | Role                |
|--------|---------------------|
| `0*`   | Political Strategist |
| `1*`   | USAID Worker         |
| `2*`   | System Administrator |

---

## 🧭 Getting Started Summary

1. Clone the repo and set up your own branch.
2. Navigate through the codebase:  
   `./app` ➝ `./api` ➝ `./database-files`
3. Set up `.env` in the `api` folder.
4. Use `task` commands to spin up the app.
5. Explore the RBAC features and page routing.

---

Happy building! 🚀
