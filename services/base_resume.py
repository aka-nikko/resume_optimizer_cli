from models.schemas import ResumeOutput


BASE_RESUME = ResumeOutput(
    summary=(
        "**Embedded Software Engineer** with 2.5+ years of experience building real-time **automotive systems** "
        "using **C/C++**, specializing in **camera pipelines**, **performance optimization**, and **low-level debugging** "
        "on **QNX-based systems**. Experienced in designing **modular, platform agnostic architectures** and "
        "debugging complex system-level issues. Additional experience in backend and **full-stack development** "
        "with a focus on scalable, production-ready systems."
    ),

    experiences=[
        [
            "Developed **real-time camera pipeline** and **ADAS** related features for BMW systems on **QNX-based HLOS**.",
            "Optimized **C/C++** modules to reduce **latency** and **memory footprint** in **performance-critical embedded environments**.",
            "Built and deployed applications on **QNX**, handling **cross-compilation** and integration with **system-level services**."
        ],
        [
            "Delivered **production-grade camera features** under strict latency and reliability constraints in **embedded systems**.",
            "Enhanced **CI/CD pipelines** with automated validation, improving release quality, and reducing regression.",
            "Diagnosed and resolved cross-module system issues in complex embedded workflows."
        ],
        [
            "Strengthened fundamentals in **C/C++**, **memory management**, **debugging**, and **performance optimization**.",
            "Worked in **Agile** teams using **Git** workflows and industry-standard development practices."
        ],
        [
            "Developed an end-to-end **web application** using **Django** and **MySQL** with secure authentication and role-based access control.",
            "Designed scalable backend logic and implemented **admin-driven workflows**."
        ],
        [
            "Contributed to **HimSabe**, a real-time vehicle tracking system with responsive UI and backend integration.",
            "Integrated frontend with **Spring Boot** services and **MySQL** for seamless data flow."
        ]
    ],

    skills={
        "Programming Languages": ["C", "C++", "Python", "Java", "JavaScript", "SQL"],
        "Embedded & Automotive": ["QNX", "Linux", "Embedded Systems", "Automotive Software", "ADAS", "AUTOSAR", "Camera Systems", "IPC",
                                  "Multithreading", "Memory Management", "Performance Optimization", "Debugging", "Cross Compilation", "Real-Time Systems"],
        "Software Engineering": ["Data Structures", "Algorithms", "Low-Level Design", "Design Patterns", "OOPs", "Git", "CI/CD", "Agile Development"],
        "Backend & Full Stack": ["Django", "Flask", "FastAPI", "Spring Boot", "React", "Node.js", "REST APIs", "MySQL", "PostgreSQL"],
        "AI & Automation": ["OpenAI API", "Hugging Face", "LLM Fine-Tuning", "Selenium", "Playwright", "FFmpeg", "NumPy", "Pandas"]
    },

    projects=[
        [
            "Built a **Windows-based** tracker with **encrypted local storage** and low runtime overhead.",
            "Processed user activity data and generated **AI-based daily summaries** using **OpenAI API**."
        ],
        [
            "Fine-tuned **DialoGPT** on a custom dataset, handling **data preprocessing**, **tokenization**, and **training**.",
            "Improved response relevance and contextual understanding through model tuning."
        ],
        [
            "Built an end-to-end automation pipeline for **content scraping**, **TTS**, **video generation**, and **publishing**.",
            "Integrated multiple APIs and tools to create a **modular and scalable workflow**."
        ],
        [
            "Developed a full-featured secure **CMS** with **role-based authentication** and **content publishing workflows**.",
            "Designed scalable backend architecture and responsive frontend."
        ]
    ]
)