
import json
from haystack.dataclasses import Document

def read_json_file(file_path):
    """
    Read and parse a JSON file
    Args:
        file_path (str): Path to the JSON file
    Returns:
        dict: Parsed JSON data
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    
def save_to_json_file(data, file_path):
    """
    Save data to a JSON file
    Args:
        data: Data to save (dict or list)
        file_path (str): Path where to save the JSON file
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {str(e)}")
        return False
    
def extract_dieu_data():
    data = read_json_file('backend/data/chunking_data.json')
    dieu_info = []
    for doc in data:
        if doc["document_info"]["document_id"] == '157721':
            for part in doc["data"]:
                if part["type"] == "CHAPTER" or part["type"] == "SECTION":
                    for sub_part in part["children"]:
                        if sub_part["type"] == "ARTICLE":
                            dieu_info.append({"id": sub_part["id"], "content": sub_part["content"]})
                        elif sub_part["type"] == "SECTION":
                            for sub_sub_part in sub_part["children"]:
                                if sub_sub_part["type"] == "ARTICLE":
                                    dieu_info.append({"id": sub_sub_part["id"], "content": sub_sub_part["content"]})
                elif part["type"] == "ARTICLE":
                    dieu_info.append({"id": part["id"], "content": part["content"]})
                else:
                    print("Missing document: " + doc["document_info"]["document_id"])
                    
        save_to_json_file(dieu_info, "backend/data/dieu_info_157721.json")   
        

def vector_embeeding():
    # from haystack.dataclasses import Document
    from backend.retrieval.utils import insert
    
    dieu_data = read_json_file('backend/data/dieu_info_157721.json')
    documents = []
    for i, item in enumerate(dieu_data):
        doc = Document(
            content=item['content'],
            meta={
                'id': item['id']
            }
        )
        documents.append(doc)
    
    # Actually insert the documents into Qdrant
    print(f"📄 Embedding {len(documents)} documents...")
    insert(documents)
    print("✅ Documents embedded and stored in Qdrant!")

def query(query):
    from backend.retrieval.utils import search

    # Search uses stored embeddings automatically
    print(f"Query: '{query}'")

    # Search for the query
    try:
        results = search(query)
        # 4. Print the results
        print("\nSearch results:")
        if results:
            for doc in results:
                # The score might not always be present depending on the retriever
                score_info = f"(Score: {doc.score})" if hasattr(doc, 'score') and doc.score is not None else ""
                print(f"- Content: {doc.content[:50]} {score_info}")
        else:
            print("No results found.")
    except Exception as e:
        print(f"An error occurred during search: {e}")

if __name__ == "__main__":
    # extract_dieu_data()
    # vector_embeeding()
    query("Trách nhiệm của Ngân hàng Nhà nước Việt Nam")
