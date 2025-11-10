"""Certificate model for course completion certificates.

This module defines the Certificate model for issuing and managing
course completion certificates.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from src.models import db
import secrets


class Certificate(db.Model):
    """Certificate model for course completions.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        course_id: Foreign key to courses table
        certificate_number: Unique certificate number
        issued_at: Certificate issue timestamp
        expires_at: Certificate expiration timestamp (if applicable)
    """
    
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    certificate_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    @classmethod
    def generate_certificate_number(cls) -> str:
        """Generate a unique certificate number.
        
        Returns:
            Unique certificate number string
        """
        while True:
            # Format: CERT-YYYYMMDD-RANDOM8
            date_str = datetime.utcnow().strftime('%Y%m%d')
            random_str = secrets.token_hex(4).upper()
            cert_number = f'CERT-{date_str}-{random_str}'
            
            # Check if number already exists
            if not cls.query.filter_by(certificate_number=cert_number).first():
                return cert_number
    
    @classmethod
    def create(cls, user_id: int, course_id: int, 
               expiration_months: Optional[int] = None) -> 'Certificate':
        """Create a new certificate.
        
        Args:
            user_id: User's unique identifier
            course_id: Course's unique identifier
            expiration_months: Months until expiration (None = no expiration)
            
        Returns:
            Created Certificate instance
        """
        certificate_number = cls.generate_certificate_number()
        expires_at = None
        
        if expiration_months:
            expires_at = datetime.utcnow() + timedelta(days=30 * expiration_months)
        
        certificate = cls(
            user_id=user_id,
            course_id=course_id,
            certificate_number=certificate_number,
            expires_at=expires_at
        )
        db.session.add(certificate)
        db.session.commit()
        return certificate
    
    @classmethod
    def get_by_id(cls, certificate_id: int) -> Optional['Certificate']:
        """Retrieve certificate by ID.
        
        Args:
            certificate_id: Certificate's unique identifier
            
        Returns:
            Certificate instance or None if not found
        """
        return cls.query.filter_by(id=certificate_id).first()
    
    @classmethod
    def get_by_number(cls, certificate_number: str) -> Optional['Certificate']:
        """Retrieve certificate by certificate number.
        
        Args:
            certificate_number: Certificate number
            
        Returns:
            Certificate instance or None if not found
        """
        return cls.query.filter_by(certificate_number=certificate_number).first()
    
    @classmethod
    def get_by_user(cls, user_id: int, valid_only: bool = False) -> List['Certificate']:
        """Retrieve all certificates for a user.
        
        Args:
            user_id: User's unique identifier
            valid_only: Only return non-expired certificates (default: False)
            
        Returns:
            List of Certificate instances
        """
        query = cls.query.filter_by(user_id=user_id)
        if valid_only:
            query = query.filter(
                (cls.expires_at.is_(None)) | (cls.expires_at > datetime.utcnow())
            )
        return query.all()
    
    @classmethod
    def get_by_course(cls, course_id: int) -> List['Certificate']:
        """Retrieve all certificates for a course.
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            List of Certificate instances
        """
        return cls.query.filter_by(course_id=course_id).all()
    
    @classmethod
    def get_by_user_and_course(cls, user_id: int, course_id: int) -> Optional['Certificate']:
        """Get certificate for specific user and course.
        
        Args:
            user_id: User's unique identifier
            course_id: Course's unique identifier
            
        Returns:
            Certificate instance or None if not found
        """
        return cls.query.filter_by(user_id=user_id, course_id=course_id).first()
    
    @classmethod
    def get_expiring_soon(cls, days: int = 30) -> List['Certificate']:
        """Get certificates expiring within specified days.
        
        Args:
            days: Number of days to check (default: 30)
            
        Returns:
            List of Certificate instances
        """
        cutoff_date = datetime.utcnow() + timedelta(days=days)
        return cls.query.filter(
            cls.expires_at.isnot(None),
            cls.expires_at <= cutoff_date,
            cls.expires_at > datetime.utcnow()
        ).all()
    
    def delete(self) -> None:
        """Delete certificate from database."""
        db.session.delete(self)
        db.session.commit()
    
    def is_valid(self) -> bool:
        """Check if certificate is still valid.
        
        Returns:
            True if certificate has not expired
        """
        if not self.expires_at:
            return True
        return datetime.utcnow() < self.expires_at
    
    def renew(self, months: int) -> 'Certificate':
        """Renew certificate expiration.
        
        Args:
            months: Number of months to extend
            
        Returns:
            Updated Certificate instance
        """
        if self.expires_at:
            # Extend from current expiration or now, whichever is later
            base_date = max(datetime.utcnow(), self.expires_at)
        else:
            base_date = datetime.utcnow()
        
        self.expires_at = base_date + timedelta(days=30 * months)
        db.session.commit()
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert certificate to dictionary.
        
        Returns:
            Dictionary representation of certificate
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'certificate_number': self.certificate_number,
            'issued_at': self.issued_at.isoformat() if self.issued_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_valid': self.is_valid(),
        }
    
    def __repr__(self) -> str:
        """String representation of Certificate."""
        return f'<Certificate {self.certificate_number}>'
