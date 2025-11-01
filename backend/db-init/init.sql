CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  correo VARCHAR(100)
);

INSERT INTO usuarios (nombre, correo)
VALUES
('Juan Pérez', 'juan@example.com'),
('María López', 'maria@example.com');
