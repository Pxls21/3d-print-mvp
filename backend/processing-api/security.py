"""
Security Middleware and Utilities
Handles authentication, rate limiting, input validation, and security headers
"""

import os
import time
from typing import Optional, Callable
from fastapi import HTTPException, Security, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import Headers
from functools import wraps
import redis
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwt123456789")
JWT_ALGORITHM = "HS256"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Rate limiting configuration
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds

# File upload limits
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default
MAX_FILES_PER_REQUEST = int(os.getenv("MAX_FILES_PER_REQUEST", "50"))
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

# Security headers configuration
ENABLE_HSTS = os.getenv("ENABLE_HSTS", "true").lower() == "true"
HSTS_MAX_AGE = int(os.getenv("HSTS_MAX_AGE", "31536000"))  # 1 year

# Initialize Redis for rate limiting
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    REDIS_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Redis not available for rate limiting: {e}")
    REDIS_AVAILABLE = False

# ============================================================================
# JWT AUTHENTICATION
# ============================================================================

security = HTTPBearer()


class AuthUser:
    """Authenticated user object"""
    def __init__(self, user_id: str, email: str, role: str = "user"):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.is_admin = role == "admin"


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> AuthUser:
    """
    Verify JWT token from Medusa.js backend

    Args:
        credentials: HTTP Authorization Bearer token

    Returns:
        AuthUser object with user details

    Raises:
        HTTPException: 401 if token is invalid or expired
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        user_id = payload.get("actor_id") or payload.get("sub") or payload.get("user_id")
        email = payload.get("email", "")
        role = payload.get("role", "user")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing user identifier"
            )

        return AuthUser(user_id=user_id, email=email, role=role)

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_admin(user: AuthUser = Security(verify_token)) -> AuthUser:
    """
    Verify user has admin role

    Args:
        user: Authenticated user from verify_token

    Returns:
        AuthUser if admin

    Raises:
        HTTPException: 403 if user is not admin
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user


def optional_auth(credentials: Optional[HTTPAuthorizationCredentials] = Security(security, auto_error=False)) -> Optional[AuthUser]:
    """
    Optional authentication - returns None if no token provided
    Used for endpoints that provide enhanced features for authenticated users
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("actor_id") or payload.get("sub") or payload.get("user_id")
        email = payload.get("email", "")
        role = payload.get("role", "user")

        if user_id:
            return AuthUser(user_id=user_id, email=email, role=role)
    except:
        pass

    return None


# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """Redis-backed rate limiter"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def _get_key(self, identifier: str, endpoint: str) -> str:
        """Generate Redis key for rate limiting"""
        return f"ratelimit:{identifier}:{endpoint}"

    async def check_rate_limit(
        self,
        request: Request,
        max_requests: Optional[int] = None,
        window_seconds: Optional[int] = None
    ) -> bool:
        """
        Check if request exceeds rate limit

        Args:
            request: FastAPI request object
            max_requests: Override default max requests
            window_seconds: Override default window

        Returns:
            True if within limit, False if exceeded
        """
        if not RATE_LIMIT_ENABLED or not REDIS_AVAILABLE:
            return True

        max_reqs = max_requests or self.max_requests
        window = window_seconds or self.window_seconds

        # Use IP address as identifier
        client_ip = request.client.host
        endpoint = request.url.path

        key = self._get_key(client_ip, endpoint)

        try:
            # Increment counter
            current = redis_client.incr(key)

            # Set expiry on first request
            if current == 1:
                redis_client.expire(key, window)

            # Check limit
            if current > max_reqs:
                return False

            return True

        except Exception as e:
            print(f"⚠️  Rate limit check failed: {e}")
            # Fail open - allow request if Redis is down
            return True

    async def get_rate_limit_info(self, request: Request) -> dict:
        """Get current rate limit status"""
        if not REDIS_AVAILABLE:
            return {
                "limit": self.max_requests,
                "remaining": self.max_requests,
                "reset": int(time.time()) + self.window_seconds
            }

        client_ip = request.client.host
        endpoint = request.url.path
        key = self._get_key(client_ip, endpoint)

        try:
            current = int(redis_client.get(key) or 0)
            ttl = redis_client.ttl(key)

            return {
                "limit": self.max_requests,
                "remaining": max(0, self.max_requests - current),
                "reset": int(time.time()) + (ttl if ttl > 0 else self.window_seconds)
            }
        except:
            return {
                "limit": self.max_requests,
                "remaining": self.max_requests,
                "reset": int(time.time()) + self.window_seconds
            }


# Global rate limiter instance
rate_limiter = RateLimiter(
    max_requests=RATE_LIMIT_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW
)


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Decorator for endpoint-specific rate limiting

    Usage:
        @app.post("/jobs/create")
        @rate_limit(max_requests=10, window_seconds=60)
        async def create_job():
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs
            request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)

            if request:
                allowed = await rate_limiter.check_rate_limit(
                    request,
                    max_requests=max_requests,
                    window_seconds=window_seconds
                )

                if not allowed:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds.",
                        headers={"Retry-After": str(window_seconds)}
                    )

            return await func(*args, **kwargs)

        return wrapper
    return decorator


# ============================================================================
# SECURITY HEADERS MIDDLEWARE
# ============================================================================

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # XSS protection (legacy, but still good to include)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # HSTS - Force HTTPS
        if ENABLE_HSTS:
            response.headers["Strict-Transport-Security"] = f"max-age={HSTS_MAX_AGE}; includeSubDomains; preload"

        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers["Content-Security-Policy"] = csp

        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions policy (formerly Feature-Policy)
        response.headers["Permissions-Policy"] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        )

        return response


# ============================================================================
# RATE LIMIT MIDDLEWARE
# ============================================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Global rate limiting middleware"""

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/", "/health"]:
            return await call_next(request)

        # Check rate limit
        allowed = await rate_limiter.check_rate_limit(request)

        if not allowed:
            # Get rate limit info
            info = await rate_limiter.get_rate_limit_info(request)

            return Response(
                content=f'{{"detail":"Rate limit exceeded. Try again in {info["reset"] - int(time.time())} seconds."}}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": str(info["reset"] - int(time.time())),
                    "X-RateLimit-Limit": str(info["limit"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(info["reset"])
                }
            )

        # Add rate limit headers to response
        response = await call_next(request)
        info = await rate_limiter.get_rate_limit_info(request)

        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(info["reset"])

        return response


# ============================================================================
# INPUT VALIDATION
# ============================================================================

class FileValidator:
    """Validate file uploads for security"""

    @staticmethod
    async def validate_image_upload(
        filename: str,
        content_type: str,
        file_size: int
    ) -> None:
        """
        Validate image file upload

        Args:
            filename: Name of uploaded file
            content_type: MIME type
            file_size: Size in bytes

        Raises:
            HTTPException: 400 if validation fails
        """
        # Check file extension
        import os
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '{ext}' not allowed. Allowed types: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )

        # Check MIME type
        if content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"MIME type '{content_type}' not allowed. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
            )

        # Check file size
        if file_size > MAX_FILE_SIZE:
            max_mb = MAX_FILE_SIZE / 1024 / 1024
            raise HTTPException(
                status_code=400,
                detail=f"File '{filename}' exceeds maximum size of {max_mb:.1f}MB"
            )

    @staticmethod
    async def validate_batch_upload(files: list, max_files: int = MAX_FILES_PER_REQUEST) -> None:
        """
        Validate batch file upload

        Args:
            files: List of uploaded files
            max_files: Maximum number of files allowed

        Raises:
            HTTPException: 400 if validation fails
        """
        if len(files) > max_files:
            raise HTTPException(
                status_code=400,
                detail=f"Too many files. Maximum {max_files} files allowed per request."
            )

        total_size = 0
        for file in files:
            # Individual file validation
            file.file.seek(0, 2)  # Seek to end
            size = file.file.tell()
            file.file.seek(0)  # Reset

            await FileValidator.validate_image_upload(
                filename=file.filename,
                content_type=file.content_type,
                file_size=size
            )

            total_size += size

        # Check total batch size (500MB max)
        max_batch_size = 500 * 1024 * 1024
        if total_size > max_batch_size:
            raise HTTPException(
                status_code=400,
                detail=f"Total upload size exceeds {max_batch_size/1024/1024:.0f}MB limit"
            )


# ============================================================================
# AUDIT LOGGING
# ============================================================================

class AuditLogger:
    """Log security-relevant events"""

    @staticmethod
    async def log_event(
        event_type: str,
        user_id: Optional[str],
        ip_address: str,
        endpoint: str,
        details: dict = None
    ):
        """
        Log audit event

        Args:
            event_type: Type of event (e.g., "auth_success", "auth_failed", "job_created")
            user_id: User ID if authenticated
            ip_address: Client IP address
            endpoint: API endpoint accessed
            details: Additional event details
        """
        import logging

        logger = logging.getLogger("audit")

        log_data = {
            "timestamp": time.time(),
            "event_type": event_type,
            "user_id": user_id or "anonymous",
            "ip_address": ip_address,
            "endpoint": endpoint,
            "details": details or {}
        }

        logger.info(f"AUDIT: {log_data}")

        # TODO: Send to external SIEM/logging service
        # if SENTRY_DSN:
        #     sentry_sdk.capture_message(f"Audit: {event_type}", level="info", extra=log_data)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_client_ip(request: Request) -> str:
    """Get client IP address, accounting for proxies"""
    # Check X-Forwarded-For header (if behind reverse proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Check X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fall back to direct connection IP
    return request.client.host


def hash_api_key(api_key: str) -> str:
    """Hash API key for secure storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()
