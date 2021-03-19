import logging

from django.contrib.auth.models import BaseUserManager

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------------
# ManagerAccountUser
# -------------------------------------------------------------------------------
class ManagerAccountUser(BaseUserManager):
    """
    Provides manager methods for the user model.
    """

    # ---------------------------------------------------------------------------
    # create_user
    # ---------------------------------------------------------------------------
    def create_user(self, email, **kwargs):
        """
        This method creates a new user and its associated profile(empty)
        that can be updated whenever required.
        """

        if not email:
            raise ValueError('Users must have a valid email address...')

        try:
            password = kwargs.pop('password')

        except KeyError:
            logger.warning("Password for user %s not supplied", email)
            password = ''

        user = self.model(email=self.normalize_email(email), **kwargs)

        # update user password
        user.set_password(password)

        # save the new user
        user.save(using=self._db)

        return user

    # ---------------------------------------------------------------------------
    # create_superuser
    # ---------------------------------------------------------------------------
    def create_superuser(self, email, password):
        """
        This method creates a superuser for the system.
        
        It takes following arguments:
        1) email - email of superuser (required)
        2) password - strong password of superuser (required)
        3) is_active - set to true
        """

        logger.info('Creating superuser with email %s', email)

        user = self.create_user(email=email,
                                password=password,
                                is_staff=True,
                                is_superuser=True,
                                is_active=True
                                )

        # update user password
        user.set_password(password)

        # save the new user
        user.save(using=self._db)
        

        logger.info('Superuser %s successfully created!', user)

        return user
