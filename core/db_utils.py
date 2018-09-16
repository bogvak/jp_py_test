from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # Creating instance of database object


def init_db():
    """ Initialising all tables in DB according to models
    Args:
        Nothing

    Returns:
        Nothing

    """
    db.drop_all()
    db.create_all()


def add_and_save_db(*args):
    """ Adding entities to DB ans committing changes
    Args:
        *args: List of entities to insert

    Returns:
        Nothing

    """
    for entity in args:
        db.session.add(entity)
    db.session.commit()


def save_db():
    """ Commit changes to DB
        Args:
            Nothing

        Returns:
            Nothing

    """
    db.session.commit()


def delete_from_db(*args):
    """ Delete from DB and committing changes
    Args:
        *args: List of entities to delete

    Returns:
        Nothing

    """
    for entity in args:
        db.session.delete(entity)
    db.session.commit()


def delete_from_db_no_commit(*args):
    """ Delete from DB without committing
        Args:
            *args: List of entities to delete

        Returns:
            Nothing

    """
    for entity in args:
        db.session.delete(entity)
