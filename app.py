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
    "Operating System": "An operating system (OS) is system software that acts as an interface between the user and the computer hardware. It manages hardware resources such as the processor, memory, storage, and input/output devices, and provides a platform for running applications efficiently and securely. Common operating systems include Windows, Linux, macOS, Android, and iOS.",
    "DBMS": "A Database Management System (DBMS) is software that allows users to create, store, manage, and retrieve data efficiently from a database. It provides a structured way to organize data, ensures data security and integrity, and allows multiple users or applications to access the data at the same time.",
    "Data Structures": "A data structure is a way of organizing and storing data in a computer so it can be used efficiently. It defines how data elements are arranged, accessed, and modified, allowing programs to perform operations like searching, sorting, inserting, and deleting data effectively. Common data structures include arrays, linked lists.",
    "Artificial Intelligence": "Artificial intelligence (AI) is the ability of computers and machines to perform tasks that usually require human intelligence, such as learning from experience, understanding language, recognizing images, solving problems, and making decisions. Instead of being programmed with only fixed rules, AI systems use data and algorithms.",
    "Cloud Computing": "Cloud computing is the delivery of computing services such as storage, servers, databases, and software over the internet. It allows users to access resources on demand without owning physical hardware, offering scalability, flexibility, and cost efficiency.",
    "Computer Network": "A computer network is a group of interconnected computers and devices that communicate with each other to share data, resources, and services. Networks enable file sharing, internet access, communication, and collaboration, and can be classified as LAN, MAN, or WAN based on their size and coverage.",
    "Cyber Security": "Cyber security is the practice of protecting computer systems, networks, and data from unauthorized access, attacks, and damage. It involves techniques such as encryption, firewalls, and authentication to ensure confidentiality, integrity, and availability of information.",
    "Input Device":"An input device is a hardware component used to enter data and instructions into a computer. It allows users to communicate with the computer. Input devices help in sending information for processing. Examples of input devices are keyboard, mouse, scanner, microphone, and webcam. Without input devices, users cannot give commands to the computer.",
    "Output Device":"An output device is a hardware component used to display or produce the results of processed data. It shows the information in a form that users can understand. Output devices help in presenting the final result of the computer's work. Examples of output devices are monitor, printer, speaker, and projector. Without output devices, users cannot see or hear the results.",
    "CPU":"The CPU(Central Processing Unit) is the main part of a computer that performs all processing tasks. It is known as the “brain of the computer” because it controls and manages all operations. The CPU executes instructions, performs calculations, and processes data given by the user.",
    "Memory Unit":"A memory unit is a part of the computer that stores data, instructions, and information. It holds information either temporarily or permanently so that the computer can process it when needed. The memory unit plays an important role in the speed and performance of a computer. Examples of memory units include RAM, ROM, hard disk, and pen drive.",
    "Storage Device":"A storage device is a hardware component used to store data, information, and programs for future use. It helps in saving files permanently or temporarily. Storage devices allow users to access their data whenever needed. Examples of storage devices are hard disk, pen drive, CD, DVD, and memory card.",
    "System Software": "System software is a type of software that controls and manages the computer hardware. It acts as a bridge between the user and the computer. System software helps the computer to start, run programs, and perform basic functions smoothly. An example of system software is the operating system.",
    "Web Application":"A web application is a software program that runs on a web browser and is accessed through the internet. Examples include Gmail, Google Docs, and online shopping websites.",
    "Programming Language":"A programming language is a set of rules and instructions used to write programs that tell a computer what to do. Examples include Python, Java, C, and JavaScript.",
    "Computer Science":"Computer Science is the study of computers and how they work. It includes programming, software development, and problem-solving using computers. It also deals with algorithms, data, and computer systems.",
    "Hardware":"Hardware refers to the physical parts of a computer that we can see and touch. It includes devices like the keyboard, mouse, monitor, CPU, printer, and hard disk. Hardware helps the computer to perform input, processing, storage, and output operations. Without hardware, a computer system cannot function",
    "Data":"Data are raw facts and figures that have not yet been processed or organized. They can be numbers, words, symbols, or images collected for reference or analysis. By themselves, data may not have clear meaning, but when they are arranged and processed, they become useful information.",
    "Internet":"The Internet is a global network of interconnected computers that communicate and share information with each other. It allows people to access websites, send emails, watch videos, and exchange data from anywhere in the world. The Internet helps in communication, education, business, and entertainment by connecting millions of users worldwide.",
    "RAM":"RAM is a temporary memory of a computer used to store data and instructions that are currently being used. It helps the CPU to access data quickly, which increases the speed and performance of the computer. RAM is volatile memory, which means the data is lost when the power is turned off. The more RAM a computer has, the faster it can perform multiple tasks.",
    "ROM":"ROM (Read Only Memory) is a permanent memory of a computer used to store important instructions required to start the computer. It contains the basic input/output system (BIOS) and other essential programs. ROM is non-volatile memory, which means the data is not lost even when the power is turned off. It helps the computer to boot and function properly.",
    "Information":"Information is processed and organized data that has meaning and usefulness. When raw facts, numbers, or symbols are arranged and understood properly, they become information. Information helps people to gain knowledge, make decisions, and understand situations clearly.",
}

# -------- QUIZ BANK --------
quiz_bank = {
    "Operating System": [
        {"q": "What acts as the interface between the user and computer hardware?", "o": ["CPU", "Operating System", "RAM"], "a": "Operating System"},
        {"q": "Which of these is an example of an open-source OS?", "o": ["Windows", "Linux", "macOS"], "a": "Linux"},
        {"q": "What is the primary goal of an OS?", "o": ["To play music", "To manage system resources", "To browse the web"], "a": "To manage system resources"}
    ],
    "DBMS": [
        {"q": "What does DBMS stand for?", "o": ["Data Base Management System", "Digital Base Main System", "Data Binary Management Software"], "a": "Data Base Management System"},
        {"q": "Which language is most commonly used to interact with a DBMS?", "o": ["HTML", "SQL", "Python"], "a": "SQL"},
        {"q": "Which of these is a popular DBMS?", "o": ["Oracle", "Excel", "Notepad"], "a": "Oracle"}
    ],
    "Data Structures": [
        {"q": "Which data structure follows the LIFO principle?", "o": ["Queue", "Stack", "Linked List"], "a": "Stack"},
        {"q": "Which of these is a non-linear data structure?", "o": ["Array", "Stack", "Tree"], "a": "Tree"},
        {"q": "What is a collection of elements where each element points to the next?", "o": ["Array", "Linked List", "Variable"], "a": "Linked List"}
    ],
    "Artificial Intelligence": [
        {"q": "What allows AI to learn from experience without being explicitly programmed?", "o": ["Fixed Logic", "Machine Learning", "Manual Entry"], "a": "Machine Learning"},
        {"q": "Which is a common application of AI today?", "o": ["Calculators", "Voice Assistants", "Floppy Disks"], "a": "Voice Assistants"},
        {"q": "AI mimics which human capability?", "o": ["Physical Strength", "Intelligence", "Digestion"], "a": "Intelligence"}
    ],
    "Cloud Computing": [
        {"q": "What is the delivery of computing services over the internet called?", "o": ["Local Hosting", "Cloud Computing", "Broadcasting"], "a": "Cloud Computing"},
        {"q": "Which of these is a major cloud provider?", "o": ["AWS", "Intel", "Nvidia"], "a": "AWS"},
        {"q": "Storing photos on Google Photos is an example of?", "o": ["Local Storage", "Cloud Storage", "RAM Storage"], "a": "Cloud Storage"}
    ],
    "Computer Network": [
        {"q": "A network that covers a small area like a home or office is a?", "o": ["WAN", "MAN", "LAN"], "a": "LAN"},
        {"q": "What is the largest network in the world?", "o": ["The Internet", "Intranet", "Ethernet"], "a": "The Internet"},
        {"q": "Which device connects multiple computers in a network?", "o": ["CPU", "Router", "Hard Drive"], "a": "Router"}
    ],
    "Cyber Security": [
        {"q": "Which process converts readable data into an unreadable format?", "o": ["Deletion", "Encryption", "Formatting"], "a": "Encryption"},
        {"q": "What software is used to block unauthorized network access?", "o": ["Firewall", "Browser", "Word Processor"], "a": "Firewall"},
        {"q": "A 'Strong Password' is a key part of?", "o": ["Hardware Design", "Cyber Security", "Operating Systems"], "a": "Cyber Security"}
    ],
    "Input Device": [
        {"q": "Which is used to enter text into a computer?", "o": ["Monitor", "Keyboard", "Printer"], "a": "Keyboard"},
        {"q": "Which device is used to capture sound?", "o": ["Speaker", "Microphone", "Webcam"], "a": "Microphone"},
        {"q": "Which is an input device used for gaming?", "o": ["Joystick", "Projector", "Plotter"], "a": "Joystick"}
    ],
    "Output Device": [
        {"q": "Which device displays the visual output?", "o": ["Scanner", "Monitor", "Mouse"], "a": "Monitor"},
        {"q": "What is used to produce a hard copy of a document?", "o": ["Printer", "Keyboard", "RAM"], "a": "Printer"},
        {"q": "Which device is used to listen to audio?", "o": ["Microphone", "Speakers", "Scanner"], "a": "Speakers"}
    ],
    "CPU": [
        {"q": "What is the CPU often called?", "o": ["The Heart", "The Brain", "The Memory"], "a": "The Brain"},
        {"q": "Which part of the CPU performs mathematical calculations?", "o": ["ALU", "Control Unit", "Registers"], "a": "ALU"},
        {"q": "What does CPU stand for?", "o": ["Central Process Unit", "Central Processing Unit", "Computer Processing Unit"], "a": "Central Processing Unit"}
    ],
    "Memory Unit": [
        {"q": "Which memory is temporary and volatile?", "o": ["ROM", "RAM", "Hard Disk"], "a": "RAM"},
        {"q": "Where are the startup instructions for a computer stored?", "o": ["RAM", "ROM", "Cache"], "a": "ROM"},
        {"q": "Which memory is faster but smaller than RAM?", "o": ["Cache", "HDD", "SSD"], "a": "Cache"}
    ],
    "Storage Device": [
        {"q": "Which storage device uses flash memory and is faster than a HDD?", "o": ["Floppy Disk", "SSD", "CD"], "a": "SSD"},
        {"q": "Which is a portable storage device?", "o": ["Internal RAM", "USB Pen Drive", "Motherboard"], "a": "USB Pen Drive"},
        {"q": "A hard disk is an example of?", "o": ["Primary Memory", "Secondary Storage", "Temporary Memory"], "a": "Secondary Storage"}
    ],
    "System Software": [
        {"q": "Which of these is system software?", "o": ["MS Word", "Windows 11", "WhatsApp"], "a": "Windows 11"},
        {"q": "What is the main purpose of system software?", "o": ["To write letters", "To manage hardware", "To play games"], "a": "To manage hardware"},
        {"q": "Which is an example of utility software?", "o": ["Antivirus", "Chrome", "Excel"], "a": "Antivirus"}
    ],
    "Web Application": [
        {"q": "Where do you typically access a web application?", "o": ["In a Browser", "In the BIOS", "On a Desktop without Internet"], "a": "In a Browser"},
        {"q": "Which is an example of a web application?", "o": ["Google Docs", "Notepad", "Calculator"], "a": "Google Docs"},
        {"q": "Web applications require which of the following to function?", "o": ["Printer", "Internet Connection", "Scanner"], "a": "Internet Connection"}
    ],
    "Programming Language": [
        {"q": "Which is a high-level programming language?", "o": ["Binary", "Python", "Assembly"], "a": "Python"},
        {"q": "What is used to translate high-level code into machine code?", "o": ["Printer", "Compiler", "Keyboard"], "a": "Compiler"},
        {"q": "Which language is commonly used for Android development?", "o": ["HTML", "Java", "CSS"], "a": "Java"}
    ],
    "Computer Science": [
        {"q": "What is the study of algorithms and computer systems?", "o": ["Biology", "Computer Science", "Geography"], "a": "Computer Science"},
        {"q": "CS focuses on which of the following?", "o": ["Only repair", "Problem-solving with data", "Manual filing"], "a": "Problem-solving with data"},
        {"q": "Which is a core field within CS?", "o": ["Botany", "Software Engineering", "Sculpting"], "a": "Software Engineering"}
    ],
    "Hardware": [
        {"q": "What are the physical components of a computer called?", "o": ["Software", "Hardware", "Firmware"], "a": "Hardware"},
        {"q": "Which of these is a piece of hardware?", "o": ["Windows", "Mouse", "Photoshop"], "a": "Mouse"},
        {"q": "Can you touch software?", "o": ["Yes", "No"], "a": "No"}
    ],
    "Data": [
        {"q": "What are raw facts and figures called?", "o": ["Information", "Data", "Knowledge"], "a": "Data"},
        {"q": "When data is processed, it becomes?", "o": ["Information", "Noise", "Binary"], "a": "Information"},
        {"q": "Which is an example of data?", "o": ["A weather report", "The number 25", "A final grade"], "a": "The number 25"}
    ],
    "Internet": [
        {"q": "What is the 'Network of Networks'?", "o": ["Intranet", "The Internet", "LAN"], "a": "The Internet"},
        {"q": "What is used to identify a website?", "o": ["URL", "CPU", "RAM"], "a": "URL"},
        {"q": "Which protocol is the foundation of the internet?", "o": ["HTTP/HTTPS", "Bluetooth", "NFC"], "a": "HTTP/HTTPS"}
    ],
    "RAM": [
        {"q": "What happens to data in RAM when the computer restarts?", "o": ["It is saved", "It is lost", "It moves to the cloud"], "a": "It is lost"},
        {"q": "RAM is also known as?", "o": ["Read Only Memory", "Main Memory", "Secondary Memory"], "a": "Main Memory"},
        {"q": "What does RAM stand for?", "o": ["Random Access Memory", "Ready Action Memory", "Real Always Memory"], "a": "Random Access Memory"}
    ],
    "ROM": [
        {"q": "Is ROM volatile or non-volatile?", "o": ["Volatile", "Non-Volatile"], "a": "Non-Volatile"},
        {"q": "What is stored in ROM?", "o": ["User files", "BIOS/Startup instructions", "Browsing history"], "a": "BIOS/Startup instructions"},
        {"q": "Can a standard user easily delete data from ROM?", "o": ["Yes", "No"], "a": "No"}
    ],
    "Information": [
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
    "Operating System": [
        "Draw a diagram showing the relationship between User, OS, and Hardware.",
        "Compare and contrast Batch Processing and Time-Sharing systems.",
        "Explain the concept of 'Thrashing' in Virtual Memory.",
        "List four essential functions of a modern Operating System."
    ],
    "DBMS": [
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
    "Operating System","DBMS","Data Structures","Artificial Intelligence","Cloud Computing",
    "Computer Network","Cyber Security","Input Device"," Output Device","CPU","Memory Unit",
    "Storage Device", "System Software ","Web Application ","Programming Language ","Computer Science"
    ,"Hardware","Data","Internet ","RAM","ROM","Information "

]

for t in knowledge_topics:
    if st.sidebar.button(t):
        st.session_state.topic_input = t

# ---------------- 6. MAIN UI & LOGIC ----------------
st.title("📘 AI Smart Learning Assistant")
st.info("📌 Enter a topic below to get instant explanations, practice, and quizzes.")

topic_input = st.text_input("Enter Topic", key="topic_input")
level = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

col1, col2 = st.columns(2)
with col1:
    explain_clicked = st.button("Explain Topic")
with col2:
    practice_clicked = st.button("Generate Practice")

# ---------------- MAIN LOGIC ----------------
if topic_input:
    clean_input = topic_input.lower().strip()

    topic_keys = {k.lower(): k for k in explanations.keys()}
    matches = difflib.get_close_matches(clean_input, topic_keys.keys(), n=1, cutoff=0.3)

    if matches:
        matched_topic = topic_keys[matches[0]]

        # Reset practice questions if topic changes
        if matched_topic != st.session_state.current_topic:
            st.session_state.practice_questions = None
            st.session_state.current_topic = matched_topic

        # ---------------- EXPLANATION ----------------
        if explain_clicked:
            st.success(f"Smart Match: **{matched_topic.upper()}**")
            st.subheader("📖 Explanation")

            if level == "Easy":
                st.write(explanations[matched_topic][:200] + "...")
            elif level == "Medium":
                st.write(explanations[matched_topic])
            else:
                st.write(explanations[matched_topic] + "\n\nAdvanced concepts can be explored further.")

        # ---------------- PRACTICE ----------------
        if practice_clicked:
            pool = practice_bank.get(matched_topic, practice_bank["generic"])
            st.session_state.practice_questions = random.sample(pool, min(len(pool), 2))

        if st.session_state.practice_questions:
            st.markdown("---")
            st.subheader(f"📝 Interactive Practice: {matched_topic}")
            for i, q in enumerate(st.session_state.practice_questions, start=1):
                st.markdown(f"**Q{i}:** {q}")
                st.text_area("Your Response:", key=f"ans_{matched_topic}_{i}")

        # ---------------- QUIZ ----------------
        st.markdown("---")
        st.subheader(f"🧠 Quiz: {matched_topic}")
        current_quiz = quiz_bank.get(matched_topic, quiz_bank["generic"])

        user_responses = []
        for i, item in enumerate(current_quiz):
            user_responses.append(
                st.radio(f"Q{i+1}: {item['q']}", item['o'], key=f"quiz_{matched_topic}_{i}")
            )

        if st.button("Submit Quiz", key=f"submit_{matched_topic}"):
            score = sum(
                1 for i, ans in enumerate(user_responses)
                if ans == current_quiz[i]['a']
            )
            st.metric("Score", f"{score}/{len(current_quiz)}")

    else:
        st.warning("Topic not found. Try keywords from the sidebar Knowledge Map.")
