from typing import List, Dict, Any
import random

def generate_interview_questions(topic: str, technology: str, difficulty: str = "beginner") -> List[Dict[str, Any]]:
    """
    Generate AI interview questions (viva) for a topic
    """
    
    # Clean topic and technology strings
    topic = topic.strip()
    technology = technology.strip()
    
    # Question templates based on difficulty
    question_templates = {
        "beginner": [
            f"What is {topic} and why is it important in {technology}?",
            f"Can you explain the basic concept of {topic}?",
            f"What are the key features of {topic}?",
            f"How would you describe {topic} to someone new to {technology}?",
            f"What problem does {topic} solve in {technology}?",
            f"What are the main components of {topic}?",
            f"When would you use {topic} in a {technology} project?",
            f"What are the advantages of using {topic}?",
        ],
        "intermediate": [
            f"How does {topic} work internally in {technology}?",
            f"What are the best practices when implementing {topic}?",
            f"Can you compare {topic} with alternative approaches?",
            f"What are common pitfalls when working with {topic}?",
            f"How would you optimize {topic} for better performance?",
            f"Explain a real-world scenario where you would use {topic}.",
            f"What are the limitations of {topic}?",
            f"How does {topic} integrate with other {technology} features?",
        ],
        "advanced": [
            f"What are the advanced use cases of {topic} in {technology}?",
            f"How would you architect a system using {topic}?",
            f"What are the performance implications of {topic}?",
            f"How would you debug issues related to {topic}?",
            f"Explain the internals and implementation details of {topic}.",
            f"What are the security considerations when using {topic}?",
            f"How would you scale {topic} in a production environment?",
            f"What are the trade-offs of using {topic}?",
        ]
    }
    
    # Select questions based on difficulty
    templates = question_templates.get(difficulty, question_templates["beginner"])
    
    # Generate 5 unique questions
    questions = []
    selected_templates = random.sample(templates, min(5, len(templates)))
    
    for i, template in enumerate(selected_templates, 1):
        # Ensure question is properly formatted
        question_text = template.strip()
        
        questions.append({
            "id": i,
            "question": question_text,
            "type": "open-ended",
            "difficulty": difficulty,
            "topic": topic,
            "tips": generate_answer_tips(question_text, topic, technology)
        })
    
    return questions

def generate_answer_tips(question: str, topic: str, technology: str) -> List[str]:
    """
    Generate tips for answering interview questions
    """
    tips = [
        f"Start by defining {topic} clearly",
        f"Provide a real-world example from {technology}",
        "Structure your answer: What, Why, How",
        "Mention practical applications",
        "Discuss advantages and limitations",
        "Show your understanding with examples"
    ]
    
    return random.sample(tips, 3)

def generate_viva_session(topic: str, technology: str, day_number: int, skill_level: str = "beginner") -> Dict[str, Any]:
    """
    Generate a complete viva/interview session for a day
    """
    
    # Adjust difficulty based on day number
    if day_number <= 2:
        difficulty = "beginner"
    elif day_number <= 5:
        difficulty = "intermediate"
    else:
        difficulty = "advanced"
    
    # Override with user's skill level if advanced
    if skill_level == "advanced":
        difficulty = "advanced"
    elif skill_level == "intermediate" and difficulty == "beginner":
        difficulty = "intermediate"
    
    questions = generate_interview_questions(topic, technology, difficulty)
    
    return {
        "day": day_number,
        "topic": topic,
        "technology": technology,
        "difficulty": difficulty,
        "duration_minutes": 15,
        "questions": questions,
        "instructions": [
            "🎥 This is a video-based AI interview simulation",
            "📝 Answer each question in 2-3 minutes",
            "🎯 Focus on clarity and practical examples",
            "💡 Think out loud to show your thought process",
            "✅ Review the tips before answering"
        ],
        "preparation_tips": [
            f"Review your notes on {topic}",
            f"Think of real-world examples",
            "Practice explaining concepts simply",
            "Prepare questions you might ask back"
        ]
    }
