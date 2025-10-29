CREATE TABLE companies (
    company_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              VARCHAR(255) NOT NULL UNIQUE,
    domain_name       VARCHAR(255) UNIQUE,
    subscription_plan VARCHAR(50) NOT NULL DEFAULT 'trial',
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at        TIMESTAMPTZ
);

CREATE TABLE locations (
    location_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id    UUID NOT NULL REFERENCES companies(company_id),
    name          VARCHAR(100) NOT NULL,
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city          VARCHAR(100),
    state_province VARCHAR(100),
    postal_code   VARCHAR(20),
    country       VARCHAR(100),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ,
    UNIQUE(company_id, name)
);

CREATE TABLE departments (
    department_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id    UUID NOT NULL REFERENCES companies(company_id),
    name          VARCHAR(100) NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ,
    UNIQUE(company_id, name)
);

CREATE TABLE employment_types (
    employment_type_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id         UUID NOT NULL REFERENCES companies(company_id),
    name               VARCHAR(100) NOT NULL,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at         TIMESTAMPTZ,
    UNIQUE(company_id, name)
);

CREATE TABLE roles (
    role_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(company_id),
    name       VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(company_id, name)
);

CREATE TABLE users (
    user_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id         UUID NOT NULL REFERENCES companies(company_id),
    role_id            UUID NOT NULL REFERENCES roles(role_id),
    manager_id         UUID REFERENCES users(user_id),
    department_id      UUID REFERENCES departments(department_id),
    location_id        UUID REFERENCES locations(location_id),
    employment_type_id UUID REFERENCES employment_types(employment_type_id),
    email              VARCHAR(255) NOT NULL,
    password_hash      TEXT NOT NULL,
    first_name         VARCHAR(100) NOT NULL,
    last_name          VARCHAR(100) NOT NULL,
    job_title          VARCHAR(255),
    start_date         DATE,
    profile_picture_url TEXT,
    last_login_at      TIMESTAMPTZ,
    is_active          BOOLEAN NOT NULL DEFAULT true,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at         TIMESTAMPTZ,
    UNIQUE(company_id, email)
);

CREATE TABLE onboarding_plans (
    plan_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id       UUID NOT NULL REFERENCES companies(company_id),
    name             VARCHAR(255) NOT NULL,
    description      TEXT,
    is_template      BOOLEAN NOT NULL DEFAULT true,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ
);

CREATE TABLE task_lists (
    task_list_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id      UUID NOT NULL REFERENCES onboarding_plans(plan_id),
    name         VARCHAR(255) NOT NULL,
    description  TEXT,
    order_index  INTEGER NOT NULL DEFAULT 0,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at   TIMESTAMPTZ
);

CREATE TABLE tasks (
    task_id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_list_id                  UUID NOT NULL REFERENCES task_lists(task_list_id),
    title                         VARCHAR(255) NOT NULL,
    description                   TEXT,
    task_type                     VARCHAR(50) NOT NULL DEFAULT 'GENERAL' CHECK (task_type IN ('GENERAL', 'LEARNING', 'SURVEY', 'INTEGRATION')),
    default_due_days_after_start  INTEGER,
    order_index                   INTEGER NOT NULL DEFAULT 0,
    created_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at                    TIMESTAMPTZ
);

CREATE TABLE task_dependencies (
    task_id            UUID NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    depends_on_task_id UUID NOT NULL REFERENCES tasks(task_id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, depends_on_task_id)
);

CREATE TABLE onboarding_journeys (
    journey_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    new_hire_user_id UUID NOT NULL REFERENCES users(user_id),
    plan_id          UUID NOT NULL REFERENCES onboarding_plans(plan_id),
    start_date       DATE NOT NULL,
    status           VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED' CHECK (status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED', 'ARCHIVED')),
    completed_at     TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ
);

CREATE TABLE journey_tasks (
    journey_task_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id       UUID NOT NULL REFERENCES onboarding_journeys(journey_id),
    task_id          UUID NOT NULL REFERENCES tasks(task_id),
    assignee_user_id UUID NOT NULL REFERENCES users(user_id),
    due_date         DATE,
    status           VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'OVERDUE', 'SKIPPED')),
    completed_at     TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ
);

CREATE TABLE learning_modules (
    module_id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id                UUID NOT NULL REFERENCES companies(company_id),
    title                     VARCHAR(255) NOT NULL,
    description               TEXT,
    content_type              VARCHAR(50) NOT NULL CHECK (content_type IN ('VIDEO', 'ARTICLE', 'QUIZ', 'DOCUMENT')),
    content_url               TEXT,
    estimated_duration_minutes INTEGER,
    created_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at                TIMESTAMPTZ
);

CREATE TABLE learning_pathways (
    pathway_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id  UUID NOT NULL REFERENCES companies(company_id),
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ
);

CREATE TABLE pathway_modules (
    pathway_id  UUID NOT NULL REFERENCES learning_pathways(pathway_id) ON DELETE CASCADE,
    module_id   UUID NOT NULL REFERENCES learning_modules(module_id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (pathway_id, module_id)
);

CREATE TABLE journey_pathway_assignments (
    journey_id UUID NOT NULL REFERENCES onboarding_journeys(journey_id),
    pathway_id UUID NOT NULL REFERENCES learning_pathways(pathway_id),
    PRIMARY KEY (journey_id, pathway_id)
);

CREATE TABLE user_module_progress (
    progress_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID NOT NULL REFERENCES users(user_id),
    module_id    UUID NOT NULL REFERENCES learning_modules(module_id),
    journey_id   UUID REFERENCES onboarding_journeys(journey_id),
    status       VARCHAR(50) NOT NULL DEFAULT 'NOT_STARTED' CHECK (status IN ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETED')),
    started_at   TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, module_id, journey_id)
);

CREATE TABLE buddy_assignments (
    assignment_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id       UUID NOT NULL UNIQUE REFERENCES onboarding_journeys(journey_id),
    new_hire_user_id UUID NOT NULL REFERENCES users(user_id),
    buddy_user_id    UUID NOT NULL REFERENCES users(user_id),
    start_date       DATE NOT NULL,
    end_date         DATE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at       TIMESTAMPTZ,
    CHECK (new_hire_user_id <> buddy_user_id)
);

CREATE TABLE shout_outs (
    shout_out_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id     UUID NOT NULL REFERENCES companies(company_id),
    sender_user_id UUID NOT NULL REFERENCES users(user_id),
    receiver_user_id UUID NOT NULL REFERENCES users(user_id),
    message        TEXT NOT NULL,
    is_public      BOOLEAN NOT NULL DEFAULT true,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at     TIMESTAMPTZ,
    CHECK (sender_user_id <> receiver_user_id)
);

CREATE TABLE survey_templates (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id  UUID NOT NULL REFERENCES companies(company_id),
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ
);

CREATE TABLE survey_questions (
    question_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id   UUID NOT NULL REFERENCES survey_templates(template_id),
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL CHECK (question_type IN ('NPS', 'TEXT', 'MULTIPLE_CHOICE_SINGLE', 'MULTIPLE_CHOICE_MULTI', 'RATING_SCALE')),
    options       JSONB,
    is_required   BOOLEAN NOT NULL DEFAULT true,
    order_index   INTEGER NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ
);

CREATE TABLE survey_instances (
    instance_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id  UUID NOT NULL REFERENCES survey_templates(template_id),
    journey_id   UUID REFERENCES onboarding_journeys(journey_id),
    user_id      UUID NOT NULL REFERENCES users(user_id),
    status       VARCHAR(50) NOT NULL DEFAULT 'SENT' CHECK (status IN ('SENT', 'IN_PROGRESS', 'COMPLETED')),
    sent_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at   TIMESTAMPTZ
);

CREATE TABLE survey_responses (
    response_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_id   UUID NOT NULL REFERENCES survey_instances(instance_id),
    question_id   UUID NOT NULL REFERENCES survey_questions(question_id),
    user_id       UUID NOT NULL REFERENCES users(user_id),
    response_value TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(instance_id, question_id, user_id)
);

CREATE TABLE integrations (
    integration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR(100) NOT NULL UNIQUE,
    description    TEXT
);

CREATE TABLE company_integrations (
    company_integration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id             UUID NOT NULL REFERENCES companies(company_id),
    integration_id         UUID NOT NULL REFERENCES integrations(integration_id),
    is_active              BOOLEAN NOT NULL DEFAULT false,
    config_details         JSONB,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(company_id, integration_id)
);

CREATE TABLE task_external_references (
    reference_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_task_id        UUID NOT NULL REFERENCES journey_tasks(journey_task_id),
    company_integration_id UUID NOT NULL REFERENCES company_integrations(company_integration_id),
    external_id            VARCHAR(255) NOT NULL,
    external_url           TEXT,
    metadata               JSONB,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(journey_task_id, company_integration_id)
);

CREATE INDEX idx_locations_company_id ON locations(company_id);
CREATE INDEX idx_departments_company_id ON departments(company_id);
CREATE INDEX idx_employment_types_company_id ON employment_types(company_id);
CREATE INDEX idx_roles_company_id ON roles(company_id);
CREATE INDEX idx_users_company_id ON users(company_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_manager_id ON users(manager_id);
CREATE INDEX idx_onboarding_plans_company_id ON onboarding_plans(company_id);
CREATE INDEX idx_task_lists_plan_id ON task_lists(plan_id);
CREATE INDEX idx_tasks_task_list_id ON tasks(task_list_id);
CREATE INDEX idx_onboarding_journeys_new_hire_user_id ON onboarding_journeys(new_hire_user_id);
CREATE INDEX idx_onboarding_journeys_plan_id ON onboarding_journeys(plan_id);
CREATE INDEX idx_journey_tasks_journey_id ON journey_tasks(journey_id);
CREATE INDEX idx_journey_tasks_task_id ON journey_tasks(task_id);
CREATE INDEX idx_journey_tasks_assignee_user_id ON journey_tasks(assignee_user_id);
CREATE INDEX idx_journey_tasks_status ON journey_tasks(status);
CREATE INDEX idx_learning_modules_company_id ON learning_modules(company_id);
CREATE INDEX idx_learning_pathways_company_id ON learning_pathways(company_id);
CREATE INDEX idx_user_module_progress_user_id ON user_module_progress(user_id);
CREATE INDEX idx_user_module_progress_module_id ON user_module_progress(module_id);
CREATE INDEX idx_buddy_assignments_new_hire_user_id ON buddy_assignments(new_hire_user_id);
CREATE INDEX idx_buddy_assignments_buddy_user_id ON buddy_assignments(buddy_user_id);
CREATE INDEX idx_shout_outs_company_id ON shout_outs(company_id);
CREATE INDEX idx_shout_outs_sender_user_id ON shout_outs(sender_user_id);
CREATE INDEX idx_shout_outs_receiver_user_id ON shout_outs(receiver_user_id);
CREATE INDEX idx_survey_templates_company_id ON survey_templates(company_id);
CREATE INDEX idx_survey_questions_template_id ON survey_questions(template_id);
CREATE INDEX idx_survey_instances_template_id ON survey_instances(template_id);
CREATE INDEX idx_survey_instances_journey_id ON survey_instances(journey_id);
CREATE INDEX idx_survey_instances_user_id ON survey_instances(user_id);
CREATE INDEX idx_survey_responses_instance_id ON survey_responses(instance_id);
CREATE INDEX idx_survey_responses_question_id ON survey_responses(question_id);
CREATE INDEX idx_company_integrations_company_id ON company_integrations(company_id);
CREATE INDEX idx_task_external_references_journey_task_id ON task_external_references(journey_task_id);