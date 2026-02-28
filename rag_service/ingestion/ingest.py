import os
import sys
import uuid
import logging
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from db.snowflake_conn import get_cursor, initialize_schema
from ingestion.chunker import chunk_document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_markdown_files(docs_dir: str = None) -> list[dict]:

    if docs_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        docs_dir = os.path.join(os.path.dirname(current_dir), "docs")

    docs_path = Path(docs_dir)

    if not docs_path.exists():
        logger.warning(f"Docs directory not found: {docs_dir}")
        return []

    documents = []

    for md_file in docs_path.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            concept = md_file.stem

            documents.append(
                {
                    "concept": concept,
                    "content": content,
                    "filename": md_file.name,
                }
            )

            logger.info(f"Loaded document: {md_file.name}")

        except Exception as e:
            logger.error(f"Error reading {md_file}: {e}")

    return documents


def insert_chunks_with_embeddings(chunks: list[dict]):

    cursor = get_cursor()

    try:
        insert_query = """
        INSERT INTO KNOWLEDGE_BASE (ID, CONCEPT, CONTENT, EMBEDDING)
        SELECT
            %s,
            %s,
            %s,
            SNOWFLAKE.CORTEX.EMBED_TEXT_768(
                'snowflake-arctic-embed-m-v1.5',
                %s
            )
        """

        inserted_count = 0

        for chunk in chunks:
            chunk_id = str(uuid.uuid4())

            try:
                cursor.execute(
                    insert_query,
                    (
                        chunk_id,
                        chunk["concept"],
                        chunk["content"],
                        chunk["content"],  # needed again for embedding
                    ),
                )

                inserted_count += 1
                logger.info(
                    f"Inserted chunk {inserted_count}: "
                    f"{chunk['concept']} "
                    f"(index {chunk.get('chunk_index', 0)})"
                )

            except Exception as e:
                logger.error(f"Error inserting chunk: {e}")
                raise

        logger.info(f"Successfully inserted {inserted_count} chunks")

    except Exception as e:
        logger.error(f"Error during insertion: {e}")
        raise

    finally:
        cursor.close()


def ingest_documents(docs_dir: str = None):

    logger.info("Starting knowledge ingestion process...")

    config.validate_config()

    logger.info("Initializing Snowflake schema...")
    initialize_schema()

    logger.info("Reading markdown documents...")
    documents = read_markdown_files(docs_dir)

    if not documents:
        logger.warning("No documents found to ingest")
        return

    logger.info(f"Found {len(documents)} documents")

    all_chunks = []

    for doc in documents:
        logger.info(f"Chunking document: {doc['filename']}")
        chunks = chunk_document(doc["content"], doc["concept"])
        all_chunks.extend(chunks)
        logger.info(f"Created {len(chunks)} chunks from {doc['filename']}")

    logger.info(f"Total chunks to ingest: {len(all_chunks)}")

    logger.info("Inserting chunks into Snowflake...")
    insert_chunks_with_embeddings(all_chunks)

    logger.info("✅ Ingestion complete!")


if __name__ == "__main__":
    try:
        ingest_documents()
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)