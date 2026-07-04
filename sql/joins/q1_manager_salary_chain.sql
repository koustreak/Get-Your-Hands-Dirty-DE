-- ============================================================
-- QUESTION 1: The Salary Chain (Multi-Level Self JOIN)
-- Difficulty: Advanced | Google / MS DE Level
-- ============================================================
--
-- PROBLEM:
-- Find all employees who earn MORE than their direct manager,
-- AND whose manager also earns more than the manager's manager (grandparent).
--
-- Return: employee_name, employee_salary, manager_name, manager_salary,
--         grand_manager_name, grand_manager_salary
--
-- Order by employee_salary DESC.
--
-- Note: Employees with no manager are the top-level executives.
--       Employees whose manager is a top-level executive should be excluded
--       (as there is no grandparent to compare against).
-- ============================================================

DROP table if exists employees;

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    salary INT,
    manager_id INT -- NULL means top-level
);

INSERT INTO
    employees
VALUES (1, 'Alice', 250000, NULL),
    (2, 'Bob', 180000, 1),
    (3, 'Carol', 160000, 1),
    (4, 'Dave', 110000, 2),
    (5, 'Eve', 195000, 2), -- earns more than Bob (180k)
    (6, 'Frank', 140000, 3),
    (7, 'Grace', 170000, 3), -- earns more than Carol (160k)
    (8, 'Heidi', 90000, 4),
    (9, 'Ivan', 125000, 5), -- earns more than Eve (195k)? No.
    (10, 'Judy', 210000, 5), -- earns more than Eve (195k). Eve earns less than Bob. Interesting chain.
    (11, 'Karl', 80000, 6),
    (12, 'Laura', 175000, 7), -- earns more than Grace (170k). Grace earns more than Carol (160k).
    (13, 'Mallory', 155000, 7),
    (14, 'Niaj', 100000, 8),
    (15, 'Oscar', 115000, 9),
    (16, 'Peggy', 130000, 10),
    (17, 'Quinn', 95000, 11),
    (18, 'Romeo', 185000, 12), -- earns more than Laura (175k). Laura > Grace > Carol. Full 3-level chain!
    (19, 'Sybil', 160000, 12),
    (20, 'Trent', 70000, 13);

SELECT
    e.emp_name AS employee,
    m2.emp_name AS manager,
    m3.emp_name AS grand_manager,
    e.salary emp_salary,
    m2.salary manager_salary,
    m3.salary grand_manager_salary
FROM
    employees e
    INNER JOIN employees m2 ON e.manager_id = m2.emp_id
    AND e.salary > m2.salary -- Filter 1 in the ON
    INNER JOIN employees m3 ON m2.manager_id = m3.emp_id
    AND m2.salary > m3.salary;

-- YOUR QUERY HERE: