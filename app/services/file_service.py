from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.file import File
from app.models.file_version import FileVersion


# create functionality
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
        owner_id=user_id,
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


# upload functionality
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


# delete functionality


def delete_file(
    db: Session,
    file_id: int,
):
    """
    Soft delete a file.

    Marks the file as deleted without removing its versions."""

    file_query = select(File).where(
        File.id == file_id,
        File.is_deleted.is_(False),
    )

    file = db.execute(file_query).scalar_one_or_none()

    if not file:
        raise ValueError("File not found or already deleted")

    file.is_deleted = True

    db.commit()


# restore functionality


def restore_file(
    db: Session,
    file_id: int,
):
    """
    Restore a soft-deleted file.

    Fails if another active file with the same name exists
    in the same folder.

    Args:
        db (Session): Database session
        file_id (int): ID of the file to restore

    Returns:
        File: Restored file

    Raises:
        ValueError:
            - If file does not exist
            - If file is already active
            - If name conflict exists in folder
    """

    # 1. Get the file (must exist)
    file_query = select(File).where(
        File.id == file_id,
    )

    file = db.execute(file_query).scalar_one_or_none()

    if not file:
        raise ValueError("File not found")

    # 2. Ensure it is actually deleted
    if not file.is_deleted:
        raise ValueError("File is already active")

    # 3. Check for name conflict in same folder
    conflict_query = select(File).where(
        File.folder_id == file.folder_id,
        File.name == file.name,
        File.is_deleted.is_(False),
    )

    conflict_file = db.execute(conflict_query).scalar_one_or_none()

    if conflict_file:
        raise ValueError("Cannot restore: file with same name already exists")

    # 4. Restore
    file.is_deleted = False

    # 5. Commit
    db.commit()
    db.refresh(file)

    return file


#get_latest_version functionality 
def get_latest_version(db: Session, file_id: int):
    """
    Return the latest FileVersion for a given file_id.

    Selects the version with the highest version_number.
    Returns None if no versions exist.
    """
    query = (
        select(FileVersion)
        .where(FileVersion.file_id == file_id)
        .order_by(FileVersion.version_number.desc())
        .limit(1)
    )
    
    result = db.execute(query).scalar_one_or_none()
    return result