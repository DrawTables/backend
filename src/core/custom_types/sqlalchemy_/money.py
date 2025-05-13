from typing import Any

from sqlalchemy import cast, TypeDecorator
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.types import Numeric


class NumericMoney(TypeDecorator):
    impl = MONEY

    def column_expression(self, column: Any):
        return cast(column, Numeric())
