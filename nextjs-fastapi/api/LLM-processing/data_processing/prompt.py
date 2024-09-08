import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.evaluation import load_evaluator, EvaluatorType

# Load environment variables
load_dotenv(".env")

# Initialize the language model
llm = HuggingFaceHub(
    repo_id="google/gemma-2-2b-it", 
    model_kwargs={'temperature': 0.001, 'max_length': 512}
)

criteria = {
    "accuracy": "Is the answer correct?",
    "clarity": "Is the answer clear and well-expressed?",
    "use_of_concepts": "Does the answer demonstrate understanding of key concepts?",
}

# Create a single evaluator for all criteria
evaluator = load_evaluator(
    EvaluatorType.CRITERIA,
    criteria=criteria,
    llm=llm
)

# Create a prompt template for criteria evaluation summary
criteria_summary_template = """
Summarize the following criteria evaluations:

{eval_result}

Summary:
"""

criteria_summary_prompt = PromptTemplate(
    input_variables=["eval_result"],
    template=criteria_summary_template
)

criteria_summary_chain = LLMChain(llm=llm, prompt=criteria_summary_prompt, output_key="criteria_summary")

# Create the final scoring prompt template
scoring_template = """You are an exam marker that returns a score based on how correct an answer is to a question.
Evaluate the student's answer and provide a score out of the maximum score.

Question: {question}
Maximum Score: {max_score}
Correct Answer: {answer}
Student's Answer: {student_answer}

Criteria Evaluation Summary:
{criteria_summary}

Please provide your evaluation in the following format:
Score: [numerical score]
Explanation: [brief explanation of the score]
"""

scoring_prompt = PromptTemplate(
    input_variables=["question", "max_score", "answer", "student_answer", "criteria_summary"],
    template=scoring_template
)

scoring_chain = LLMChain(llm=llm, prompt=scoring_prompt, output_key="result")

# Create the overall chain
overall_chain = SequentialChain(
    chains=[criteria_summary_chain, scoring_chain],
    input_variables=["question", "max_score", "answer", "student_answer", "eval_result"],
    output_variables=["result"],
    verbose=True
)

def mark_answer(question, max_score, correct_answer, student_answer):
    # Run criteria evaluations
    eval_result = evaluator.evaluate_strings(
        prediction=student_answer,
        reference=correct_answer,
        input=question,
    )
    
    # Run the overall chain
    result = overall_chain({
        "question": question,
        "max_score": max_score,
        "answer": correct_answer,
        "student_answer": student_answer,
        "eval_result": str(eval_result)
    })
    
    return result['result']

# Example usage
question = "Why did the Roman Empire fall?"
max_score = 4
correct_answer = "The fall of the Roman Empire was a result of various internal and external factors. Internally, the empire dealt with significant economic challenges, such as heavy taxation and a heavy dependence on slave labor, which hindered technological progress. Politically, weak leadership, ongoing civil wars, and the division of the empire into Eastern and Western halves led to increased instability. Externally, the empire faced growing threats from migrating barbarian groups, including the Visigoths, who sacked Rome in 410 CE, and the Vandals in 455 CE. These combined pressures, along with a weakening military and the rise of the Byzantine Empire in the East, ultimately led to the fall of the Western Roman Empire in 476 CE."
student_answer = "The fall of the Roman Empire was a complex process involving multiple internal and external pressures. Internally, the empire suffered from economic troubles, including heavy taxation and reliance on slave labor, which stunted technological innovation. Politically, weak leadership, civil wars, and the splitting of the empire into Eastern and Western regions created further instability. Externally, the empire faced increasing pressure from migrating barbarian tribes, including the Visigoths, who sacked Rome in 410 CE, and the Vandals in 455 CE. These pressures, combined with a declining military and the rise of the Byzantine Empire in the East, led to the collapse of the Western Roman Empire in 476 CE."

result = mark_answer(question, max_score, correct_answer, student_answer)
print(result)