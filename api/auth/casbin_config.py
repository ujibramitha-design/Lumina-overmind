"""
Casbin Authorization Configuration
RBAC policy enforcement for LUMINA OS Enterprise
"""

import casbin
from casbin import Enforcer
from typing import Optional
import os

# Casbin model configuration
MODEL_CONFIG = """
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = r.sub == p.sub && (r.obj == p.obj || p.obj == "*") && (r.act == p.act || p.act == "*")
"""

# Model and policy file paths
MODEL_FILE = "api/auth/model.conf"
POLICY_FILE = "api/auth/policy.csv"

def get_enforcer() -> Optional[Enforcer]:
    """Get Casbin enforcer instance"""
    try:
        # Create enforcer with model and policy file
        enforcer = Enforcer(MODEL_FILE, POLICY_FILE)
        
        return enforcer
    except Exception as e:
        print(f"Error creating Casbin enforcer: {e}")
        return None

def initialize_policy():
    """Initialize default RBAC policies"""
    # Ensure directory exists
    os.makedirs(os.path.dirname(POLICY_FILE), exist_ok=True)
    
    # Write model file
    with open(MODEL_FILE, 'w') as f:
        f.write(MODEL_CONFIG)
    
    # Write policy file
    policy_content = """p, admin, *, *
p, manager, leads, read
p, manager, leads, write
p, manager, projects, read
p, manager, projects, write
p, user, leads, read
p, user, projects, read
p, user, dashboard, read
p, user, growth, read
p, user, geo-intel, read
p, user, inbox, read
p, user, jarvis, read
p, user, workflows, read
p, user, settings, read
"""
    
    with open(POLICY_FILE, 'w') as f:
        f.write(policy_content)
    
    print(f"✅ Casbin model initialized at {MODEL_FILE}")
    print(f"✅ Casbin policy initialized at {POLICY_FILE}")

def check_permission(enforcer: Enforcer, subject: str, object: str, action: str) -> bool:
    """Check if subject has permission to perform action on object"""
    if not enforcer:
        return True  # Fallback to allow if enforcer not available
    
    return enforcer.enforce(subject, object, action)

if __name__ == "__main__":
    # Initialize policy
    initialize_policy()
    
    # Test enforcer
    enforcer = get_enforcer()
    if enforcer:
        print("✅ Casbin enforcer created successfully")
        
        # Test permissions
        print("Admin can read leads:", check_permission(enforcer, "admin", "leads", "read"))
        print("User can write leads:", check_permission(enforcer, "user", "leads", "write"))
        print("Manager can write projects:", check_permission(enforcer, "manager", "projects", "write"))
