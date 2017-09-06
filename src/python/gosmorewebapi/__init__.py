import sys
import logging

logging.basicConfig( \
	stream=sys.stderr, \
	level=logging.WARN, \
	format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s.%(funcName)s %(message)s', \
	datefmt="%Y-%m-%dT%H:%M:%S" \
)
