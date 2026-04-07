from typing import Dict, List, Any
import json
from app.services.scraper_service import get_learning_topics

def calculate_topic_duration(topic: str, skill_level: str) -> int:
    """
    Calculate realistic duration for a topic based on its complexity and skill level
    """
    topic_lower = topic.lower()
    
    # Base duration by skill level
    base_duration = {
        'beginner': 5,
        'intermediate': 4,
        'advanced': 3
    }.get(skill_level, 5)
    
    # Introductory/Basic topics - shorter duration
    if any(word in topic_lower for word in ['introduction', 'basics', 'fundamentals', 'getting started', 'overview', 'what is']):
        return max(2, base_duration - 2)
    
    # Simple/Quick topics - short duration
    if any(word in topic_lower for word in ['syntax', 'variables', 'data types', 'operators', 'hello world']):
        return max(2, base_duration - 2)
    
    # Intermediate topics - medium duration
    if any(word in topic_lower for word in ['functions', 'classes', 'modules', 'packages', 'components', 'hooks']):
        return base_duration
    
    # Complex topics - longer duration
    if any(word in topic_lower for word in ['architecture', 'design patterns', 'advanced', 'optimization', 'performance', 
                                             'security', 'deployment', 'production', 'scaling', 'microservices']):
        return base_duration + 2
    
    # Very complex topics - longest duration
    if any(word in topic_lower for word in ['machine learning', 'deep learning', 'neural networks', 'kubernetes', 
                                             'distributed systems', 'cloud architecture', 'devops pipeline']):
        return base_duration + 3
    
    # Project/Practice topics - medium-long duration
    if any(word in topic_lower for word in ['project', 'building', 'creating', 'developing', 'implementing']):
        return base_duration + 1
    
    # Testing/Debugging topics - medium duration
    if any(word in topic_lower for word in ['testing', 'debugging', 'troubleshooting', 'error handling']):
        return base_duration
    
    # Default to base duration
    return base_duration

def generate_learning_path(technology: str, skill_level: str) -> Dict[str, Any]:
    """
    Generate a structured learning path for a given technology.
    Uses web scraping to get real topics with intelligent duration assignment.
    """
    # Get topics from web scraping
    topics_list = get_learning_topics(technology)
    
    # Adjust number of topics based on skill level
    topic_count = {
        'beginner': min(8, len(topics_list)),
        'intermediate': min(10, len(topics_list)),
        'advanced': len(topics_list)
    }.get(skill_level, 8)
    
    topics_list = topics_list[:topic_count]
    
    # Create subtopics structure with intelligent duration
    subtopics = []
    for topic in topics_list:
        duration = calculate_topic_duration(topic, skill_level)
        subtopics.append({
            "name": topic,
            "duration_days": duration
        })
    
    # Generate daily plan from subtopics
    day = 1
    daily_plan = []
    
    for subtopic in subtopics:
        for day_in_topic in range(subtopic["duration_days"]):
            tasks = generate_daily_tasks(subtopic["name"], day_in_topic, skill_level)
            duration = estimate_daily_duration(subtopic["name"], day_in_topic, skill_level)
            daily_plan.append({
                "day": day,
                "topic": subtopic["name"],
                "day_in_topic": day_in_topic + 1,
                "tasks": tasks,
                "resources": generate_resources(subtopic["name"], technology),
                "estimated_duration": duration
            })
            day += 1
    
    return {
        "subtopics": subtopics,
        "daily_plan": daily_plan,
        "total_days": day - 1
    }

def estimate_daily_duration(topic: str, day_in_topic: int, skill_level: str) -> str:
    """
    Estimate time duration needed to complete daily tasks
    """
    topic_lower = topic.lower()
    
    # Base duration by skill level (in hours)
    base_hours = {
        'beginner': 3.0,
        'intermediate': 2.5,
        'advanced': 2.0
    }.get(skill_level, 3.0)
    
    # Adjust based on day in topic
    if day_in_topic == 0:  # Introduction day
        hours = base_hours - 0.5
    elif day_in_topic in [3, 4, 6]:  # Project/Advanced days
        hours = base_hours + 1.0
    else:
        hours = base_hours
    
    # Adjust for complex topics
    if any(word in topic_lower for word in ['advanced', 'architecture', 'optimization', 'kubernetes', 'microservices']):
        hours += 0.5
    
    # Format duration range
    min_hours = max(1.5, hours - 0.5)
    max_hours = hours + 0.5
    
    # Convert to readable format
    if min_hours == int(min_hours) and max_hours == int(max_hours):
        return f"{int(min_hours)}-{int(max_hours)} hours"
    else:
        return f"{min_hours:.1f}-{max_hours:.1f} hours"

def generate_daily_tasks(topic: str, day_in_topic: int, skill_level: str) -> List[str]:
    """
    Generate specific daily tasks for a topic with concrete learning objectives
    """
    # Try to get technology-specific tasks first
    specific_tasks = get_technology_specific_tasks(topic, day_in_topic)
    if specific_tasks:
        return specific_tasks
    
    # Extract key concepts from topic name
    topic_lower = topic.lower()
    
    # Determine what to focus on based on keywords in the topic
    is_intro = any(word in topic_lower for word in ['introduction', 'basics', 'fundamentals', 'getting started'])
    is_advanced = any(word in topic_lower for word in ['advanced', 'optimization', 'production', 'scaling'])
    
    # Day 1: Introduction and Fundamentals
    if day_in_topic == 0:
        if is_intro:
            return [
                f"📚 Learn what {topic} is and why it matters in modern development",
                f"🎯 Understand the core problems {topic} solves",
                f"📖 Study the key terminology and concepts",
                f"🔍 Explore real-world use cases and applications",
                f"⚙️ Set up your environment and install necessary tools"
            ]
        else:
            return [
                f"📚 Read comprehensive overview of {topic}",
                f"🎥 Watch introductory tutorial covering {topic} basics",
                f"📝 Document key concepts, definitions, and terminology",
                f"💡 Understand when and why to use {topic}",
                f"🔧 Prepare your development environment"
            ]
    
    # Day 2: Hands-on Basics
    elif day_in_topic == 1:
        return [
            f"💻 Follow step-by-step tutorial for {topic}",
            f"✍️ Write your first working example",
            f"🔨 Practice basic commands and operations",
            f"🧪 Experiment with different configurations",
            f"📊 Compare your results with expected outcomes"
        ]
    
    # Day 3: Deep Dive and Practice
    elif day_in_topic == 2:
        return [
            f"🎯 Complete 5-7 hands-on exercises",
            f"🔬 Explore different approaches and patterns",
            f"📚 Study best practices and common mistakes",
            f"💪 Solve coding challenges on practice platforms",
            f"🤔 Analyze and debug sample code"
        ]
    
    # Day 4: Building Projects
    elif day_in_topic == 3:
        return [
            f"🚀 Design a mini-project using {topic}",
            f"📐 Plan your project architecture and structure",
            f"💻 Implement core features step-by-step",
            f"🔍 Research industry best practices",
            f"📝 Document your code and decisions"
        ]
    
    # Day 5: Advanced Concepts
    elif day_in_topic == 4:
        if is_advanced:
            return [
                f"🎓 Master advanced techniques in {topic}",
                f"⚡ Learn performance optimization strategies",
                f"🛡️ Implement security best practices",
                f"🔄 Refactor code for production readiness",
                f"📊 Benchmark and measure improvements"
            ]
        else:
            return [
                f"🎓 Explore advanced features of {topic}",
                f"🔬 Study performance optimization techniques",
                f"🛡️ Learn security considerations",
                f"🔄 Refactor and improve previous code",
                f"💡 Understand design patterns and architecture"
            ]
    
    # Day 6: Integration and Testing
    elif day_in_topic == 5:
        return [
            f"🧪 Write unit tests for your {topic} code",
            f"🔗 Integrate with other tools and technologies",
            f"📦 Explore related libraries and frameworks",
            f"🐛 Practice debugging complex scenarios",
            f"✅ Validate your understanding with quizzes"
        ]
    
    # Day 7+: Mastery and Real-world Application
    else:
        return [
            f"🏆 Build a complete production-ready project",
            f"🌐 Deploy your application to cloud/production",
            f"📚 Study real-world case studies and implementations",
            f"💬 Engage with community forums and discussions",
            f"🎯 Solve advanced challenges and contribute to open-source"
        ]

def get_technology_specific_tasks(topic: str, day_in_topic: int) -> List[str]:
    """
    Get technology-specific tasks based on the topic - complete 7-day schedules
    """
    topic_lower = topic.lower()
    
    # Docker/Containerization specific tasks
    if 'docker' in topic_lower or 'container' in topic_lower:
        tasks_by_day = {
            0: [
                "📚 Learn what containers are and how they differ from VMs",
                "🎯 Understand Docker architecture (images, containers, registry)",
                "📖 Study Docker use cases and benefits in modern development",
                "🔍 Explore Docker Hub and browse popular official images",
                "⚙️ Install Docker Desktop and verify installation with hello-world"
            ],
            1: [
                "💻 Run your first containers (nginx, ubuntu, alpine)",
                "✍️ Master basic Docker commands (run, ps, stop, rm, logs)",
                "🔨 Practice pulling images and managing containers",
                "🧪 Experiment with container ports and networking basics",
                "📊 Inspect running containers and understand container lifecycle"
            ],
            2: [
                "🎯 Create your first Dockerfile from scratch",
                "🔬 Build custom Docker images with different base images",
                "📚 Learn Dockerfile instructions (FROM, RUN, COPY, CMD, EXPOSE)",
                "💪 Understand image layers and caching mechanisms",
                "🤔 Debug image build issues and optimize build time"
            ],
            3: [
                "🚀 Build a multi-container application with Docker Compose",
                "📐 Design docker-compose.yml for web app + database",
                "💻 Implement volume mounting for data persistence",
                "🔍 Configure environment variables and secrets",
                "📝 Document your Docker setup and architecture"
            ],
            4: [
                "🎓 Master advanced Dockerfile techniques (multi-stage builds)",
                "⚡ Optimize image size and build performance",
                "🛡️ Implement Docker security best practices",
                "🔄 Set up health checks and restart policies",
                "📊 Use Docker networks for container communication"
            ],
            5: [
                "🧪 Test your containers and write integration tests",
                "🔗 Integrate Docker with CI/CD pipelines",
                "📦 Push images to Docker Hub or private registry",
                "🐛 Debug container issues using logs and exec",
                "✅ Review Docker best practices checklist"
            ],
            6: [
                "🏆 Build a complete microservices project with Docker",
                "🌐 Deploy containers to cloud (AWS ECS, Azure, GCP)",
                "📚 Study production Docker patterns and anti-patterns",
                "💬 Explore Docker Swarm or Kubernetes for orchestration",
                "🎯 Contribute to Dockerized open-source projects"
            ]
        }
        return tasks_by_day.get(day_in_topic)
    
    # Kubernetes specific tasks
    elif 'kubernetes' in topic_lower or 'k8s' in topic_lower:
        tasks_by_day = {
            0: [
                "📚 Learn Kubernetes architecture (control plane, nodes, etcd)",
                "🎯 Understand pods, deployments, services, and namespaces",
                "📖 Study why Kubernetes is essential for container orchestration",
                "🔍 Explore Kubernetes use cases in production environments",
                "⚙️ Install kubectl, minikube, and set up local cluster"
            ],
            1: [
                "💻 Create your first pod using kubectl and YAML",
                "✍️ Master kubectl commands (get, describe, logs, exec)",
                "🔨 Deploy a simple application with a deployment",
                "🧪 Scale deployments and observe pod behavior",
                "📊 Understand pod lifecycle and container states"
            ],
            2: [
                "🎯 Create and expose services (ClusterIP, NodePort, LoadBalancer)",
                "🔬 Configure ConfigMaps and Secrets for configuration",
                "📚 Learn about labels, selectors, and annotations",
                "💪 Practice service discovery and DNS in Kubernetes",
                "🤔 Debug networking issues between pods"
            ],
            3: [
                "🚀 Build a multi-tier application (frontend, backend, database)",
                "📐 Design deployment manifests with proper resource limits",
                "💻 Implement persistent volumes and storage classes",
                "🔍 Configure liveness and readiness probes",
                "📝 Document your Kubernetes architecture"
            ],
            4: [
                "🎓 Master Ingress controllers for external access",
                "⚡ Learn Horizontal Pod Autoscaling (HPA)",
                "🛡️ Implement RBAC and security policies",
                "🔄 Set up rolling updates and rollback strategies",
                "📊 Monitor cluster health with kubectl top and metrics"
            ],
            5: [
                "🧪 Write Helm charts for application packaging",
                "🔗 Integrate Kubernetes with CI/CD pipelines",
                "📦 Deploy applications using GitOps (ArgoCD/Flux)",
                "🐛 Debug complex issues using logs and events",
                "✅ Implement health checks and monitoring"
            ],
            6: [
                "🏆 Deploy a production-grade application to Kubernetes",
                "🌐 Set up monitoring with Prometheus and Grafana",
                "📚 Study production patterns (blue-green, canary deployments)",
                "💬 Explore service mesh (Istio, Linkerd)",
                "🎯 Prepare for CKA/CKAD certification"
            ]
        }
        return tasks_by_day.get(day_in_topic)
    
    # Generative AI / LLM specific tasks
    elif 'generative ai' in topic_lower or 'llm' in topic_lower or 'large language' in topic_lower:
        tasks_by_day = {
            0: [
                "📚 Learn what Generative AI is and how LLMs work",
                "🎯 Understand transformers, attention mechanisms, and tokens",
                "📖 Study popular models (GPT-4, Claude, Gemini, Llama)",
                "🔍 Explore real-world Gen AI applications and use cases",
                "⚙️ Sign up for OpenAI/Anthropic API and get API keys"
            ],
            1: [
                "💻 Make your first API call to GPT-4 or Claude",
                "✍️ Learn prompt engineering fundamentals",
                "🔨 Experiment with system prompts and user messages",
                "🧪 Test different temperature and max_tokens settings",
                "📊 Analyze response quality and token usage"
            ],
            2: [
                "🎯 Master advanced prompt engineering techniques",
                "🔬 Practice few-shot, zero-shot, and chain-of-thought prompting",
                "📚 Study prompt patterns (role-playing, step-by-step reasoning)",
                "💪 Build a conversational chatbot with context memory",
                "🤔 Debug and improve prompt responses iteratively"
            ],
            3: [
                "🚀 Build a RAG (Retrieval Augmented Generation) system",
                "📐 Design vector database integration (Pinecone, Weaviate)",
                "💻 Implement document chunking and embedding generation",
                "🔍 Create semantic search for knowledge retrieval",
                "📝 Document your RAG architecture and flow"
            ],
            4: [
                "🎓 Learn about fine-tuning and model customization",
                "⚡ Optimize LLM performance and reduce latency",
                "🛡️ Implement content filtering and safety measures",
                "🔄 Handle rate limits and implement retry logic",
                "📊 Monitor costs and token usage in production"
            ],
            5: [
                "🧪 Test your AI application with various edge cases",
                "🔗 Integrate LLMs with external tools (function calling)",
                "📦 Use LangChain or LlamaIndex for complex workflows",
                "🐛 Debug hallucinations and improve accuracy",
                "✅ Implement evaluation metrics for AI responses"
            ],
            6: [
                "🏆 Build a complete AI-powered application",
                "🌐 Deploy your LLM application to production",
                "📚 Study AI ethics, bias, and responsible AI practices",
                "💬 Explore multi-modal AI (text, image, audio)",
                "🎯 Contribute to open-source AI projects"
            ]
        }
        return tasks_by_day.get(day_in_topic)
    
    # Prompt Engineering specific tasks
    elif 'prompt engineering' in topic_lower or 'prompt' in topic_lower:
        tasks_by_day = {
            0: [
                "📚 Learn what prompt engineering is and why it matters",
                "🎯 Understand how LLMs interpret and respond to prompts",
                "📖 Study the anatomy of effective prompts",
                "🔍 Explore prompt engineering use cases and applications",
                "⚙️ Set up access to multiple LLMs for testing"
            ],
            1: [
                "💻 Write your first structured prompts with clear instructions",
                "✍️ Practice basic prompt patterns (instruction, context, examples)",
                "🔨 Experiment with different prompt formats",
                "🧪 Test prompt variations and compare outputs",
                "📊 Analyze what makes prompts effective"
            ],
            2: [
                "🎯 Master few-shot learning with examples",
                "🔬 Practice zero-shot prompting for new tasks",
                "📚 Learn chain-of-thought (CoT) prompting",
                "💪 Build prompts for complex reasoning tasks",
                "🤔 Debug prompts that produce inconsistent results"
            ],
            3: [
                "🚀 Create a prompt library for common tasks",
                "📐 Design role-based prompts (expert personas)",
                "💻 Implement prompt templates with variables",
                "🔍 Optimize prompts for specific domains",
                "📝 Document your prompt engineering best practices"
            ],
            4: [
                "🎓 Learn advanced techniques (self-consistency, tree-of-thought)",
                "⚡ Optimize prompts for speed and token efficiency",
                "🛡️ Implement prompt injection prevention",
                "🔄 Create iterative refinement workflows",
                "📊 Measure prompt performance with metrics"
            ],
            5: [
                "🧪 A/B test different prompt strategies",
                "🔗 Integrate prompts with external data sources",
                "📦 Build prompt chains for multi-step tasks",
                "🐛 Debug edge cases and handle errors gracefully",
                "✅ Create evaluation criteria for prompt quality"
            ],
            6: [
                "🏆 Build a complete prompt-powered application",
                "🌐 Deploy production-ready prompts with versioning",
                "📚 Study real-world prompt engineering case studies",
                "💬 Share your prompts with the community",
                "🎯 Master prompt engineering for specific industries"
            ]
        }
        return tasks_by_day.get(day_in_topic)
    
    # React Components specific tasks
    elif 'react' in topic_lower and ('component' in topic_lower or 'jsx' in topic_lower):
        tasks_by_day = {
            0: [
                "📚 Learn what React components are and component-based architecture",
                "🎯 Understand functional vs class components",
                "📖 Study JSX syntax, rules, and expressions",
                "🔍 Explore component composition and reusability",
                "⚙️ Set up React project with Vite or Create React App"
            ],
            1: [
                "💻 Create your first functional components",
                "✍️ Practice JSX syntax and embedding expressions",
                "🔨 Pass props between parent and child components",
                "🧪 Build a simple component hierarchy",
                "📊 Inspect components with React DevTools"
            ],
            2: [
                "🎯 Master props validation with PropTypes",
                "🔬 Learn props destructuring and default props",
                "📚 Study component composition patterns",
                "💪 Build reusable UI components (Button, Card, Input)",
                "🤔 Debug props flow and component rendering"
            ],
            3: [
                "🚀 Build a multi-component application (Todo app, Dashboard)",
                "📐 Design component structure and data flow",
                "💻 Implement conditional rendering techniques",
                "🔍 Handle lists and keys properly",
                "📝 Document component APIs and usage"
            ],
            4: [
                "🎓 Learn component lifecycle and side effects",
                "⚡ Optimize component performance (React.memo, useMemo)",
                "🛡️ Implement error boundaries for error handling",
                "🔄 Create higher-order components (HOCs)",
                "📊 Profile components and identify bottlenecks"
            ],
            5: [
                "🧪 Write tests for components (Jest, React Testing Library)",
                "🔗 Integrate components with state management",
                "📦 Build a component library with Storybook",
                "🐛 Debug complex component interactions",
                "✅ Follow React best practices and patterns"
            ],
            6: [
                "🏆 Build a production-ready component library",
                "🌐 Publish components to npm registry",
                "📚 Study advanced patterns (render props, compound components)",
                "💬 Contribute to React open-source projects",
                "🎯 Master React component design principles"
            ]
        }
        return tasks_by_day.get(day_in_topic)
    
    # Python Basics specific tasks
    elif 'python' in topic_lower and ('basic' in topic_lower or 'fundamental' in topic_lower or 'syntax' in topic_lower):
        tasks_by_day = {
            0: [
                "📚 Learn Python syntax, indentation, and code structure",
                "🎯 Understand variables, data types (int, float, str, bool)",
                "📖 Study Python's philosophy and use cases",
                "🔍 Explore Python REPL and interactive mode",
                "⚙️ Install Python, set up IDE (VS Code, PyCharm)"
            ],
            1: [
                "💻 Write your first Python programs (Hello World, calculator)",
                "✍️ Practice with operators (arithmetic, comparison, logical)",
                "🔨 Work with strings (concatenation, formatting, methods)",
                "🧪 Experiment with type conversion and casting",
                "📊 Use print() and input() for user interaction"
            ],
            2: [
                "🎯 Master control flow (if/elif/else statements)",
                "🔬 Learn loops (for, while) and iteration",
                "📚 Study break, continue, and pass statements",
                "💪 Solve 10+ practice problems on conditionals and loops",
                "🤔 Debug common syntax errors and logic issues"
            ],
            3: [
                "🚀 Build mini-projects (number guessing game, calculator)",
                "📐 Design program logic with flowcharts",
                "💻 Implement input validation and error handling",
                "🔍 Learn about code organization and comments",
                "📝 Document your code with docstrings"
            ],
            4: [
                "🎓 Learn about functions and code reusability",
                "⚡ Master function parameters and return values",
                "🛡️ Understand scope (local vs global variables)",
                "🔄 Practice with built-in functions",
                "📊 Write modular, reusable code"
            ],
            5: [
                "🧪 Test your code with different inputs",
                "🔗 Import and use Python standard library modules",
                "📦 Organize code into multiple files",
                "🐛 Debug using print statements and debugger",
                "✅ Follow PEP 8 style guidelines"
            ],
            6: [
                "🏆 Build a complete beginner project (text-based game)",
                "🌐 Share your code on GitHub",
                "📚 Study Python best practices and idioms",
                "💬 Join Python communities and forums",
                "🎯 Prepare for intermediate Python topics"
            ]
        }
        return tasks_by_day.get(day_in_topic)
    
    return None

def generate_resources(topic: str, technology: str) -> List[Dict[str, str]]:
    """
    Generate specific learning resources with real URLs for a topic
    """
    # Clean up topic name for better resource suggestions
    topic_clean = topic.replace('(', '').replace(')', '').strip()
    tech_clean = technology.replace(' ', '+')
    topic_url = topic_clean.replace(' ', '+')
    
    resources = [
        {
            "type": "📚 Official Documentation",
            "title": f"{technology} Documentation",
            "description": f"Official docs and guides for {topic_clean}",
            "url": f"https://www.google.com/search?q={tech_clean}+{topic_url}+official+documentation"
        },
        {
            "type": "🎥 Video Tutorial",
            "title": f"{topic_clean} - Complete Tutorial",
            "description": f"Step-by-step video guide with examples",
            "url": f"https://www.youtube.com/results?search_query={tech_clean}+{topic_url}+tutorial+complete+guide"
        },
        {
            "type": "📖 Reference Documents",
            "title": f"Multiple Learning Resources",
            "description": f"W3Schools, GeeksforGeeks, MDN, and more",
            "url": "multiple",  # Special marker for multiple URLs
            "urls": [
                {
                    "name": "W3Schools",
                    "url": f"https://www.google.com/search?q=site:w3schools.com+{tech_clean}+{topic_url}"
                },
                {
                    "name": "GeeksforGeeks",
                    "url": f"https://www.google.com/search?q=site:geeksforgeeks.org+{tech_clean}+{topic_url}"
                },
                {
                    "name": "MDN Web Docs",
                    "url": f"https://www.google.com/search?q=site:developer.mozilla.org+{tech_clean}+{topic_url}"
                },
                {
                    "name": "Stack Overflow",
                    "url": f"https://stackoverflow.com/search?q={tech_clean}+{topic_url}"
                },
                {
                    "name": "Dev.to",
                    "url": f"https://dev.to/search?q={tech_clean}+{topic_url}"
                }
            ]
        },
        {
            "type": "🎯 Quiz & Assessment",
            "title": f"Test Your Knowledge",
            "description": f"Take quiz on {topic_clean} concepts",
            "url": f"https://www.google.com/search?q={tech_clean}+{topic_url}+quiz+test+assessment+questions"
        }
    ]
    
    return resources
