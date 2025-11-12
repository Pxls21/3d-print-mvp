"""
Bambu Lab Integration Service
Automatically queue FDM print jobs to Bambu Lab printers via MQTT API
Uses bambulabs-api (MIT licensed) - https://pypi.org/project/bambulabs-api/

Hardware: 2x Bambu Lab P1S printers
"""

import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import logging
import httpx
from pathlib import Path

# bambulabs-api library (MIT licensed)
# Install: pip install bambulabs-api
try:
    from bambulabs_api import BambuClient
    from bambulabs_api.printer import PrinterStatus
except ImportError:
    raise ImportError(
        "bambulabs-api not installed. Install with: pip install bambulabs-api\n"
        "This is an MIT licensed library for Bambu Lab printer control."
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BambuPrinterState(str, Enum):
    """Bambu Lab printer states"""
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


@dataclass
class BambuLabConfig:
    """Bambu Lab printer configuration"""
    ip_address: str
    access_code: str
    serial_number: str
    printer_id: str
    printer_name: str


@dataclass
class PrintJob:
    """Print job information"""
    job_id: str
    file_name: str
    file_url: str  # STL file URL (from R2)
    estimated_time: Optional[float] = None  # seconds
    status: str = "queued"


class BambuLabService:
    """Service for interacting with Bambu Lab printers via MQTT API"""

    def __init__(self, config: BambuLabConfig):
        self.config = config
        self.client: Optional[BambuClient] = None
        self._connected = False
        logger.info(f"🔧 Initialized Bambu Lab service: {config.printer_name}")

    async def connect(self) -> bool:
        """
        Connect to Bambu Lab printer via MQTT

        Returns:
            True if connected successfully
        """
        try:
            # Initialize Bambu Client
            self.client = BambuClient(
                hostname=self.config.ip_address,
                access_code=self.config.access_code,
                serial=self.config.serial_number
            )

            # Connect to printer
            await asyncio.to_thread(self.client.connect)
            self._connected = True
            logger.info(f"✅ Connected to {self.config.printer_name}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to {self.config.printer_name}: {e}")
            self._connected = False
            return False

    async def disconnect(self):
        """Disconnect from printer"""
        if self.client and self._connected:
            try:
                await asyncio.to_thread(self.client.disconnect)
                self._connected = False
                logger.info(f"🔌 Disconnected from {self.config.printer_name}")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")

    async def get_printer_status(self) -> Dict[str, Any]:
        """
        Get current printer status

        Returns:
            Dict with printer state, temperatures, progress, etc.
        """
        if not self._connected or not self.client:
            return {
                "state": BambuPrinterState.OFFLINE,
                "error": "Not connected"
            }

        try:
            # Get status from Bambu API
            status = await asyncio.to_thread(lambda: self.client.get_device())

            return {
                "state": self._map_state(status),
                "nozzle_temp": getattr(status, "nozzle_temp", 0),
                "bed_temp": getattr(status, "bed_temp", 0),
                "target_nozzle_temp": getattr(status, "target_nozzle_temp", 0),
                "target_bed_temp": getattr(status, "target_bed_temp", 0),
                "print_progress": getattr(status, "print_progress", 0),
                "current_file": getattr(status, "current_file", None),
                "printer_name": self.config.printer_name,
                "printer_id": self.config.printer_id
            }

        except Exception as e:
            logger.error(f"Failed to get printer status: {e}")
            return {
                "state": BambuPrinterState.UNKNOWN,
                "error": str(e)
            }

    def _map_state(self, status) -> BambuPrinterState:
        """Map Bambu API status to our state enum"""
        try:
            state = getattr(status, "state", "UNKNOWN").upper()

            if state in ["IDLE", "READY"]:
                return BambuPrinterState.IDLE
            elif state in ["RUNNING", "PRINTING"]:
                return BambuPrinterState.RUNNING
            elif state == "PAUSED":
                return BambuPrinterState.PAUSED
            elif state in ["COMPLETE", "FINISHED"]:
                return BambuPrinterState.COMPLETE
            elif state in ["FAILED", "ERROR"]:
                return BambuPrinterState.FAILED
            else:
                return BambuPrinterState.UNKNOWN

        except Exception:
            return BambuPrinterState.UNKNOWN

    async def is_printer_ready(self) -> bool:
        """
        Check if printer is ready to accept jobs

        Returns:
            True if printer is idle and ready
        """
        status = await self.get_printer_status()
        state = status.get("state")
        return state == BambuPrinterState.IDLE

    async def upload_and_print(self, print_job: PrintJob, auto_start: bool = True) -> Dict[str, Any]:
        """
        Upload STL file and optionally start printing

        Args:
            print_job: PrintJob with file URL and metadata
            auto_start: Whether to automatically start printing

        Returns:
            Job status information
        """
        logger.info(f"📥 Queueing print job: {print_job.file_name} on {self.config.printer_name}")

        if not self._connected:
            await self.connect()

        try:
            # Download STL file from R2
            logger.info(f"⬇️  Downloading {print_job.file_name} from R2...")
            async with httpx.AsyncClient(timeout=60.0) as http_client:
                response = await http_client.get(print_job.file_url)
                response.raise_for_status()
                file_content = response.content

            # Save to temporary file
            temp_path = Path(f"/tmp/{print_job.file_name}")
            temp_path.write_bytes(file_content)
            logger.info(f"💾 Saved to {temp_path}")

            # Upload to Bambu Lab printer
            logger.info(f"⬆️  Uploading to {self.config.printer_name}...")
            await asyncio.to_thread(
                self.client.upload_file,
                str(temp_path)
            )
            logger.info(f"✅ Uploaded {print_job.file_name}")

            # Start print if auto_start is enabled
            started = False
            if auto_start:
                is_ready = await self.is_printer_ready()

                if is_ready:
                    logger.info(f"🖨️  Starting print...")
                    await asyncio.to_thread(
                        self.client.start_print,
                        print_job.file_name
                    )
                    started = True
                    logger.info(f"✅ Print started: {print_job.file_name}")
                else:
                    logger.warning(f"⚠️  Printer busy, job queued but not started")

            # Clean up temp file
            temp_path.unlink()

            return {
                "job_id": print_job.job_id,
                "file_name": print_job.file_name,
                "uploaded": True,
                "started": started,
                "printer_id": self.config.printer_id,
                "printer_name": self.config.printer_name
            }

        except Exception as e:
            logger.error(f"❌ Failed to queue print job: {e}")
            return {
                "job_id": print_job.job_id,
                "uploaded": False,
                "started": False,
                "error": str(e)
            }

    async def pause_print(self) -> Dict[str, Any]:
        """Pause current print job"""
        try:
            await asyncio.to_thread(self.client.pause)
            logger.info(f"⏸️  Paused print on {self.config.printer_name}")
            return {"success": True, "action": "paused"}
        except Exception as e:
            logger.error(f"Failed to pause: {e}")
            return {"success": False, "error": str(e)}

    async def resume_print(self) -> Dict[str, Any]:
        """Resume paused print job"""
        try:
            await asyncio.to_thread(self.client.resume)
            logger.info(f"▶️  Resumed print on {self.config.printer_name}")
            return {"success": True, "action": "resumed"}
        except Exception as e:
            logger.error(f"Failed to resume: {e}")
            return {"success": False, "error": str(e)}

    async def stop_print(self) -> Dict[str, Any]:
        """Stop/cancel current print job"""
        try:
            await asyncio.to_thread(self.client.stop)
            logger.info(f"⏹️  Stopped print on {self.config.printer_name}")
            return {"success": True, "action": "stopped"}
        except Exception as e:
            logger.error(f"Failed to stop: {e}")
            return {"success": False, "error": str(e)}


class BambuLabManager:
    """Manages multiple Bambu Lab P1S printers"""

    def __init__(self):
        self.printers: Dict[str, BambuLabService] = {}
        logger.info("🏭 Initialized Bambu Lab Manager")

    async def add_printer(self, config: BambuLabConfig) -> bool:
        """
        Add a printer to the manager

        Returns:
            True if printer connected successfully
        """
        service = BambuLabService(config)
        connected = await service.connect()

        if connected:
            self.printers[config.printer_id] = service
            logger.info(f"➕ Added printer: {config.printer_name} ({config.printer_id})")
            return True
        else:
            logger.error(f"❌ Failed to add printer: {config.printer_name}")
            return False

    def remove_printer(self, printer_id: str):
        """Remove a printer from the manager"""
        if printer_id in self.printers:
            del self.printers[printer_id]
            logger.info(f"➖ Removed printer: {printer_id}")

    def get_printer(self, printer_id: str) -> Optional[BambuLabService]:
        """Get printer service by ID"""
        return self.printers.get(printer_id)

    async def get_all_printer_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all printers"""
        statuses = {}
        for printer_id, service in self.printers.items():
            try:
                status = await service.get_printer_status()
                statuses[printer_id] = {
                    "status": status,
                    "ready": status.get("state") == BambuPrinterState.IDLE
                }
            except Exception as e:
                statuses[printer_id] = {
                    "error": str(e),
                    "ready": False
                }
        return statuses

    async def find_available_printer(self) -> Optional[str]:
        """Find the first available (idle) printer"""
        for printer_id, service in self.printers.items():
            try:
                if await service.is_printer_ready():
                    logger.info(f"✅ Found available printer: {printer_id}")
                    return printer_id
            except Exception as e:
                logger.error(f"Error checking {printer_id}: {e}")
                continue
        return None

    async def queue_to_next_available(self, print_job: PrintJob) -> Dict[str, Any]:
        """
        Queue print job to the next available Bambu Lab printer

        Args:
            print_job: Print job to queue

        Returns:
            Job status with assigned printer
        """
        printer_id = await self.find_available_printer()

        if not printer_id:
            logger.warning("⚠️  No available printers")
            return {
                "success": False,
                "message": "No available printers - both Bambu Lab P1S printers are busy",
                "job_id": print_job.job_id
            }

        service = self.printers[printer_id]
        result = await service.upload_and_print(print_job, auto_start=True)

        return {
            "success": result.get("uploaded", False),
            "printer_id": printer_id,
            "printer_name": service.config.printer_name,
            **result
        }

    async def disconnect_all(self):
        """Disconnect all printer connections"""
        logger.info("🔌 Disconnecting all printers...")
        for service in self.printers.values():
            await service.disconnect()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_usage():
    """Example of how to use the Bambu Lab service"""

    # Initialize manager
    manager = BambuLabManager()

    # Add Bambu Lab P1S printers (from .env config)
    await manager.add_printer(BambuLabConfig(
        ip_address="192.168.1.100",
        access_code="YOUR_ACCESS_CODE",  # From printer settings
        serial_number="YOUR_SERIAL",
        printer_id="bambu-p1s-1",
        printer_name="Bambu Lab P1S #1"
    ))

    await manager.add_printer(BambuLabConfig(
        ip_address="192.168.1.101",
        access_code="YOUR_ACCESS_CODE",
        serial_number="YOUR_SERIAL",
        printer_id="bambu-p1s-2",
        printer_name="Bambu Lab P1S #2"
    ))

    # Check all printer statuses
    statuses = await manager.get_all_printer_statuses()
    print("🖨️  Printer Statuses:", statuses)

    # Queue a print job to next available printer
    job = PrintJob(
        job_id="job-123",
        file_name="prototype-part.stl",
        file_url="https://your-r2-bucket.r2.dev/files/prototype-part.stl"
    )

    result = await manager.queue_to_next_available(job)
    print("📋 Queue Result:", result)

    # Disconnect all
    await manager.disconnect_all()


if __name__ == "__main__":
    asyncio.run(example_usage())
