from haystack.dataclasses import Document
from retrieval.utils import insert, search, generate_response, ask_question
from core.utils import read_json_file, save_to_json_file

def run_test():
    """
    A simple script to test the insert and search functionality.
    """
    # 1. Create some sample documents
    documents = [
        Document(content="Hanoi is the capital of Vietnam."),
        Document(content="The National Assembly is the highest representative body of the people."),
        Document(content="The Government is the highest state administrative body of the Socialist Republic of Vietnam."),
    ]

    # 2. Insert the documents into the document store
    print("--- Inserting documents ---")
    try:
        insert(documents)
        print("Documents inserted successfully.")
    except Exception as e:
        print(f"An error occurred during insertion: {e}")
        import traceback
        traceback.print_exc()
        # If insertion fails, no point in searching
        return

    print("\n--- Searching for a query ---")
    query = "What is the capital of Vietnam?"
    print(f"Query: '{query}'")

    # 3. Search for the query
    try:
        results = search(query)
        # 4. Print the results
        print("\nSearch results:")
        if results:
            for doc in results:
                # The score might not always be present depending on the retriever
                score_info = f"(Score: {doc.score})" if hasattr(doc, 'score') and doc.score is not None else ""
                print(f"- Content: {doc.content} {score_info}")
        else:
            print("No results found.")
    except Exception as e:
        print(f"An error occurred during search: {e}")


def run_query(query):
    """
    A simple script to test the search functionality with a specific query.
    """
    print(f"Running query test with query: '{query}'")
    
    # Search for the query
    try:
        results = search(query)
        # 4. Print the results
        print("\nSearch results:")
        if results:
            for doc in results:
                # The score might not always be present depending on the retriever
                score_info = f"(Score: {doc.score})" if hasattr(doc, 'score') and doc.score is not None else ""
                print(f"- Content: {doc.meta} {score_info}")
        else:
            print("No results found.")
    except Exception as e:
        print(f"An error occurred during search: {e}")


def run_query_with_generation(query):
    """
    Test the complete RAG pipeline with generation.
    """
    print(f"Running RAG test with query: '{query}'")
    
    try:
        # Use the complete RAG pipeline
        result = ask_question(query)
        
        print("\n=== RAG Results ===")
        print(f"Query: {result['query']}")
        print(f"\nResponse: {result['response']}")
        print(f"\nMetadata: {result['metadata']}")
        
        print("\n=== Retrieved Documents ===")
        for i, doc in enumerate(result['context_documents'], 1):
            score_info = f"(Score: {doc.score})" if hasattr(doc, 'score') and doc.score is not None else ""
            print(f"Document {i}: {doc.meta} {score_info}")
            
    except Exception as e:
        print(f"An error occurred during RAG test: {e}")
        import traceback
        traceback.print_exc()


def test_generation_only():
    """
    Test generation with sample context documents.
    """
    print("Testing generation with sample context...")
    
    # Create sample documents
    sample_docs = [
        Document(
            content="Điều 15. Nguyên tắc cho vay của tổ chức tín dụng: 1. Cho vay dựa trên hợp đồng tín dụng; 2. Cho vay có đảm bảo tiền vay, trừ các trường hợp cho vay không có đảm bảo theo quy định của pháp luật; 3. Bảo đảm an toàn trong cho vay.",
            meta={"source": "Luật các tổ chức tín dụng", "article_id": "Điều 15", "title": "Nguyên tắc cho vay"}
        )
    ]
    
    query = "Nguyên tắc cho vay của tổ chức tín dụng là gì?"
    
    try:
        response = generate_response(query, context_documents=sample_docs)
        print(f"Query: {query}")
        print(f"Generated Response: {response}")
    except Exception as e:
        print(f"Error in generation test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Running retrieval utils test...")
    
    # Test basic retrieval
    # run_test()
    # run_query("Nguyên tắc cho vay, vay vốn của tổ chức tín dụng nước ngoài đối với khách hàng là gì")
    
    # Test generation only
    # print("\n" + "="*50)
    # test_generation_only()
    
    # Test complete RAG pipeline
    print("\n" + "="*50)
    run_query_with_generation("Nguyên tắc cho vay, vay vốn của tổ chức tín dụng nước ngoài đối với khách hàng là gì")
    
    print("\nRetrieval utils test finished.")