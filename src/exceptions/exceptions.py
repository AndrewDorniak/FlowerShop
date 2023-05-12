from sqlalchemy.exc import SQLAlchemyError


class DuplicateExistingUserError(SQLAlchemyError):
    """ Raises uppon user registration when the user
    specifies existing unique fields in the database."""
    pass
