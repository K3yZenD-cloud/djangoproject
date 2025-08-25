-- =====================================================
-- ESQUEMA DE BASE DE DATOS POSTGRESQL 
-- CLUB DE LECTURA ELIXIR
-- =====================================================

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLAS PRINCIPALES
-- =====================================================

-- Tabla de Géneros
CREATE TABLE main_genre (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT DEFAULT ''
);

-- Tabla de Libros
CREATE TABLE main_book (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) DEFAULT '',
    publication_year INTEGER,
    synopsis TEXT NOT NULL,
    cover_image TEXT DEFAULT '',
    reading_status VARCHAR(20) DEFAULT 'upcoming' CHECK (reading_status IN ('current', 'upcoming', 'completed')),
    reading_start_date DATE,
    reading_end_date DATE,
    average_rating DECIMAL(3,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla intermedia para relación Many-to-Many entre Libros y Géneros
CREATE TABLE main_book_genres (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT REFERENCES main_book(id) ON DELETE CASCADE,
    genre_id BIGINT REFERENCES main_genre(id) ON DELETE CASCADE,
    UNIQUE(book_id, genre_id)
);

-- Tabla de Reseñas de Libros
CREATE TABLE main_bookreview (
    id BIGSERIAL PRIMARY KEY,
    book_id BIGINT REFERENCES main_book(id) ON DELETE CASCADE,
    author_name VARCHAR(100) NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_featured BOOLEAN DEFAULT FALSE
);

-- Tabla de Eventos
CREATE TABLE main_event (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    event_type VARCHAR(20) DEFAULT 'meeting' CHECK (event_type IN ('meeting', 'discussion', 'author_talk', 'workshop', 'other')),
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    location VARCHAR(200) DEFAULT '',
    online_link TEXT DEFAULT '',
    book_id BIGINT REFERENCES main_book(id) ON DELETE SET NULL,
    max_participants INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Entradas de Blog
CREATE TABLE main_blogpost (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    book_id BIGINT REFERENCES main_book(id) ON DELETE SET NULL,
    featured_quote TEXT DEFAULT '',
    is_published BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Miembros
CREATE TABLE main_member (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(20) DEFAULT '',
    bio TEXT DEFAULT '',
    join_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    profile_image TEXT DEFAULT ''
);

-- Tabla intermedia para géneros favoritos de miembros
CREATE TABLE main_member_favorite_genres (
    id BIGSERIAL PRIMARY KEY,
    member_id BIGINT REFERENCES main_member(id) ON DELETE CASCADE,
    genre_id BIGINT REFERENCES main_genre(id) ON DELETE CASCADE,
    UNIQUE(member_id, genre_id)
);

-- Tabla de Sugerencias de Libros
CREATE TABLE main_booksuggestion (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    suggested_by_name VARCHAR(100) NOT NULL,
    suggested_by_email VARCHAR(254) NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Newsletter
CREATE TABLE main_newsletter (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    name VARCHAR(100) DEFAULT '',
    subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabla de Galería
CREATE TABLE main_gallery (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    image_url TEXT NOT NULL,
    event_id BIGINT REFERENCES main_event(id) ON DELETE SET NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_featured BOOLEAN DEFAULT FALSE
);

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para búsquedas frecuentes
CREATE INDEX idx_book_reading_status ON main_book(reading_status);
CREATE INDEX idx_book_created_at ON main_book(created_at);
CREATE INDEX idx_event_date ON main_event(date);
CREATE INDEX idx_event_is_active ON main_event(is_active);
CREATE INDEX idx_blogpost_is_published ON main_blogpost(is_published);
CREATE INDEX idx_blogpost_is_featured ON main_blogpost(is_featured);
CREATE INDEX idx_blogpost_created_at ON main_blogpost(created_at);
CREATE INDEX idx_member_is_active ON main_member(is_active);
CREATE INDEX idx_booksuggestion_status ON main_booksuggestion(status);
CREATE INDEX idx_gallery_is_featured ON main_gallery(is_featured);
CREATE INDEX idx_newsletter_is_active ON main_newsletter(is_active);

-- Índices para búsquedas de texto
CREATE INDEX idx_book_title ON main_book USING gin(to_tsvector('spanish', title));
CREATE INDEX idx_book_author ON main_book USING gin(to_tsvector('spanish', author));
CREATE INDEX idx_genre_name ON main_genre USING gin(to_tsvector('spanish', name));

-- =====================================================
-- TRIGGERS PARA ACTUALIZACIÓN AUTOMÁTICA
-- =====================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar updated_at en blogpost
CREATE TRIGGER update_blogpost_updated_at 
    BEFORE UPDATE ON main_blogpost 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- DATOS INICIALES (OPCIONAL)
-- =====================================================

-- Insertar géneros básicos
INSERT INTO main_genre (name, description) VALUES
('Ficción', 'Obras de literatura narrativa imaginaria'),
('No Ficción', 'Obras basadas en hechos reales'),
('Misterio', 'Novelas de suspense y misterio'),
('Romance', 'Historias de amor y relaciones'),
('Ciencia Ficción', 'Literatura especulativa sobre el futuro'),
('Fantasía', 'Historias con elementos mágicos o sobrenaturales'),
('Biografía', 'Relatos de vidas reales'),
('Historia', 'Libros sobre eventos históricos'),
('Filosofía', 'Obras de pensamiento filosófico'),
('Poesía', 'Colecciones de poemas y versos');

-- =====================================================
-- COMENTARIOS SOBRE LAS TABLAS
-- =====================================================

COMMENT ON TABLE main_genre IS 'Géneros literarios disponibles para clasificar libros';
COMMENT ON TABLE main_book IS 'Catálogo principal de libros del club de lectura';
COMMENT ON TABLE main_bookreview IS 'Reseñas y calificaciones de libros por miembros';
COMMENT ON TABLE main_event IS 'Eventos y actividades del club de lectura';
COMMENT ON TABLE main_blogpost IS 'Entradas del blog con reflexiones literarias';
COMMENT ON TABLE main_member IS 'Miembros registrados del club de lectura';
COMMENT ON TABLE main_booksuggestion IS 'Sugerencias de libros propuestas por miembros';
COMMENT ON TABLE main_newsletter IS 'Suscriptores al boletín informativo';
COMMENT ON TABLE main_gallery IS 'Galería de fotos de eventos y actividades';

-- =====================================================
-- CONSULTAS ÚTILES PARA VERIFICACIÓN
-- =====================================================

-- Verificar que todas las tablas se crearon correctamente
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'main_%'
ORDER BY table_name;

-- Verificar índices creados
SELECT indexname, tablename 
FROM pg_indexes 
WHERE tablename LIKE 'main_%'
ORDER BY tablename, indexname;
