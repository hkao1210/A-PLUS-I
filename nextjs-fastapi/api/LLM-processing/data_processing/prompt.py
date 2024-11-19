import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.evaluation import load_evaluator, EvaluatorType

load_dotenv(".env")

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_TOKEN'),
    temperature=0.01,
    max_length=512
)

def mark_answer(question, max_score, correct_answer, student_answer):
    try:
        # Updated Criteria Definitions
        criteria = {
            "accuracy": "Provide a numeric score between 0 and 4 for factual correctness and completeness based on the reference answer. Consider whether the student included all key points and explanations.",
            "clarity": "Provide a numeric score between 0 and 4 for writing clarity, organization, and coherence.",
            "concepts": "Provide a numeric score between 0 and 4 for the depth of understanding demonstrated. Assess whether the student provides detailed explanations showing insight into the concepts."
        }

        # Step 1: Get evaluation in JSON format
        evaluation_prompt = PromptTemplate.from_template("""
You are to evaluate a student's answer to an exam question based on the reference answer provided. Your evaluation should focus on three criteria: accuracy, clarity, and understanding of concepts. For each criterion, provide a numeric score between 0 and 4, and a brief comment explaining the score. Pay close attention to the completeness and depth of the student's answer. If the student misses important details or explanations present in the reference answer, deduct points accordingly.

Question: {question}
Reference Answer: {correct_answer}
Student's Answer: {student_answer}

Please provide your evaluation in the following JSON format:
{{
    "accuracy": <numeric score between 0 and 4>,
    "clarity": <numeric score between 0 and 4>,
    "concepts": <numeric score between 0 and 4>,
    "comments": {{
        "accuracy": "<one sentence explaining the accuracy score, focusing on correctness and completeness>",
        "clarity": "<one sentence explaining the clarity score>",
        "concepts": "<one sentence explaining the concepts score, focusing on depth of understanding>"
    }}
}}

Do not include any additional text outside this JSON format.
""")
        evaluation_response = llm.invoke(evaluation_prompt.format(
            question=question,
            correct_answer=correct_answer,
            student_answer=student_answer
        ))

        # Step 2: Parse the JSON response
        import json

        try:
            eval_result = json.loads(evaluation_response)
        except json.JSONDecodeError:
            print("Error parsing JSON response from evaluator.")
            eval_result = {}

        # Step 3: Extract scores and comments
        accuracy_score = int(eval_result.get('accuracy', 0))
        clarity_score = int(eval_result.get('clarity', 0))
        concepts_score = int(eval_result.get('concepts', 0))

        accuracy_comment = eval_result.get('comments', {}).get('accuracy', '')
        clarity_comment = eval_result.get('comments', {}).get('clarity', '')
        concepts_comment = eval_result.get('comments', {}).get('concepts', '')

        # Step 4: Calculate total and scaled scores
        total_score = accuracy_score + clarity_score + concepts_score
        max_total_score = 4 * 3  # Each criterion is out of 4
        scaled_total_score = (total_score / max_total_score) * max_score
        scaled_total_score = round(scaled_total_score, 2)

        # Step 5: Generate the final grading response
        prompt = PromptTemplate.from_template("""
Based on the evaluation results below, provide a grading response for the student's answer to the question.

Evaluation Results:
- Accuracy Score: {accuracy_score} out of 4
  Comment: {accuracy_comment}
- Clarity Score: {clarity_score} out of 4
  Comment: {clarity_comment}
- Understanding Score: {concepts_score} out of 4
  Comment: {concepts_comment}

Your response should follow this format exactly:

Score: {scaled_total_score} out of {max_score}
Accuracy: {accuracy_comment}
Clarity: {clarity_comment}
Understanding: {concepts_comment}
Overall: [Your overall summary in one sentence that reflects the scores and comments.]

Do not include any other text besides what is specified in this format.
""")

        grading_response = llm.invoke(prompt.format(
            accuracy_score=accuracy_score,
            clarity_score=clarity_score,
            concepts_score=concepts_score,
            accuracy_comment=accuracy_comment,
            clarity_comment=clarity_comment,
            concepts_comment=concepts_comment,
            scaled_total_score=scaled_total_score,
            max_score=max_score
        ))

        return grading_response

    except Exception as e:
        return f"Error during grading: {str(e)}"

if __name__ == "__main__":
    result = mark_answer(
        question="Why did the Roman Empire fall?",
        max_score=4,
        correct_answer="The fall of the Roman Empire was a result of various internal and external factors. Internally, the empire dealt with significant economic challenges, such as heavy taxation and a heavy dependence on slave labor, which hindered technological progress. Politically, weak leadership, ongoing civil wars, and the division of the empire into Eastern and Western halves led to increased instability. Externally, the empire faced growing threats from migrating barbarian groups, including the Visigoths, who sacked Rome in 410 CE, and the Vandals in 455 CE. These combined pressures, along with a weakening military and the rise of the Byzantine Empire in the East, ultimately led to the fall of the Western Roman Empire in 476 CE.",
        student_answer="The Roman Empire collapsed because of economic issues like taxation and slave labor, political problems including weak leaders and civil wars, and barbarian attacks in 410 CE and 455 CE, ending in 476 CE."
    )
    print("\nGrading Result:")
    print(result)
