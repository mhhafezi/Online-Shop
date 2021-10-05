import logging

# Create a custom logger
logger = logging.getLogger(__name__)
# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('my_file.log')
logger.setLevel(logging.DEBUG)  # <<< Added Line
f_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.INFO)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(process)d - %(levelname)s - %(message)s %d-%b-%y %H:%M:%S')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
# Add handlers to the logger
logger.addHandler(c_handler)  # for print in output
logger.addHandler(f_handler)
