# SQL Learning Path: Basics to Intermediate

Work through each section in order. Each section builds on the previous one.

---

## STAGE 1 — Understanding Databases

Before writing any SQL, understand what you are working with:
- A **database** is a collection of organized data.
- A **table** is like a spreadsheet — rows and columns.
- A **row** (record) is one entry. A **column** (field) is a category of data.
- SQL (Structured Query Language) is the language used to talk to a database.

---

## STAGE 2 — Setting Up: DDL (Data Definition Language)

These commands define the *structure* of your data.

### 1. CREATE DATABASE
Create a new database.
```sql
CREATE DATABASE school;
```

### 2. USE
Select which database to work in (MySQL/MariaDB).
```sql
USE school;
```

### 3. CREATE TABLE
Define a table and its columns with data types.
```sql
CREATE TABLE students (
    id      INTEGER PRIMARY KEY,
    name    TEXT    NOT NULL,
    age     INTEGER,
    grade   TEXT
);
```

Common data types to know:
| Type | Meaning |
|------|---------|
| `INTEGER` | Whole numbers |
| `TEXT` / `VARCHAR(n)` | Text strings |
| `REAL` / `FLOAT` | Decimal numbers |
| `DATE` | Date values (YYYY-MM-DD) |
| `BOOLEAN` | True / False |

### 4. ALTER TABLE
Add, modify, or remove a column from an existing table.
```sql
-- Add a column
ALTER TABLE students ADD COLUMN email TEXT;

-- Remove a column
ALTER TABLE students DROP COLUMN email;
```

### 5. DROP TABLE
Delete a table and all its data permanently.
```sql
DROP TABLE students;
```

### 6. TRUNCATE TABLE
Delete all rows but keep the table structure.
```sql
TRUNCATE TABLE students;
```

---

## STAGE 3 — Adding Data: DML (Data Manipulation Language)

### 7. INSERT INTO
Add new rows to a table.
```sql
-- Insert one row
INSERT INTO students (id, name, age, grade)
VALUES (1, 'Alice', 20, 'A');

-- Insert multiple rows at once
INSERT INTO students (id, name, age, grade)
VALUES
    (2, 'Bob',   22, 'B'),
    (3, 'Carol', 21, 'A'),
    (4, 'David', 23, 'C');
```

---

## STAGE 4 — Reading Data: SELECT (The Most Important Command)

### 8. SELECT — Read All Columns
```sql
SELECT * FROM students;
```

### 9. SELECT — Read Specific Columns
```sql
SELECT name, grade FROM students;
```

### 10. SELECT with WHERE — Filter Rows
```sql
SELECT * FROM students WHERE grade = 'A';
SELECT * FROM students WHERE age > 21;
```

### 11. Comparison Operators in WHERE
```sql
=       -- equal
!=  <>  -- not equal
>   <   -- greater / less than
>=  <=  -- greater or equal / less or equal
```

### 12. AND / OR / NOT — Combine Conditions
```sql
SELECT * FROM students WHERE age > 20 AND grade = 'A';
SELECT * FROM students WHERE grade = 'A' OR grade = 'B';
SELECT * FROM students WHERE NOT grade = 'C';
```

### 13. ORDER BY — Sort Results
```sql
SELECT * FROM students ORDER BY name ASC;   -- A to Z
SELECT * FROM students ORDER BY age DESC;   -- oldest first
```

### 14. LIMIT — Restrict Number of Results
```sql
SELECT * FROM students LIMIT 2;            -- first 2 rows
SELECT * FROM students LIMIT 2 OFFSET 1;  -- skip 1, then get 2
```

### 15. DISTINCT — Remove Duplicates
```sql
SELECT DISTINCT grade FROM students;
```

---

## STAGE 5 — Updating and Deleting Data

### 16. UPDATE — Modify Existing Rows
Always use WHERE or you will update every row.
```sql
UPDATE students SET grade = 'B' WHERE id = 1;
UPDATE students SET age = 24, grade = 'A' WHERE name = 'David';
```

### 17. DELETE — Remove Rows
Always use WHERE or you will delete every row.
```sql
DELETE FROM students WHERE id = 4;
```

---

## STAGE 6 — Filtering with Pattern Matching and Lists

### 18. LIKE — Pattern Matching
```sql
SELECT * FROM students WHERE name LIKE 'A%';   -- starts with A
SELECT * FROM students WHERE name LIKE '%ol%'; -- contains "ol"
SELECT * FROM students WHERE name LIKE '_ob';  -- any char then "ob"
```
`%` matches any number of characters. `_` matches exactly one character.

### 19. IN — Match Against a List
```sql
SELECT * FROM students WHERE grade IN ('A', 'B');
SELECT * FROM students WHERE id IN (1, 3);
```

### 20. BETWEEN — Range Check (inclusive)
```sql
SELECT * FROM students WHERE age BETWEEN 20 AND 22;
```

### 21. IS NULL / IS NOT NULL — Check for Missing Values
```sql
SELECT * FROM students WHERE grade IS NULL;
SELECT * FROM students WHERE grade IS NOT NULL;
```

---

## STAGE 7 — Aggregate Functions

These collapse many rows into a single summary value.

### 22. COUNT
```sql
SELECT COUNT(*) FROM students;              -- total rows
SELECT COUNT(grade) FROM students;          -- rows where grade is not NULL
```

### 23. SUM, AVG, MIN, MAX
```sql
SELECT SUM(age) FROM students;
SELECT AVG(age) FROM students;
SELECT MIN(age) FROM students;
SELECT MAX(age) FROM students;
```

### 24. GROUP BY — Aggregate per Category
```sql
SELECT grade, COUNT(*) FROM students GROUP BY grade;
SELECT grade, AVG(age) FROM students GROUP BY grade;
```

### 25. HAVING — Filter After GROUP BY
WHERE filters rows before grouping; HAVING filters groups after aggregation.
```sql
SELECT grade, COUNT(*) AS total
FROM students
GROUP BY grade
HAVING COUNT(*) > 1;
```

---

## STAGE 8 — Aliases

### 26. AS — Rename Columns or Tables in Output
```sql
SELECT name AS student_name, age AS student_age FROM students;
SELECT COUNT(*) AS total_students FROM students;
```

---

## STAGE 9 — Working with Multiple Tables

### 27. FOREIGN KEY — Linking Tables
```sql
CREATE TABLE courses (
    id         INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    course     TEXT,
    score      INTEGER
);

INSERT INTO courses (id, student_id, course, score)
VALUES
    (1, 1, 'Math',    95),
    (2, 1, 'Science', 88),
    (3, 2, 'Math',    72),
    (4, 3, 'Science', 91);
```

### 28. INNER JOIN — Rows That Match in Both Tables
```sql
SELECT students.name, courses.course, courses.score
FROM students
INNER JOIN courses ON students.id = courses.student_id;
```

### 29. LEFT JOIN — All Rows from Left Table, Matching Rows from Right
```sql
SELECT students.name, courses.course
FROM students
LEFT JOIN courses ON students.id = courses.student_id;
-- Students with no courses will appear with NULL in course column
```

### 30. RIGHT JOIN — All Rows from Right Table (not supported in SQLite)
```sql
SELECT students.name, courses.course
FROM students
RIGHT JOIN courses ON students.id = courses.student_id;
```

### 31. Table Aliases in JOINs (cleaner syntax)
```sql
SELECT s.name, c.course, c.score
FROM students AS s
INNER JOIN courses AS c ON s.id = c.student_id;
```

---

## STAGE 10 — Subqueries

A query nested inside another query.

### 32. Subquery in WHERE
```sql
-- Students who are enrolled in at least one course
SELECT name FROM students
WHERE id IN (SELECT student_id FROM courses);
```

### 33. Subquery in FROM (Derived Table)
```sql
SELECT grade, avg_age
FROM (
    SELECT grade, AVG(age) AS avg_age
    FROM students
    GROUP BY grade
) AS summary;
```

---

## STAGE 11 — String and Date Functions

### 34. String Functions
```sql
SELECT UPPER(name) FROM students;          -- ALICE
SELECT LOWER(name) FROM students;          -- alice
SELECT LENGTH(name) FROM students;         -- number of characters
SELECT SUBSTR(name, 1, 3) FROM students;   -- first 3 chars
```

### 35. Date Functions (SQLite)
```sql
SELECT DATE('now');                        -- today's date
SELECT DATE('now', '-7 days');             -- 7 days ago
```

---

## STAGE 12 — Constraints

Constraints enforce rules on data at the table level.

### 36. Common Constraints
```sql
CREATE TABLE employees (
    id       INTEGER PRIMARY KEY,          -- unique, not null
    email    TEXT    UNIQUE,               -- no duplicates allowed
    name     TEXT    NOT NULL,             -- cannot be empty
    salary   REAL    DEFAULT 50000.0,      -- default value if not provided
    dept_id  INTEGER REFERENCES departments(id)  -- foreign key
);
```

---

## STAGE 13 — Transactions

Group multiple statements into one atomic operation.

### 37. BEGIN / COMMIT / ROLLBACK
```sql
BEGIN;
    UPDATE students SET grade = 'A' WHERE id = 2;
    INSERT INTO courses (id, student_id, course, score) VALUES (5, 2, 'English', 85);
COMMIT;   -- save both changes together

-- If something goes wrong:
ROLLBACK; -- undo everything back to BEGIN
```

---

## Quick Reference Cheat Sheet

| Category | Commands |
|----------|----------|
| Define structure | `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` |
| Add data | `INSERT INTO` |
| Read data | `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT` |
| Filter | `AND/OR/NOT`, `LIKE`, `IN`, `BETWEEN`, `IS NULL` |
| Modify data | `UPDATE`, `DELETE` |
| Summarize | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING` |
| Multiple tables | `INNER JOIN`, `LEFT JOIN`, `FOREIGN KEY` |
| Nested queries | Subqueries |
| Safety | `BEGIN`, `COMMIT`, `ROLLBACK` |

---

## Recommended Practice Order

1. Create a table, insert rows, select all rows.
2. Filter with WHERE using different operators.
3. Sort with ORDER BY, limit with LIMIT.
4. Update and delete specific rows.
5. Use COUNT, AVG, GROUP BY on your data.
6. Create a second table with a foreign key and practice JOINs.
7. Write a subquery to replace a JOIN, compare the two approaches.
8. Wrap multiple statements in a transaction.
