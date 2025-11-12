"""
OctoPrint Integration Service
Automatically queue FDM print jobs to OctoPrint-enabled 3D printers
"""

import httpx
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PrinterState(str, Enum):
    """OctoPrint printer states"""
    OPERATIONAL = "Operational"
    PRINTING = "Printing"
    PAUSED = "Paused"
    ERROR = "Error"
    OFFLINE = "Offline"
    READY = "Operational"

@dataclass
class OctoPrintConfig:
    """OctoPrint instance configuration"""
    url: str
    api_key: str
    printer_id: str
    printer_name: str

@dataclass
class PrintJob:
    """Print job information"""
    job_id: str
    file_name: str
    file_url: str  # STL file URL
    estimated_time: Optional[float] = None  # seconds
    status: str = "queued"

class OctoPrintService:
    """Service for interacting with OctoPrint API"""

    def __init__(self, config: OctoPrintConfig):
        self.config = config
        self.base_url = config.url.rstrip('/')
        self.headers = {
            "X-Api-Key": config.api_key,
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_printer_status(self) -> Dict[str, Any]:
        """Get current printer status"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/printer",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to get printer status: {e}")
            raise

    async def is_printer_ready(self) -> bool:
        """Check if printer is ready to accept jobs"""
        try:
            status = await self.get_printer_status()
            state = status.get("state", {}).get("text", "Unknown")
            return state == PrinterState.OPERATIONAL or state == PrinterState.READY
        except Exception as e:
            logger.error(f"Error checking printer readiness: {e}")
            return False

    async def upload_file(self, file_url: str, file_name: str) -> Dict[str, Any]:
        """
        Upload STL file to OctoPrint

        Args:
            file_url: URL to download the STL file from (e.g., R2 pre-signed URL)
            file_name: Name to save the file as

        Returns:
            Upload response from OctoPrint
        """
        try:
            # Download the file first
            download_response = await self.client.get(file_url)
            download_response.raise_for_status()
            file_content = download_response.content

            # Upload to OctoPrint
            files = {
                'file': (file_name, file_content, 'application/octet-stream')
            }

            # Remove Content-Type from headers for multipart/form-data
            upload_headers = {"X-Api-Key": self.config.api_key}

            response = await self.client.post(
                f"{self.base_url}/api/files/local",
                headers=upload_headers,
                files=files
            )
            response.raise_for_status()

            logger.info(f"✅ Uploaded {file_name} to OctoPrint")
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to upload file: {e}")
            raise

    async def start_print(self, file_path: str) -> Dict[str, Any]:
        """
        Start printing a file

        Args:
            file_path: Path to the file in OctoPrint (e.g., "filename.stl")

        Returns:
            Response from OctoPrint
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/api/files/local/{file_path}",
                headers=self.headers,
                json={"command": "select", "print": True}
            )
            response.raise_for_status()

            logger.info(f"✅ Started print: {file_path}")
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Failed to start print: {e}")
            raise

    async def queue_print_job(self, print_job: PrintJob, auto_start: bool = False) -> Dict[str, Any]:
        """
        Queue a print job (upload and optionally start printing)

        Args:
            print_job: PrintJob with file URL and metadata
            auto_start: Whether to automatically start printing (if printer is ready)

        Returns:
            Job status information
        """
        logger.info(f"📥 Queueing print job: {print_job.file_name}")

        # Check printer status
        is_ready = await self.is_printer_ready()

        # Upload file
        upload_result = await self.upload_file(
            print_job.file_url,
            print_job.file_name
        )

        # Extract file path from upload result
        file_path = upload_result.get("files", {}).get("local", {}).get("name")
        if not file_path:
            raise ValueError("Failed to get file path from upload response")

        result = {
            "job_id": print_job.job_id,
            "file_path": file_path,
            "uploaded": True,
            "started": False,
            "printer_ready": is_ready,
            "printer_id": self.config.printer_id
        }

        # Auto-start if requested and printer is ready
        if auto_start and is_ready:
            try:
                await self.start_print(file_path)
                result["started"] = True
                logger.info(f"🖨️  Auto-started print job: {print_job.file_name}")
            except Exception as e:
                logger.warning(f"Failed to auto-start print: {e}")
                result["error"] = str(e)
        elif auto_start and not is_ready:
            logger.warning(f"⚠️  Printer not ready. Job queued but not started: {print_job.file_name}")

        return result

    async def get_job_status(self) -> Dict[str, Any]:
        """Get current job status"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/job",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to get job status: {e}")
            raise

    async def cancel_job(self) -> Dict[str, Any]:
        """Cancel current print job"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/job",
                headers=self.headers,
                json={"command": "cancel"}
            )
            response.raise_for_status()
            logger.info("❌ Cancelled current print job")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to cancel job: {e}")
            raise

    async def pause_job(self) -> Dict[str, Any]:
        """Pause current print job"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/job",
                headers=self.headers,
                json={"command": "pause", "action": "pause"}
            )
            response.raise_for_status()
            logger.info("⏸️  Paused current print job")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to pause job: {e}")
            raise

    async def resume_job(self) -> Dict[str, Any]:
        """Resume paused print job"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/job",
                headers=self.headers,
                json={"command": "pause", "action": "resume"}
            )
            response.raise_for_status()
            logger.info("▶️  Resumed print job")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to resume job: {e}")
            raise

    async def get_temperature(self) -> Dict[str, Any]:
        """Get current temperature readings"""
        try:
            status = await self.get_printer_status()
            return status.get("temperature", {})
        except Exception as e:
            logger.error(f"Failed to get temperature: {e}")
            raise

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class OctoPrintManager:
    """Manages multiple OctoPrint instances"""

    def __init__(self):
        self.printers: Dict[str, OctoPrintService] = {}

    def add_printer(self, config: OctoPrintConfig):
        """Add a printer to the manager"""
        service = OctoPrintService(config)
        self.printers[config.printer_id] = service
        logger.info(f"➕ Added printer: {config.printer_name} ({config.printer_id})")

    def remove_printer(self, printer_id: str):
        """Remove a printer from the manager"""
        if printer_id in self.printers:
            del self.printers[printer_id]
            logger.info(f"➖ Removed printer: {printer_id}")

    def get_printer(self, printer_id: str) -> Optional[OctoPrintService]:
        """Get printer service by ID"""
        return self.printers.get(printer_id)

    async def get_all_printer_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all printers"""
        statuses = {}
        for printer_id, service in self.printers.items():
            try:
                statuses[printer_id] = {
                    "status": await service.get_printer_status(),
                    "ready": await service.is_printer_ready()
                }
            except Exception as e:
                statuses[printer_id] = {
                    "error": str(e),
                    "ready": False
                }
        return statuses

    async def find_available_printer(self) -> Optional[str]:
        """Find the first available (ready) printer"""
        for printer_id, service in self.printers.items():
            try:
                if await service.is_printer_ready():
                    return printer_id
            except Exception:
                continue
        return None

    async def queue_to_next_available(self, print_job: PrintJob) -> Dict[str, Any]:
        """
        Queue print job to the next available printer

        Args:
            print_job: Print job to queue

        Returns:
            Job status with assigned printer
        """
        printer_id = await self.find_available_printer()

        if not printer_id:
            return {
                "success": False,
                "message": "No available printers",
                "job_id": print_job.job_id
            }

        service = self.printers[printer_id]
        result = await service.queue_print_job(print_job, auto_start=True)

        return {
            "success": True,
            "printer_id": printer_id,
            "printer_name": service.config.printer_name,
            **result
        }

    async def close_all(self):
        """Close all printer connections"""
        for service in self.printers.values():
            await service.close()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_usage():
    """Example of how to use the OctoPrint service"""

    # Initialize manager
    manager = OctoPrintManager()

    # Add printers
    manager.add_printer(OctoPrintConfig(
        url="http://192.168.1.100",
        api_key="YOUR_API_KEY_HERE",
        printer_id="fdm-printer-1",
        printer_name="Prusa i3 MK3S"
    ))

    manager.add_printer(OctoPrintConfig(
        url="http://192.168.1.101",
        api_key="YOUR_API_KEY_HERE",
        printer_id="fdm-printer-2",
        printer_name="Ender 3 V2"
    ))

    # Check all printer statuses
    statuses = await manager.get_all_printer_statuses()
    print("Printer Statuses:", statuses)

    # Queue a print job to next available printer
    job = PrintJob(
        job_id="job-123",
        file_name="prototype-part.stl",
        file_url="https://r2.example.com/files/prototype-part.stl"
    )

    result = await manager.queue_to_next_available(job)
    print("Queue Result:", result)

    # Close all connections
    await manager.close_all()


if __name__ == "__main__":
    asyncio.run(example_usage())
