class AIReDTeamError(Exception):
    """Base exception for framework errors."""


class TestCaseValidationError(AIReDTeamError):
    """Raised when a test case definition is invalid."""
