"""
LUMINA OS - Security Utilities
JWT Authentication and Password Hashing for Enterprise System
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# JWT Configuration
SECRET_KEY = 'LUMINA_SUPER_SECRET_KEY_2026'
ALGORITHM = 'HS256'
DEFAULT_EXPIRE_HOURS = 24

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        # Check if password matches hash
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def create_access_token(data: Dict[str, Any], expires_delta: int = DEFAULT_EXPIRE_HOURS) -> str:
    """
    Create JWT access token
    
    Args:
        data: Payload data to encode in token
        expires_delta: Token expiration time in hours (default: 24 hours)
        
    Returns:
        Encoded JWT token string
    """
    try:
        # Create token payload
        to_encode = data.copy()
        
        # Set expiration time
        expire = datetime.utcnow() + timedelta(hours=expires_delta)
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        # Create JWT token
        encoded_jwt = jwt.encode(
            to_encode, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )
        
        return encoded_jwt
        
    except Exception as e:
        print(f"Token creation error: {e}")
        raise ValueError(f"Failed to create access token: {e}")

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Decoded payload if valid, None if invalid
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        
        # Check if token is expired
        exp = payload.get('exp')
        if exp and datetime.utcnow().timestamp() > exp:
            return None
            
        return payload
        
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

def create_refresh_token(data: Dict[str, Any], expires_delta: int = 168) -> str:
    """
    Create JWT refresh token (7 days default)
    
    Args:
        data: Payload data to encode in token
        expires_delta: Token expiration time in hours (default: 168 hours = 7 days)
        
    Returns:
        Encoded JWT refresh token string
    """
    try:
        # Create token payload
        to_encode = data.copy()
        
        # Set expiration time
        expire = datetime.utcnow() + timedelta(hours=expires_delta)
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        # Create JWT token
        encoded_jwt = jwt.encode(
            to_encode, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )
        
        return encoded_jwt
        
    except Exception as e:
        print(f"Refresh token creation error: {e}")
        raise ValueError(f"Failed to create refresh token: {e}")

def get_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """
    Get payload from token without expiration check
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload if valid, None if invalid
    """
    try:
        # Decode token without expiration check
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            options={"verify_exp": False}
        )
        
        return payload
        
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None
    except Exception as e:
        print(f"Token payload extraction error: {e}")
        return None

def is_token_expired(token: str) -> bool:
    """
    Check if token is expired
    
    Args:
        token: JWT token string
        
    Returns:
        True if expired, False if valid
    """
    try:
        payload = get_token_payload(token)
        if not payload:
            return True
            
        exp = payload.get('exp')
        if not exp:
            return True
            
        return datetime.utcnow().timestamp() > exp
        
    except Exception:
        return True

def generate_password_reset_token(email: str, expires_delta: int = 1) -> str:
    """
    Generate password reset token
    
    Args:
        email: User email for password reset
        expires_delta: Token expiration time in hours (default: 1 hour)
        
    Returns:
        Encoded JWT reset token string
    """
    try:
        # Create token payload
        to_encode = {
            "email": email,
            "type": "password_reset"
        }
        
        # Set expiration time
        expire = datetime.utcnow() + timedelta(hours=expires_delta)
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow()
        })
        
        # Create JWT token
        encoded_jwt = jwt.encode(
            to_encode, 
            SECRET_KEY, 
            algorithm=ALGORITHM
        )
        
        return encoded_jwt
        
    except Exception as e:
        print(f"Password reset token creation error: {e}")
        raise ValueError(f"Failed to create password reset token: {e}")

def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify password reset token and return email
    
    Args:
        token: Password reset token string
        
    Returns:
        Email if valid, None if invalid
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        
        # Check token type
        if payload.get('type') != 'password_reset':
            return None
            
        # Check expiration
        exp = payload.get('exp')
        if exp and datetime.utcnow().timestamp() > exp:
            return None
            
        return payload.get('email')
        
    except jwt.ExpiredSignatureError:
        print("Password reset token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid password reset token: {e}")
        return None
    except Exception as e:
        print(f"Password reset token verification error: {e}")
        return None

# Security utility functions
def generate_session_id() -> str:
    """Generate unique session ID"""
    import uuid
    return str(uuid.uuid4())

def sanitize_input(input_string: str) -> str:
    """Sanitize user input to prevent injection"""
    if not input_string:
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
    sanitized = input_string
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")
    
    return sanitized.strip()

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Dictionary with validation results
    """
    results = {
        "is_valid": True,
        "errors": [],
        "score": 0
    }
    
    # Check length
    if len(password) < 8:
        results["errors"].append("Password must be at least 8 characters long")
        results["is_valid"] = False
    else:
        results["score"] += 1
    
    # Check for uppercase
    if not any(c.isupper() for c in password):
        results["errors"].append("Password must contain at least one uppercase letter")
        results["is_valid"] = False
    else:
        results["score"] += 1
    
    # Check for lowercase
    if not any(c.islower() for c in password):
        results["errors"].append("Password must contain at least one lowercase letter")
        results["is_valid"] = False
    else:
        results["score"] += 1
    
    # Check for numbers
    if not any(c.isdigit() for c in password):
        results["errors"].append("Password must contain at least one number")
        results["is_valid"] = False
    else:
        results["score"] += 1
    
    # Check for special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        results["errors"].append("Password must contain at least one special character")
        results["is_valid"] = False
    else:
        results["score"] += 1
    
    return results

# Test functions for development
def test_security_functions():
    """Test security functions"""
    print("🧪 Testing Security Functions")
    print("=" * 50)
    
    # Test password hashing
    password = "hunter2026"
    hashed = hash_password(password)
    print(f"✅ Password hashed: {hashed[:20]}...")
    
    # Test password verification
    is_valid = verify_password(password, hashed)
    print(f"✅ Password verification: {is_valid}")
    
    # Test token creation
    token_data = {"user_id": 1, "email": "admin@lumina.os", "role": "admin"}
    token = create_access_token(token_data)
    print(f"✅ Token created: {token[:20]}...")
    
    # Test token verification
    payload = verify_token(token)
    print(f"✅ Token verified: {payload is not None}")
    
    # Test token expiration
    print(f"✅ Token expired: {is_token_expired(token)}")
    
    # Test email validation
    test_email = "admin@lumina.os"
    print(f"✅ Email validation: {validate_email(test_email)}")
    
    # Test password strength
    strength = validate_password_strength("Hunter2026!")
    print(f"✅ Password strength: {strength['score']}/5, Valid: {strength['is_valid']}")
    
    print("✅ All security tests completed!")

if __name__ == "__main__":
    test_security_functions()
