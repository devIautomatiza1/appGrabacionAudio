-- 1. Crear tabla de Grabaciones (Recordings)
CREATE TABLE recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    transcription TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsquedas por filename
CREATE INDEX idx_recordings_filename ON recordings(filename);

-- 2. Crear tabla de Transcripciones (Transcriptions)
CREATE TABLE transcriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID NOT NULL,
    content TEXT NOT NULL,
    language TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Relación con recordings
    CONSTRAINT fk_recording_transcription 
        FOREIGN KEY (recording_id) 
        REFERENCES recordings(id) 
        ON DELETE CASCADE
);

-- Índices para mejor rendimiento
CREATE INDEX idx_transcriptions_recording_id ON transcriptions(recording_id);
CREATE INDEX idx_transcriptions_created_at ON transcriptions(created_at DESC);

-- 3. Crear tabla de Oportunidades (Opportunities)
CREATE TABLE opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID,
    title TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    priority TEXT,
    ticket_number INT4,
    notes TEXT,

    -- Relación con recordings
    CONSTRAINT fk_recording_opportunity 
        FOREIGN KEY (recording_id) 
        REFERENCES recordings(id) 
        ON DELETE SET NULL
);

-- Índices para mejor rendimiento
CREATE INDEX idx_opportunities_recording_id ON opportunities(recording_id);
CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_opportunities_priority ON opportunities(priority);