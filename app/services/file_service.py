from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.file import File
from app.models.file_version import FileVersion


def create_file(
    db: Session, user_id: int, folder_id: int, file_name: str, metadata: dict
):

    storage_key = metadata.get("storage_key")
    size = metadata.get("size")
    mime_type = metadata.get("mime_type")

    if not all([storage_key, size, mime_type]):
        raise ValueError("Invalid metadata")

    existing_file_query = select(File).where(
        File.folder_id == folder_id,
        File.name == file_name,
        File.is_deleted.is_(False),
    )

    existing_file = db.execute(existing_file_query).scalar_one_or_none()

    if existing_file:
        raise ValueError("File with same name already exists in this folder")

    new_file = File(
        user_id=user_id,
        folder_id=folder_id,
        name=file_name,
        is_deleted=False,
    )

    db.add(new_file)
    db.flush()

    file_version = FileVersion(
        file_id=new_file.id,
        version_number=1,
        storage_key=storage_key,
        size=size,
        mime_type=mime_type,
    )

    db.add(file_version)

    db.commit()
    db.refresh(new_file)

    return new_file


def upload_new_version(db: Session, file_id: int, metadata: dict):

    storage_key = metadata.get("storage_key")
    size = metadata.get("size")
    mime_type = metadata.get("mime_type")

    if not all([storage_key, size, mime_type]):
        raise ValueError("Invalid metadata")

    file_query = select(File).where(
        File.id == file_id,
        File.is_deleted.is_(False),
    )

    file = db.execute(file_query).scalar_one_or_none()

    if not file:
        raise ValueError("File not found or has been deleted")

    latest_version_query = select(func.max(FileVersion.version_number)).where(
        FileVersion.file_id == file_id
    )

    latest_version_number = db.execute(latest_version_query).scalar()

    next_version_number = (latest_version_number or 0) + 1

    new_version = FileVersion(
        file_id=file_id,
        version_number=next_version_number,
        storage_key=storage_key,
        size=size,
        mime_type=mime_type,
    )

    db.add(new_version)

    db.commit()
    db.refresh(new_version)

    return new_version
