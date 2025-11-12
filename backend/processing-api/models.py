"""
Database Models for R&D Platform
SQLAlchemy ORM models for PostgreSQL
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

# ============================================================================
# ENUMS
# ============================================================================

class JobStatus(str, enum.Enum):
    """Processing job status states"""
    PENDING = "pending"
    UPLOADING = "uploading"
    QUEUED = "queued"
    PROCESSING = "processing"
    COLMAP_RUNNING = "colmap_running"
    POINT2CAD_RUNNING = "point2cad_running"
    MESH_REPAIR = "mesh_repair"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ManufacturingMethod(str, enum.Enum):
    """Manufacturing methods available"""
    FDM = "fdm"
    SLS = "sls"
    CFC = "cfc"
    CNC = "cnc"
    NONE = "none"

class ManufacturingStatus(str, enum.Enum):
    """Manufacturing job status"""
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    POST_PROCESSING = "post_processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SubscriptionTier(str, enum.Enum):
    """User subscription tiers"""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

# ============================================================================
# MODELS
# ============================================================================

class User(Base):
    """User account (synced from Medusa.js)"""
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.STARTER)
    stripe_customer_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    quotas = relationship("UserQuota", back_populates="user", uselist=False)

class Project(Base):
    """User project (collection of scans)"""
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="projects")
    processing_jobs = relationship("ProcessingJob", back_populates="project", cascade="all, delete-orphan")

class ProcessingJob(Base):
    """Processing job (COLMAP + Point2CAD)"""
    __tablename__ = "processing_jobs"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)

    # Job metadata
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    progress_percentage = Column(Float, default=0.0)
    estimated_time_remaining = Column(Integer, nullable=True)  # seconds

    # Input
    image_count = Column(Integer, nullable=False)
    images_storage_path = Column(String, nullable=True)

    # Output files (R2 URLs)
    step_file_url = Column(String, nullable=True)
    stl_file_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    point_cloud_url = Column(String, nullable=True)

    # Processing stats
    colmap_time = Column(Float, nullable=True)  # seconds
    point2cad_time = Column(Float, nullable=True)  # seconds
    total_processing_time = Column(Float, nullable=True)  # seconds

    # GPU server info
    gpu_server_id = Column(String, nullable=True)
    gpu_job_id = Column(String, nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User")
    project = relationship("Project", back_populates="processing_jobs")
    manufacturing_jobs = relationship("ManufacturingJob", back_populates="processing_job", cascade="all, delete-orphan")
    geometry_analysis = relationship("GeometryAnalysis", back_populates="processing_job", uselist=False)

class GeometryAnalysis(Base):
    """AI geometry analysis for manufacturing recommendations"""
    __tablename__ = "geometry_analysis"

    id = Column(String, primary_key=True)
    processing_job_id = Column(String, ForeignKey("processing_jobs.id"), nullable=False, unique=True)

    # Dimensional analysis
    bounding_box_x = Column(Float, nullable=True)  # mm
    bounding_box_y = Column(Float, nullable=True)  # mm
    bounding_box_z = Column(Float, nullable=True)  # mm
    volume = Column(Float, nullable=True)  # mm³
    surface_area = Column(Float, nullable=True)  # mm²

    # Geometric features
    has_overhangs = Column(Boolean, default=False)
    has_thin_walls = Column(Boolean, default=False)
    has_complex_geometry = Column(Boolean, default=False)
    has_internal_cavities = Column(Boolean, default=False)
    min_wall_thickness = Column(Float, nullable=True)  # mm

    # Manufacturing recommendations
    recommended_method = Column(Enum(ManufacturingMethod), nullable=True)
    recommendation_confidence = Column(Float, nullable=True)
    recommendation_reasoning = Column(Text, nullable=True)
    alternative_methods = Column(JSON, nullable=True)

    # Cost estimates
    estimated_fdm_cost = Column(Float, nullable=True)
    estimated_sls_cost = Column(Float, nullable=True)
    estimated_cfc_cost = Column(Float, nullable=True)
    estimated_cnc_cost = Column(Float, nullable=True)

    # Time estimates
    estimated_fdm_time = Column(String, nullable=True)
    estimated_sls_time = Column(String, nullable=True)
    estimated_cfc_time = Column(String, nullable=True)
    estimated_cnc_time = Column(String, nullable=True)

    # Timestamps
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    processing_job = relationship("ProcessingJob", back_populates="geometry_analysis")

class ManufacturingJob(Base):
    """Manufacturing job (FDM/SLS/CFC/CNC)"""
    __tablename__ = "manufacturing_jobs"

    id = Column(String, primary_key=True)
    processing_job_id = Column(String, ForeignKey("processing_jobs.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)

    # Manufacturing details
    method = Column(Enum(ManufacturingMethod), nullable=False)
    status = Column(Enum(ManufacturingStatus), default=ManufacturingStatus.PENDING, nullable=False)
    queue_position = Column(Integer, nullable=True)

    # Machine assignment
    machine_id = Column(String, nullable=True)
    machine_name = Column(String, nullable=True)

    # Integration IDs
    bambu_job_id = Column(String, nullable=True)  # For FDM (Bambu Lab)
    external_job_id = Column(String, nullable=True)  # For SLS/CFC/CNC

    # User notes
    notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)  # Admin only

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Estimated delivery
    estimated_completion = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    processing_job = relationship("ProcessingJob", back_populates="manufacturing_jobs")
    user = relationship("User")
    project = relationship("Project")

class UserQuota(Base):
    """User monthly quota tracking"""
    __tablename__ = "user_quotas"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)

    # Quota limits based on tier
    monthly_limit = Column(Integer, nullable=False)
    used_this_month = Column(Integer, default=0)
    overage_count = Column(Integer, default=0)

    # Billing period
    billing_period_start = Column(DateTime(timezone=True), nullable=False)
    billing_period_end = Column(DateTime(timezone=True), nullable=False)

    # Rate limiting (daily)
    daily_limit = Column(Integer, nullable=False)
    used_today = Column(Integer, default=0)
    last_reset_date = Column(DateTime(timezone=True), server_default=func.now())

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="quotas")

class Machine(Base):
    """Manufacturing machine tracking"""
    __tablename__ = "machines"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    method = Column(Enum(ManufacturingMethod), nullable=False)

    # Status
    is_online = Column(Boolean, default=True)
    is_available = Column(Boolean, default=True)
    current_job_id = Column(String, nullable=True)

    # Specs
    build_volume_x = Column(Float, nullable=True)  # mm
    build_volume_y = Column(Float, nullable=True)  # mm
    build_volume_z = Column(Float, nullable=True)  # mm

    # Integration (Bambu Lab)
    bambu_ip = Column(String, nullable=True)
    bambu_access_code = Column(String, nullable=True)
    bambu_serial = Column(String, nullable=True)

    # Stats
    total_jobs_completed = Column(Integer, default=0)
    total_print_time = Column(Float, default=0.0)  # hours
    last_maintenance = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AuditLog(Base):
    """Audit log for all operations"""
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)  # job, project, user, etc.
    resource_id = Column(String, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
