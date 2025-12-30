-- ============================================================
-- ContentForge Supabase Tabloları
-- Bu SQL'i Supabase Dashboard > SQL Editor'de çalıştırın
-- ============================================================

-- 1. Profiller tablosu (kullanıcı bilgileri)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL DEFAULT '',
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'pro')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. İçerikler tablosu (oluşturulan bloglar)
CREATE TABLE IF NOT EXISTS contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. İndeksler (performans için)
CREATE INDEX IF NOT EXISTS idx_contents_user_id ON contents(user_id);
CREATE INDEX IF NOT EXISTS idx_contents_created_at ON contents(created_at DESC);

-- 4. Row Level Security (RLS) - Güvenlik
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE contents ENABLE ROW LEVEL SECURITY;

-- Mevcut policy'leri temizle (hata önleme)
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Service role can insert profiles" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
DROP POLICY IF EXISTS "Users can view own contents" ON contents;
DROP POLICY IF EXISTS "Users can insert own contents" ON contents;
DROP POLICY IF EXISTS "Users can delete own contents" ON contents;

-- Kullanıcılar sadece kendi profillerini görebilir
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Kullanıcılar kendi profillerini oluşturabilir
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Kullanıcılar sadece kendi içeriklerini yönetebilir
CREATE POLICY "Users can view own contents" ON contents
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own contents" ON contents
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own contents" ON contents
    FOR DELETE USING (auth.uid() = user_id);

-- 5. Mevcut kullanıcılar için profil oluştur (eksik olanlar için)
INSERT INTO profiles (id, email, plan)
SELECT id, email, 'free'
FROM auth.users
WHERE id NOT IN (SELECT id FROM profiles)
ON CONFLICT (id) DO NOTHING;

-- ============================================================
-- Kurulum tamamlandı!
-- ============================================================
