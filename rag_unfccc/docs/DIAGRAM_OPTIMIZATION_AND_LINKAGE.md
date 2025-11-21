# Diagram Optimization & Entity-Document Linkage Recommendations

## 1. Making Diagrams More Compact for Document Display

### Current Challenge
Mermaid diagrams in markdown can be verbose and may not render compactly in all document formats (Word, PDF, presentations). Here are several strategies:

### Option A: Simplified, Compact Versions (Recommended)
Create separate simplified diagrams optimized for different audiences:

**For Technical Collaborators:**
- Keep current detailed diagrams
- Add numbered annotations for key components
- Use more compact node labels

**For Strategic Documents (Supervisors/Funders):**
- Create ultra-simplified versions with 3-5 key components
- Focus on value proposition, not technical details
- Use horizontal layouts (LR) for better page fit

### Option B: Export to Static Images
Convert Mermaid diagrams to PNG/SVG for better document integration:

**Tools:**
- `mermaid-cli` (npm package): `mmdc -i diagram.mmd -o diagram.png`
- Online tools: mermaid.live (export as PNG/SVG)
- VS Code extensions: "Markdown Preview Mermaid Support" with export

**Benefits:**
- Consistent rendering across all document formats
- Can be resized and positioned precisely
- Better for presentations (PowerPoint, Google Slides)

### Option C: More Compact Diagram Syntax
Optimize existing diagrams:

**Strategies:**
1. **Shorter node labels**: Use abbreviations with legends
2. **Remove subgraphs**: Flatten structure where possible
3. **Horizontal layouts**: Use `graph LR` instead of `graph TB`
4. **Combine related nodes**: Group multiple steps into single nodes
5. **Use icons/symbols**: Replace text with Unicode symbols where clear

### Recommended Approach: Hybrid
1. **Keep detailed diagrams** in `ARCHITECTURE_DIAGRAM.md` for technical reference
2. **Create simplified versions** in a new section "Compact Diagrams for Documents"
3. **Provide export scripts** to generate PNG/SVG versions
4. **Add diagram legends** explaining abbreviations

---

## 2. Entity Management and Document Metadata Linkage

### Current State Analysis

**Entity Management System:**
- Location: `data/entities/` (JSON files)
- Contains: Countries, companies, banks with metadata (sector, geography, document_type preferences)
- Purpose: Centralized entity definitions for filtering and batch processing

**Document Metadata:**
- Location: PostgreSQL `documents` table
- Contains: `country` (TEXT, references `countries` table), `document_type`, title, dates, URLs
- Purpose: Store document metadata and link to entities

**Current Disconnect:**
- Database has a separate `countries` table (simple list)
- Entity management has `countries.json` (potentially with richer metadata)
- Documents reference database `countries` table, not entity management
- No direct link between entity metadata and document filtering

### Should They Be Linked? **YES - Strongly Recommended**

### Benefits of Linking:

1. **Single Source of Truth**
   - Entity management becomes authoritative source
   - Database entities sync from entity management
   - Eliminates duplication and inconsistency

2. **Rich Filtering Capabilities**
   - Filter documents by entity metadata (e.g., "all documents for lower-middle income countries")
   - Filter by sector (for companies/banks)
   - Filter by geography (headquarters_country for companies)
   - Filter by document_type preferences per entity

3. **Consistent Entity Recognition**
   - Same entity names/aliases used in documents and queries
   - Handles entity name variations consistently
   - Supports entity matching in document ingestion

4. **Project-Specific Configurations**
   - Different entity sets per project (ASCOR vs Banking)
   - Entity metadata can drive document type preferences
   - Enables project-specific document filtering

5. **Scalability**
   - Easy to add new entity types (regions, cities, organizations)
   - Metadata-driven document routing
   - Supports multi-entity documents (e.g., company reports mentioning multiple countries)

### Proposed Linkage Architecture

```
Entity Management (JSON) → Entity Sync → Database Entities Table
                                         ↓
                                    Documents Table
                                    (references entities)
                                         ↓
                                    Retrieval Filtering
                                    (uses entity metadata)
```

### Implementation Options:

#### Option 1: Database-First (Recommended for Production)
- Entity management JSON files remain source of truth
- Sync script updates database `entities` table from JSON
- Documents reference `entities` table (with foreign key)
- Entity metadata stored in database for fast filtering
- Supports both JSON (development) and database (production)

**Pros:**
- Fast queries with database indexes
- Referential integrity
- Supports complex filtering

**Cons:**
- Requires sync mechanism
- More complex setup

#### Option 2: JSON-First (Current Approach, Enhanced)
- Keep entity management as primary source
- Documents store entity name (string) matching JSON
- EntityManager validates entity names during document ingestion
- Filtering done in application layer using EntityManager

**Pros:**
- Simpler, no sync needed
- Easy to modify entities
- Works well for current scale

**Cons:**
- No referential integrity
- Slower filtering for large datasets
- Potential name mismatches

#### Option 3: Hybrid (Best of Both)
- Entity management JSON = source of truth
- Database `entities` table = cached/synced copy
- Documents reference database entities (with FK)
- EntityManager validates against JSON during ingestion
- Sync script keeps database in sync with JSON

**Pros:**
- Fast database queries
- JSON flexibility for development
- Referential integrity
- Validation layer prevents errors

**Cons:**
- Most complex
- Requires sync discipline

### Recommended Implementation Plan:

**Phase 1: Immediate (Low Risk)**
1. Add entity validation during document ingestion
   - Check entity name exists in EntityManager before inserting document
   - Log warnings for mismatches
   - Use EntityManager aliases for matching

**Phase 2: Short-term (Medium Risk)**
2. Create entity sync script
   - `scripts/sync_entities_to_db.py`
   - Reads from `data/entities/*.json`
   - Updates/creates database `entities` table
   - Adds metadata columns (income_group, sector, etc.)

3. Enhance database schema
   - Add metadata columns to `entities` table
   - Add foreign key from `documents.country` to `entities.id`
   - Create indexes on metadata columns

**Phase 3: Long-term (Higher Value)**
4. Implement metadata-driven filtering
   - Update retrieval to filter by entity metadata
   - Support queries like "all NDCs for lower-middle income countries"
   - Enable project-specific entity filtering

5. Multi-entity document support
   - Allow documents to reference multiple entities
   - Support junction table: `document_entities`
   - Enable filtering by any referenced entity

### Database Schema Changes Needed:

```sql
-- Enhanced entities table
CREATE TABLE entities (
    id VARCHAR(255) PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,  -- 'country', 'company', 'bank'
    -- Metadata fields (JSONB for flexibility)
    metadata JSONB,
    -- Common fields
    income_group VARCHAR(100),
    sector VARCHAR(100),
    headquarters_country VARCHAR(255),
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Update documents to reference entities
ALTER TABLE documents 
    ADD COLUMN entity_id VARCHAR(255) REFERENCES entities(id),
    ADD CONSTRAINT fk_documents_entity FOREIGN KEY (entity_id) REFERENCES entities(id);

-- For multi-entity documents (future)
CREATE TABLE document_entities (
    doc_id UUID REFERENCES documents(doc_id) ON DELETE CASCADE,
    entity_id VARCHAR(255) REFERENCES entities(id) ON DELETE CASCADE,
    PRIMARY KEY (doc_id, entity_id)
);
```

### Migration Path:

1. **Backward Compatibility**: Keep `documents.country` during transition
2. **Dual Support**: Support both `country` (string) and `entity_id` (FK) temporarily
3. **Data Migration**: Script to populate `entity_id` from `country` using EntityManager
4. **Validation**: Ensure all documents have valid `entity_id` before removing `country`

---

## Summary Recommendations

### For Diagrams:
1. ✅ Create simplified, compact versions for strategic documents
2. ✅ Provide export scripts for PNG/SVG generation
3. ✅ Keep detailed versions for technical documentation
4. ✅ Use horizontal layouts and shorter labels for compactness

### For Entity-Document Linkage:
1. ✅ **YES - Link them** (strongly recommended)
2. ✅ Start with Phase 1 (validation) - low risk, immediate value
3. ✅ Plan Phase 2 (sync + schema) - medium term
4. ✅ Design Phase 3 (metadata filtering) - long-term enhancement
5. ✅ Use hybrid approach (JSON source of truth, database for queries)

### Priority:
- **High**: Entity validation during ingestion (prevents data quality issues)
- **Medium**: Entity sync script (enables rich filtering)
- **Low**: Multi-entity document support (future enhancement)

