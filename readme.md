# Expense Sharing Application

## Overview

This backend service provides functionality for an expense sharing application, allowing users to add expenses, split them among participants, and maintain balances between users.

## Architecture

The application follows a standard Django architecture with Django REST Framework for building RESTful APIs. The main components include:

- **Models:** Define the data models for users, expenses, and expense participants using Django models.
- **Views:** Implement API endpoints using Django REST Framework's class-based views.
- **Serializers:** Serialize and deserialize data between JSON and Python objects.
- **Business Logic:** Implement logic for calculating and updating balances based on different expense types.
- **Task Queue (Celery):** Use Celery for handling asynchronous tasks, such as sending emails.

- **Structure of Classes:**

**Models**

- **User:** Represents a user with userId, name, email, mobile_number.
- **Expense:** Represents an expense with name, notes, image, amount, payer, participants, created_at, share_type.
- **ExpenseParticipant:** Represents the participants in an expense with expense, user, share_type, value.
- **Balance**Represents the participants  expense with debtor,creditor,amount.

- **Serializers**

- **UserSerializer:**Serializes User model.
- **ExpenseSerializer:** Serializes Expense model, including nested serialization of participants.
- **ExpenseParticipantSerializer:** Serializes ExpenseParticipant model.
- **BalanceSerializer**Serializes Balance model.




## API Contracts

### Users

#### `POST /api/register/`

Get a list of all users.

#### `GET /api/users/{user_id}/`

Get details of a specific user.

### Expenses

#### `POST /api/expense/`

Register User

```json
{
    "email": "shivasingh@gmail.com",
    "name": "Shiva",
    "mobile": "9624037027",
    "password": "admin@123",
    "password2": "admin@123"
}

Create a new expense.

```json
{
  "name": "Monthly Rent",
  "notes":"add some nots",
  "image":"add image",
  "amount": 1200.00,
  "payer": 1,
  "participants": [2, 3, 4],
  "share_type": "EQUAL"
}
