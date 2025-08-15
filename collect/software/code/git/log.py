"""
avaktrahu/dataset

Logging utilities
"""

# =============================================================================
# Imports
#

import sys
from logging import DEBUG, Formatter, FileHandler, StreamHandler, getLogger

# =============================================================================
# Main
#

formatter = Formatter(
    fmt='%(process)d %(thread)d %(asctime)s %(module)s.%(filename)s:%(lineno)d [%(levelname)s] %(message)s',
)

file_handler = FileHandler(filename='diagnostic.log')
file_handler.setFormatter(formatter)

stream_handler = StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Get a logger instance
logger = getLogger(__file__)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(DEBUG)
