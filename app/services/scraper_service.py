import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import re
import json

def scrape_roadmap_sh(technology: str) -> Dict[str, Any]:
    """
    Scrape roadmap.sh for technology learning paths
    """
    tech_map = {
        'python': 'python',
        'javascript': 'javascript',
        'react': 'react',
        'nodejs': 'nodejs',
        'node': 'nodejs',
        'devops': 'devops',
        'frontend': 'frontend',
        'backend': 'backend',
        'fullstack': 'full-stack',
        'java': 'java',
        'golang': 'golang',
        'go': 'golang',
        'docker': 'docker',
        'kubernetes': 'kubernetes',
        'aws': 'aws',
        'android': 'android',
        'flutter': 'flutter',
        'vue': 'vue',
        'angular': 'angular',
        'ai': 'ai-data-scientist',
        'ml': 'ai-data-scientist',
        'machine learning': 'ai-data-scientist',
        'data science': 'ai-data-scientist',
        'generative ai': 'ai-data-scientist',
        'gen ai': 'ai-data-scientist'
    }
    
    tech_key = tech_map.get(technology.lower(), technology.lower())
    
    try:
        # Try to get roadmap data
        url = f"https://roadmap.sh/{tech_key}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract topics from the page
            topics = []
            
            # Look for common patterns in roadmap.sh structure
            headings = soup.find_all(['h2', 'h3', 'h4'])
            for heading in headings[:15]:  # Limit to first 15 topics
                text = heading.get_text().strip()
                if text and len(text) > 3 and len(text) < 100:
                    topics.append(text)
            
            if topics:
                return {
                    'source': 'roadmap.sh',
                    'topics': topics,
                    'url': url
                }
    except Exception as e:
        print(f"Error scraping roadmap.sh: {e}")
    
    return None

def scrape_wikipedia_outline(technology: str) -> Dict[str, Any]:
    """
    Scrape Wikipedia for technology outlines and topics
    """
    try:
        # Search Wikipedia for the technology
        search_url = f"https://en.wikipedia.org/wiki/{technology.replace(' ', '_')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            topics = []
            
            # Find table of contents
            toc = soup.find('div', {'id': 'toc'})
            if toc:
                links = toc.find_all('a', {'class': 'toctext'})
                for link in links[:12]:
                    text = link.get_text().strip()
                    if text and len(text) > 3 and len(text) < 80:
                        topics.append(text)
            
            # Also get section headings
            if not topics:
                headings = soup.find_all(['h2', 'h3'], limit=12)
                for heading in headings:
                    text = heading.get_text().strip()
                    # Clean up the text
                    text = re.sub(r'\[edit\]', '', text).strip()
                    if text and len(text) > 3 and len(text) < 80:
                        topics.append(text)
            
            if topics:
                return {
                    'source': 'wikipedia',
                    'topics': topics[:10],
                    'url': search_url
                }
    except Exception as e:
        print(f"Error scraping Wikipedia: {e}")
    
    return None

def scrape_github_awesome(technology: str) -> Dict[str, Any]:
    """
    Search GitHub Awesome lists for learning resources
    """
    try:
        search_url = f"https://github.com/search?q=awesome+{technology}+learning&type=repositories"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find repository links
            repos = soup.find_all('a', {'class': 'v-align-middle'}, limit=3)
            resources = []
            
            for repo in repos:
                repo_name = repo.get_text().strip()
                repo_url = 'https://github.com' + repo.get('href', '')
                if repo_name and repo_url:
                    resources.append({
                        'name': repo_name,
                        'url': repo_url
                    })
            
            if resources:
                return {
                    'source': 'github',
                    'resources': resources
                }
    except Exception as e:
        print(f"Error scraping GitHub: {e}")
    
    return None

def get_learning_topics(technology: str) -> List[str]:
    """
    Get learning topics from multiple sources
    """
    topics = []
    
    # Try roadmap.sh first
    roadmap_data = scrape_roadmap_sh(technology)
    if roadmap_data and roadmap_data.get('topics'):
        topics.extend(roadmap_data['topics'][:10])
    
    # Try Wikipedia if we don't have enough topics
    if len(topics) < 5:
        wiki_data = scrape_wikipedia_outline(technology)
        if wiki_data and wiki_data.get('topics'):
            topics.extend(wiki_data['topics'][:8])
    
    # Remove duplicates and clean up
    if topics:
        topics = list(dict.fromkeys(topics))
        # Filter out generic/unhelpful topics and questions
        topics = [t for t in topics if not any(skip in t.lower() for skip in 
                  ['see also', 'references', 'external links', 'notes', 'further reading', 'contents',
                   'what is', 'what are', 'how to', 'why', 'when', '?'])]
        
        # Filter out topics that are too short or too long
        topics = [t for t in topics if 5 < len(t) < 80]
        
        if len(topics) >= 8:
            return topics[:12]
    
    # Fallback to predefined topics
    return get_fallback_topics(technology)

def get_fallback_topics(technology: str) -> List[str]:
    """
    Comprehensive fallback topics when scraping fails
    """
    tech_topics = {
        'python': [
            'Python Basics & Syntax',
            'Data Types & Variables',
            'Control Flow (if/else, loops)',
            'Functions & Modules',
            'Object-Oriented Programming',
            'File Handling & I/O',
            'Exception Handling',
            'Data Structures (Lists, Dicts, Sets)',
            'Libraries (NumPy, Pandas)',
            'Web Development (Django/Flask)',
            'APIs & Web Scraping',
            'Testing & Debugging'
        ],
        'javascript': [
            'JavaScript Fundamentals',
            'Variables, Data Types & Operators',
            'ES6+ Features (Arrow Functions, Destructuring)',
            'DOM Manipulation',
            'Event Handling',
            'Async Programming & Callbacks',
            'Promises & Async/Await',
            'Fetch API & AJAX',
            'Modern Frameworks Overview',
            'Node.js Basics',
            'Package Management (npm/yarn)',
            'Testing (Jest, Mocha)'
        ],
        'react': [
            'React Fundamentals & Setup',
            'JSX & Components',
            'Props & State Management',
            'Hooks (useState, useEffect, useContext)',
            'Component Lifecycle',
            'Event Handling & Forms',
            'Conditional Rendering',
            'Lists & Keys',
            'React Router & Navigation',
            'State Management (Context API, Redux)',
            'API Integration & Data Fetching',
            'Performance Optimization'
        ],
        'devops': [
            'Linux Fundamentals & Command Line',
            'Version Control (Git & GitHub)',
            'CI/CD Pipelines',
            'Docker & Containerization',
            'Kubernetes Orchestration',
            'Cloud Platforms (AWS/Azure/GCP)',
            'Infrastructure as Code (Terraform)',
            'Configuration Management (Ansible)',
            'Monitoring & Logging (Prometheus, ELK)',
            'Security Best Practices',
            'Automation & Scripting',
            'Networking Basics'
        ],
        'java': [
            'Java Basics & Syntax',
            'OOP Concepts (Classes, Objects, Inheritance)',
            'Collections Framework',
            'Exception Handling',
            'Multithreading & Concurrency',
            'JDBC & Database Connectivity',
            'Spring Framework Basics',
            'Spring Boot',
            'Maven/Gradle Build Tools',
            'Unit Testing (JUnit, Mockito)',
            'Design Patterns',
            'RESTful Web Services'
        ],
        'nodejs': [
            'Node.js Fundamentals',
            'NPM & Package Management',
            'Express.js Framework',
            'RESTful API Development',
            'Middleware & Routing',
            'Database Integration (MongoDB, PostgreSQL)',
            'Authentication & Authorization (JWT)',
            'Error Handling & Validation',
            'File System Operations',
            'Async Programming',
            'Testing (Mocha/Jest)',
            'Deployment & Production'
        ],
        'generative ai': [
            'Introduction to Generative AI',
            'Large Language Models (LLMs)',
            'Prompt Engineering Techniques',
            'GPT Models & Architecture',
            'Fine-tuning & Transfer Learning',
            'Retrieval Augmented Generation (RAG)',
            'Vector Databases & Embeddings',
            'AI Ethics & Responsible AI',
            'Building AI Applications',
            'LangChain & AI Frameworks',
            'Multimodal AI (Text, Image, Audio)',
            'Deployment & Scaling AI Systems'
        ],
        'machine learning': [
            'Introduction to Machine Learning',
            'Python for ML (NumPy, Pandas)',
            'Data Preprocessing & Feature Engineering',
            'Supervised Learning Algorithms',
            'Unsupervised Learning',
            'Model Evaluation & Validation',
            'Deep Learning Basics',
            'Neural Networks',
            'TensorFlow & PyTorch',
            'Computer Vision',
            'Natural Language Processing',
            'Model Deployment'
        ],
        'data science': [
            'Introduction to Data Science',
            'Python for Data Science',
            'Data Collection & Cleaning',
            'Exploratory Data Analysis (EDA)',
            'Statistical Analysis',
            'Data Visualization (Matplotlib, Seaborn)',
            'Machine Learning Basics',
            'SQL & Databases',
            'Big Data Technologies',
            'Feature Engineering',
            'Model Building & Evaluation',
            'Data Storytelling & Communication'
        ],
        'docker': [
            'Introduction to Containerization',
            'Docker Architecture & Components',
            'Docker Images & Containers',
            'Dockerfile Best Practices',
            'Docker Compose',
            'Container Networking',
            'Volume Management & Data Persistence',
            'Docker Registry & Hub',
            'Multi-stage Builds',
            'Container Security',
            'Docker in Production',
            'Troubleshooting & Debugging'
        ],
        'kubernetes': [
            'Introduction to Kubernetes',
            'Kubernetes Architecture',
            'Pods, Deployments & Services',
            'ConfigMaps & Secrets',
            'Persistent Volumes & Storage',
            'Networking in Kubernetes',
            'Ingress Controllers',
            'Helm Package Manager',
            'Monitoring & Logging',
            'Auto-scaling',
            'Security Best Practices',
            'Production Deployment'
        ],
        'aws': [
            'AWS Fundamentals & Cloud Concepts',
            'IAM (Identity & Access Management)',
            'EC2 (Elastic Compute Cloud)',
            'S3 (Simple Storage Service)',
            'VPC (Virtual Private Cloud)',
            'RDS (Relational Database Service)',
            'Lambda & Serverless',
            'CloudFormation & IaC',
            'CloudWatch Monitoring',
            'Load Balancing & Auto Scaling',
            'Security Best Practices',
            'Cost Optimization'
        ],
        'vue': [
            'Vue.js Fundamentals',
            'Vue Instance & Lifecycle',
            'Template Syntax & Directives',
            'Components & Props',
            'Data Binding & Reactivity',
            'Event Handling',
            'Computed Properties & Watchers',
            'Vue Router',
            'Vuex State Management',
            'Composition API',
            'API Integration',
            'Building & Deployment'
        ],
        'angular': [
            'Angular Fundamentals',
            'TypeScript Basics',
            'Components & Templates',
            'Data Binding',
            'Directives & Pipes',
            'Services & Dependency Injection',
            'Routing & Navigation',
            'Forms (Template & Reactive)',
            'HTTP Client & APIs',
            'RxJS & Observables',
            'State Management (NgRx)',
            'Testing & Deployment'
        ]
    }
    
    tech_lower = technology.lower()
    
    # Check for exact match
    if tech_lower in tech_topics:
        return tech_topics[tech_lower]
    
    # Check for partial match
    for key, topics in tech_topics.items():
        if key in tech_lower or tech_lower in key:
            return topics
    
    # Check for AI/ML related terms
    ai_terms = ['ai', 'artificial intelligence', 'gen ai', 'llm', 'gpt', 'chatgpt']
    if any(term in tech_lower for term in ai_terms):
        return tech_topics['generative ai']
    
    ml_terms = ['ml', 'machine learning', 'deep learning', 'neural network']
    if any(term in tech_lower for term in ml_terms):
        return tech_topics['machine learning']
    
    # Generic fallback with more detail
    return [
        f'Introduction to {technology}',
        f'{technology} Fundamentals & Core Concepts',
        f'Setting Up {technology} Environment',
        f'Basic {technology} Operations',
        f'Intermediate {technology} Techniques',
        f'Advanced {technology} Features',
        f'{technology} Best Practices',
        f'{technology} Project Development',
        f'Testing & Debugging in {technology}',
        f'{technology} Performance Optimization',
        f'{technology} Security Considerations',
        f'Deploying {technology} Applications'
    ]
