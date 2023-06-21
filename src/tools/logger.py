import logging


def set_logger():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                        datefmt="%m-%d %H:%M",
                        filename="genetic_algorithm.log",
                        filemode="w")
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
