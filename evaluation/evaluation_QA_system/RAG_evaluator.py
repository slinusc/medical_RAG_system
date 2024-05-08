import time
from tqdm import tqdm
import re
import json
import sys
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


class RAG_evaluator:
    """
    This class is designed to evaluate the performance of a Retrieval-Augmented Generation (RAG) system by processing a set of questions provided in a JSON file. It supports handling different types of questions, evaluates the accuracy of the RAG's responses, and measures the system's effectiveness in retrieving relevant documents.

    Attributes:
        path_to_jsonfile (str): Path to the JSON file containing the questions for evaluation.
        output_path (str): Path where the output results will be written in JSON format.
    """

    def __init__(
        self, rag_model, path_to_question_json, output_path, multiplechoice=False
    ):
        # Initialization can be used to set up necessary variables or states
        self.rag_model = rag_model
        self.path_to_jsonfile = path_to_question_json
        self.output_path = output_path
        self.multiple_choice = multiplechoice
        """
        Initializes the RAG_evaluator with the specified paths for the question JSON file and the output file.

        Parameters:
            path_to_question_json (str): Path to the JSON file containing the questions for evaluation.
            output_path (str): Path where the output results will be written in JSON format.
        """

    def run_eval(self):
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
        iter = 0
        # Process each question and display progress
        # since both data sets have different file strucutres we must differentiate here ibetween them
        for question in tqdm(data["questions"], desc="Processing questions"):
            # response = self.request_selector(question['id'], question['type'])
            response = self.request_selector(question)
            if response is not None:
                results.append(response)
                # iter = iter + 1
                # if iter >= 10:
                #    break

        # Write the results to the output JSON file
        with open(self.output_path, "w") as file:
            json.dump(results, file, indent=4)

        end_time = time.time()  # End timing
        elapsed_time = end_time - start_time
        print(f"Results written to {self.output_path}")
        print(f"Processing time: {elapsed_time:.2f} seconds")

    def request_selector(self, question):
        """
        Selects the appropriate RAG model based on the question type and processes the question to get the RAG's response. It also evaluates the correctness of the response and the effectiveness of the document retrieval.

        Parameters:
            question (dict): A dictionary representing a question with keys for ID, body, type, and the exact answer.

        Returns:
            dict: A dictionary containing detailed evaluation results for the question.
        """

        # be aware that in the current implementation only yesno and list questions are answered
        # we transfered tje logic into the match case  to reduce api requests
        # here we select between the file format of the QA and multiple choice dataset
        if self.multiple_choice == False:
            match question["type"]:
                case "yesno":

                    # time request
                    start_time = time.time()
                    rag_answer = self.rag_model.get_answer(
                        question["body"]
                    )  # dummy_request(question["body"],question["type"])
                    # Stop timing
                    end_time = time.time()

                    try:
                        # typecast string into json object
                        rag_answer = json.loads(rag_answer)
                        # Extracting the necessary information if the keys are present
                        response = rag_answer.get("response")
                        k_pubmedids = list(map(str, rag_answer["retrieved_PMIDs"]))
                        # garantee that the ids are strings
                        used_pubmedids = list(map(str, rag_answer["used_PMIDs"]))
                        # garantee that the ids are strings
                        # Calculate elapsed time in seconds
                        elapsed_time = end_time - start_time
                        # get the time it took to retreieve und generate the answer
                        retriever_time = rag_answer["retrieval_time"]

                        generation_time = rag_answer["generation_time"]

                        ground_truth_ids = self.extraxt_pubmedid(question["documents"])
                        (
                            retrieved_correct_ids,
                            num_correct_retrived_ids,
                            matching_retrieved_ids,
                        ) = self.compare_pubmed_ids(k_pubmedids, question["documents"])
                        (
                            rag_used_correct_ids,
                            rag_used_num_correct_retrived_ids,
                            rag_used_matching_retrieved_ids,
                        ) = self.compare_pubmed_ids(
                            used_pubmedids, question["documents"]
                        )
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
                "questionid": question["id"],  # question ID
                "querytype": question["type"],  # question type
                "question": question["body"],  # question
                "trueresponse_exact": question[
                    "exact_answer"
                ].lower(),  # groundtruth answer
                "ragresponse": response.lower(),  # response of the rag
                "answered_correct": answered_correct,  # groundtruth / correct answer
                "pmids_retrieved": str(
                    k_pubmedids
                ),  # the pubmedids that where retrived
                "pmids_uses_by_rag": str(
                    used_pubmedids
                ),  #  the pubmedids that where actually used
                "pmids_ground_truth": ground_truth_ids,  # the pubmed ids that are the ideal answer
                "retreived_correct_pubmedid": retrieved_correct_ids,  # bool, wether or not any correct pubmed ids where retrived
                "num_correct_retrieved_ids": num_correct_retrived_ids,  # numeric. number of pubmed ids correctly retrieved
                "matching_retrieved_ids": matching_retrieved_ids,  # numeric, correctly used pubmedids retrieved
                "rag_used_correct_ids": rag_used_correct_ids,  # bool, wether or not any current pubmedid was used by the rag
                "rag_used_num_correct_retrived_ids": rag_used_num_correct_retrived_ids,  # numeric, numer of pubmed ids correctly used by the rag
                "rag_used_matching_retrieved_ids": rag_used_matching_retrieved_ids,  # numeric pubmedids that where correclty used
                "requestime": elapsed_time,  # time used for the entire request
                "retrievment_time": retriever_time,  # time used for retrievment
                "generation_time": generation_time,  # time used for generation
            }
        # now we handle the case of multiple choice datasets
        else:

            # time request
            start_time = time.time()
            rag_answer = self.rag_model.get_answer(
                f"{question['question']} \n"
                f"1: {question['opa']} \n"
                f"2: {question['opb']} \n"
                f"3: {question['opc']} \n"
                f"4: {question['opd']}"
            )
            # Stop timing
            end_time = time.time()

            try:
                # typecast string into json object
                rag_answer = json.loads(rag_answer)
                # Extracting the necessary information if the keys are present
                response = rag_answer.get("response")
                k_pubmedids = rag_answer["retrieved_PMIDs"]
                used_pubmedids = rag_answer["used_PMIDs"]
                # Calculate elapsed time in seconds
                elapsed_time = end_time - start_time
                # get the time it took to retreieve und generate the answer
                retriever_time = rag_answer["retrieval_time"]
                generation_time = rag_answer["generation_time"]
                ground_truth_ids = "none_for_question_type"

            except Exception as e:
                print(e)
                return None

            answered_correct = self.evaluate_MEDMCQA(response, question["cop"])

        return {
            "questionid": question["id"],  # question ID
            "querytype": "MEDCQA" + question["choice_type"],  # question type
            "question": question["question"],  # question
            "trueresponse_exact": question["cop"],  # groundtruth answer
            "ragresponse": response,  #
            "answered_correct": answered_correct,
            "pmids_retrieved": k_pubmedids,
            "pmids_uses_by_rag": used_pubmedids,
            "pmids_ground_truth": ground_truth_ids,
            "requestime": elapsed_time,
            "retrievment_time": retriever_time,  # time used for retrievment
            "generation_time": generation_time,  # time used for generation
        }

    def evaluate_MEDMCQA(self, rag_response, true_response):
        try:
            if int(rag_response) == int(true_response):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None

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

    def extraxt_pubmedid(self, documents):
        # Extract PubMed IDs from the document URLs
        extracted_ids = [
            re.search(r"pubmed/(\d+)", doc).group(1)
            for doc in documents
            if re.search(r"pubmed/(\d+)", doc)
        ]
        return extracted_ids

    def manual_accuracy_score(self, y_true, y_pred):
        # Ensure that y_true and y_pred are the same length
        if len(y_true) != len(y_pred):
            raise ValueError(
                "The length of true labels and predicted labels must be the same."
            )

        # Calculate the number of correct predictions
        correct_predictions = sum(
            1 for true, pred in zip(y_true, y_pred) if true == pred
        )

        # Calculate accuracy as the ratio of correct predictions to total observations
        total_predictions = len(y_true)
        accuracy = correct_predictions / total_predictions

        return accuracy


    def analyze_performance(self, json_file_path):
        """Analysiert die Performance anhand der Daten aus einer JSON-Datei."""
        # Load the JSON data
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Convert JSON data into a DataFrame
        df = pd.DataFrame(data)

        # Extract the retriever number from the file path
        retriever_match = re.search(r"ragver_(\d+)", json_file_path)
        retriever = retriever_match.group(1) if retriever_match else "Unknown"
        print(f"Summary Statistics for RAG with retriever {retriever}")
        print(f"Total Questions: {len(df)}")

        # Calculate mean and standard deviation for the response time
        mean_response_time = df["requestime"].mean()
        sd_response_time = df["requestime"].std()
        print("\nResponse Time:")
        print("Mean: {:.2f} seconds".format(mean_response_time))
        print("Standard Deviation: {:.2f} seconds".format(sd_response_time))

        # Calculate accuracy, recall, precision, and F1-score
        # Assuming 'actual' and 'predicted' are the column names for your true and predicted binary classification outcomes
        accuracy = self.manual_accuracy_score(
            df["trueresponse_exact"], df["ragresponse"]
        )
        recall = recall_score(
            df["trueresponse_exact"],
            df["ragresponse"],
            average="weighted",
            zero_division=0,
        )
        precision = precision_score(
            df["trueresponse_exact"],
            df["ragresponse"],
            average="weighted",
            zero_division=0,
        )
        f1 = f1_score(
            df["trueresponse_exact"],
            df["ragresponse"],
            average="weighted",
            zero_division=0,
        )

        recall_list = []
        precision_list = []
        f1_score_list = []

        # Iterating over the DataFrame
        for i in range(len(df)):
            ground_truth_pmids = list(df["pmids_ground_truth"][i])
            matching_retrieved_ids = list(df["matching_retrieved_ids"][i])
            retrieved_pmids = list(df["pmids_retrieved"][i])

            # Calculate Recall
            recall_retriever = len(matching_retrieved_ids) / len(ground_truth_pmids)
            print(len(matching_retrieved_ids))
            print(len(ground_truth_pmids))
            recall_list.append(recall_retriever)

            # Calculate Precision
            precision_retriever = len(matching_retrieved_ids) / len(retrieved_pmids)
            precision_list.append(precision_retriever)

            # Calculate F1-Score
            if precision_retriever + recall_retriever != 0:
                f1_retriever = 2 * (precision_retriever * recall_retriever) / (precision_retriever + recall_retriever)
            else:
                f1_retriever = 0.0
            f1_score_list.append(f1_retriever)

        # Calculate average scores
        avg_recall_retriever = sum(recall_list) / len(recall_list)
        avg_precision_retriever = sum(precision_list) / len(precision_list)
        avg_f1_retriever = sum(f1_score_list) / len(f1_score_list)

        # Count the number of "no answer given" cases
        count_no_docs_found = (df["ragresponse"] == "no_docs_found").sum()
        count_five = (df["ragresponse"] == 5).sum()
        # Total specific counts
        total_specific_counts = count_no_docs_found + count_five

        # Total rows in the DataFrame
        total_rows = len(df)

        # Calculate percentages
        percentage_not_answered = (total_specific_counts / total_rows) * 100

        # Print or save the results
        print("\nSummary of non-answered questions:")
        print(f"Absolute count - No Docs Found: {total_specific_counts}")
        print(f"Percentage - No Docs Found: {percentage_not_answered:.2f}%")
        print("\nMetrics - RAG:")
        print("Accuracy: {:.2f}".format(accuracy))
        print("Recall: {:.2f}".format(recall))
        print("Precision: {:.2f}".format(precision))
        print("F1 Score: {:.2f}".format(f1))
        print("\nMetrics - Retriever:")
        print("Recall: {:.2f}".format(avg_recall_retriever))
        print("Precision: {:.2f}".format(avg_precision_retriever))
        print("F1 Score: {:.2f}".format(avg_f1_retriever))

        print("\nAdditional metrics:")
        print(f"Mean response time overall: {round(df['requestime'].mean(), 2)}")
        print(f"Mean response time retriever: {round(df['retrievment_time'].mean(), 2)}")
        print(f"Mean response time generation: {round(df['generation_time'].mean(), 2)}")