import time
from tqdm import tqdm
import re
import json
import sys
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

# Navigate up from 'dataset_filter' to 'evaluation', then 'information_retrieval', and up to the root
# Then access the 'rag_system' directory
sys.path.append("../../rag_system/")

# Import the module
from RAG import RAG


class RAG_evaluator:
    """
    This class is designed to evaluate the performance of a Retrieval-Augmented Generation (RAG) system by processing a set of questions provided in a JSON file. It supports handling different types of questions, evaluates the accuracy of the RAG's responses, and measures the system's effectiveness in retrieving relevant documents.

    Attributes:
        path_to_jsonfile (str): Path to the JSON file containing the questions for evaluation.
        output_path (str): Path where the output results will be written in JSON format.
    """

    def __init__(self, path_to_question_json, output_path):
        # Initialization can be used to set up necessary variables or states
        self.path_to_jsonfile = path_to_question_json
        self.output_path = output_path
        """
        Initializes the RAG_evaluator with the specified paths for the question JSON file and the output file.

        Parameters:
            path_to_question_json (str): Path to the JSON file containing the questions for evaluation.
            output_path (str): Path where the output results will be written in JSON format.
        """

    def run_eval(self, retriever_type=1):
        """
        Executes the evaluation of the RAG system by reading the question JSON file, processing each question, and writing the results to the output JSON file. The process includes timing the evaluation and displaying progress.
        """
        start_time = time.time()  # Start timing

        # Read the input JSON file
        with open(self.path_to_jsonfile, "r") as file:
            data = json.load(file)

        results = []
        # here we implement a variable to limit the amount of request sent for testing purposes uncomment this and line 55 - 60 in order to limit
        # amount of requests send
        # iter = 0
        # Process each question and display progress
        for question in tqdm(data["questions"], desc="Processing questions"):
            # response = self.request_selector(question['id'], question['type'])
            response = self.request_selector(question, retriever_type)
            if response is not None:
                results.append(response)
        #       iter = iter + 1
        #      if iter%10 == 0: #keep track how many iterations where done
        #              print(iter)
        #      if iter > 20:

        #          break

        # Write the results to the output JSON file
        with open(self.output_path, "w") as file:
            json.dump(results, file, indent=4)

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time
        print(f"Results written to {self.output_path}")
        print(f"Processing time: {elapsed_time:.2f} seconds")

    def request_selector(self, question, retriever_type=1):
        """
        Selects the appropriate RAG model based on the question type and processes the question to get the RAG's response. It also evaluates the correctness of the response and the effectiveness of the document retrieval.

        Parameters:
            question (dict): A dictionary representing a question with keys for ID, body, type, and the exact answer.

        Returns:
            dict: A dictionary containing detailed evaluation results for the question.
        """

        # be aware that in the current implementation only yesno and list questions are answered
        # we transfered tje logic into the match case  to reduce api requests
        match question["type"]:
            case "yesno":

                # Method to evaluate  based on the query type
                rag = RAG(retriever=retriever_type, question_type=2)
                # time request
                start_time = time.time()
                rag_answer = rag.get_answer(
                    question["body"]
                )  # dummy_request(question["body"],question["type"])
                # Stop timing
                end_time = time.time()

                # typecast string into json object
                rag_answer = json.loads(rag_answer)
                try:
                    # Extracting the necessary information if the keys are present
                    response = rag_answer.get("response")
                    k_pubmedids = rag_answer["retrieved_PMIDs"]
                    used_pubmedids = rag_answer["used_PMIDs"]
                    # Calculate elapsed time in seconds
                    elapsed_time = end_time - start_time
                    correct_pubmed, num_correct_pubmed, matched_ids = (
                        self.compare_pubmed_ids(used_pubmedids, question["documents"])
                    )
                    (
                        correct_pubmed_retrieved,
                        num_correct_pubmed_retrieved,
                        matched_ids_retrieved,
                    ) = self.compare_pubmed_ids(k_pubmedids, question["documents"])
                except Exception as e:
                    print(question["body"])
                    print("caused the following error:")
                    print(e)
                    return None

                answered_correct, percentage_correct_answers = self.yesno_eval(
                    response, question["exact_answer"]
                )
            case "summary":
                return None
                # currently we dont evaluate summary responses
            case "factoid":
                # currently we dont evaluate factoid responses

                return None
            case "list":
                # currently we dont evaluate summary responses

                return None

            case _:
                return None

        return {
            "questionid": question["id"],
            "querytype": question["type"],
            "question": question["body"],
            "trueresponse_exact": question["exact_answer"],
            "ragresponse": response,
            "answered_correct": answered_correct,
            "percentage_correct_answers": percentage_correct_answers,
            "returned_correct_pubmedid": correct_pubmed,
            "numb_of_pubmedid_returned": num_correct_pubmed,
            "returned_pubmedids": matched_ids,
            "retrieved_correct_pubmed": correct_pubmed_retrieved,
            "num_of_pubmedid_retrieved": num_correct_pubmed_retrieved,
            "retrieved_pubmedids": matched_ids_retrieved,
            "requestime": elapsed_time,
        }

    def yesno_eval(self, rag_response, true_response):
        """
        Evaluates the RAG's response for yes/no questions against the true response.

        Parameters:
            rag_response (str): The RAG's response to the question.
            true_response (str): The correct answer to the question.

        Returns:
            tuple: A tuple containing a boolean indicating if the response was correct and the percentage of correctness.
        """
        # Define valid responses
        valid_responses = {"yes", "no"}

        # Check if both responses are valid
        if (
            rag_response.lower() not in valid_responses
            or true_response.lower() not in valid_responses
        ):
            return -5, -5

        # Calculate if the answers are correct (1 if true, 0 if false)
        answered_correct = (
            True if rag_response.lower() == true_response.lower() else False
        )

        # Since it's a single comparison, correct percentage is 100% or 0%
        percentage_correct_answers = 100 if answered_correct else 0

        return answered_correct, percentage_correct_answers
    

    def compare_pubmed_ids(self, pubmed_ids, documents):
        """
        Compares PubMed IDs returned by the RAG system with those listed in the documents to evaluate the accuracy of document retrieval.

        Parameters:
            pubmed_ids (list): A list of PubMed IDs retrieved by the RAG system.
            documents (list): A list of document URLs containing the correct PubMed IDs.

        Returns:
            tuple: A tuple containing a boolean indicating if any correct PubMed ID was retrieved, the number of correct PubMed IDs, and a list of matched PubMed IDs.
        """
        # Ensure pubmed_ids is a list, if not, set it to an empty list
        if not isinstance(pubmed_ids, list):
            pubmed_ids = []

        # Extract PubMed IDs from the document URLs
        extracted_ids = [
            re.search(r"pubmed/(\d+)", doc).group(1)
            for doc in documents
            if re.search(r"pubmed/(\d+)", doc)
        ]
        # print(extracted_ids)
        # Compare the extracted IDs with the provided list of PubMed IDs
        matched_ids = [pid for pid in extracted_ids if pid in pubmed_ids]
        # print(matched_ids)

        # Determine if any correct PubMed ID was found
        correct_pubmed = len(matched_ids) > 0
        num_correct_pubmed = len(matched_ids)

        return correct_pubmed, num_correct_pubmed, matched_ids

    @staticmethod
    def analyze_performance(json_file_path):
        # Load the JSON data
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Convert JSON data into a DataFrame
        df = pd.DataFrame(data)

        # extract the retriever number from the file path
        retriever = re.search(r"ragver_(\d+)", json_file_path).group(1)
        print(f'Summary Statistics for RAG with retriever {retriever}')
        print(f"Total Questions: {len(df)}")

        # Calculate mean and standard deviation for the response time
        mean_response_time = df['requestime'].mean()
        sd_response_time = df['requestime'].std()
        print("\nResponse Time:")
        print("Mean: {:.2f} seconds".format(mean_response_time))
        print("Standard Deviation: {:.2f} seconds".format(sd_response_time))

        # Calculate accuracy, recall, precision, and F1-score
        # Assuming 'actual' and 'predicted' are the column names for your true and predicted binary classification outcomes
        accuracy = accuracy_score(df['trueresponse_exact'], df['ragresponse'])
        recall = recall_score(df['trueresponse_exact'], df['ragresponse'], average='macro', zero_division=0)
        precision = precision_score(df['trueresponse_exact'], df['ragresponse'], average='macro', zero_division=0)
        f1 = f1_score(df['trueresponse_exact'], df['ragresponse'], average='macro', zero_division=0)

        print("\nClassification Metrics:")
        print("Accuracy: {:.2f}".format(accuracy))
        print("Recall: {:.2f}".format(recall))
        print("Precision: {:.2f}".format(precision))
        print("F1 Score: {:.2f}".format(f1))

        # Additional summary statistics for other data aspects
        print("\nAdditional Summary Statistics:")
        print("Average Number of PubMed IDs Returned: {:.2f}".format(df['numb_of_pubmedid_returned'].mean()))
        print("Average Number of PubMed IDs Retrieved: {:.2f}".format(df['num_of_pubmedid_retrieved'].mean()))
