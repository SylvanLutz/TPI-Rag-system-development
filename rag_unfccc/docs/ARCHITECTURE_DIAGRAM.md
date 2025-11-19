# System Architecture Diagrams

## 1. Current State: Refactored System Architecture

This diagram shows the **current implementation** with the new modular architecture we've built, styled similar to LobbyMap pipeline:

```mermaid
graph TB
    subgraph 1["1. Data Ingestion & Knowledge Base"]
        direction TB
        A[UNFCCC Scraper] --> B[PDF Documents]
        B --> C[(Database<br/>PostgreSQL)]
        C --> D[Metadata Extraction<br/>document_type, dates, URLs]
    end
    
    subgraph 2["2. RAG Processing Pipeline"]
        direction TB
        B --> E[Chunking<br/>2_chunk.py]
        E --> F[Embedding Generation<br/>3_embed.py]
        F --> G[Transformer/Word2Vec]
        G --> H[Store]
        H --> I[(PostgreSQL<br/>+ pgvector)]
    end
    
    subgraph 3["3. Entity & Prompt Management"]
        direction TB
        J[Entity JSON Files<br/>countries.json<br/>companies.json<br/>banks.json] --> K[EntityManager]
        K --> L[Entity Filtering<br/>Type, Sector, Geography]
        M[TPI Centre ID<br/>EP4a, EP4ai] --> N[TPI Centre Mapping<br/>tpi_centres.py]
        N --> O[Prompt Registry<br/>questions/prompts/]
        O --> P{Project?}
        P -->|ASCOR| Q[ASCOR Prompts]
        P -->|Banking| R[Banking Prompts]
        P -->|Shared| S[Shared Prompts]
        Q --> T[Prompt Metadata<br/>entity_types, document_types<br/>top_k, keywords]
        R --> T
        S --> T
    end
    
    subgraph 4["4. Batch Processing & Retrieval"]
        direction TB
        L --> U[Batch Process<br/>batch_process.py]
        U --> V[Entity Loop<br/>Filtered by type]
        V --> W[Retrieval<br/>4_retrieve.py]
        I -->|Semantic Search| W
        W --> X[Top K Chunks]
        X --> Y[LLM Response<br/>5_llm_response.py]
        T --> Y
        Y --> Z[Response Processing<br/>with Citations]
    end
    
    subgraph 5["5. Output Generation"]
        direction TB
        Z --> AA[CSV/Excel Export<br/>6_output.py]
        AA --> AB[Organized Structure<br/>outputs/csv/entity_type/TPI_ID/date/]
        AB --> AC[Source Citations<br/>Chunk metadata, pages, URLs]
    end
    
    D --> I
    
    style C fill:#FFE0B2,stroke:#F57C00,stroke-width:2px
    style I fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style K fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
    style O fill:#FFF9C4,stroke:#F57F17,stroke-width:2px
    style U fill:#FFCCBC,stroke:#D84315,stroke-width:2px
    style AB fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
```

**Key Features:**
- ✅ Centralized entity management (JSON-based)
- ✅ Project-based prompt organization
- ✅ TPI Centre ID mapping system
- ✅ Batch processing with metadata filtering
- ✅ Structured CSV/Excel outputs with citations

---

## 2. Future State: Ideal TPI Centre RAG System

This diagram shows the **target architecture** for MVP (January 2026) and end-state vision, styled similar to LobbyMap pipeline:

```mermaid
graph TB
    subgraph 1["1. Data Ingestion & Knowledge Base"]
        direction TB
        A1[UNFCCC Scraper] --> B1[Document Repos<br/>ASCOR, Banking]
        B1 --> C1[Manual Upload<br/>UI]
        C1 --> D1[Targeted Scrapers<br/>CPR, Other]
        D1 --> E1[(Database<br/>PostgreSQL)]
        A1 --> E1
        B1 --> E1
        C1 --> E1
        D1 --> E1
        E1 --> F1[PDF Documents]
        F1 --> G1[Metadata Tagging<br/>Type, Date, Source]
        G1 --> H1[Noise Filtering]
    end
    
    subgraph 2["2. RAG Processing Pipeline"]
        direction TB
        H1 --> I1[Parse]
        I1 --> J1[Docling<br/>Layout-Aware]
        J1 --> K1[Chunk]
        K1 --> L1[Layout Chunker]
        L1 --> M1[Embed]
        M1 --> N1[Nomic/Qwen<br/>Embeddings]
        N1 --> O1[Store]
        O1 --> P1[(PostgreSQL<br/>+ pgvector)]
    end
    
    subgraph 3["3. Entity & Prompt Management"]
        direction TB
        Q1[Entity JSON Files<br/>countries.json<br/>companies.json<br/>banks.json] --> R1[EntityManager]
        R1 --> S1[Metadata Filter<br/>Type, Sector, Date]
        T1[TPI Centre IDs<br/>EP4a, EP4ai] --> U1[Prompt Registry]
        U1 --> V1[Project Prompts<br/>ASCOR, Banking]
        U1 --> W1[Shared Prompts]
        V1 --> X1[Analyst UI<br/>Edit & Test]
        W1 --> X1
    end
    
    subgraph 4["4. Query & Retrieval API"]
        direction TB
        X1 --> Y1[Query Input]
        Y1 --> Z1[Prompt]
        Z1 --> AA1[Embed Query]
        AA1 --> AB1[Nomic/Qwen]
        P1 -->|Semantic Search| AC1[API]
        AC1 --> AD1[Retrieve<br/>Top K Chunks]
        AD1 --> AE1[Evidences]
        AE1 --> AF1[Sort]
        AF1 --> AG1[Reranker]
        AB1 --> AG1
        AG1 --> AH1[Ranked Evidence]
        AH1 --> AI1[LLM<br/>Response Generation]
        AI1 --> AJ1[Response<br/>with Citations]
    end
    
    subgraph 5["5. Analyst Review & Feedback"]
        direction TB
        AJ1 --> AK1[Analyst Review<br/>UI]
        AK1 --> AL1[Chunk Curation<br/>Mark Relevant/Irrelevant]
        AL1 --> AM1[Feedback Store]
        AM1 -->|Improve Retrieval| P1
        AK1 --> AN1[Validate Results]
        AN1 --> AO1[Scorecard<br/>Excel/CSV]
    end
    
    subgraph 6["6. Evaluation & Tracing"]
        direction TB
        AJ1 -->|Store| AP1[(MongoDB<br/>or PostgreSQL)]
        Y1 -->|Artifacts| AP1
        AP1 -->|If Annotated| AQ1[Annotation<br/>Stance, Rank, Evidence]
        AP1 -->|If Annotated| AR1[Metrics<br/>Recall, Precision, Agreement]
        AQ1 --> AR1
    end
    
    S1 --> AC1
    P1 --> AC1
    
    style E1 fill:#FFE0B2,stroke:#F57C00,stroke-width:2px
    style P1 fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style X1 fill:#FFCCBC,stroke:#D84315,stroke-width:2px
    style AK1 fill:#FFF9C4,stroke:#F57F17,stroke-width:3px
    style AM1 fill:#E1BEE7,stroke:#7B1FA2,stroke-width:2px
    style AP1 fill:#E3F2FD,stroke:#1976D2,stroke-width:2px
```

**Key Capabilities:**
- 🔄 Multi-source ingestion (UNFCCC, repos, manual, webhooks)
- 📄 Layout-aware parsing (multilingual, tables)
- 🎯 Flexible prompt editing via UI
- 🔍 Multi-hop retrieval with evidence chains
- 💬 Analyst feedback loop for continuous improvement
- 📊 Interactive querying and traceable reasoning
- ✅ Back-testing and validation framework
- 🧠 Advanced embeddings: Nomic (robust across configs) / Qwen (recall, high chunk dilution, multilingual)

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
    System->>System: Check feedback scores<br/>(direct + semantic transfer)
    System->>UI: Show results + sources<br/>with relevance indicators
    Analyst->>UI: Review & curate chunks
    Analyst->>UI: Mark relevant/irrelevant<br/>(one-click feedback)
    UI->>Feedback: Store feedback<br/>(chunk_id, prompt_id, entity)
    Feedback->>System: Update retrieval weights<br/>(boost relevant, demote irrelevant)
    System->>UI: Re-ranked results<br/>(immediate improvement)
    UI->>Analyst: Interactive scorecard<br/>with traceable sources
```

**Key Technical Details:**
- **Feedback Storage**: Simple database table with `(chunk_id, prompt_id, entity)` uniqueness constraint
- **Semantic Generalization**: Uses existing embeddings to find similar chunks and transfer feedback (see `FEEDBACK_GENERALIZATION_DESIGN.md`)
- **Re-ranking Logic**: Adjusts similarity scores by ±20% based on feedback (conservative, reversible)
- **Real-time Updates**: Feedback applied immediately to next retrieval (no model retraining required)
- **Implementation Complexity**: Low-Medium (Phase 1+2 from `FEEDBACK_LOOP_FEASIBILITY.md` = 3-6 weeks)

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

---

## 8. Pitch-Ready Diagrams: Strategic Vision

### Current State: Analyst-Centered RAG System

**For project pitch documents and strategic presentations:**

```mermaid
graph TB
    subgraph "Document Sources"
        A[Climate Policy Documents<br/>NDCs, Reports, Policies]
    end
    
    subgraph "Automated Processing"
        A --> B[Document Ingestion]
        B --> C[Intelligent Chunking]
        C --> D[Semantic Search Index]
    end
    
    subgraph "Analyst-Centered Workflow"
        E[Analyst Query<br/>TPI Research Question] --> D
        D --> F[Relevant Evidence<br/>with Source Citations]
        F --> G[Analyst Review<br/>& Validation]
        G --> H[Assessment Output<br/>Excel/CSV Reports]
    end
    
    subgraph "Key Principles"
        I[Analyst at Center<br/>AI Augments Research]
        J[TPI Independence<br/>Data Sovereignty]
        K[Transparent Methodology<br/>Reproducible Results]
    end
    
    G -.->|Informs| I
    H -.->|Supports| J
    F -.->|Enables| K
    
    style E fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    style G fill:#FFF9C4,stroke:#F57F17,stroke-width:3px
    style I fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style J fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style K fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
```

**Value Proposition:**
- ⚡ **Speed**: Rapid document-to-results pipeline
- 🎯 **Quality**: Analyst validation ensures accuracy
- 📊 **Scalability**: Process multiple entities and document types
- 🔍 **Transparency**: Full source citations for verification
- 🏛️ **Independence**: TPI-controlled infrastructure

---

### Future State: Scalable Multi-Project Platform

**For strategic vision and roadmap presentations:**

```mermaid
graph TB
    subgraph "Multi-Source Document Collection"
        A1[Automated Scrapers<br/>UNFCCC, Repositories]
        A2[Manual Upload<br/>Analyst-Controlled]
        A3[Targeted Sources<br/>CPR, Other Platforms]
        A1 --> B1[Unified Ingestion]
        A2 --> B1
        A3 --> B1
    end
    
    subgraph "Intelligent Processing"
        B1 --> C1[Advanced Parsing<br/>Multilingual, Tables]
        C1 --> D1[Semantic Understanding<br/>Nomic/Qwen Embeddings]
        D1 --> E1[Knowledge Base<br/>TPI-Controlled Storage]
    end
    
    subgraph "Analyst-Driven Analysis"
        F1[Analyst Queries<br/>TPI Research Questions] --> E1
        E1 --> G1[Evidence Retrieval<br/>with Confidence Scores]
        G1 --> H1[Analyst Review<br/>Curate & Validate]
        H1 --> I1[Feedback Loop<br/>Continuous Improvement]
        I1 --> E1
    end
    
    subgraph "Multi-Project Support"
        H1 --> J1[ASCOR<br/>Sovereign Assessments]
        H1 --> K1[Banking<br/>Financial Sector]
        H1 --> L1[Corporate<br/>Company Analysis]
    end
    
    subgraph "Output & Impact"
        J1 --> M1[Standardized Reports<br/>Excel/CSV]
        K1 --> M1
        L1 --> M1
        M1 --> N1[Faster Assessments<br/>Time to Results]
        M1 --> O1[Analyst Time Freed<br/>Methodology Innovation]
    end
    
    style F1 fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    style H1 fill:#FFF9C4,stroke:#F57F17,stroke-width:3px
    style I1 fill:#E1BEE7,stroke:#7B1FA2,stroke-width:2px
    style E1 fill:#C8E6C9,stroke:#388E3C,stroke-width:2px
    style N1 fill:#FFCCBC,stroke:#D84315,stroke-width:2px
    style O1 fill:#FFCCBC,stroke:#D84315,stroke-width:2px
```

**Strategic Vision:**
- 🌍 **Multi-Entity Support**: Corporates, Banks, Sovereigns
- 🔄 **Continuous Learning**: Analyst feedback improves system
- 🎯 **Project Scalability**: Single platform, multiple TPI projects
- ⚡ **Speed & Quality**: Faster assessments, analyst-validated
- 🏛️ **TPI Sovereignty**: Independent, controlled infrastructure
- 📚 **Methodology Focus**: Frees analysts for research innovation

---

### Key Differentiators

```mermaid
graph LR
    A[TPI RAG System] --> B[Analyst-Centered]
    A --> C[TPI-Controlled]
    A --> D[Transparent]
    A --> E[Scalable]
    
    B --> B1[AI Augments<br/>Not Replaces]
    C --> C1[Data Sovereignty<br/>Independent Infrastructure]
    D --> D1[Source Citations<br/>Reproducible Methods]
    E --> E1[Multi-Project<br/>Multi-Entity]
    
    style A fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
    style B fill:#FFF9C4
    style C fill:#C8E6C9
    style D fill:#C8E6C9
    style E fill:#FFCCBC
```

---

**Last Updated**: November 18, 2025  
**Status**: Current state implemented, future state planned for MVP (January 2026)
