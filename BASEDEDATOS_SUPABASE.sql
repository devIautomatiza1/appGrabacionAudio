-- ============================================================================
-- PROYECTO: Audio Recorder & Opportunity Manager
-- DESCRIPCIÓN: Script completo de creación de Base de Datos Supabase
-- FECHA: 2026-02-06
-- NOTA: Ejecutar en el SQL Editor de Supabase console
-- ============================================================================

-- 1. TABLA: recordings
-- Almacena la metadata de los archivos de audio subidos o grabados.
CREATE TABLE IF NOT EXISTS public.recordings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    filename text NOT NULL,
    filepath text NOT NULL,
    transcription text, -- ⚠️ Mantenido por compatibilidad legacy
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- 2. TABLA: transcriptions
-- Almacena el texto procesado por IA de los audios.
-- Relación 1:N con recordings (un audio puede re-transcribirse).
CREATE TABLE IF NOT EXISTS public.transcriptions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id uuid NOT NULL REFERENCES public.recordings(id) ON DELETE CASCADE,
    content text NOT NULL,
    language text DEFAULT 'es',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- 3. TABLA: opportunities
-- Gestiona los tickets de soporte generados automáticamente a partir de palabras clave.
CREATE TABLE IF NOT EXISTS public.opportunities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id uuid NOT NULL REFERENCES public.recordings(id) ON DELETE CASCADE,
    ticket_number int4 GENERATED ALWAYS AS IDENTITY, -- Identificador secuencial único
    title text NOT NULL,
    description text NOT NULL,
    status text DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'closed', 'won')),
    priority text DEFAULT 'Low' CHECK (priority IN ('Low', 'Medium', 'High')),
    notes text, -- Campo para observaciones del técnico
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- ============================================================================
-- ÍNDICES DE OPTIMIZACIÓN
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_transcriptions_recording_id ON public.transcriptions(recording_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_recording_id ON public.opportunities(recording_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON public.opportunities(status);

-- ============================================================================
-- POLÍTICAS DE SEGURIDAD (RLS)
-- Nota: Configurado para DESARROLLO (sin autenticación estricta)
-- IMPORTANTE: Para PRODUCCIÓN, implementar Supabase Auth y políticas por usuario
-- ============================================================================

ALTER TABLE public.recordings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.opportunities ENABLE ROW LEVEL SECURITY;

-- Política de acceso público/desarrollo (Permitir todo por ahora)
CREATE POLICY "Public Access Recordings" ON public.recordings FOR ALL USING (true);
CREATE POLICY "Public Access Transcriptions" ON public.transcriptions FOR ALL USING (true);
CREATE POLICY "Public Access Opportunities" ON public.opportunities FOR ALL USING (true);

-- ============================================================================
-- COMENTARIOS DE DOCUMENTACIÓN
-- ============================================================================
COMMENT ON TABLE public.recordings IS 'Metadata de archivos de audio guardados en Storage.';
COMMENT ON TABLE public.transcriptions IS 'Texto generado por IA. Relación dependiente de recordings.';
COMMENT ON TABLE public.opportunities IS 'Tickets de soporte/negocio extraídos por contexto.';