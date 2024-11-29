1. Lista de empleados con salarios por encima del promedio del departamento
SELECT e.employee_id, e.name, e.salary, e.department_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);

2. Productos que se venden más que el promedio de su categoría sql
SELECT p.product_id, p.name, p.category_id, p.sales
FROM products p
WHERE p.sales > (
    SELECT AVG(sales)
    FROM products
    WHERE category_id = p.category_id
);

3. Clientes con el gasto total más alto por país
SELECT c.customer_id, c.name, c.country, c.total_spent
FROM customers c
WHERE c.total_spent = (
    SELECT MAX(total_spent)
    FROM customers
    WHERE country = c.country
);

4. Empleados cuyo salario es superior al del jefe directo
SELECT e.employee_id, e.name, e.salary, e.manager_id
FROM employees e
WHERE e.salary > (
    SELECT m.salary
    FROM employees m
    WHERE m.employee_id = e.manager_id
);

5. Departamentos con menos empleados que el promedio de la empresa
SELECT d.department_id, d.name, d.employee_count
FROM departments d
WHERE d.employee_count < (
    SELECT AVG(employee_count)
    FROM departments
);

6. Productos que nunca se vendieron
SELECT p.product_id, p.name
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM sales s
    WHERE s.product_id = p.product_id
);

7. Clientes con más pedidos que el promedio de pedidos por cliente
SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > (
    SELECT AVG(order_count)
    FROM (
        SELECT COUNT(order_id) AS order_count
        FROM orders
        GROUP BY customer_id
    ) AS subquery
);

8. Películas con duración mayor a la duración promedio del director
SELECT m.movie_id, m.title, m.duration, m.director_id
FROM movies m
WHERE m.duration > (
    SELECT AVG(duration)
    FROM movies
    WHERE director_id = m.director_id
);

9. Productos con precios mayores que cualquier producto de una categoría específica
SELECT p.product_id, p.name, p.price
FROM products p
WHERE p.price > ALL (
    SELECT p2.price
    FROM products p2
    WHERE p2.category_id = 3
);

10. Tiendas donde no se alcanzó el objetivo de ventas
SELECT s.store_id, s.name, s.sales
FROM stores s
WHERE s.sales < (
    SELECT AVG(target_sales)
    FROM stores
);



