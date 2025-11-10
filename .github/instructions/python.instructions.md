---
applyTo: '**'
---

# Python Coding Guidelines for Flask Application

## Core Philosophy

This project follows the **Zen of Python** (PEP 20) principles:
- **Simple is better than complex**
- **Explicit is better than implicit**
- **Readability counts**
- **Flat is better than nested**
- **Sparse is better than dense**

## Architecture Pattern: Thin Controllers, Thick Services

### Layer Responsibilities

#### 1. Controllers (Thin) - `src/controllers/`
**Purpose:** Route handling and template rendering ONLY

**Responsibilities:**
- Define routes using Flask decorators
- Extract request data (query params, form data, JSON)
- Call service layer functions
- Return rendered templates or JSON responses
- Handle HTTP-specific concerns (status codes, redirects)

**Controllers Should NOT:**
- ❌ Contain business logic
- ❌ Directly interact with databases
- ❌ Perform calculations or data transformations
- ❌ Make external API calls
- ❌ Handle complex validation

**Example:**
```python
from flask import Blueprint, render_template, request, jsonify
from src.services.user_service import get_user_dashboard_data, create_new_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    """Render user dashboard page.
    
    Returns:
        str: Rendered HTML template with dashboard data
    """
    user_id = request.args.get('user_id')
    dashboard_data = get_user_dashboard_data(user_id)
    return render_template('private/user/dashboard/index.html', data=dashboard_data)

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user.
    
    Returns:
        tuple: JSON response and HTTP status code
    """
    user_data = request.get_json()
    result = create_new_user(user_data)
    return jsonify(result), 201
```

#### 2. Services (Thick) - `src/services/`
**Purpose:** Business logic and orchestration

**Responsibilities:**
- ✅ All business logic
- ✅ Data validation and transformation
- ✅ Orchestrate multiple model calls
- ✅ External API integrations
- ✅ Complex calculations
- ✅ Error handling and logging
- ✅ Transaction management

**Services Should NOT:**
- ❌ Handle HTTP requests/responses directly
- ❌ Render templates
- ❌ Write raw SQL (use models instead)

**Example:**
```python
from src.models.user_model import User
from src.models.activity_model import Activity
from src.utils.validators import validate_email
from typing import Dict, Any

def get_user_dashboard_data(user_id: str) -> Dict[str, Any]:
    """Retrieve and prepare dashboard data for a user.
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Dictionary containing user info and recent activities
        
    Raises:
        ValueError: If user_id is invalid or user not found
    """
    if not user_id:
        raise ValueError("User ID is required")
    
    user = User.get_by_id(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    recent_activities = Activity.get_recent_by_user(user_id, limit=10)
    
    return {
        'user': user.to_dict(),
        'activities': [activity.to_dict() for activity in recent_activities],
        'stats': _calculate_user_stats(user_id)
    }

def _calculate_user_stats(user_id: str) -> Dict[str, int]:
    """Calculate statistics for a user.
    
    Private helper function (prefixed with underscore).
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Dictionary with stat names and values
    """
    total_activities = Activity.count_by_user(user_id)
    return {
        'total_activities': total_activities,
        'completion_rate': Activity.get_completion_rate(user_id)
    }
```

#### 3. Models (Thin) - `src/models/`
**Purpose:** Database interaction ONLY

**Responsibilities:**
- ✅ Define database schema/tables
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Simple database queries
- ✅ Data serialization (to_dict, from_dict)

**Models Should NOT:**
- ❌ Contain business logic
- ❌ Perform complex validations
- ❌ Make decisions about data processing
- ❌ Call other services or external APIs

**Example:**
```python
from sqlalchemy import Column, Integer, String, DateTime
from src.database import db
from datetime import datetime
from typing import Optional, List

class User(db.Model):
    """User model for database interaction.
    
    Attributes:
        id: Primary key
        email: User's email address
        name: User's full name
        created_at: Account creation timestamp
    """
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Retrieve user by ID.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            User instance or None if not found
        """
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Retrieve user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User instance or None if not found
        """
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_all(cls, limit: int = 100) -> List['User']:
        """Retrieve all users with optional limit.
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List of User instances
        """
        return cls.query.limit(limit).all()
    
    def save(self) -> None:
        """Persist user to database."""
        db.session.add(self)
        db.session.commit()
    
    def delete(self) -> None:
        """Remove user from database."""
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary.
        
        Returns:
            Dictionary representation of user
        """
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

## Function Design Principles

### 1. Single Responsibility
Each function should do ONE thing and do it well. Max 20-25 lines per function.

### 2. Type Hints & Parameters
- Use type hints for ALL parameters and returns
- Maximum 3-5 parameters per function
- Return early to avoid deep nesting

### 3. Example
```python
def get_user(user_id: int) -> Optional[dict]:
    """Retrieve active user by ID.
    
    Args:
        user_id: User's unique identifier
        
    Returns:
        User dictionary or None if not found/inactive
    """
    user = User.query.get(user_id)
    
    if not user or not user.is_active:
        return None
    
    return user.to_dict()
```

## Documentation Standards

### Docstrings (Required for ALL functions/classes)
Use Google-style docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Short one-line description.
    
    Longer description if needed explaining what the function does,
    any important details, or context.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ErrorType: When and why this error occurs
        
    Examples:
        >>> function_name("value1", 42)
        expected_output
    """
    pass
```

### Class Docstrings
```python
class ClassName:
    """Short description of the class.
    
    Longer description explaining purpose, usage, and any
    important implementation details.
    
    Attributes:
        attribute1: Description of attribute
        attribute2: Description of attribute
        
    Example:
        >>> obj = ClassName(param1, param2)
        >>> obj.method()
    """
    pass
```

## Code Style & Formatting

**Naming Conventions:**
- Functions/Variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

**Imports (ordered):**
```python
# Standard library
import os
from typing import Dict, List, Optional

# Third-party
from flask import Blueprint, request

# Local application
from src.models.user_model import User
```

**Formatting:**
- Max 88 characters per line
- 2 blank lines between top-level functions/classes
- 1 blank line between class methods

## Error Handling

**Explicit Errors:**
```python
def get_user_by_email(email: str) -> User:
    """Retrieve user by email address.
    
    Raises:
        ValueError: If email is invalid
        UserNotFoundError: If user doesn't exist
    """
    if not email or '@' not in email:
        raise ValueError(f"Invalid email format: {email}")
    
    user = User.get_by_email(email)
    if not user:
        raise UserNotFoundError(f"User with email {email} not found")
    
    return user
```

## Type Hints (Required)

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional, Union, Any, Tuple

def process_users(
    user_ids: List[int],
    filters: Optional[Dict[str, Any]] = None
) -> Tuple[List[User], int]:
    """Process multiple users with optional filters.
    
    Args:
        user_ids: List of user IDs to process
        filters: Optional dictionary of filter criteria
        
    Returns:
        Tuple of (processed users list, total count)
    """
    pass
```

## Anti-Patterns to Avoid

### 1. Deep Nesting
❌ Avoid more than 3 levels of indentation

**Bad:**
```python
def process(data):
    if data:
        if data.get('user'):
            if data['user'].get('email'):
                if validate_email(data['user']['email']):
                    pass  # Too deep!
```

**Good:**
```python
def process(data: dict) -> None:
    if not data or not data.get('user'):
        return
    
    email = data['user'].get('email')
    if not email or not validate_email(email):
        return
    
    # Process email
```

### 2. Mutable Default Arguments
❌ Never use mutable defaults

**Bad:**
```python
def add_item(item, items=[]):  # Bug: shared list!
    items.append(item)
    return items
```

**Good:**
```python
def add_item(item: Any, items: Optional[List] = None) -> List:
    if items is None:
        items = []
    items.append(item)
    return items
```

### 3. Magic Numbers/Strings
❌ Use named constants

**Bad:**
```python
if user.role == 'admin' and user.level > 5:
    pass
```

**Good:**
```python
ADMIN_ROLE = 'admin'
SENIOR_LEVEL_THRESHOLD = 5

if user.role == ADMIN_ROLE and user.level > SENIOR_LEVEL_THRESHOLD:
    pass
```

## Quick Reference Checklist

Before committing code, verify:

- [ ] All functions have docstrings
- [ ] All functions have type hints
- [ ] Controllers only handle routing/templates
- [ ] Services contain all business logic
- [ ] Models only interact with database
- [ ] Functions do ONE thing
- [ ] No function exceeds 25 lines
- [ ] No nesting deeper than 3 levels
- [ ] No magic numbers or strings
- [ ] Proper error handling
- [ ] Follows naming conventions
- [ ] Imports are organized
- [ ] Code is readable and simple

## Resources

- [PEP 8 - Style Guide](https://pep8.org/)
- [PEP 20 - The Zen of Python](https://www.python.org/dev/peps/pep-0020/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)