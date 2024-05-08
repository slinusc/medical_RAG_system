import time
from tqdm import tqdm
import re
import json
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

class RAG_evaluator:
    """
    Evaluates the performance of a Retrieval-Augmented Generation (RAG) system.
    """

    def __init__(self, rag_model, path_to_question_json, output_path, multiplechoice=False):
        self.rag_model = rag_model
        self.path_to_jsonfile = path_to_question_json
        self.output_path = output_path
        self.multiple_choice = multiplechoice

    def run_eval(self):
        """Executes the evaluation of the RAG system."""
        start_time = time.time()  # Start timing

        # Read the input JSON file
        with open(self.path_to_jsonfile, "r") as file:
            data = json.load(file)

        results = []
        for question in tqdm(data["questions"], desc="Processing questions"):
            response = self.request_selector(question)
            if response is not None:
                results.append(response)

        # Write the results to the output JSON file
        with open(self.output_path, "w") as file:
            json.dump(results, file, indent=4)

        elapsed_time = time.time() - start_time
        print(f"Results written to {self.output_path}")
        print(f"Processing time: {elapsed_time:.2f} seconds")

    def request_selector(self, question):
        """Selects the appropriate RAG model and processes the question."""
        if not self.multiple_choice:
            match question["type"]:
                case "yesno":
                    return self.handle_yesno(question)
                case "summary" | "factoid" | "list":
                    return None
                case _:
                    return None
        else:
            return self.handle_multiple_choice(question)

    def handle_yesno(self, question):
        """Handles 'yesno' questions."""
        start_time = time.time()
        rag_answer = json.loads(self.rag_model.get_answer(question["body"]))
        elapsed_time = time.time() - start_time

        response = rag_answer.get("response")
        k_pubmedids = list(map(str, rag_answer["retrieved_PMIDs"]))
        used_pubmedids = list(map(str, rag_answer["used_PMIDs"]))

        retriever_time = rag_answer["retrieval_time"]
        generation_time = rag_answer["generation_time"]

        ground_truth_ids = self.extract_pubmedid(question["documents"])
        retrieved_correct_ids, num_correct_retrieved_ids, matching_retrieved_ids = self.compare_pubmed_ids(k_pubmedids, question["documents"])
        rag_used_correct_ids, rag_used_num_correct_retrieved_ids, rag_used_matching_retrieved_ids = self.compare_pubmed_ids(used_pubmedids, question["documents"])

        answered_correct = self.yesno_eval(response, question["exact_answer"])

        return {
            "questionid": question["id"],
            "querytype": question["type"],
            "question": question["body"],
            "trueresponse_exact": question["exact_answer"].lower(),
            "ragresponse": response.lower(),
            "answered_correct": answered_correct,
            "pmids_retrieved": k_pubmedids,
            "pmids_uses_by_rag": used_pubmedids,
            "pmids_ground_truth": ground_truth_ids,
            "retrieved_correct_pubmedid": retrieved_correct_ids,
            "num_correct_retrieved_ids": num_correct_retrieved_ids,
            "matching_retrieved_ids": matching_retrieved_ids,
            "rag_used_correct_ids": rag_used_correct_ids,
            "rag_used_num_correct_retrieved_ids": rag_used_num_correct_retrieved_ids,
            "rag_used_matching_retrieved_ids": rag_used_matching_retrieved_ids,
            "requestime": elapsed_time,
            "retrievment_time": retriever_time,
            "generation_time": generation_time,
        }

    def handle_multiple_choice(self, question):
        """Handles multiple-choice questions."""
        start_time = time.time()
        rag_answer = json.loads(self.rag_model.get_answer(
            f"{question['question']} \n"
            f"1: {question['opa']} \n"
            f"2: {question['opb']} \n"
            f"3: {question['opc']} \n"
            f"4: {question['opd']}"
        ))
        elapsed_time = time.time() - start_time

        response = rag_answer.get("response")
        k_pubmedids = rag_answer["retrieved_PMIDs"]
        used_pubmedids = rag_answer["used_PMIDs"]

        retriever_time = rag_answer["retrieval_time"]
        generation_time = rag_answer["generation_time"]

        answered_correct = self.evaluate_MEDMCQA(response, question["cop"])

        return {
            "questionid": question["id"],
            "querytype": "MEDCQA" + question["choice_type"],
            "question": question["question"],
            "trueresponse_exact": question["cop"],
            "ragresponse": response,
            "answered_correct": answered_correct,
            "pmids_retrieved": k_pubmedids,
            "pmids_uses_by_rag": used_pubmedids,
            "pmids_ground_truth": "none_for_question_type",
            "requestime": elapsed_time,
            "retrievment_time": retriever_time,
            "generation_time": generation_time,
        }

    def evaluate_MEDMCQA(self, rag_response, true_response):
        """Evaluates multiple-choice questions."""
        try:
            return int(rag_response) == int(true_response)
        except Exception:
            return False

    def yesno_eval(self, rag_response, true_response):
        """Evaluates 'yesno' questions."""
        valid_responses = {"yes", "no"}
        if rag_response.lower() not in valid_responses or true_response.lower() not in valid_responses:
            return False
        return rag_response.lower() == true_response.lower()

    def compare_pubmed_ids(self, pubmed_ids, documents):
        """Compares PubMed IDs returned by the RAG system."""
        if not isinstance(pubmed_ids, list):
            pubmed_ids = []

        extracted_ids = [
            re.search(r"pubmed/(\d+)", doc).group(1)
            for doc in documents
            if re.search(r"pubmed/(\d+)", doc)
        ]

        matched_ids = [pid for pid in extracted_ids if pid in pubmed_ids]

        return bool(matched_ids), len(matched_ids), matched_ids

    def extract_pubmedid(self, documents):
        """Extracts PubMed IDs from document URLs."""
        return [
            re.search(r"pubmed/(\d+)", doc).group(1)
            for doc in documents
            if re.search(r"pubmed/(\d+)", doc)
        ]

    def manual_accuracy_score(self, y_true, y_pred):
        """Calculates the accuracy manually."""
        if len(y_true) != len(y_pred):
            raise ValueError("The length of true labels and predicted labels must be the same.")
        return sum(1 for true, pred in zip(y_true, y_pred) if true == pred) / len(y_true)

    def analyze_performance(self, json_file_path):
        """Analysiert die Performance anhand der Daten aus einer JSON-Datei."""
        with open(json_file_path, "r") as file:
            data = json.load(file)

        df = pd.DataFrame(data)

        retriever_match = re.search(r"ragver_(\d+)", json_file_path)
        retriever = retriever_match.group(1) if retriever_match else "Unknown"
        print(f"Summary Statistics for RAG with retriever {retriever}")
        print(f"Total Questions: {len(df)}")

        mean_response_time = df["requestime"].mean()
        sd_response_time = df["requestime"].std()
        print("\nResponse Time:")
        print(f"Mean: {mean_response_time:.2f} seconds")
        print(f"Standard Deviation: {sd_response_time:.2f} seconds")

        accuracy = self.manual_accuracy_score(df["trueresponse_exact"], df["ragresponse"])
        recall = recall_score(df["trueresponse_exact"], df["ragresponse"], average="weighted", zero_division=0)
        precision = precision_score(df["trueresponse_exact"], df["ragresponse"], average="weighted", zero_division=0)
        f1 = f1_score(df["trueresponse_exact"], df["ragresponse"], average="weighted", zero_division=0)

        recall_list = []
        precision_list = []
        f1_score_list = []
        recall_used_vs_retrieved_list = []
        precision_used_vs_retrieved_list = []
        f1_used_vs_retrieved_list = []

        for i in range(len(df)):
            ground_truth_pmids = list(df["pmids_ground_truth"][i])
            matching_retrieved_ids = list(df["matching_retrieved_ids"][i])
            retrieved_pmids = list(df["pmids_retrieved"][i])
            matching_used_ids = list(df["rag_used_matching_retrieved_ids"][i])
            used_pmids = list(df["pmids_uses_by_rag"][i])

            recall_retriever = len(matching_retrieved_ids) / len(ground_truth_pmids) if ground_truth_pmids else 0
            precision_retriever = len(matching_retrieved_ids) / len(retrieved_pmids) if retrieved_pmids else 0

            recall_used_vs_retrieved = len(used_pmids) / len(retrieved_pmids) if retrieved_pmids else 0
            precision_used_vs_retrieved = len(matching_used_ids) / len(retrieved_pmids) if retrieved_pmids else 0

            if precision_retriever + recall_retriever:
                f1_retriever = 2 * (precision_retriever * recall_retriever) / (precision_retriever + recall_retriever)
            else:
                f1_retriever = 0.0

            if precision_used_vs_retrieved + recall_used_vs_retrieved:
                f1_used_vs_retrieved = 2 * (precision_used_vs_retrieved * recall_used_vs_retrieved) / (precision_used_vs_retrieved + recall_used_vs_retrieved)
            else:
                f1_used_vs_retrieved = 0.0

            recall_list.append(recall_retriever)
            precision_list.append(precision_retriever)
            f1_score_list.append(f1_retriever)

            recall_used_vs_retrieved_list.append(recall_used_vs_retrieved)
            precision_used_vs_retrieved_list.append(precision_used_vs_retrieved)
            f1_used_vs_retrieved_list.append(f1_used_vs_retrieved)

        avg_recall_retriever = sum(recall_list) / len(recall_list)
        avg_precision_retriever = sum(precision_list) / len(precision_list)
        avg_f1_retriever = sum(f1_score_list) / len(f1_score_list)

        avg_recall_used_vs_retrieved = sum(recall_used_vs_retrieved_list) / len(recall_used_vs_retrieved_list)
        avg_precision_used_vs_retrieved = sum(precision_used_vs_retrieved_list) / len(precision_used_vs_retrieved_list)
        avg_f1_used_vs_retrieved = sum(f1_used_vs_retrieved_list) / len(f1_used_vs_retrieved_list)

        count_no_docs_found = (df["ragresponse"] == "no_docs_found").sum()
        count_five = (df["ragresponse"] == 5).sum()
        total_specific_counts = count_no_docs_found + count_five

        total_rows = len(df)
        percentage_not_answered = (total_specific_counts / total_rows) * 100

        print("\nSummary of non-answered questions:")
        print(f"Absolute count - No Docs Found: {total_specific_counts}")
        print(f"Percentage - No Docs Found: {percentage_not_answered:.2f}%")
        print("\nMetrics - RAG Q&A:")
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"F1 Score: {f1:.2f}")
        print("\nMetrics - Retriever:")
        print(f"Recall Retriever: {avg_recall_retriever:.2f}")
        print(f"Precision Retriever: {avg_precision_retriever:.2f}")
        print(f"F1 Score Retriever: {avg_f1_retriever:.2f}")
        print("\nMetrics - Used vs Retrieved:")
        print(f"Recall Used vs Retrieved: {avg_recall_used_vs_retrieved:.2f}")
        print(f"Precision Used vs Retrieved: {avg_precision_used_vs_retrieved:.2f}")
        print(f"F1 Score Used vs Retrieved: {avg_f1_used_vs_retrieved:.2f}")

        print("\nAdditional metrics:")
        print(f"Mean response time retriever: {round(df['retrievment_time'].mean(), 2)}")
        print(f"Standard deviation response time retriever: {round(df['retrievment_time'].std(), 2)}")
        print(f"Mean response time generation: {round(df['generation_time'].mean(), 2)}")
        print(f"Standard deviation response time generation: {round(df['generation_time'].std(), 2)}")