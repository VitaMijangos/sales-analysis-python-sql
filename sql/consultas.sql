-- Mostrar todas las ventas
SELECT *
FROM ventas;


-- Contar registros
SELECT COUNT(*) AS total_ventas
FROM ventas;


-- Calcular los ingresos totales
SELECT SUM(total_venta) AS ingresos_totales
FROM ventas;


-- Calcular el ticket promedio
SELECT AVG(total_venta) AS ticket_promedio
FROM ventas;


-- Ventas por producto
SELECT
    producto,
    SUM(cantidad) AS unidades_vendidas,
    SUM(total_venta) AS ingresos
FROM ventas
GROUP BY producto
ORDER BY ingresos DESC;


-- Ventas por ciudad
SELECT
    ciudad,
    SUM(total_venta) AS ingresos
FROM ventas
GROUP BY ciudad
ORDER BY ingresos DESC;


-- Ventas por categoría
SELECT
    categoria,
    SUM(total_venta) AS ingresos
FROM ventas
GROUP BY categoria
ORDER BY ingresos DESC;