from model_bakery import baker

from django.contrib.auth.models import User

from core.tests import BaseClassTestCase
from forecasts.models import Forecast, Prediction


class ForecastCalculationsTestCase(BaseClassTestCase):
    """
    Test user predictions point calculations.
    """

    def setUp(self):
        self.forecast1 = baker.make(Forecast)

    def test_prediction_calculations(self):
        pass
