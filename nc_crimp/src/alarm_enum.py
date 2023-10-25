from enum import Enum

class Alarm(Enum):
    PART_DROP_LEFT_JIG = 9000
    PART_DROP_RIGHT_JIG = 9001
    PART_MISSING_STAMPING_MACHINE = 9002
    PART_DROP_AFTER_STAMPING_MACHINE = 9003
    PART_STUCK_UNLOADING = 9004
    PART_LOAD_STAMPING_MACHINE_FAILED = 9005
    NOT_IN_AUTO_MODE = 9006
    STAMP_TRIGGER_ERROR = 9007
    PUSHER_UNLOAD_FAILED = 9008
    PUSHER_LOAD_FAILED = 9009
    PART_DROP_PLACING_STAMPING_MACHINE = 9010
    PART_PRESENT_ERROR = 9011
    PART_PRESENT_ERROR_DANGEROUS = 9012
    ROBOT_NOT_HOME_POSITION = 9013
    EMERGENCY_STOP = 7
    UNKNOWN_ERROR = -1
    