"""
Role-Based Access Control (RBAC) module
Defines which pages each role can access
"""

# Role definitions and permissions
ROLE_PERMISSIONS = {
    'Student': ['Home', 'Student'],
    'Faculty': ['Home', 'Faculty'],
    'Developer': ['Home', 'Developer'],
    'Admin': ['Home', 'Student', 'Faculty', 'Developer', 'Admin']
}

def get_accessible_pages(role: str) -> list:
    """
    Get list of pages accessible to a role
    
    Args:
        role: User role
    
    Returns:
        List of accessible page names
    """
    return ROLE_PERMISSIONS.get(role, ['Home'])

def check_page_access(role: str, page: str) -> bool:
    """
    Check if a role has access to a specific page
    
    Args:
        role: User role
        page: Page name to check
    
    Returns:
        True if role has access, False otherwise
    """
    accessible_pages = get_accessible_pages(role)
    return page in accessible_pages

def get_role_description(role: str) -> str:
    """
    Get a description of role permissions
    
    Args:
        role: User role
    
    Returns:
        Description string
    """
    descriptions = {
        'Student': 'Access to personal learning analytics and performance metrics',
        'Faculty': 'Access to cohort performance, student analytics, and teaching insights',
        'Developer': 'Access to system monitoring, data quality, and technical metrics',
        'Admin': 'Full access to all dashboards and administrative functions'
    }
    return descriptions.get(role, 'Limited access')
