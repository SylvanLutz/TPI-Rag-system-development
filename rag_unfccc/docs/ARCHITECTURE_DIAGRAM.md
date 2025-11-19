# System Architecture Diagrams

## 1. Current State: Refactored System Architecture

This diagram shows the **current implementation** with the new modular architecture we've built:

```mermaid
graph TB
    subgraph "Data Ingestion"
        A[Document Sources] --> B[Scraper<br/>UNFCCC]
        B --> C[Document Storage<br/>PostgreSQL]
        C --> D[Metadata Extraction<br/>document_type, dates, URLs]
    end
    
    subgraph "Entity Management System"
        E[Entity JSON Files<br/>countries.json<br/>companies.json<br/>banks.json] --> F[EntityManager]
        F --> G[Entity Filtering<br/>by type, sector, geography]
    end
    
    subgraph "Document Processing"
        C --> H[Chunking<br/>2_chunk.py]
        H --> I[Embedding Generation<br/>3_embed.py]
        I --> J[(PostgreSQL + pgvector<br/>Chunks + Embeddings)]
    end
    
    subgraph "Prompt System"
        K[TPI Centre ID<br/>e.g., EP4a, EP4ai] --> L[TPI Centre Mapping<br/>tpi_centres.py]
        L --> M[Prompt Registry<br/>questions/prompts/]
        M --> N{Project?}
        N -->|ASCOR| O[ASCOR Prompts<br/>projects/ascor/]
        N -->|Banking| P[Banking Prompts<br/>projects/banking/]
        N -->|Shared| Q[Shared Prompts<br/>prompts/shared/]
        O --> R[Prompt Metadata<br/>entity_types, document_types<br/>top_k, keywords]
        P --> R
        Q --> R
    end
    
    subgraph "Batch Processing"
        S[Batch Process<br/>batch_process.py] --> T[Entity Loop<br/>Filtered by type]
        T --> U[Retrieval<br/>4_retrieve.py<br/>Top K chunks]
        U --> V[LLM Response<br/>5_llm_response.py]
        V --> W[Response Processing<br/>with citations]
    end
    
    subgraph "Output Generation"
        W --> X[CSV/Excel Export<br/>6_output.py]
        X --> Y[Organized Structure<br/>outputs/csv/{entity_type}/{TPI_ID}/{date}/]
        Y --> Z[Source Citations<br/>Chunk metadata, pages, URLs]
    end
    
    G --> T
    R --> V
    J --> U
    D --> J
    
    style E fill:#E3F2FD
    style F fill:#E3F2FD
    style M fill:#FFF9C4
    style R fill:#FFF9C4
    style S fill:#FFCCBC
    style J fill:#C8E6C9
    style Y fill:#C8E6C9
```

**Key Features:**
- ✅ Centralized entity management (JSON-based)
- ✅ Project-based prompt organization
- ✅ TPI Centre ID mapping system
- ✅ Batch processing with metadata filtering
- ✅ Structured CSV/Excel outputs with citations
- ✅ No PDF/email generation (removed legacy components)

---

## 2. Future State: Ideal TPI Centre RAG System

This diagram shows the **target architecture** for MVP (January 2026) and end-state vision:

```mermaid
graph TB
    subgraph "Multi-Source Data Ingestion"
        A1[UNFCCC Scraper<br/>Automated] --> B1[Unified Ingestion Pipeline]
        A2[TPI Document Repos<br/>ASCOR, Banking] --> B1
        A3[Manual Upload<br/>UI Interface] --> B1
        A4[Targeted Scrapers<br/>CPR, Other Sources] --> B1
        A5[Webhooks<br/>Real-time Updates] --> B1
        B1 --> C1[Metadata Tagging<br/>Consistent IDs<br/>Project mapping]
        C1 --> D1[Noise Filtering<br/>Quality Control]
    end
    
    subgraph "Unified Processing Pipeline"
        D1 --> E1[Layout-Aware Parsing<br/>Docling Integration<br/>Multilingual + Tables]
        E1 --> F1[Semantic Chunking<br/>Current DSI Codebase]
        F1 --> G1[Embedding Generation<br/>Baseline: Unstructured I/O/BGE<br/>Advanced: Zurich Strategy]
        G1 --> H1[(PostgreSQL + pgvector<br/>Unified Storage)]
    end
    
    subgraph "Entity & Metadata Management"
        I1[Entity JSON Files<br/>Centralized] --> J1[EntityManager<br/>Cross-project]
        J1 --> K1[Metadata Filtering<br/>By project, date, type]
        L1[Document Metadata<br/>Type, source, dates] --> H1
    end
    
    subgraph "Flexible Prompt System"
        M1[TPI Centre IDs] --> N1[Prompt Registry<br/>Versioned]
        N1 --> O1[Project-Specific<br/>Prompts]
        N1 --> P1[Shared Prompts<br/>Cross-project]
        O1 --> Q1[Analyst UI<br/>Edit & Test Prompts]
        P1 --> Q1
        Q1 --> R1[Prompt Testing<br/>In Repository Context]
    end
    
    subgraph "Advanced Retrieval & Analysis"
        H1 --> S1[Multi-Hop Retrieval<br/>Evidence Chains]
        H1 --> T1[Reranked Embeddings<br/>Precision Optimization]
        S1 --> U1[Contextual Retrieval]
        T1 --> U1
    end
    
    subgraph "Analyst Feedback Loop"
        U1 --> V1[LLM Response<br/>with Citations]
        V1 --> W1[Analyst Review]
        W1 --> X1[Chunk Curation<br/>Mark relevant/irrelevant]
        X1 --> Y1[Model Improvement<br/>Feedback Integration]
        Y1 --> H1
    end
    
    subgraph "Output & Interface"
        V1 --> Z1[Scorecard Generation<br/>Excel/CSV]
        Z1 --> AA1[Auditable Outputs<br/>Result + Source + Quote]
        W1 --> AB1[Interactive Querying<br/>Live Document Sets]
        AB1 --> AC1[Traceable Reasoning<br/>Model Explanations]
    end
    
    subgraph "Testing & Validation"
        AA1 --> AD1[Back-Testing Framework<br/>vs Analyst Outputs]
        AD1 --> AE1[Metrics: Recall, Precision<br/>Agreement Rates]
        AE1 --> AF1[Performance Dashboard]
    end
    
    K1 --> S1
    R1 --> V1
    
    style B1 fill:#E3F2FD
    style E1 fill:#FFF9C4
    style H1 fill:#C8E6C9
    style Q1 fill:#FFCCBC
    style Y1 fill:#E1BEE7
    style AA1 fill:#C8E6C9
    style AD1 fill:#FFF9C4
```

**Key Capabilities:**
- 🔄 Multi-source ingestion (UNFCCC, repos, manual, webhooks)
- 📄 Layout-aware parsing (multilingual, tables)
- 🎯 Flexible prompt editing via UI
- 🔍 Multi-hop retrieval with evidence chains
- 💬 Analyst feedback loop for continuous improvement
- 📊 Interactive querying and traceable reasoning
- ✅ Back-testing and validation framework

---

## 3. Current vs Future: Key Differences

```mermaid
graph LR
    subgraph "Current State ✅"
        A1[Single Source<br/>UNFCCC Only] --> B1[Basic Chunking]
        B1 --> C1[Fixed Prompts<br/>Code-based]
        C1 --> D1[Static Outputs<br/>CSV/Excel]
        D1 --> E1[No Feedback Loop]
    end
    
    subgraph "Future State 🎯"
        A2[Multiple Sources<br/>UNFCCC, Repos, Manual, Webhooks] --> B2[Layout-Aware<br/>Multilingual Parsing]
        B2 --> C2[Flexible Prompts<br/>UI-Based Editing]
        C2 --> D2[Interactive Outputs<br/>+ Feedback Loop]
        D2 --> E2[Model Improvement]
        E2 --> B2
    end
    
    style A1 fill:#FFE0B2
    style A2 fill:#C8E6C9
    style C1 fill:#FFE0B2
    style C2 fill:#C8E6C9
    style D1 fill:#FFE0B2
    style D2 fill:#C8E6C9
    style E1 fill:#FFE0B2
    style E2 fill:#E1BEE7
```

---

## 4. Analyst Workflow Comparison

### Current Workflow (CLI-Based)
```mermaid
sequenceDiagram
    participant Analyst
    participant CLI
    participant System
    participant Output
    
    Analyst->>CLI: Run batch_process.py<br/>with TPI Centre ID
    CLI->>System: Process entities
    System->>System: Retrieve chunks
    System->>System: Generate LLM responses
    System->>Output: Generate CSV/Excel
    Output->>Analyst: Static file
    Note over Analyst: Manual review<br/>No feedback loop
```

### Future Workflow (UI-Based with Feedback)
```mermaid
sequenceDiagram
    participant Analyst
    participant UI
    participant System
    participant Feedback
    
    Analyst->>UI: Select project & TPI ID
    Analyst->>UI: Edit/Test prompt
    UI->>System: Process with prompt
    System->>System: Multi-hop retrieval
    System->>UI: Show results + sources
    Analyst->>UI: Review & curate chunks
    Analyst->>UI: Mark relevant/irrelevant
    UI->>Feedback: Store feedback
    Feedback->>System: Improve future retrieval
    System->>UI: Updated results
    UI->>Analyst: Interactive scorecard
```

---

## 5. Detailed Component Diagrams

### Prompt System Architecture

```mermaid
graph LR
    A[TPI Centre ID<br/>e.g., EP4a] --> B[TPI Centre Mapping]
    B --> C[Prompt Registry]
    C --> D{Project?}
    D -->|ASCOR| E[ASCOR Prompts]
    D -->|Banking| F[Banking Prompts]
    D -->|Shared| G[Shared Prompts]
    
    E --> H[Prompt Definition]
    F --> H
    G --> H
    
    H --> I[Metadata]
    I --> J[Entity Types]
    I --> K[Document Types]
    I --> L[Top K]
    I --> M[Keywords]
    
    style A fill:#E3F2FD
    style H fill:#FFF9C4
    style I fill:#C8E6C9
```

### Entity Management Flow

```mermaid
graph TD
    A[JSON Entity Files] --> B[EntityManager]
    B --> C{Entity Type?}
    C -->|countries| D[Countries List]
    C -->|companies| E[Companies List]
    C -->|banks| F[Banks List]
    
    D --> G[Filter by Metadata]
    E --> G
    F --> G
    
    G --> H{Filter Criteria}
    H -->|By Sector| I[Sector Filter]
    H -->|By Geography| J[Geography Filter]
    H -->|By Document Type| K[Document Type Filter]
    
    I --> L[Filtered Entities]
    J --> L
    K --> L
    
    L --> M[Batch Processing]
    
    style A fill:#E3F2FD
    style B fill:#FFF9C4
    style L fill:#C8E6C9
```

### Batch Processing Workflow

```mermaid
sequenceDiagram
    participant User
    participant BatchProcess
    participant EntityManager
    participant PromptSystem
    participant Retrieval
    participant LLM
    participant Output
    
    User->>BatchProcess: Run with TPI Centre ID
    BatchProcess->>PromptSystem: Get prompt for TPI ID
    BatchProcess->>EntityManager: Get entities by type
    loop For each entity
        BatchProcess->>Retrieval: Get top K chunks
        Retrieval-->>BatchProcess: Chunks with metadata
        BatchProcess->>LLM: Generate response
        LLM-->>BatchProcess: Response with citations
        BatchProcess->>BatchProcess: Process response
    end
    BatchProcess->>Output: Aggregate results
    Output->>User: CSV/Excel file
```

---

## 6. MVP Roadmap (January 2026)

### Phase 1: Enhanced Ingestion
- ✅ Multi-source support (repos, manual upload)
- ✅ Metadata tagging system
- ✅ Noise filtering

### Phase 2: Advanced Processing
- 🔄 Layout-aware parsing (Docling)
- 🔄 Multilingual support
- 🔄 Table recognition

### Phase 3: Flexible Prompts
- 🔄 UI for prompt editing
- 🔄 Prompt testing interface
- 🔄 Version control

### Phase 4: Feedback Loop
- 🔄 Chunk curation interface
- 🔄 Model improvement integration
- 🔄 Performance tracking

---

## 7. End-State Vision (2026+)

### Advanced Features
- **Automated Source Collection**: Scalable web crawler with noise filtering
- **Enhanced Processing**: Full layout-aware, multilingual parsing
- **Contextual Retrieval**: Multi-hop and reranked embeddings
- **Analyst Feedback Loop**: Curate chunks, improve model performance
- **Interactive Workflows**: Live querying with traceable reasoning
- **Scalable Architecture**: PostgreSQL metadata, API endpoints
- **Governance & Transparency**: Versioned documentation, optional open-source

---

**Last Updated**: November 18, 2025  
**Status**: Current state implemented, future state planned for MVP (January 2026)
