# RAG Workflow

1. Parse Data

2. Chunk Data

3. Create Metadata

   - Extract auto-suggested or custom labels
   - Human in the loop validation of labels
   - Generate hierarchies between labels and across documents (and other datasets)
   - Cluster and filter data and export labels

   a. Add document level or cluster (agentic) level descriptive metadata so LLM can decide if it's worth consulting a document set or cluser

4. Index Data (vector DB)

   - Use metadata to segredate documents in vector space

5. Enhanced retrieval with metadata

   - Filter or **increaed routing accuracy**
   - Pre filter embedding search space based on metadata
   - Metadata can be used by LLM to assess relevance, possibly retrieve answer from metada, or if necessary, retreive document(s)

- Filter embedings
- Vector auto-index retriever

### Chunk Level Metadata

- Small number of tags with defined output values (not open ended), which allow you to quickly segment the data based on a quesiton

  - Domain specific type
  - High level tag
  - Version
  - Date

- Use as an initial filter by vectorDB to identify relevant docuemnts or chunks from the embedding space

### RAG Setup

- Domain specific taigs
- Subject tags
- Document type
- Author
- Generic tags
- Purpose/summary
- Key questions
