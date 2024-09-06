from fastapi.testclient import TestClient
from main import app
import pytest


client = TestClient(app)


