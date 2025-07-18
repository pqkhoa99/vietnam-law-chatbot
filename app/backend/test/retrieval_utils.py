from haystack.dataclasses import Document
from backend.retrieval.utils import insert, search
from backend.core.utils import read_json_file, save_to_json_file

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
                print(f"- Content: {doc.content[:50]} {score_info}")
        else:
            print("No results found.")
    except Exception as e:
        print(f"An error occurred during search: {e}")


if __name__ == "__main__":
    print("Running retrieval utils test...")
    run_test()
    print("\nRetrieval utils test finished.")