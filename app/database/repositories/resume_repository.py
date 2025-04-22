"""Resume repository module for database operations.

This module contains the implementation of ResumeRepository class which handles
CRUD operations for resume data in the database, including storing, retrieving,
updating, and deleting resume information.
"""

from datetime import datetime
from typing import Dict, List, Optional

from bson import ObjectId

from app.database.models.resume import Resume, ResumeData
from app.database.repositories.base_repo import BaseRepository


class ResumeRepository(BaseRepository):
    """Repository for handling resume-related database operations.

    This class extends BaseRepository to provide specific methods for
    working with resume documents in the database.
    """

    def __init__(self, db_name: str = "myresumo", collection_name: str = "resumes"):
        """Initialize the resume repository with database and collection names.

        Args:
            db_name (str): Name of the database. Defaults to "myresumo".
            collection_name (str): Name of the collection. Defaults to "resumes".
        """
        super().__init__(db_name, collection_name)

    async def create_resume(self, resume: Resume) -> str:
        """Create a new resume document in the database.

        Args:
            resume (Resume): Resume object to be created.

        Returns:
        -------
            str: ID of the created resume document, or empty string if operation fails.
        """
        resume_dict = resume.dict(by_alias=True)
        return await self.insert_one(resume_dict)

    async def get_resume_by_id(self, resume_id: str) -> Optional[Dict]:
        """Retrieve a resume document by its ID.

        Args:
            resume_id (str): ID of the resume to retrieve.

        Returns:
        -------
            Optional[Dict]: Resume document if found, None otherwise.
        """
        try:
            return await self.find_one({"_id": ObjectId(resume_id)})
        except Exception:
            return None

    async def get_resumes_by_user_id(self, user_id: str) -> List[Dict]:
        """Retrieve all resumes belonging to a specific user.

        Args:
            user_id (str): ID of the user whose resumes to retrieve.

        Returns:
        -------
            List[Dict]: List of resume documents, or empty list if none found.
        """
        return await self.find_many({"user_id": user_id}, [("created_at", -1)])

    async def update_resume(self, resume_id: str, update_data: Dict) -> bool:
        """Update a resume document.

        Args:
            resume_id (str): ID of the resume to update.
            update_data (Dict): Dictionary containing updated fields.

        Returns:
        -------
            bool: True if update was successful, False otherwise.
        """
        try:
            update_data["updated_at"] = datetime.now()
            return await self.update_one(
                {"_id": ObjectId(resume_id)}, {"$set": update_data}
            )
        except Exception:
            return False

    async def update_optimized_data(
        self, resume_id: str, optimized_data: ResumeData, ats_score: int
    ) -> bool:
        """Update a resume with AI-optimized data and ATS score.

        Args:
            resume_id (str): ID of the resume to update.
            optimized_data (ResumeData): Optimized resume data from AI processing.
            ats_score (int): ATS compatibility score (0-100).

        Returns:
        -------
            bool: True if update was successful, False otherwise.
        """
        try:
            return await self.update_one(
                {"_id": ObjectId(resume_id)},
                {
                    "$set": {
                        "optimized_data": optimized_data.dict(),
                        "ats_score": ats_score,
                        "updated_at": datetime.now(),
                    }
                },
            )
        except Exception as e:
            print(f"Error updating optimized data: {e}")
            return False

    async def delete_resume(self, resume_id: str) -> bool:
        """Delete a resume document.

        Args:
            resume_id (str): ID of the resume to delete.

        Returns:
        -------
            bool: True if deletion was successful, False otherwise.
        """
        try:
            return await self.delete_one({"_id": ObjectId(resume_id)})
        except Exception:
            return False
