"""Target Exceptions"""


class TargetCntNotFoundError(Exception):
    """Target center not found"""
    def __init__(self, trg_cnt: int | str):
        super().__init__(f"Target center {trg_cnt} not found")


class TargetNotFoundError(Exception):
    """Target not found"""
    def __init__(self, trg_id: int):
        super().__init__(f"Target {trg_id} not found")


class TargetCntExist(Exception):
    """"Target already exist"""
    def __init__(self, target_cnt_name):
        super().__init__(f"Target Center {target_cnt_name} already exist")

