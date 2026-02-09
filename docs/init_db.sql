-- Script de configuración de base de datos
-- Proyecto: BolsosApp
-- Alumna: Yasbel Olivares Soto
-- Curso: 2DAW

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS yasbel;

-- Crear el usuario 2DAW
CREATE USER IF NOT EXISTS '2DAW'@'localhost' IDENTIFIED BY '2DAW_pass';

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON yasbel.* TO '2DAW'@'localhost';
FLUSH PRIVILEGES;

-- Usar la base de datos
USE yasbel;

-- Tabla de bolsos
CREATE TABLE IF NOT EXISTS bolsos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    color VARCHAR(50) NOT NULL,
    tipo ENUM('bandolera', 'mochila', 'tote') NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO bolsos (nombre, marca, precio, color, tipo, stock) VALUES

('Bolso a Eliminar', 'Delete Test', 25.00, 'Gris', 'bandolera', 3),
('Mochila Urban', 'UrbanStyle', 79.99, 'Negro', 'mochila', 15),
('Tote Elegante', 'LuxBrand', 45.50, 'Beige', 'tote', 8),
('Bandolera Casual', 'CasualWear', 35.00, 'Azul', 'bandolera', 12),
('Mochila Deportiva', 'SportMax', 65.00, 'Rojo', 'mochila', 20),
('Tote Minimalista', 'SimpleStyle', 40.00, 'Blanco', 'tote', 10),
('Bandolera Vintage', 'RetroChic', 55.00, 'Marrón', 'bandolera', 5),
('Mochila Escolar', 'StudyPro', 50.00, 'Verde', 'mochila', 25),
('Tote Shopping', 'ShopEasy', 30.00, 'Rosa', 'tote', 18),
('Bandolera Compacta', 'MiniStyle', 28.00, 'Negro', 'bandolera', 14);

SELECT 'Base de datos configurada - Yasbel Olivares Soto 2DAW' AS mensaje;
