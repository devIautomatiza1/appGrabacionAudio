-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.opportunities (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  recording_id uuid,
  title text,
  description text,
  created_at timestamp without time zone DEFAULT now(),
  status text DEFAULT 'Open'::text,
  priority text DEFAULT 'Medium'::text,
  ticket_number integer NOT NULL DEFAULT nextval('opportunities_ticket_number_seq'::regclass),
  notes text,
  updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT opportunities_pkey PRIMARY KEY (id),
  CONSTRAINT opportunities_recording_id_fkey FOREIGN KEY (recording_id) REFERENCES public.recordings(id)
);
CREATE TABLE public.recordings (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  filename text NOT NULL,
  filepath text NOT NULL,
  transcription text,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  CONSTRAINT recordings_pkey PRIMARY KEY (id)
);
CREATE TABLE public.transcriptions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  recording_id uuid NOT NULL,
  content text NOT NULL,
  language text DEFAULT 'es'::text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT transcriptions_pkey PRIMARY KEY (id),
  CONSTRAINT transcriptions_recording_id_fkey FOREIGN KEY (recording_id) REFERENCES public.recordings(id)
);