# backend/tests/test_user_model.py
from sqlalchemy.inspection import inspect
from backend.app.models.user import User

def test_user_mapping_columns_exist():
    mapper = inspect(User)
    cols = mapper.columns
    for name in ["id", "email", "hashed_password", "role", "created_at"]:
        assert name in cols

def test_user_pk_and_constraints():
    mapper = inspect(User)
    id_col = mapper.columns["id"]
    email_col = mapper.columns["email"]
    role_col = mapper.columns["role"]
    created_col = mapper.columns["created_at"]

    assert id_col.primary_key is True
    assert email_col.nullable is False
    assert email_col.unique is True
    assert role_col.nullable is False
    assert created_col.nullable is False
