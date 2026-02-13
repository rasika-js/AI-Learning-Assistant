import streamlit as st
import difflib
import random

# ---------------- 1. PAGE CONFIG & SESSION STATE ----------------
st.set_page_config(page_title="AI Smart Learning Assistant", layout="centered")

# Initialize Session State to remember practice questions and answers
if "practice_questions" not in st.session_state:
    st.session_state.practice_questions = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""

# ---------------- 2. KNOWLEDGE BASE ----------------
explanations = {
"operating system": "An operating system (OS) is system software that acts as an interface between the user and the computer hardware. It manages hardware resources such as the processor, memory, storage, and input/output devices, and provides a platform for running applications efficiently and securely. Common operating systems include Windows, Linux, macOS, Android, and iOS, which enable users to interact with computers and perform everyday tasks.",
    "dbms": "A Database Management System (DBMS) is software that allows users to create, store, manage, and retrieve data efficiently from a database. It provides a structured way to organize data, ensures data security and integrity, and allows multiple users or applications to access the data at the same time.",
    "data structures": "A data structure is a way of organizing and storing data in a computer so it can be used efficiently. It defines how data elements are arranged, accessed, and modified, allowing programs to perform operations like searching, sorting, inserting, and deleting data effectively. Common data structures include arrays, linked lists, stacks, queues, trees, and graphs, each designed for specific types of tasks and performance needs.",
    "artificial intelligence": "Artificial intelligence (AI) is the ability of computers and machines to perform tasks that usually require human intelligence, such as learning from experience, understanding language, recognizing images, solving problems, and making decisions. Instead of being programmed with only fixed rules, AI systems use data and algorithms to identify patterns and improve their performance over time.",
    "cloud computing": "Cloud computing is the delivery of computing services such as storage, servers, databases, and software over the internet. It allows users to access resources on demand without owning physical hardware, offering scalability, flexibility, and cost efficiency.",
    "computer network": "A computer network is a group of interconnected computers and devices that communicate with each other to share data, resources, and services. Networks enable file sharing, internet access, communication, and collaboration, and can be classified as LAN, MAN, or WAN based on their size and coverage.",
    "cyber security": "Cyber security is the practice of protecting computer systems, networks, and data from unauthorized access, attacks, and damage. It involves techniques such as encryption, firewalls, and authentication to ensure confidentiality, integrity, and availability of information.",
    "input device":"An input device is a hardware component used to enter data and instructions into a computer.Examples include keyboard, mouse, scanner, microphone, and webcam.",
    "output device":"An output device is a hardware component that displays the results of processed data from a computer. Examples include monitor, printer, speaker, and projector.",
    "cpu":"The CPU(Central Processing Unit) is the main processing unit of a computer that performs calculations and controls all operations.It is known as the 'brain of the computer'.",
    "memory unit":"The memory unit stores data, instructions, and results temporarily or permanently for the computer.Examples include RAM and ROM.",
    "storage device":"A storage device is used to store data and programs permanently for future use. Examples include hard disk, SSD, pen drive, and CD/DVD.",
    "system software": "System software includes the programs that manage the computer's hardware and provide a platform for application software (e.g., Windows).",
    "web application":"A web application is a software program that runs on a web browser and is accessed through the internet. Examples include Gmail, Google Docs, and online shopping websites.",
    "programming language":"A programming language is a set of rules and instructions used to write programs that tell a computer what to do. Examples include Python, Java, C, and JavaScript.",
    "computer science":"Computer Science is the study of computers and how they work. It includes programming, software development, and problem-solving using computers. It also deals with algorithms, data, and computer systems.",
    "hardware":"Hardware refers to the physical parts of a computer that can be seen and touched. Examples include the keyboard, mouse, monitor, CPU, and printer.",
    "data":"Data is raw facts and figures that are processed to produce meaningful information. Examples include numbers, text, images, and symbols.",
    "internet":"The Internet is a global network of interconnected computers. It allows users to share information and communicate worldwide.",
    "ram":"RAM (Random Access Memory) is the temporary memory of a computer.It stores data and instructions that are currently being used. Data in RAM is lost when the computer is turned off.",
    "rom":"ROM (Read Only Memory) is permanent memory that stores important instructions. It contains the startup instructions of the computer. Data in ROM is not lost when power is turned off.",
    "information":"Information is processed data that is meaningful and useful. It helps in decision-making.",
}

# -------- QUIZ BANK --------
quiz_bank = {
    "operating system": [
        {"q": "What acts as the interface between the user and computer hardware?", "o": ["CPU", "Operating System", "RAM"], "a": "Operating System"},
        {"q": "Which of these is an example of an open-source OS?", "o": ["Windows", "Linux", "macOS"], "a": "Linux"},
        {"q": "What is the primary goal of an OS?", "o": ["To play music", "To manage system resources", "To browse the web"], "a": "To manage system resources"}
    ],
    "dbms": [
        {"q": "What does DBMS stand for?", "o": ["Data Base Management System", "Digital Base Main System", "Data Binary Management Software"], "a": "Data Base Management System"},
        {"q": "Which language is most commonly used to interact with a DBMS?", "o": ["HTML", "SQL", "Python"], "a": "SQL"},
        {"q": "Which of these is a popular DBMS?", "o": ["Oracle", "Excel", "Notepad"], "a": "Oracle"}
    ],
    "data structures": [
        {"q": "Which data structure follows the LIFO principle?", "o": ["Queue", "Stack", "Linked List"], "a": "Stack"},
        {"q": "Which of these is a non-linear data structure?", "o": ["Array", "Stack", "Tree"], "a": "Tree"},
        {"q": "What is a collection of elements where each element points to the next?", "o": ["Array", "Linked List", "Variable"], "a": "Linked List"}
    ],
    "artificial intelligence": [
        {"q": "What allows AI to learn from experience without being explicitly programmed?", "o": ["Fixed Logic", "Machine Learning", "Manual Entry"], "a": "Machine Learning"},
        {"q": "Which is a common application of AI today?", "o": ["Calculators", "Voice Assistants", "Floppy Disks"], "a": "Voice Assistants"},
        {"q": "AI mimics which human capability?", "o": ["Physical Strength", "Intelligence", "Digestion"], "a": "Intelligence"}
    ],
    "cloud computing": [
        {"q": "What is the delivery of computing services over the internet called?", "o": ["Local Hosting", "Cloud Computing", "Broadcasting"], "a": "Cloud Computing"},
        {"q": "Which of these is a major cloud provider?", "o": ["AWS", "Intel", "Nvidia"], "a": "AWS"},
        {"q": "Storing photos on Google Photos is an example of?", "o": ["Local Storage", "Cloud Storage", "RAM Storage"], "a": "Cloud Storage"}
    ],
    "computer network": [
        {"q": "A network that covers a small area like a home or office is a?", "o": ["WAN", "MAN", "LAN"], "a": "LAN"},
        {"q": "What is the largest network in the world?", "o": ["The Internet", "Intranet", "Ethernet"], "a": "The Internet"},
        {"q": "Which device connects multiple computers in a network?", "o": ["CPU", "Router", "Hard Drive"], "a": "Router"}
    ],
    "cyber security": [
        {"q": "Which process converts readable data into an unreadable format?", "o": ["Deletion", "Encryption", "Formatting"], "a": "Encryption"},
        {"q": "What software is used to block unauthorized network access?", "o": ["Firewall", "Browser", "Word Processor"], "a": "Firewall"},
        {"q": "A 'Strong Password' is a key part of?", "o": ["Hardware Design", "Cyber Security", "Operating Systems"], "a": "Cyber Security"}
    ],
    "input device": [
        {"q": "Which is used to enter text into a computer?", "o": ["Monitor", "Keyboard", "Printer"], "a": "Keyboard"},
        {"q": "Which device is used to capture sound?", "o": ["Speaker", "Microphone", "Webcam"], "a": "Microphone"},
        {"q": "Which is an input device used for gaming?", "o": ["Joystick", "Projector", "Plotter"], "a": "Joystick"}
    ],
    "output device": [
        {"q": "Which device displays the visual output?", "o": ["Scanner", "Monitor", "Mouse"], "a": "Monitor"},
        {"q": "What is used to produce a hard copy of a document?", "o": ["Printer", "Keyboard", "RAM"], "a": "Printer"},
        {"q": "Which device is used to listen to audio?", "o": ["Microphone", "Speakers", "Scanner"], "a": "Speakers"}
    ],
    "cpu": [
        {"q": "What is the CPU often called?", "o": ["The Heart", "The Brain", "The Memory"], "a": "The Brain"},
        {"q": "Which part of the CPU performs mathematical calculations?", "o": ["ALU", "Control Unit", "Registers"], "a": "ALU"},
        {"q": "What does CPU stand for?", "o": ["Central Process Unit", "Central Processing Unit", "Computer Processing Unit"], "a": "Central Processing Unit"}
    ],
    "memory unit": [
        {"q": "Which memory is temporary and volatile?", "o": ["ROM", "RAM", "Hard Disk"], "a": "RAM"},
        {"q": "Where are the startup instructions for a computer stored?", "o": ["RAM", "ROM", "Cache"], "a": "ROM"},
        {"q": "Which memory is faster but smaller than RAM?", "o": ["Cache", "HDD", "SSD"], "a": "Cache"}
    ],
    "storage device": [
        {"q": "Which storage device uses flash memory and is faster than a HDD?", "o": ["Floppy Disk", "SSD", "CD"], "a": "SSD"},
        {"q": "Which is a portable storage device?", "o": ["Internal RAM", "USB Pen Drive", "Motherboard"], "a": "USB Pen Drive"},
        {"q": "A hard disk is an example of?", "o": ["Primary Memory", "Secondary Storage", "Temporary Memory"], "a": "Secondary Storage"}
    ],
    "system software": [
        {"q": "Which of these is system software?", "o": ["MS Word", "Windows 11", "WhatsApp"], "a": "Windows 11"},
        {"q": "What is the main purpose of system software?", "o": ["To write letters", "To manage hardware", "To play games"], "a": "To manage hardware"},
        {"q": "Which is an example of utility software?", "o": ["Antivirus", "Chrome", "Excel"], "a": "Antivirus"}
    ],
    "web application": [
        {"q": "Where do you typically access a web application?", "o": ["In a Browser", "In the BIOS", "On a Desktop without Internet"], "a": "In a Browser"},
        {"q": "Which is an example of a web application?", "o": ["Google Docs", "Notepad", "Calculator"], "a": "Google Docs"},
        {"q": "Web applications require which of the following to function?", "o": ["Printer", "Internet Connection", "Scanner"], "a": "Internet Connection"}
    ],
    "programming language": [
        {"q": "Which is a high-level programming language?", "o": ["Binary", "Python", "Assembly"], "a": "Python"},
        {"q": "What is used to translate high-level code into machine code?", "o": ["Printer", "Compiler", "Keyboard"], "a": "Compiler"},
        {"q": "Which language is commonly used for Android development?", "o": ["HTML", "Java", "CSS"], "a": "Java"}
    ],
    "computer science": [
        {"q": "What is the study of algorithms and computer systems?", "o": ["Biology", "Computer Science", "Geography"], "a": "Computer Science"},
        {"q": "CS focuses on which of the following?", "o": ["Only repair", "Problem-solving with data", "Manual filing"], "a": "Problem-solving with data"},
        {"q": "Which is a core field within CS?", "o": ["Botany", "Software Engineering", "Sculpting"], "a": "Software Engineering"}
    ],
    "hardware": [
        {"q": "What are the physical components of a computer called?", "o": ["Software", "Hardware", "Firmware"], "a": "Hardware"},
        {"q": "Which of these is a piece of hardware?", "o": ["Windows", "Mouse", "Photoshop"], "a": "Mouse"},
        {"q": "Can you touch software?", "o": ["Yes", "No"], "a": "No"}
    ],
    "data": [
        {"q": "What are raw facts and figures called?", "o": ["Information", "Data", "Knowledge"], "a": "Data"},
        {"q": "When data is processed, it becomes?", "o": ["Information", "Noise", "Binary"], "a": "Information"},
        {"q": "Which is an example of data?", "o": ["A weather report", "The number 25", "A final grade"], "a": "The number 25"}
    ],
    "internet": [
        {"q": "What is the 'Network of Networks'?", "o": ["Intranet", "The Internet", "LAN"], "a": "The Internet"},
        {"q": "What is used to identify a website?", "o": ["URL", "CPU", "RAM"], "a": "URL"},
        {"q": "Which protocol is the foundation of the internet?", "o": ["HTTP/HTTPS", "Bluetooth", "NFC"], "a": "HTTP/HTTPS"}
    ],
    "ram": [
        {"q": "What happens to data in RAM when the computer restarts?", "o": ["It is saved", "It is lost", "It moves to the cloud"], "a": "It is lost"},
        {"q": "RAM is also known as?", "o": ["Read Only Memory", "Main Memory", "Secondary Memory"], "a": "Main Memory"},
        {"q": "What does RAM stand for?", "o": ["Random Access Memory", "Ready Action Memory", "Real Always Memory"], "a": "Random Access Memory"}
    ],
    "rom": [
        {"q": "Is ROM volatile or non-volatile?", "o": ["Volatile", "Non-Volatile"], "a": "Non-Volatile"},
        {"q": "What is stored in ROM?", "o": ["User files", "BIOS/Startup instructions", "Browsing history"], "a": "BIOS/Startup instructions"},
        {"q": "Can a standard user easily delete data from ROM?", "o": ["Yes", "No"], "a": "No"}
    ],
    "information": [
        {"q": "What is processed data that is meaningful?", "o": ["Information", "Raw Data", "Noise"], "a": "Information"},
        {"q": "Which helps in decision-making?", "o": ["Raw Data", "Information", "Confusion"], "a": "Information"},
        {"q": "Is a list of student grades sorted by rank 'Data' or 'Information'?", "o": ["Data", "Information"], "a": "Information"}
    ],
    "generic": [
        {"q": "This topic is a branch of which field?", "o": ["Computer Science", "Arts", "Medicine"], "a": "Computer Science"},
        {"q": "Learning this topic helps build?", "o": ["Cooking Skills", "Technical Knowledge", "History Knowledge"], "a": "Technical Knowledge"},
        {"q": "Where is this concept mainly applied?", "o": ["Farms", "Technology and Computing", "Archaeology"], "a": "Technology and Computing"}
    ]
}


# -------- PRACTICE BANK --------
practice_bank = {
    "operating system": [
        "Draw a diagram showing the relationship between User, OS, and Hardware.",
        "Compare and contrast Batch Processing and Time-Sharing systems.",
        "Explain the concept of 'Thrashing' in Virtual Memory.",
        "List four essential functions of a modern Operating System."
    ],
    "dbms": [
        "Explain the difference between DDL and DML commands with examples.",
        "What are the ACID properties in a transaction?",
        "Draw an ER diagram for a simple Library Management System.",
        "Compare SQL vs NoSQL."
    ],
    "generic": [
        "Summarize the importance of this topic in modern computing.",
        "Identify three real-world applications of this concept.",
        "Create a 5-point summary of the key features of this topic.",
        "Explain this topic using a real-world analogy."
    ]
}
# ---------------- 5. THEME & SIDEBAR ----------------
if "dark_mode" not in st.session_state: 
    st.session_state.dark_mode = False

st.sidebar.title("📚 AI Smart Learning")
st.sidebar.toggle("🌙 Dark Mode", key="dark_mode")

# Optimized CSS to fix text visibility
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #0f172a; color: white; }
        p, h1, h2, h3, label { color: white !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; color: #1e293b; }
        p, h1, h2, h3, label { color: #1e293b !important; }
        </style>
        """, unsafe_allow_html=True)

#-------------SIDE BAR-------------

st.sidebar.title("🔎 Knowledge Map")

knowledge_topics = [
    "operating system","DBMS","data structures","artificial intelligence","cloud computing",
    "computer network","cyber security","input device"," output device","cpu","memory unit",
    "storage device", "system software ","web application ","programming language ","computer science "
    ,"hardware","data","internet ","ram","rom","information "

]

for t in knowledge_topics:
    if st.sidebar.button(t):
        st.session_state.topic_input = t

# ---------------- 6. MAIN UI & LOGIC ----------------
st.title("📘 AI Smart Learning Assistant")
st.info("📌 Enter a topic below to get instant explanations, practice, and quizzes.")

topic_input = st.text_input(
    "Enter Topic",
    key="topic_input"
)
level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

col1, col2 = st.columns(2)
with col1: 
    explain_clicked = st.button("Explain Topic")
with col2: 
    practice_clicked = st.button("Generate Practice")

# Main logic must stay within the 'if topic_input' block to avoid errors
if topic_input:
    clean_input = topic_input.lower().strip()
    matches = difflib.get_close_matches(clean_input, list(explanations.keys()), n=1, cutoff=0.3)
    
    if matches:
        matched_topic = matches[0]
        
        # Reset questions if topic changes
        if matched_topic != st.session_state.current_topic:
            st.session_state.practice_questions = None
            st.session_state.current_topic = matched_topic

        # --- A. EXPLANATION SECTION ---
        if explain_clicked:
            st.success(f"Smart Match: **{matched_topic.upper()}**")
            st.subheader("📖 Explanation")
            st.write(explanations[matched_topic])

        # --- B. PRACTICE SECTION ---
        if practice_clicked:
            pool = practice_bank.get(matched_topic, practice_bank["generic"])
            st.session_state.practice_questions = random.sample(pool, min(len(pool), 2))

        if st.session_state.practice_questions:
            st.markdown("---")
            # CORRECTED: Call subheader properly with text
            st.subheader(f"📝 Interactive Practice: {matched_topic.title()}")
            for i, q in enumerate(st.session_state.practice_questions, start=1):
                st.markdown(f"**Q{i}:** {q}")
                st.text_area("Your Response:", key=f"ans_{matched_topic}_{i}")

        # --- C. QUIZ SECTION ---
        st.markdown("---")
        st.subheader(f"🧠 Quiz: {matched_topic.title()}")
        current_quiz = quiz_bank.get(matched_topic, quiz_bank["generic"])
        
        user_responses = []
        for i, item in enumerate(current_quiz):
            user_responses.append(st.radio(f"Q{i+1}: {item['q']}", item['o'], key=f"quiz_{matched_topic}_{i}"))
            
        if st.button("Submit Quiz"):
            score = sum(1 for i, ans in enumerate(user_responses) if ans == current_quiz[i]['a'])
            st.metric("Score", f"{score}/{len(current_quiz)}")
    else:
        st.warning("Topic not found. Try keywords from the sidebar Knowledge Map.")