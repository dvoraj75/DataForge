class InvalidConfigurationError(Exception):
    pass


class InvalidJobConfigurationError(InvalidConfigurationError):
    pass


class JobDoesNotExistError(Exception):
    pass
