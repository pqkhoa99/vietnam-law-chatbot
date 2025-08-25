from backend.core.utils import read_json_file, save_to_json_file
from backend.retrieval.utils import insert
from haystack.dataclasses import Document
from backend.test.retrieval_utils import run_query_with_generation
from backend.core.config import settings
from neo4j import GraphDatabase

test_document_ids = ["157663", "171352", "34094"]
uri = settings.NEO4J_URI
driver = GraphDatabase.driver(uri, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))

def extract_chunks_data(chunks_file):
    chunks = read_json_file("backend/dataset/articles_full_data.json")
    pipeline_chunks = []
    for chunk in chunks:
        if chunk["vbpl_id"] in test_document_ids:
            pipeline_chunks.append(chunk)
    save_to_json_file(pipeline_chunks, chunks_file)


def embedding_dieu_data(chunks_file):
    """
    Embed article data from a specific document ID into Qdrant vector database.
    """
    chunks_data = read_json_file(chunks_file)
    print(f"Embedding {len(chunks_data)} chunks from {chunks_file}...")
    documents = []

    for i, chunk in enumerate(chunks_data):            
        doc = Document(
            content=chunk['content'],
            meta={
                'id': chunk['id'],
                'title': chunk['title'],
                'vbpl_id': chunk['vbpl_id'],
                'document_id': chunk['document_id'],
                'document_title': chunk['document_title'],
                'document_status': chunk['document_status'],
                'effective_date': chunk['effective_date'],
                'expired_date': chunk['expired_date'],
                'sua_doi_bo_sung': chunk['sua_doi_bo_sung'],
                'thay_the': chunk['thay_the'],
                'bai_bo': chunk['bai_bo'],
                'dinh_chi': chunk['dinh_chi'],
                'huong_dan_quy_dinh': chunk['huong_dan_quy_dinh']
            }
        )
        documents.append(doc)
    
    print(f"Embedding {len(documents)} documents into Qdrant...")
    insert(documents)

def save_graph_to_neo4j(chunks_file):
    chunk_data = read_json_file(chunks_file)
    REL_MAP = {
        "sua_doi_bo_sung": "SUA_DOI_BO_SUNG",
        "huong_dan_quy_dinh": "HUONG_DAN_QUY_DINH",
        "thay_the": "THAY_THE",
        "bai_bo": "BAI_BO",
        "dinh_chi": "DINH_CHI",
    }
    node_batch = []
    rel_batch = []
    for row in chunk_data:
        node_batch.append({
            k: row.get(k)
            for k in [
                "id", "title", "content", "vbpl_id", "document_id",
                "document_title", "document_status", "effective_date", "expired_date"
            ]
        })

        relation_entries = []
        
        for raw_key, rel_type in REL_MAP.items():
            targets = row.get(raw_key, [])
            if targets:
                targets = [str(t) for t in targets]
                relation_entries.append({"type": rel_type, "targets": targets})

        if relation_entries:
            rel_batch.append({"id": row["id"], "relations": relation_entries})

    print(f"Length of node_batch: {len(node_batch)}")
    print(f"Length of rel_batch: {len(rel_batch)}")

    def create_nodes(tx, nodes):
        for node in nodes:
            tx.run(
                """
                MERGE (a:Article {id: $id})
                SET a.title = $title,
                    a.content = $content,
                    a.vbpl_id = $vbpl_id,
                    a.document_id = $document_id,
                    a.document_title = $document_title,
                    a.document_status = $document_status,
                    a.effective_date = $effective_date,
                    a.expired_date = $expired_date
                """,
                **node
            )

    def create_relationships(tx, rels):
        for rel in rels:
            source_id = rel["id"]
            for entry in rel["relations"]:
                rel_type = entry["type"]
                for target_id in entry["targets"]:
                    tx.run(
                        """
                        MATCH (a:Article {id: $source_id})
                        MATCH (b:Article {id: $target_id})
                        MERGE (a)-[r:%s]->(b)
                        """ % rel_type,
                        source_id=source_id,
                        target_id=target_id
                    )

    with driver.session() as session:
        print("Creating nodes in Neo4j...")
        session.execute_write(create_nodes, node_batch)
        print("Creating relationships in Neo4j...")
        session.execute_write(create_relationships, rel_batch)
        print("Graph creation complete.")



def run_neo4j_query(parameters):
    """
    Connect to Neo4j database and run a query to check the connection.
    """
    with driver.session() as session:
        query = """MATCH (a:Article {id: $id})
            OPTIONAL MATCH (a)-[r1]->(b:Article)
            OPTIONAL MATCH (c:Article)-[r2]->(a)
            RETURN a, r1, b, r2, c"""
        result = session.run(query, parameters)
        
        print(f"=== Relationships for Article ID: {parameters['id']} ===\n")
        
        for record in result:
            data = record.data()
            
            # Print center article
            if data['a']:
                print("CENTER ARTICLE:")
                print(f"  ID: {data['a'].get('id', 'N/A')}")
                print(f"  Title: {data['a'].get('title', 'N/A')[:100]}...")
                print(f"  Document ID: {data['a'].get('document_id', 'N/A')}")
                print(f"  Status: {data['a'].get('document_status', 'N/A')}")
                print()
            
            # Print outgoing relationship
            if data['r1'] and data['b']:
                print("OUTGOING RELATIONSHIP:")
                rel_type = data['r1'].type if hasattr(data['r1'], 'type') else str(type(data['r1']))
                print(f"  Relationship Type: {rel_type}")
                print(f"  Target Article ID: {data['b'].get('id', 'N/A')}")
                print(f"  Target Title: {data['b'].get('title', 'N/A')[:100]}...")
                print(f"  Target Document: {data['b'].get('document_id', 'N/A')}")
                print()
            
            # Print incoming relationship
            if data['r2'] and data['c']:
                print("INCOMING RELATIONSHIP:")
                rel_type = data['r2'].type if hasattr(data['r2'], 'type') else str(type(data['r2']))
                print(f"  Relationship Type: {rel_type}")
                print(f"  Source Article ID: {data['c'].get('id', 'N/A')}")
                print(f"  Source Title: {data['c'].get('title', 'N/A')[:100]}...")
                print(f"  Source Document: {data['c'].get('document_id', 'N/A')}")
                print()
            
            print("-" * 80)
    
    driver.close()


def setup():
    chunks_file = "backend/dataset/articles.json"
    # extract_chunks()
    # extract_chunks_data(chunks_file=chunks_file)
    embedding_dieu_data(chunks_file=chunks_file)
    # save_graph_to_neo4j(chunks_file=chunks_file)

if __name__ == "__main__":
    setup()
    query = "Cơ cấu tổ chức của Ngân hàng Nhà nước Việt Nam được quy định tại nghị định 102/2022 như thế nào?"
    # query = "Điều 2 Thông tư 37/2024/TT-NHNN quy định gì"
    # query = "Trình tự Ngân hàng Nhà nước xem xét, quyết định gia hạn thời hạn cho vay đặc biệt đối với tổ chức tín dụng được kiểm soát đặc biệt như thế nào?"
    # run_query_with_generation(query)
    # parameters = {"id": "157663_3"}
    # run_neo4j_query(parameters)



