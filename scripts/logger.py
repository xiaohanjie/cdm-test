import logging

def get_logger(name, file, formatter):
	handler = logging.FileHandler(file)
	handler.setFormatter(formatter)
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	for h in logger.handlers[:]:
		logger.removeHandler(h)
	logger.addHandler(handler)
	return logger
