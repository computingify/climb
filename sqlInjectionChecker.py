import re

class SQLInjectionChecker:
    """
    A class to check for potential SQL injection patterns in input strings.
    """

    def __init__(self):
        # Regular expression to match common SQL injection patterns
        self.sql_injection_pattern = re.compile(
            r"(--|\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC|DECLARE|TRUNCATE|ALTER)\b|--|;|/\*|\*/|')",
            re.IGNORECASE
        )

    def is_not_potential_injection(self, input_string: str) -> bool:
        """
        Checks if the input string contains potential SQL injection patterns.
        
        Args:
            input_string (str): The string to check.
        
        Returns:
            bool: True if potential injection is detected, False otherwise.
        """
        return not bool(self.sql_injection_pattern.search(input_string))

    def _is_safe_input(self, input_string: str) -> bool:
        """
        Checks if the input string contains only alphanumeric characters,
        which is a simple whitelist-based approach to validate inputs.
        
        Args:
            input_string (str): The string to check.
        
        Returns:
            bool: True if the input is considered safe, False otherwise.
        """
        return input_string.isalnum()

    def is_safe(self, input_string: str) -> bool:
        """
        Performs a comprehensive check on the input string.
        
        Args:
            input_string (str): The string to check.
        
        Returns:
            bool: True if potential injection is detected, False otherwise.
        """
        if not self._is_safe_input(input_string) and not self.is_not_potential_injection(input_string):
            return False
        
        return True
