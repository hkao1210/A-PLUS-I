import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.evaluation.criteria import CriteriaEvalChain

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

# Create CriteriaEvalChain for each criterion
eval_chains = {
    k: CriteriaEvalChain.from_llm(
        llm=llm,
        criteria=v,
        requires_reference=True,
    )
    for k, v in criteria.items()
}

# Create the prompt template
template = """You are an exam marker that returns a score based on how correct an answer is to a question. 
Evaluate the student's answer and provide a score out of the maximum score.

Question: {question}
Maximum Score: {max_score}
Correct Answer: {answer}
Student's Answer: {student_answer}

Please provide your singular evaluation in the following format:
Score: [numerical score]
Explanation: [brief explanation of the score]

"""

prompt = PromptTemplate(
    input_variables=["question", "max_score", "answer", "student_answer"],
    template=template
)

# Create the LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

def mark_answer(question, max_score, correct_answer, student_answer):
    return chain.run({
        "question": question,
        "max_score": max_score,
        "answer": correct_answer,
        "student_answer": student_answer
    })

# Example usage
question = "Why did the Roman Empire fall?"
max_score = 4
correct_answer = "The fall of the Roman Empire was a result of various internal and external factors. Internally, the empire dealt with significant economic challenges, such as heavy taxation and a heavy dependence on slave labor, which hindered technological progress. Politically, weak leadership, ongoing civil wars, and the division of the empire into Eastern and Western halves led to increased instability. Externally, the empire faced growing threats from migrating barbarian groups, including the Visigoths, who sacked Rome in 410 CE, and the Vandals in 455 CE. These combined pressures, along with a weakening military and the rise of the Byzantine Empire in the East, ultimately led to the fall of the Western Roman Empire in 476 CE."
student_answer = "The Roman Empire fell because of several reasons. It became too large to manage, and the government couldn’t defend all the borders. Invaders like the Huns and Goths attacked. Also, the empire had economic problems and couldn’t afford to keep a strong army."

result = mark_answer(question, max_score, correct_answer, student_answer)
print(result)