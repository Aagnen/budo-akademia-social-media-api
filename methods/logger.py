import logging
import colorlog

# Create a logger object
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the base logging level

# Check if handlers are already added to avoid duplicate logs
if not logger.handlers:
    # Create a handler for console output
    handler = colorlog.StreamHandler()

    # Define the log format
    log_format = "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s"

    # Create a formatter with colors
    formatter = colorlog.ColoredFormatter(
        log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG':    'white',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        },
        style='%'
    )

    # Add the formatter to the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

def main():
    logger.info("✅ Logger configuration module working correctly.")

if __name__ == "__main__":
    main()