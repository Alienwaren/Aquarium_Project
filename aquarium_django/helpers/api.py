from monitor.models import Habitat


def write_data_and_log(value: float, target_habitat: Habitat, topic: str) -> None:
    """
    Write data to database; log and actual value of habitat
    :param topic:
    :param value: Value to be
    :param target_habitat: Target habitat which holds data
    """
    if topic == "temperature":
        target_habitat.actual_temperature = value
    elif topic == "insolation":
        target_habitat.actual_insolation = value

    target_habitat.save()

