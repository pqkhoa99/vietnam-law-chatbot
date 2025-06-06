"""
Neo4j graph database client for the Vietnam Legal Chatbot.
"""
from typing import Dict, List, Optional

from neo4j import GraphDatabase

from core.config import settings


def get_neo4j_driver():
    """
    Get a Neo4j driver instance.
    
    Returns:
        Neo4j driver
    """
    return GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    )


class Neo4jManager:
    """Manager for Neo4j graph database operations."""
    
    def __init__(self, driver=None):
        """
        Initialize the Neo4j manager.
        
        Args:
            driver: Neo4j driver
        """
        self.driver = driver or get_neo4j_driver()
    
    def create_document_node(self, document_data: Dict) -> str:
        """
        Create a document node in the graph.
        
        Args:
            document_data: Document metadata
            
        Returns:
            Document ID
        """
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_document_node_tx, document_data
            )
            return result
    
    def _create_document_node_tx(self, tx, document_data):
        """Transaction function to create a document node."""
        query = """
        CREATE (d:Document {
            id: $id,
            title: $title,
            file_path: $file_path,
            file_type: $file_type,
            created_at: datetime()
        })
        RETURN d.id as document_id
        """
        result = tx.run(
            query,
            id=document_data.get("id"),
            title=document_data.get("title"),
            file_path=document_data.get("file_path"),
            file_type=document_data.get("file_type"),
        )
        record = result.single()
        return record["document_id"] if record else None
    
    def create_legal_entity_relationship(
        self, document_id: str, entity_type: str, entity_name: str
    ) -> None:
        """
        Create a relationship between a document and a legal entity.
        
        Args:
            document_id: Document ID
            entity_type: Type of legal entity (e.g., 'Law', 'Decree')
            entity_name: Name of the entity
        """
        with self.driver.session() as session:
            session.write_transaction(
                self._create_legal_entity_relationship_tx,
                document_id,
                entity_type,
                entity_name,
            )
    
    def _create_legal_entity_relationship_tx(self, tx, document_id, entity_type, entity_name):
        """Transaction function to create a legal entity relationship."""
        query = """
        MATCH (d:Document {id: $document_id})
        MERGE (e:LegalEntity {type: $entity_type, name: $entity_name})
        MERGE (d)-[:REFERENCES]->(e)
        """
        tx.run(
            query,
            document_id=document_id,
            entity_type=entity_type,
            entity_name=entity_name,
        )
