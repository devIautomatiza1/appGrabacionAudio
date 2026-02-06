-- ============================================================================
-- TABLA: transcriptions
-- DESCRIPCIÓN: Almacena las transcripciones de audio generadas por el usuario
-- RELACIÓN: 1:N con recordings (un audio puede tener múltiples versiones de transcripción)
-- CASCADA: ON DELETE CASCADE - si se elimina un recording, se eliminan sus transcripciones
-- ============================================================================

-- 1. CREAR LA TABLA transcriptions
CREATE TABLE IF NOT EXISTS public.transcriptions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id uuid NOT NULL REFERENCES public.recordings(id) ON DELETE CASCADE,
    content text NOT NULL,
    language text DEFAULT 'es',
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);

-- 2. CREAR ÍNDICE PARA OPTIMIZAR BÚSQUEDAS POR recording_id
CREATE INDEX IF NOT EXISTS idx_transcriptions_recording_id 
    ON public.transcriptions(recording_id);
