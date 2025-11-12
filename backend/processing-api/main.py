"""
R&D Platform - Processing Orchestration API
FastAPI service for managing scan jobs, GPU processing, and manufacturing workflows
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import asyncio
from datetime import datetime
import uuid

app = FastAPI(
    title="R&D Platform Processing API",
    description="Orchestrates COLMAP + Point2CAD processing and manufacturing workflows",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ENUMS & MODELS
# ============================================================================

class JobStatus(str, Enum):
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

class ManufacturingMethod(str, Enum):
    """Manufacturing methods available"""
    FDM = "fdm"  # Fused Deposition Modeling
    SLS = "sls"  # Selective Laser Sintering
    CFC = "cfc"  # Continuous Fiber Composite
    CNC = "cnc"  # CNC Machining
    NONE = "none"  # Download only

class ManufacturingStatus(str, Enum):
    """Manufacturing job status"""
    PENDING = "pending"
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    POST_PROCESSING = "post_processing"
    COMPLETED = "completed"
    FAILED = "failed"

class SubscriptionTier(str, Enum):
    """User subscription tiers"""
    STARTER = "starter"  # 50 scans/month
    PROFESSIONAL = "professional"  # 200 scans/month
    ENTERPRISE = "enterprise"  # 1000 scans/month

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ProcessingJobCreate(BaseModel):
    """Request to create a new processing job"""
    user_id: str
    project_id: str
    project_name: str
    image_count: int = Field(..., ge=20, le=50, description="Number of images (20-50)")
    subscription_tier: SubscriptionTier
    manufacturing_method: Optional[ManufacturingMethod] = ManufacturingMethod.NONE

class ProcessingJobResponse(BaseModel):
    """Processing job response"""
    job_id: str
    user_id: str
    project_id: str
    status: JobStatus
    progress_percentage: float = 0.0
    estimated_time_remaining: Optional[int] = None  # seconds
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    # Output files
    step_file_url: Optional[str] = None
    stl_file_url: Optional[str] = None
    preview_url: Optional[str] = None

    # Processing stats
    colmap_time: Optional[float] = None
    point2cad_time: Optional[float] = None
    total_processing_time: Optional[float] = None

    # Manufacturing
    manufacturing_method: Optional[ManufacturingMethod] = None
    manufacturing_status: Optional[ManufacturingStatus] = None

class ManufacturingJobCreate(BaseModel):
    """Request to create manufacturing job"""
    processing_job_id: str
    manufacturing_method: ManufacturingMethod
    user_id: str
    project_id: str
    notes: Optional[str] = None

class ManufacturingRecommendation(BaseModel):
    """AI recommendation for manufacturing method"""
    recommended_method: ManufacturingMethod
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    alternatives: List[Dict[str, Any]]
    estimated_cost: Optional[float] = None
    estimated_time: Optional[str] = None

class QuotaStatus(BaseModel):
    """User quota status"""
    user_id: str
    tier: SubscriptionTier
    monthly_limit: int
    used_this_month: int
    remaining: int
    overage_count: int
    overage_rate: float  # £ per scan
    next_reset_date: datetime
    can_submit: bool

# ============================================================================
# IN-MEMORY STORAGE (Replace with PostgreSQL in production)
# ============================================================================

jobs_db: Dict[str, Dict[str, Any]] = {}
manufacturing_db: Dict[str, Dict[str, Any]] = {}
user_quotas: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def check_user_quota(user_id: str, tier: SubscriptionTier) -> QuotaStatus:
    """Check if user has available quota"""

    # Tier limits
    tier_limits = {
        SubscriptionTier.STARTER: 50,
        SubscriptionTier.PROFESSIONAL: 200,
        SubscriptionTier.ENTERPRISE: 1000,
    }

    overage_rates = {
        SubscriptionTier.STARTER: 0.60,
        SubscriptionTier.PROFESSIONAL: 0.50,
        SubscriptionTier.ENTERPRISE: 0.40,
    }

    # Get or initialize quota
    if user_id not in user_quotas:
        user_quotas[user_id] = {
            "tier": tier,
            "used_this_month": 0,
            "overage_count": 0,
            "reset_date": datetime.now()
        }

    quota = user_quotas[user_id]
    monthly_limit = tier_limits[tier]
    used = quota["used_this_month"]
    remaining = max(0, monthly_limit - used)
    overage = max(0, used - monthly_limit)

    return QuotaStatus(
        user_id=user_id,
        tier=tier,
        monthly_limit=monthly_limit,
        used_this_month=used,
        remaining=remaining,
        overage_count=overage,
        overage_rate=overage_rates[tier],
        next_reset_date=quota["reset_date"],
        can_submit=True  # Enterprise has unlimited, others can use overage
    )

async def simulate_processing(job_id: str):
    """Simulate GPU processing workflow"""

    job = jobs_db[job_id]

    try:
        # COLMAP processing (5-8 min)
        job["status"] = JobStatus.COLMAP_RUNNING
        job["progress_percentage"] = 20
        await asyncio.sleep(2)  # Simulate
        job["colmap_time"] = 7.5
        job["progress_percentage"] = 50

        # Point2CAD processing (3-5 min)
        job["status"] = JobStatus.POINT2CAD_RUNNING
        job["progress_percentage"] = 70
        await asyncio.sleep(2)  # Simulate
        job["point2cad_time"] = 4.2
        job["progress_percentage"] = 90

        # Mesh repair & validation
        job["status"] = JobStatus.MESH_REPAIR
        await asyncio.sleep(1)  # Simulate

        # Complete
        job["status"] = JobStatus.COMPLETED
        job["progress_percentage"] = 100
        job["completed_at"] = datetime.now()
        job["total_processing_time"] = job["colmap_time"] + job["point2cad_time"] + 1.5
        job["step_file_url"] = f"https://r2.example.com/{job_id}/output.step"
        job["stl_file_url"] = f"https://r2.example.com/{job_id}/output.stl"
        job["preview_url"] = f"https://r2.example.com/{job_id}/preview.png"

        # Update quota
        if job["user_id"] in user_quotas:
            user_quotas[job["user_id"]]["used_this_month"] += 1

    except Exception as e:
        job["status"] = JobStatus.FAILED
        job["error_message"] = str(e)
        job["completed_at"] = datetime.now()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API health check"""
    return {
        "service": "R&D Platform Processing API",
        "status": "operational",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "api": "healthy",
        "database": "healthy",  # TODO: Check PostgreSQL
        "redis": "healthy",  # TODO: Check Redis
        "gpu_server": "healthy",  # TODO: Check GPU server
        "active_jobs": len([j for j in jobs_db.values() if j["status"] in [JobStatus.PROCESSING, JobStatus.QUEUED]])
    }

@app.post("/jobs/create", response_model=ProcessingJobResponse)
async def create_processing_job(
    job_request: ProcessingJobCreate,
    background_tasks: BackgroundTasks
):
    """Create a new processing job"""

    # Check quota
    quota = check_user_quota(job_request.user_id, job_request.subscription_tier)
    if not quota.can_submit:
        raise HTTPException(
            status_code=429,
            detail=f"Monthly quota exceeded. Used: {quota.used_this_month}/{quota.monthly_limit}"
        )

    # Validate image count
    if not (20 <= job_request.image_count <= 50):
        raise HTTPException(
            status_code=400,
            detail="Image count must be between 20 and 50 for manufacturing-grade accuracy"
        )

    # Create job
    job_id = str(uuid.uuid4())
    job_data = {
        "job_id": job_id,
        "user_id": job_request.user_id,
        "project_id": job_request.project_id,
        "status": JobStatus.QUEUED,
        "progress_percentage": 0.0,
        "created_at": datetime.now(),
        "started_at": None,
        "completed_at": None,
        "manufacturing_method": job_request.manufacturing_method,
        "manufacturing_status": None if job_request.manufacturing_method == ManufacturingMethod.NONE else ManufacturingStatus.PENDING,
    }

    jobs_db[job_id] = job_data

    # Start processing in background
    background_tasks.add_task(simulate_processing, job_id)

    job_data["started_at"] = datetime.now()
    job_data["status"] = JobStatus.PROCESSING

    return ProcessingJobResponse(**job_data)

@app.get("/jobs/{job_id}", response_model=ProcessingJobResponse)
async def get_job_status(job_id: str):
    """Get processing job status"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    return ProcessingJobResponse(**jobs_db[job_id])

@app.get("/jobs/user/{user_id}", response_model=List[ProcessingJobResponse])
async def get_user_jobs(user_id: str, limit: int = 50):
    """Get all jobs for a user"""

    user_jobs = [
        ProcessingJobResponse(**job)
        for job in jobs_db.values()
        if job["user_id"] == user_id
    ]

    # Sort by created_at descending
    user_jobs.sort(key=lambda x: x.created_at, reverse=True)

    return user_jobs[:limit]

@app.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a processing job"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs_db[job_id]

    if job["status"] in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status: {job['status']}"
        )

    job["status"] = JobStatus.CANCELLED
    job["completed_at"] = datetime.now()

    return {"message": "Job cancelled successfully", "job_id": job_id}

@app.get("/quota/{user_id}", response_model=QuotaStatus)
async def get_user_quota(user_id: str, tier: SubscriptionTier):
    """Get user's current quota status"""

    return check_user_quota(user_id, tier)

@app.post("/manufacturing/recommend", response_model=ManufacturingRecommendation)
async def get_manufacturing_recommendation(job_id: str):
    """Get AI recommendation for manufacturing method based on geometry analysis"""

    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs_db[job_id]

    if job["status"] != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Job must be completed before getting recommendations"
        )

    # TODO: Implement actual geometry analysis
    # For now, return a sample recommendation

    return ManufacturingRecommendation(
        recommended_method=ManufacturingMethod.SLS,
        confidence=0.85,
        reasoning="Part geometry suggests functional testing requirements. SLS provides good strength-to-weight ratio with complex geometries. Dimensions are within SLS build volume (350x350x600mm).",
        alternatives=[
            {
                "method": "FDM",
                "confidence": 0.65,
                "pros": "Faster turnaround (same day), lower cost",
                "cons": "Lower strength, visible layer lines"
            },
            {
                "method": "CFC",
                "confidence": 0.45,
                "pros": "Highest strength, end-use quality",
                "cons": "Requires STEP refinement, longer turnaround, higher cost"
            }
        ],
        estimated_cost=75.0,
        estimated_time="1-2 days"
    )

@app.post("/manufacturing/create", response_model=Dict[str, Any])
async def create_manufacturing_job(mfg_request: ManufacturingJobCreate):
    """Create a manufacturing job (FDM/SLS/CFC/CNC)"""

    if mfg_request.processing_job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Processing job not found")

    processing_job = jobs_db[mfg_request.processing_job_id]

    if processing_job["status"] != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Processing job must be completed before manufacturing"
        )

    # Create manufacturing job
    mfg_job_id = str(uuid.uuid4())
    mfg_job = {
        "mfg_job_id": mfg_job_id,
        "processing_job_id": mfg_request.processing_job_id,
        "user_id": mfg_request.user_id,
        "project_id": mfg_request.project_id,
        "method": mfg_request.manufacturing_method,
        "status": ManufacturingStatus.QUEUED,
        "created_at": datetime.now(),
        "notes": mfg_request.notes,
    }

    manufacturing_db[mfg_job_id] = mfg_job

    # Update processing job
    processing_job["manufacturing_method"] = mfg_request.manufacturing_method
    processing_job["manufacturing_status"] = ManufacturingStatus.QUEUED

    # Auto-queue for FDM
    if mfg_request.manufacturing_method == ManufacturingMethod.FDM:
        # TODO: Integrate with OctoPrint API
        mfg_job["octoprint_job_id"] = "auto-queued-placeholder"
        mfg_job["status"] = ManufacturingStatus.QUEUED

    return {
        "mfg_job_id": mfg_job_id,
        "status": mfg_job["status"],
        "message": f"Manufacturing job created for {mfg_request.manufacturing_method.value}",
        "auto_queued": mfg_request.manufacturing_method == ManufacturingMethod.FDM
    }

@app.get("/manufacturing/{mfg_job_id}")
async def get_manufacturing_status(mfg_job_id: str):
    """Get manufacturing job status"""

    if mfg_job_id not in manufacturing_db:
        raise HTTPException(status_code=404, detail="Manufacturing job not found")

    return manufacturing_db[mfg_job_id]

@app.get("/stats/dashboard")
async def get_dashboard_stats():
    """Get dashboard statistics for admin"""

    total_jobs = len(jobs_db)
    completed_jobs = len([j for j in jobs_db.values() if j["status"] == JobStatus.COMPLETED])
    failed_jobs = len([j for j in jobs_db.values() if j["status"] == JobStatus.FAILED])
    active_jobs = len([j for j in jobs_db.values() if j["status"] in [JobStatus.PROCESSING, JobStatus.QUEUED]])

    # Manufacturing stats
    total_mfg = len(manufacturing_db)
    mfg_by_method = {
        method.value: len([m for m in manufacturing_db.values() if m["method"] == method])
        for method in ManufacturingMethod
    }

    return {
        "processing": {
            "total_jobs": total_jobs,
            "completed": completed_jobs,
            "failed": failed_jobs,
            "active": active_jobs,
            "success_rate": (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
        },
        "manufacturing": {
            "total_jobs": total_mfg,
            "by_method": mfg_by_method
        },
        "users": {
            "total_active": len(user_quotas),
            "total_scans_this_month": sum(q["used_this_month"] for q in user_quotas.values())
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
