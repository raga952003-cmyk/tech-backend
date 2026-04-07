from typing import List, Dict, Any
import random

def generate_quiz(topic: str, technology: str, difficulty: str = "beginner", num_questions: int = 10) -> Dict[str, Any]:
    """
    Generate quiz questions for a given topic with real MCQ questions
    """
    # Get technology-specific questions
    questions = get_technology_questions(topic, technology, difficulty)
    
    # If no specific questions, generate generic ones
    if not questions:
        questions = generate_generic_questions(topic, technology, difficulty)
    
    # Shuffle and limit to requested number
    random.shuffle(questions)
    questions = questions[:num_questions]
    
    # Add IDs
    for i, q in enumerate(questions, 1):
        q['id'] = i
    
    return {
        "topic": topic,
        "technology": technology,
        "difficulty": difficulty,
        "total_questions": len(questions),
        "questions": questions,
        "passing_score": 70
    }

def get_technology_questions(topic: str, technology: str, difficulty: str) -> List[Dict[str, Any]]:
    """
    Get technology-specific quiz questions
    """
    topic_lower = topic.lower()
    tech_lower = technology.lower()
    
    # Docker/Containerization questions
    if 'docker' in topic_lower or 'container' in topic_lower:
        return [
            {
                "question": "What is the main difference between a Docker container and a virtual machine?",
                "options": [
                    "Containers share the host OS kernel, VMs have their own OS",
                    "Containers are slower than VMs",
                    "VMs are more portable than containers",
                    "Containers require more resources than VMs"
                ],
                "correct_answer": 0,
                "explanation": "Containers share the host operating system kernel, making them lightweight and fast to start, while VMs include a full OS and are more resource-intensive."
            },
            {
                "question": "Which Dockerfile instruction is used to specify the base image?",
                "options": ["BASE", "FROM", "IMAGE", "IMPORT"],
                "correct_answer": 1,
                "explanation": "The FROM instruction specifies the base image for your Docker image. It's typically the first instruction in a Dockerfile."
            },
            {
                "question": "What command is used to build a Docker image from a Dockerfile?",
                "options": ["docker create", "docker build", "docker make", "docker compile"],
                "correct_answer": 1,
                "explanation": "The 'docker build' command is used to build Docker images from a Dockerfile and a context."
            },
            {
                "question": "What is Docker Hub?",
                "options": [
                    "A container orchestration tool",
                    "A registry for storing and sharing Docker images",
                    "A monitoring tool for containers",
                    "A Docker configuration file"
                ],
                "correct_answer": 1,
                "explanation": "Docker Hub is a cloud-based registry service that allows you to store, share, and manage Docker images."
            },
            {
                "question": "Which command lists all running Docker containers?",
                "options": ["docker list", "docker ps", "docker show", "docker containers"],
                "correct_answer": 1,
                "explanation": "The 'docker ps' command lists all running containers. Use 'docker ps -a' to see all containers including stopped ones."
            },
            {
                "question": "What is the purpose of Docker Compose?",
                "options": [
                    "To build Docker images faster",
                    "To define and run multi-container applications",
                    "To compress Docker images",
                    "To secure Docker containers"
                ],
                "correct_answer": 1,
                "explanation": "Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file."
            },
            {
                "question": "What does the -d flag do in 'docker run -d'?",
                "options": [
                    "Deletes the container after running",
                    "Runs the container in detached mode (background)",
                    "Downloads the image first",
                    "Enables debug mode"
                ],
                "correct_answer": 1,
                "explanation": "The -d flag runs the container in detached mode, meaning it runs in the background and doesn't block your terminal."
            },
            {
                "question": "What is a Docker volume used for?",
                "options": [
                    "To increase container CPU",
                    "To persist data outside the container",
                    "To connect containers to networks",
                    "To compress container size"
                ],
                "correct_answer": 1,
                "explanation": "Docker volumes are used to persist data generated by and used by Docker containers, surviving container restarts and deletions."
            }
        ]
    
    # Kubernetes questions
    elif 'kubernetes' in topic_lower or 'k8s' in topic_lower:
        return [
            {
                "question": "What is the smallest deployable unit in Kubernetes?",
                "options": ["Container", "Pod", "Node", "Deployment"],
                "correct_answer": 1,
                "explanation": "A Pod is the smallest deployable unit in Kubernetes. It can contain one or more containers that share storage and network resources."
            },
            {
                "question": "What is the role of the Kubernetes control plane?",
                "options": [
                    "To run application containers",
                    "To manage the cluster and make decisions about scheduling",
                    "To store container images",
                    "To provide networking between pods"
                ],
                "correct_answer": 1,
                "explanation": "The control plane manages the Kubernetes cluster, making decisions about scheduling, detecting and responding to cluster events."
            },
            {
                "question": "Which Kubernetes object is used to expose pods to network traffic?",
                "options": ["Deployment", "Service", "ConfigMap", "Volume"],
                "correct_answer": 1,
                "explanation": "A Service is an abstraction that defines a logical set of Pods and a policy to access them, exposing them to network traffic."
            },
            {
                "question": "What command is used to interact with a Kubernetes cluster?",
                "options": ["k8s", "kubectl", "kubecmd", "kube"],
                "correct_answer": 1,
                "explanation": "kubectl is the command-line tool for interacting with Kubernetes clusters."
            },
            {
                "question": "What is a Kubernetes Deployment used for?",
                "options": [
                    "To store configuration data",
                    "To manage stateless applications and rolling updates",
                    "To expose services externally",
                    "To store persistent data"
                ],
                "correct_answer": 1,
                "explanation": "A Deployment provides declarative updates for Pods and ReplicaSets, managing stateless applications and enabling rolling updates."
            },
            {
                "question": "What is the purpose of a ConfigMap in Kubernetes?",
                "options": [
                    "To store sensitive data",
                    "To store non-confidential configuration data",
                    "To manage pod replicas",
                    "To define network policies"
                ],
                "correct_answer": 1,
                "explanation": "ConfigMaps are used to store non-confidential configuration data in key-value pairs that can be consumed by pods."
            }
        ]
    
    # Generative AI / LLM questions
    elif 'generative ai' in topic_lower or 'llm' in topic_lower or 'gpt' in topic_lower:
        return [
            {
                "question": "What does LLM stand for?",
                "options": [
                    "Large Language Model",
                    "Linear Learning Machine",
                    "Logical Language Method",
                    "Long Learning Memory"
                ],
                "correct_answer": 0,
                "explanation": "LLM stands for Large Language Model, which are AI models trained on vast amounts of text data to understand and generate human-like text."
            },
            {
                "question": "What is prompt engineering?",
                "options": [
                    "Building AI hardware",
                    "The practice of designing effective inputs to get desired outputs from AI models",
                    "Training AI models from scratch",
                    "Debugging AI code"
                ],
                "correct_answer": 1,
                "explanation": "Prompt engineering is the practice of crafting effective prompts to guide AI models to produce desired outputs."
            },
            {
                "question": "What is the 'temperature' parameter in LLMs?",
                "options": [
                    "The physical temperature of the server",
                    "A parameter controlling randomness in responses",
                    "The speed of response generation",
                    "The size of the model"
                ],
                "correct_answer": 1,
                "explanation": "Temperature controls the randomness of the model's output. Lower values make output more focused and deterministic, higher values make it more creative and random."
            },
            {
                "question": "What is RAG in the context of AI?",
                "options": [
                    "Random AI Generation",
                    "Retrieval Augmented Generation",
                    "Rapid Algorithm Growth",
                    "Recursive AI Guidance"
                ],
                "correct_answer": 1,
                "explanation": "RAG (Retrieval Augmented Generation) combines information retrieval with text generation, allowing LLMs to access external knowledge."
            },
            {
                "question": "What are tokens in LLMs?",
                "options": [
                    "Security credentials",
                    "Pieces of text that the model processes",
                    "API keys",
                    "Model versions"
                ],
                "correct_answer": 1,
                "explanation": "Tokens are pieces of text (words, subwords, or characters) that LLMs process. Most models charge based on token usage."
            },
            {
                "question": "What is fine-tuning in AI?",
                "options": [
                    "Adjusting server settings",
                    "Training a pre-trained model on specific data",
                    "Optimizing prompt length",
                    "Reducing model size"
                ],
                "correct_answer": 1,
                "explanation": "Fine-tuning is the process of taking a pre-trained model and training it further on a specific dataset to specialize it for particular tasks."
            }
        ]
    
    # React questions
    elif 'react' in topic_lower:
        return [
            {
                "question": "What is JSX in React?",
                "options": [
                    "A JavaScript library",
                    "A syntax extension that allows writing HTML-like code in JavaScript",
                    "A CSS framework",
                    "A testing tool"
                ],
                "correct_answer": 1,
                "explanation": "JSX is a syntax extension for JavaScript that allows you to write HTML-like code in your JavaScript files."
            },
            {
                "question": "What is the purpose of the useState hook?",
                "options": [
                    "To fetch data from APIs",
                    "To add state to functional components",
                    "To handle routing",
                    "To style components"
                ],
                "correct_answer": 1,
                "explanation": "useState is a React Hook that lets you add state to functional components."
            },
            {
                "question": "What are props in React?",
                "options": [
                    "CSS properties",
                    "Arguments passed to components",
                    "Component methods",
                    "State variables"
                ],
                "correct_answer": 1,
                "explanation": "Props (properties) are arguments passed from parent to child components, allowing data to flow down the component tree."
            },
            {
                "question": "What does the useEffect hook do?",
                "options": [
                    "Creates visual effects",
                    "Performs side effects in functional components",
                    "Optimizes performance",
                    "Handles user input"
                ],
                "correct_answer": 1,
                "explanation": "useEffect lets you perform side effects in functional components, such as data fetching, subscriptions, or manually changing the DOM."
            }
        ]
    
    # Python questions
    elif 'python' in topic_lower:
        return [
            {
                "question": "Which of the following is the correct way to create a list in Python?",
                "options": ["list = (1, 2, 3)", "list = [1, 2, 3]", "list = {1, 2, 3}", "list = <1, 2, 3>"],
                "correct_answer": 1,
                "explanation": "Lists in Python are created using square brackets []. Parentheses () create tuples, and curly braces {} create sets or dictionaries."
            },
            {
                "question": "What is the output of: print(type(5.0))?",
                "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"],
                "correct_answer": 1,
                "explanation": "5.0 is a floating-point number in Python, so type(5.0) returns <class 'float'>."
            },
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["function", "def", "func", "define"],
                "correct_answer": 1,
                "explanation": "The 'def' keyword is used to define functions in Python."
            },
            {
                "question": "What does the 'len()' function do?",
                "options": [
                    "Returns the length of an object",
                    "Converts to lowercase",
                    "Rounds a number",
                    "Sorts a list"
                ],
                "correct_answer": 0,
                "explanation": "The len() function returns the number of items in an object (string, list, tuple, etc.)."
            }
        ]
    
    return []

def generate_generic_questions(topic: str, technology: str, difficulty: str) -> List[Dict[str, Any]]:
    """
    Generate generic questions when specific ones aren't available
    """
    return [
        {
            "question": f"What is the primary purpose of {topic} in {technology}?",
            "options": [
                f"To improve performance and scalability",
                f"To add visual effects",
                f"To reduce code complexity",
                f"To handle user authentication"
            ],
            "correct_answer": 0,
            "explanation": f"{topic} is primarily used to improve performance and scalability in {technology} applications."
        },
        {
            "question": f"Which of the following is a key benefit of using {topic}?",
            "options": [
                "Increased development speed",
                "Better code organization",
                "Improved maintainability",
                "All of the above"
            ],
            "correct_answer": 3,
            "explanation": f"Using {topic} provides multiple benefits including faster development, better organization, and improved maintainability."
        },
        {
            "question": f"When should you use {topic} in your {technology} projects?",
            "options": [
                "Only in large-scale applications",
                "When you need the specific features it provides",
                "Never, it's deprecated",
                "Only for testing purposes"
            ],
            "correct_answer": 1,
            "explanation": f"You should use {topic} when your project requirements align with the features and benefits it provides."
        }
    ]

def evaluate_quiz(quiz_data: Dict[str, Any], answers: Dict[int, int]) -> Dict[str, Any]:
    """
    Evaluate quiz answers and provide detailed feedback
    """
    questions = quiz_data['questions']
    correct = 0
    total = len(questions)
    results = []
    weak_topics = []
    
    for question in questions:
        q_id = question['id']
        user_answer = answers.get(q_id, -1)
        is_correct = user_answer == question['correct_answer']
        
        if is_correct:
            correct += 1
        else:
            weak_topics.append(question['question'])
        
        results.append({
            'question_id': q_id,
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'is_correct': is_correct,
            'explanation': question['explanation']
        })
    
    score = (correct / total) * 100 if total > 0 else 0
    passed = score >= quiz_data.get('passing_score', 70)
    
    # Generate feedback
    if score >= 90:
        feedback = "Excellent! You have a strong understanding of this topic."
    elif score >= 70:
        feedback = "Good job! You passed the quiz. Review the incorrect answers to strengthen your knowledge."
    elif score >= 50:
        feedback = "Not bad, but there's room for improvement. Review the material and try again."
    else:
        feedback = "Keep studying! Review the topic materials and practice more before retaking the quiz."
    
    return {
        "score": round(score, 1),
        "correct": correct,
        "total": total,
        "passed": passed,
        "feedback": feedback,
        "results": results,
        "weak_topics": weak_topics[:3]  # Top 3 areas to improve
    }
