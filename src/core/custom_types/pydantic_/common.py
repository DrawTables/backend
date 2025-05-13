from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, HttpUrl

DecimalType = Annotated[Decimal, AfterValidator(lambda v: v.__str__())]
HttpUrlType = Annotated[HttpUrl, AfterValidator(lambda v: v.__str__())]
