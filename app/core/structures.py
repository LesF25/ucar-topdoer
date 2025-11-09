from enum import Enum


class IncidentStatus(str, Enum):
    OPEN = 'Open'
    ACKNOWLEDGED = 'Acknowledged'
    IN_PROGRESS = 'In progress'
    RESOLVED = 'Resolved'
    CLOSED = 'Closed'


class IncidentSource(str, Enum):
    OPERATOR = 'Operator'
    MONITORING = 'Monitoring'
    PARTNER = 'Partner'
    EXTERNAL = 'External'
