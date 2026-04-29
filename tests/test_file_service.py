import uuid

from app.models.user import User
from app.models.folder import Folder
from app.services.file_service import create_file


def test_create_file_success(db):
    # 1. Create user
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash="hashed_password_dummy",
    )

    # 2. Create folder
    folder = Folder(
        id=uuid.uuid4(),
        name="root",
        owner_id=user.id,
    )

    db.add(user)
    db.add(folder)
    db.commit()

    # 3. Call service
    file = create_file(
        db=db,
        user_id=user.id,
        folder_id=folder.id,
        file_name="test.txt",
        metadata={
            "storage_key": "s3/test.txt",
            "size": 100,
            "mime_type": "text/plain",
        },
    )

    # 4. Assertions
    assert file.id is not None
    assert file.name == "test.txt"
    assert file.is_deleted is False
