DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS assigned_tasks;
DROP TABLE IF EXISTS onboarding_processes;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS onboarding_plans;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'Hiring Manager', 'New Hire')),
    manager_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE,
    file_type TEXT,
    uploaded_by_user_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE onboarding_plans (
    plan_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    created_by_user_id INTEGER,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (company_id, title),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    due_days_after_start INTEGER NOT NULL,
    order_in_plan INTEGER NOT NULL,
    document_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES onboarding_plans(plan_id) ON DELETE CASCADE,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE SET NULL
);

CREATE TABLE onboarding_processes (
    process_id INTEGER PRIMARY KEY,
    new_hire_user_id INTEGER NOT NULL UNIQUE,
    plan_id INTEGER NOT NULL,
    hiring_manager_user_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Not Started' CHECK(status IN ('Not Started', 'In Progress', 'Completed')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (new_hire_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES onboarding_plans(plan_id) ON DELETE RESTRICT,
    FOREIGN KEY (hiring_manager_user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

CREATE TABLE assigned_tasks (
    assigned_task_id INTEGER PRIMARY KEY,
    process_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Completed')),
    due_date TEXT NOT NULL,
    completed_at TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (process_id, task_id),
    FOREIGN KEY (process_id) REFERENCES onboarding_processes(process_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE RESTRICT
);

CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    content TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);