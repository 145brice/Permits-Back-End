-- Supabase Setup for Contractor Leads SaaS
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/zppsfwxycmujqetsnbtj/sql

-- 1. Geocode Cache Table (persistent address to coordinates mapping)
CREATE TABLE IF NOT EXISTS geocode_cache (
    id BIGSERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(address, city)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_geocode_address_city ON geocode_cache(address, city);

-- 2. Permits Table (store all scraped permits)
CREATE TABLE IF NOT EXISTS permits (
    id BIGSERIAL PRIMARY KEY,
    permit_number TEXT,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT DEFAULT 'USA',
    zip_code TEXT,
    permit_type TEXT,
    description TEXT,
    issue_date DATE,
    estimated_cost DECIMAL,
    status TEXT,
    owner_name TEXT,
    contractor TEXT,
    contractor_phone TEXT,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    source TEXT,
    UNIQUE(permit_number, city)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_permits_city ON permits(city);
CREATE INDEX IF NOT EXISTS idx_permits_issue_date ON permits(issue_date DESC);
CREATE INDEX IF NOT EXISTS idx_permits_city_date ON permits(city, issue_date DESC);

-- 3. Users/Subscribers Table (optional - for tracking paid users)
CREATE TABLE IF NOT EXISTS subscribers (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    stripe_customer_id TEXT,
    cities TEXT[], -- Array of subscribed cities
    subscription_status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for email lookups
CREATE INDEX IF NOT EXISTS idx_subscribers_email ON subscribers(email);

-- 4. Enable Row Level Security (RLS) for public access patterns
ALTER TABLE geocode_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE permits ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscribers ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read geocode cache
CREATE POLICY "Anyone can read geocode cache" ON geocode_cache
    FOR SELECT USING (true);

-- Policy: Service role can insert/update geocode cache
CREATE POLICY "Service role can manage geocode cache" ON geocode_cache
    FOR ALL USING (auth.role() = 'service_role');

-- Policy: Anyone can read permits (public map)
CREATE POLICY "Anyone can read permits" ON permits
    FOR SELECT USING (true);

-- Policy: Service role can manage permits
CREATE POLICY "Service role can manage permits" ON permits
    FOR ALL USING (auth.role() = 'service_role');

-- Policy: Users can read their own subscriber info
CREATE POLICY "Users can read own subscriber data" ON subscribers
    FOR SELECT USING (auth.email() = email);

-- Policy: Service role can manage subscribers
CREATE POLICY "Service role can manage subscribers" ON subscribers
    FOR ALL USING (auth.role() = 'service_role');

-- Sample insert to verify tables work
-- INSERT INTO geocode_cache (address, city, lat, lng) VALUES ('123 Test St', 'Austin', 30.2672, -97.7431);

SELECT 'Supabase tables created successfully!' as status;
