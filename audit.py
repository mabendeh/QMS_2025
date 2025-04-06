class InternalAudit:
    def __init__(self, date, auditor_name, audit_area, findings, corrective_action, status, owner, closure_date):
        self.audit_id = str(uuid.uuid4())[:8]
        self.date = date
        self.auditor_name = auditor_name
        self.audit_area = audit_area
        self.findings = findings
        self.corrective_action = corrective_action
        self.status = status
        self.owner = owner
        self.closure_date = closure_date
