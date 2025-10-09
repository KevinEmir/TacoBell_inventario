-- ============================================
-- SISTEMA DE GESTIÓN DE INVENTARIO
-- Base de Datos: InventarioRestaurante
-- Versión (1-1.5 semanas)
-- ============================================

-- Crear la base de datos
CREATE DATABASE InventarioRestaurante;
GO

USE InventarioRestaurante;
GO

-- ============================================
-- TABLA: Categorias
-- ============================================
CREATE TABLE Categorias (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL UNIQUE,
    Descripcion NVARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME2 DEFAULT GETDATE()
);
GO

-- ============================================
-- TABLA: Proveedores
-- ============================================
CREATE TABLE Proveedores (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(150) NOT NULL,
    Contacto NVARCHAR(100),
    Telefono NVARCHAR(20),
    Email NVARCHAR(100),
    Direccion NVARCHAR(MAX),
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME2 DEFAULT GETDATE()
);
GO

-- ============================================
-- TABLA: Productos
-- ============================================
CREATE TABLE Productos (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(150) NOT NULL,
    Descripcion NVARCHAR(MAX),
    CodigoSKU NVARCHAR(50) UNIQUE NOT NULL,
    
    -- Stock
    CantidadActual DECIMAL(10,2) DEFAULT 0,
    UnidadMedida NVARCHAR(20) NOT NULL,
    StockMinimo DECIMAL(10,2) DEFAULT 0,
    
    -- Precio
    PrecioUnitario DECIMAL(10,2),
    
    -- Relaciones
    CategoriaId INT NOT NULL,
    ProveedorId INT NOT NULL,
    
    -- Metadata
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME2 DEFAULT GETDATE(),
    FechaActualizacion DATETIME2 DEFAULT GETDATE(),
    
    -- Foreign Keys
    CONSTRAINT FK_Productos_Categorias FOREIGN KEY (CategoriaId) 
        REFERENCES Categorias(Id),
    CONSTRAINT FK_Productos_Proveedores FOREIGN KEY (ProveedorId) 
        REFERENCES Proveedores(Id)
);
GO

-- ============================================
-- TABLA: Movimientos
-- ============================================
CREATE TABLE Movimientos (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ProductoId INT NOT NULL,
    
    -- Tipo: 'entrada', 'salida'
    Tipo NVARCHAR(20) NOT NULL CHECK (Tipo IN ('entrada', 'salida')),
    Cantidad DECIMAL(10,2) NOT NULL,
    
    -- Información adicional
    Motivo NVARCHAR(200),
    Notas NVARCHAR(MAX),
    Usuario NVARCHAR(100) DEFAULT 'Sistema',
    
    -- Metadata
    FechaCreacion DATETIME2 DEFAULT GETDATE(),
    
    -- Foreign Key
    CONSTRAINT FK_Movimientos_Productos FOREIGN KEY (ProductoId) 
        REFERENCES Productos(Id)
);
GO

-- ============================================
-- ÍNDICES
-- ============================================

-- Índices para tabla Categorias
CREATE INDEX IX_Categorias_Nombre ON Categorias(Nombre);
CREATE INDEX IX_Categorias_Activo ON Categorias(Activo);
GO

-- Índices para tabla Proveedores
CREATE INDEX IX_Proveedores_Nombre ON Proveedores(Nombre);
CREATE INDEX IX_Proveedores_Activo ON Proveedores(Activo);
GO

-- Índices para tabla Productos
CREATE INDEX IX_Productos_Nombre ON Productos(Nombre);
CREATE INDEX IX_Productos_CodigoSKU ON Productos(CodigoSKU);
CREATE INDEX IX_Productos_Activo ON Productos(Activo);
CREATE INDEX IX_Productos_CategoriaId ON Productos(CategoriaId);
CREATE INDEX IX_Productos_ProveedorId ON Productos(ProveedorId);
CREATE INDEX IX_Productos_CantidadActual ON Productos(CantidadActual);
GO

-- Índices para tabla Movimientos
CREATE INDEX IX_Movimientos_ProductoId ON Movimientos(ProductoId);
CREATE INDEX IX_Movimientos_FechaCreacion ON Movimientos(FechaCreacion);
CREATE INDEX IX_Movimientos_Tipo ON Movimientos(Tipo);
GO

PRINT '============================================';
PRINT 'Base de datos creada exitosamente!';
PRINT '============================================';
PRINT 'Total de tablas: 4';
PRINT '  - Categorias';
PRINT '  - Proveedores';
PRINT '  - Productos';
PRINT '  - Movimientos';
PRINT '============================================';
PRINT 'Total de índices: 13';
PRINT '============================================';
GO