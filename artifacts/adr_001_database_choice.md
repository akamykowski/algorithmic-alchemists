# ADR-001: Vector Store for Semantic Search and Analytics

## Status

Accepted

## Context

*   **Problem:** The OnboardPro platform requires a backend to support two core features: 1) A semantic search capability allowing users to ask natural language questions against a corpus of onboarding documents, and 2) Analytics dashboards for HR administrators to track search usage and effectiveness. This solution must store vector embeddings alongside structured metadata and support complex, filtered queries.
*   **Driving Forces:** List the key factors influencing this decision.
    *   - **Rich, Filtered Queries:** Search queries must be filterable by structured metadata (e.g., department, location, hire date) in a single, atomic operation.
    *   - **Unified Analytics:** The system must support complex analytical queries that join search activity data with relational HR data for dashboarding.
    *   - **Operational Simplicity:** Minimizing new infrastructure components and cognitive overhead for the engineering team is a high priority.
    *   - **Security and Compliance:** The solution must handle sensitive PII and confidential documents with a mature, auditable security model (e.g., for SOC 2, GDPR).
*   **Constraints:** List any constraints or limitations that must be considered.
    *   - **Moderate Scale:** The initial workload is projected to be in the tens of thousands to low millions of vectors, with a clear path for future growth.
    *   - **Existing Expertise:** The team has significant operational experience with PostgreSQL.

## Decision

We will adopt PostgreSQL with the `pgvector` extension as the primary vector store for the OnboardPro platform. This single database instance will store vector embeddings, the source text, and all associated relational metadata.

**Rationale:** This decision was made because a unified data architecture is the most effective way to meet our core product requirements. The research summary highlighted that our primary need is for rich, metadata-filtered vector searches. PostgreSQL with `pgvector` excels here, allowing us to perform metadata filtering and vector similarity search within a single, efficient SQL query. This dramatically simplifies application logic compared to the alternative of a specialized vector database, which would require complex, multi-step queries and introduce data synchronization challenges between two separate systems.

Furthermore, this approach directly supports our operational goals. By leveraging our existing PostgreSQL infrastructure and expertise, we minimize operational complexity, cost, and the learning curve for the team. The full power of SQL is available for our analytics and dashboarding features, making it straightforward to generate insights by joining search logs with user and document data. Finally, using PostgreSQL's mature, battle-tested security model (including Row-Level Security) simplifies our compliance and data protection efforts for sensitive HR information. While a specialized database might offer higher performance at extreme scale, the operational simplicity and powerful querying capabilities of the PostgreSQL solution provide a superior trade-off for our current and projected needs.

## Consequences

*   **Positive Outcomes:**
    *   - **Simplified Architecture:** A single data store for relational data and vectors reduces system complexity, making development, deployment, and maintenance easier.
    *   - **Powerful, Efficient Queries:** The ability to combine metadata filters, full-text search, and vector search in one query simplifies application code and improves performance for our key use cases.
    *   - **Reduced Operational Overhead:** We leverage existing team skills and tooling for backups, monitoring, security, and scaling, avoiding the need to manage a new type of database.
*   **Negative Trade-offs:**
    *   - **Potential Resource Contention:** Transactional (OLTP) and vector search (ANN) workloads will compete for the same database resources (CPU, RAM, I/O).
    *   - **Scaling Limitations:** While sufficient for our projected needs, this solution may not match the raw query performance of a specialized vector database at a scale of hundreds of millions of vectors.
    *   - **Extension Dependency:** Our vector search functionality is dependent on the open-source `pgvector` extension's continued development and compatibility with future PostgreSQL versions.
*   **Future Work:**
    *   - **Monitoring and Tuning:** Implement detailed monitoring on database performance to detect resource contention. Develop best practices for tuning `pgvector` indexes (`HNSW`, `IVFFlat`) and PostgreSQL configurations for our specific workload.
    *   - **Workload Isolation Strategy:** Plan for the use of read replicas to offload analytical queries or vector searches if performance degradation is observed.
    *   - **Periodic Re-evaluation:** Re-assess this decision if our data scale grows beyond 50 million vectors or if query latency becomes a critical product issue.