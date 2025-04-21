from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory

from app.database.models import DollarHistory, User
from tests.bot.v1.database import test_scoped_session


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_scoped_session

    telegram_id = 1234567


class DollarHistoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = DollarHistory
        sqlalchemy_session = test_scoped_session

    date_time = datetime.now()
    cost_value = 89.90
