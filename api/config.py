from enum import Enum
from logging import ERROR

DOTENV_PATH = './.env'
OUTPUT_PATH = 'results/'
MODELS_PATH = 'model/'


class API_Status(int,Enum):
    OKAY = 100
    NOT_FOUND = 101
    BAD_PAYLOAD = 102
    SESSION_EXPIRED = 103
    BAD_TYPE = 104
    SESSION_NOT_FOUND = 105
    ERROR = 106


class API_Status_Message(str, Enum):
    CREATED = 'Item Created'
    LIST = 'Okay'
    RETURNED = 'Item found'
    NOT_FOUND = 'Item not found'
    BAD_PAYLOAD = 'Bad Request'
    BAD_TYPE = 'Value Type incompatible'
    SESSION_EXPIRED =  'Session has Expired, Login'
    SESSION_NOT_FOUND = 'Session not found'
    ERROR = 'Model Failed'
    MISSING = 'File missing'
    WRONG_FORMAT = 'Incorrect File format'
    PREDICT = 'Prediction Conputed'

def days_in_batch(max_date, questiondate ):

    x = max_date - questiondate
    x = x.days
    if x == 0:
        return 1
    return x

categorical = ['user_badge_type']
numerical = ['user_reputation_score', 'votes', 'answer', 'views', 'accepted_answer','user_badge_number',  'tags_count', 'days_in_queue']
column_name = ['user_reputation_score', 'votes','answer', 'views','accepted_answer',  'user_badge_number','days_in_queue', 'User Badge bronze','User Badge gold','User Badge silver', 'No User Badge']