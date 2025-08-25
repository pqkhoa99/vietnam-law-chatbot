from typing import List, Optional
import logging

from domain.models import RetrievedDocument, RelatedDocument, Relationships
from core.config import settings
from neo4j import GraphDatabase, Driver

logger = logging.getLogger(__name__)


class Neo4jService:
    """Service for Neo4j graph database operations."""
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self._connect()

    def _connect(self):
        """Establish connection to Neo4j."""
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def close(self):
        """Close Neo4j connection."""
        if self.driver:
            self.driver.close()

    def get_document_relationships(
            self, 
            query: str, 
            documents: List[RetrievedDocument]
        ) -> List[RetrievedDocument]:
        """
        Populate each RetrievedDocument in `documents` with relationships.incoming/outgoing based on ids
        """

        if not self.driver:
            logger.warning("Neo4j not connected, returning original documents unchanged")
            return documents
        
        def convert_node_to_related_doc(node, rela_type: str) -> RelatedDocument:
            """Convert a Neo4j node + relationship type into RelatedDocument."""

            props = dict(node) if node else {}
            return RelatedDocument(
                rela_type=rela_type or "unknown",
                id=str(props.get("id", "unknown")),
                title=props.get("title", "unknown"),
                content=props.get("content", "unknown"),
                vbpl_id=props.get("vbpl_id", "unknown"),
                document_id=props.get("document_id", "unknown"),
                document_title=props.get("document_title", "unknown"),
                document_status=props.get("document_status", "unknown"),
                effective_date=props.get("effective_date", "unknown"),
                expired_date=props.get("expired_date", "unknown"),
            )

        cypher = """
            MATCH (a:Article {id: $id})
            OPTIONAL MATCH (a)-[r_out]->(b:Article)
            WITH a, collect({type: type(r_out), target: b, props: properties(r_out)}) AS outgoing_rels
            OPTIONAL MATCH (c:Article)-[r_in]->(a)
            WITH a, outgoing_rels, collect({type: type(r_in), source: c, props: properties(r_in)}) AS incoming_rels
            RETURN a, outgoing_rels, incoming_rels
        """

        try:
            with self.driver.session() as session:
                logger.info(f"Starting retrieve relationships for document ids: {[doc.id for doc in documents]}")
                for i, doc in enumerate(documents):
                    result = session.run(cypher, {"id": doc.id})
                    record = result.single()

                    if not record or not record["a"]:
                        logger.warning(f"Document {doc.id} not found in Neo4j; leaving relationships empty")
                        documents[i].relationships = Relationships()
                        continue

                    outgoing_rels = record["outgoing_rels"] or []
                    incoming_rels = record["incoming_rels"] or []

                    outgoing_list: List[RelatedDocument] = []
                    for rel in outgoing_rels:
                        target = rel.get("target")
                        if target is None:
                            continue
                        rtype = rel.get("type") or "unknown"
                        outgoing_list.append(convert_node_to_related_doc(target, rtype))

                    incoming_list: List[RelatedDocument] = []
                    for rel in incoming_rels:
                        source = rel.get("source")
                        if source is None:
                            continue
                        rtype = rel.get("type") or "unknown"
                        incoming_list.append(convert_node_to_related_doc(source, rtype))

                    documents[i].relationships = Relationships(
                        incoming=incoming_list,
                        outgoing=outgoing_list
                    )

            # Optional: brief summary log
            total_in = sum(len(d.relationships.incoming) for d in documents)
            total_out = sum(len(d.relationships.outgoing) for d in documents)
            logger.info(f"Sucessfully retrieve relationships for {len(documents)} documents "
                        f"(incoming={total_in}, outgoing={total_out})")

            return documents

        except Exception as e:
            logger.error(f"Error querying Neo4j relationships: {e}")
            return documents

    
    async def health_check(self) -> bool:
        """Check Neo4j service health."""
        if not self.driver:
            return False

        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            logger.error(f"❌ Neo4j health check failed: {e}")
            return False
        

# Global service instance
neo4j_service = Neo4jService()
