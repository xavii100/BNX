import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(filename)s:%(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

log.addHandler(stream_handler)