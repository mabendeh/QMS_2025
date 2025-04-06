class CalibrationRecord:
    def __init__(self, date, equipment_id, description, calibration_result, status, calibrated_by, next_due_date):
        self.record_id = str(uuid.uuid4())[:8]
        self.date = date
        self.equipment_id = equipment_id
        self.description = description
        self.calibration_result = calibration_result
        self.status = status
        self.calibrated_by = calibrated_by
        self.next_due_date = next_due_date
