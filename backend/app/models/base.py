from app.core.database import Base

# Import all models here so that Base.metadata has them registered
# before Alembic or direct table creators run.
from app.models import (  # noqa: F401
    User,
    Resume,
    ResumeVersion,
    JobDescription,
    ATSReport,
    MatchReport,
    ChatSession,
    AgentReport,
)
