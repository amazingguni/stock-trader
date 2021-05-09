import sys
import pytest
from PyQt5.QtWidgets import QApplication


@pytest.fixture(scope="session")
def application():
    return QApplication(sys.argv)
