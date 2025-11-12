-- Database initialization script for rd_platform
-- This file is automatically executed when PostgreSQL container starts

-- Create database (already created by POSTGRES_DB env var)
-- CREATE DATABASE IF NOT EXISTS rd_platform;

-- Note: Medusa.js handles its own migrations via MikroORM
-- Processing API will create its tables via SQLAlchemy

-- You can add any custom initialization here if needed
-- For example, creating extensions:

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant privileges (if using custom users)
-- GRANT ALL PRIVILEGES ON DATABASE rd_platform TO api_user;

-- Success message
SELECT 'Database initialization complete' AS status;
