"""Controller Exceptions"""


class TargetCntNotFoundError(Exception):
    """Target center not found"""
    def __init__(self, trg_cnt_id: int):
        super().__init__(f"Target center {trg_cnt_id} not found")


class TargetNotFoundError(Exception):
    """Target not found"""
    def __init__(self, trg_id: int):
        super().__init__(f"Target {trg_id} not found")
