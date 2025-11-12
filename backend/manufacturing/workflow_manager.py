"""
Manufacturing Workflow Management
Handles routing and orchestration of FDM/SLS/CFC/CNC manufacturing jobs
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManufacturingMethod(str, Enum):
    """Manufacturing methods"""
    FDM = "fdm"  # Fused Deposition Modeling
    SLS = "sls"  # Selective Laser Sintering
    CFC = "cfc"  # Continuous Fiber Composite
    CNC = "cnc"  # CNC Machining
    NONE = "none"

class JobPriority(str, Enum):
    """Job priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class WorkflowStage(str, Enum):
    """Workflow stages for each method"""
    # FDM stages
    FDM_QUEUED = "fdm_queued"
    FDM_PRINTING = "fdm_printing"
    FDM_COMPLETED = "fdm_completed"

    # SLS stages
    SLS_QUEUED = "sls_queued"
    SLS_PRINTING = "sls_printing"
    SLS_DEPOWDERING = "sls_depowdering"
    SLS_POST_PROCESS = "sls_post_process"
    SLS_COMPLETED = "sls_completed"

    # CFC stages
    CFC_AWAITING_STEP = "cfc_awaiting_step"
    CFC_STEP_RECEIVED = "cfc_step_received"
    CFC_FIBER_PLANNING = "cfc_fiber_planning"
    CFC_PRINTING = "cfc_printing"
    CFC_POST_PROCESS = "cfc_post_process"
    CFC_COMPLETED = "cfc_completed"

    # CNC stages
    CNC_AWAITING_STEP = "cnc_awaiting_step"
    CNC_STEP_RECEIVED = "cnc_step_received"
    CNC_CAM_PLANNING = "cnc_cam_planning"
    CNC_MACHINING = "cnc_machining"
    CNC_FINISHING = "cnc_finishing"
    CNC_COMPLETED = "cnc_completed"

@dataclass
class ManufacturingJob:
    """Manufacturing job data"""
    job_id: str
    method: ManufacturingMethod
    processing_job_id: str
    user_id: str
    project_id: str

    # Files
    stl_url: Optional[str] = None
    step_url: Optional[str] = None

    # Status
    current_stage: Optional[WorkflowStage] = None
    priority: JobPriority = JobPriority.NORMAL

    # Machine assignment
    machine_id: Optional[str] = None

    # Timing
    created_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None

    # Notes
    user_notes: Optional[str] = None
    internal_notes: Optional[str] = None

class WorkflowManager:
    """Manages manufacturing workflows for all methods"""

    def __init__(self):
        self.jobs: Dict[str, ManufacturingJob] = {}

        # Define workflow stages for each method
        self.workflows = {
            ManufacturingMethod.FDM: [
                WorkflowStage.FDM_QUEUED,
                WorkflowStage.FDM_PRINTING,
                WorkflowStage.FDM_COMPLETED
            ],
            ManufacturingMethod.SLS: [
                WorkflowStage.SLS_QUEUED,
                WorkflowStage.SLS_PRINTING,
                WorkflowStage.SLS_DEPOWDERING,
                WorkflowStage.SLS_POST_PROCESS,
                WorkflowStage.SLS_COMPLETED
            ],
            ManufacturingMethod.CFC: [
                WorkflowStage.CFC_AWAITING_STEP,
                WorkflowStage.CFC_STEP_RECEIVED,
                WorkflowStage.CFC_FIBER_PLANNING,
                WorkflowStage.CFC_PRINTING,
                WorkflowStage.CFC_POST_PROCESS,
                WorkflowStage.CFC_COMPLETED
            ],
            ManufacturingMethod.CNC: [
                WorkflowStage.CNC_AWAITING_STEP,
                WorkflowStage.CNC_STEP_RECEIVED,
                WorkflowStage.CNC_CAM_PLANNING,
                WorkflowStage.CNC_MACHINING,
                WorkflowStage.CNC_FINISHING,
                WorkflowStage.CNC_COMPLETED
            ]
        }

    def create_job(self, job: ManufacturingJob) -> ManufacturingJob:
        """Create a new manufacturing job"""

        # Set initial stage based on method
        if job.method == ManufacturingMethod.FDM:
            job.current_stage = WorkflowStage.FDM_QUEUED
            job.estimated_completion = datetime.now() + timedelta(hours=8)  # Same day
        elif job.method == ManufacturingMethod.SLS:
            job.current_stage = WorkflowStage.SLS_QUEUED
            job.estimated_completion = datetime.now() + timedelta(days=1.5)  # 1-2 days
        elif job.method == ManufacturingMethod.CFC:
            job.current_stage = WorkflowStage.CFC_AWAITING_STEP
            job.estimated_completion = datetime.now() + timedelta(days=2.5)  # 2-3 days
        elif job.method == ManufacturingMethod.CNC:
            job.current_stage = WorkflowStage.CNC_AWAITING_STEP
            job.estimated_completion = datetime.now() + timedelta(days=1.5)  # 1-2 days

        job.created_at = datetime.now()
        self.jobs[job.job_id] = job

        logger.info(f"✅ Created {job.method.value} job: {job.job_id}")
        return job

    def advance_stage(self, job_id: str, notes: Optional[str] = None) -> ManufacturingJob:
        """Advance job to next workflow stage"""

        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")

        job = self.jobs[job_id]
        workflow = self.workflows[job.method]

        current_index = workflow.index(job.current_stage)

        if current_index < len(workflow) - 1:
            next_stage = workflow[current_index + 1]
            logger.info(f"📈 {job_id}: {job.current_stage.value} → {next_stage.value}")
            job.current_stage = next_stage

            if notes:
                job.internal_notes = f"{job.internal_notes or ''}\n[{datetime.now()}] {notes}"

        return job

    def get_job(self, job_id: str) -> Optional[ManufacturingJob]:
        """Get job by ID"""
        return self.jobs.get(job_id)

    def get_jobs_by_method(self, method: ManufacturingMethod) -> List[ManufacturingJob]:
        """Get all jobs for a specific manufacturing method"""
        return [job for job in self.jobs.values() if job.method == method]

    def get_jobs_by_stage(self, stage: WorkflowStage) -> List[ManufacturingJob]:
        """Get all jobs at a specific stage"""
        return [job for job in self.jobs.values() if job.current_stage == stage]

    def get_queue_summary(self) -> Dict[str, Any]:
        """Get summary of all manufacturing queues"""

        summary = {}

        for method in ManufacturingMethod:
            if method == ManufacturingMethod.NONE:
                continue

            jobs = self.get_jobs_by_method(method)
            stages = {}

            for stage in self.workflows[method]:
                stage_jobs = [j for j in jobs if j.current_stage == stage]
                stages[stage.value] = {
                    "count": len(stage_jobs),
                    "jobs": [j.job_id for j in stage_jobs]
                }

            summary[method.value] = {
                "total_jobs": len(jobs),
                "stages": stages,
                "avg_queue_time": self._calculate_avg_queue_time(jobs)
            }

        return summary

    def _calculate_avg_queue_time(self, jobs: List[ManufacturingJob]) -> Optional[float]:
        """Calculate average queue time in hours"""
        if not jobs:
            return None

        total_hours = 0
        for job in jobs:
            if job.created_at and not job.current_stage.value.endswith("_completed"):
                hours = (datetime.now() - job.created_at).total_seconds() / 3600
                total_hours += hours

        return total_hours / len(jobs) if jobs else 0

    def get_next_fdm_job(self) -> Optional[ManufacturingJob]:
        """Get next FDM job to print (highest priority, oldest first)"""
        fdm_jobs = [
            job for job in self.jobs.values()
            if job.method == ManufacturingMethod.FDM
            and job.current_stage == WorkflowStage.FDM_QUEUED
        ]

        if not fdm_jobs:
            return None

        # Sort by priority (urgent first) then by created_at (oldest first)
        priority_order = {
            JobPriority.URGENT: 0,
            JobPriority.HIGH: 1,
            JobPriority.NORMAL: 2,
            JobPriority.LOW: 3
        }

        fdm_jobs.sort(key=lambda x: (priority_order[x.priority], x.created_at))
        return fdm_jobs[0]

    def assign_machine(self, job_id: str, machine_id: str) -> ManufacturingJob:
        """Assign a machine to a job"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")

        job = self.jobs[job_id]
        job.machine_id = machine_id
        logger.info(f"🔧 Assigned machine {machine_id} to job {job_id}")

        return job


class FDMWorkflow:
    """Specialized FDM workflow handler"""

    @staticmethod
    def can_auto_queue(job: ManufacturingJob) -> bool:
        """Check if job can be auto-queued to Bambu Lab printers"""
        return (
            job.method == ManufacturingMethod.FDM
            and job.stl_url is not None
            and job.current_stage == WorkflowStage.FDM_QUEUED
        )

    @staticmethod
    def prepare_for_printing(job: ManufacturingJob) -> Dict[str, Any]:
        """Prepare job data for Bambu Lab printers"""
        return {
            "job_id": job.job_id,
            "file_url": job.stl_url,
            "file_name": f"{job.project_id}_{job.job_id}.stl",
            "priority": job.priority.value,
            "user_notes": job.user_notes
        }


class SLSWorkflow:
    """Specialized SLS workflow handler"""

    @staticmethod
    def requires_depowdering(job: ManufacturingJob) -> bool:
        """Check if job needs depowdering"""
        return job.current_stage == WorkflowStage.SLS_DEPOWDERING

    @staticmethod
    def get_post_processing_steps(job: ManufacturingJob) -> List[str]:
        """Get post-processing checklist for SLS"""
        return [
            "Remove from build chamber (wait for cooldown)",
            "Depowder part (brush + air blast)",
            "Media blast surface finish",
            "Inspect dimensions",
            "Quality check",
            "Package for delivery"
        ]


class CFCWorkflow:
    """Specialized CFC (Continuous Fiber Composite) workflow handler"""

    @staticmethod
    def is_awaiting_step_file(job: ManufacturingJob) -> bool:
        """Check if waiting for user to upload refined STEP file"""
        return job.current_stage == WorkflowStage.CFC_AWAITING_STEP

    @staticmethod
    def receive_step_file(job: ManufacturingJob, step_url: str) -> ManufacturingJob:
        """Mark STEP file as received"""
        job.step_url = step_url
        job.current_stage = WorkflowStage.CFC_STEP_RECEIVED
        logger.info(f"📥 Received STEP file for CFC job: {job.job_id}")
        return job

    @staticmethod
    def get_fiber_planning_guide(job: ManufacturingJob) -> Dict[str, Any]:
        """Get fiber planning guidance"""
        return {
            "job_id": job.job_id,
            "recommendations": [
                "Identify load-bearing surfaces",
                "Plan fiber orientation for max strength",
                "Check build chamber compatibility",
                "Estimate fiber spool requirements",
                "Plan support structures"
            ],
            "tools": [
                "Eiger software (Markforged)",
                "Continuous Fiber Planning tool"
            ]
        }


class CNCWorkflow:
    """Specialized CNC workflow handler"""

    @staticmethod
    def is_awaiting_step_file(job: ManufacturingJob) -> bool:
        """Check if waiting for user to upload refined STEP file"""
        return job.current_stage == WorkflowStage.CNC_AWAITING_STEP

    @staticmethod
    def receive_step_file(job: ManufacturingJob, step_url: str) -> ManufacturingJob:
        """Mark STEP file as received"""
        job.step_url = step_url
        job.current_stage = WorkflowStage.CNC_STEP_RECEIVED
        logger.info(f"📥 Received STEP file for CNC job: {job.job_id}")
        return job

    @staticmethod
    def get_cam_planning_checklist(job: ManufacturingJob) -> List[str]:
        """Get CAM planning checklist"""
        return [
            "Import STEP file to CAM software",
            "Define stock material and dimensions",
            "Set work coordinate system (WCS)",
            "Plan toolpaths (roughing + finishing)",
            "Select cutting tools",
            "Set feeds and speeds",
            "Generate G-code",
            "Simulate toolpaths",
            "Verify collision detection",
            "Export to machine controller"
        ]


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def example_workflow():
    """Example of using the workflow manager"""

    manager = WorkflowManager()

    # Create FDM job (auto-queue)
    fdm_job = ManufacturingJob(
        job_id="fdm-001",
        method=ManufacturingMethod.FDM,
        processing_job_id="proc-123",
        user_id="user-456",
        project_id="proj-789",
        stl_url="https://r2.example.com/output.stl",
        priority=JobPriority.NORMAL
    )
    manager.create_job(fdm_job)

    # Create SLS job
    sls_job = ManufacturingJob(
        job_id="sls-001",
        method=ManufacturingMethod.SLS,
        processing_job_id="proc-124",
        user_id="user-456",
        project_id="proj-790",
        stl_url="https://r2.example.com/output2.stl"
    )
    manager.create_job(sls_job)

    # Create CFC job (needs STEP refinement)
    cfc_job = ManufacturingJob(
        job_id="cfc-001",
        method=ManufacturingMethod.CFC,
        processing_job_id="proc-125",
        user_id="user-457",
        project_id="proj-791",
        step_url="https://r2.example.com/output.step"
    )
    manager.create_job(cfc_job)

    # Get queue summary
    summary = manager.get_queue_summary()
    print("Queue Summary:", summary)

    # Advance FDM job
    manager.advance_stage(fdm_job.job_id, "Started printing")
    manager.advance_stage(fdm_job.job_id, "Print completed successfully")

    # Get next FDM job to print
    next_job = manager.get_next_fdm_job()
    if next_job:
        print(f"Next FDM job: {next_job.job_id}")


if __name__ == "__main__":
    example_workflow()
