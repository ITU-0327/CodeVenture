# CodeVenture - Learn Python the Fun Way! 🐍🎮

## Overview

**CodeVenture** is an engaging and interactive platform aimed at young learners to make Python programming not just educational, but also fun and exciting. Our platform incorporates game-like elements, quizzes, interactive tutorials, and weekly progress tracking to make learning Python a thrill.

![CodeVenture Logo](https://media.discordapp.net/attachments/1138474786914320486/1168468627557720084/logo_feedback.png?ex=6551e035&is=653f6b35&hm=83dda9762bc0ba6f9f4f33d9121b8746ec42a4603941c7bec4b1e5125a276437&=&width=303&height=181)

## Features 🌟

### Welcome Page
- Simple and secure login and sign-up features.
- **Google OAuth Integration**: Swiftly login using your Google account for a seamless experience.

### Learning Modules
- Interactive lessons tailored to enhance the Python programming skills of learners.

### Quizzes
- Test your knowledge after each module with comprehensive quizzes.

### Challenges
- Practice real-world programming problems to strengthen your coding skills.
- Engaging challenges ranging from beginner to advanced levels.

### Python Playground
- An integrated IDE environment where students can practice Python coding in real-time.
- Safely execute your Python scripts and see immediate results.

### Progress Report
- **DropView Feature**: Allows students to download a detailed PDF report of their progress. This helps in tracking learning milestones and areas that need improvement.

### Feedback
- Found at the bottom of the page, the feedback form ensures that we are constantly aware of user suggestions and areas of improvement.

### Backend Infrastructure
- **GCP SQL Hosting**: Our platform uses Google Cloud Platform to host our MySQL server, ensuring fast, reliable, and scalable database operations.

### Database Access
- Progress tracking for parents, teacher, and student. Track and analyze performance metrics over time.



## Getting Started 🚀

### Clone the Repository

```bash
git clone https://github.com/matthewchungkaishing/CodeVenture.git
```

### Install Dependencies
Navigate to the project directory and run:
```bash
pip install -r requirements.txt
```

### Run the Application 🏃‍♀️🏃‍♂️

To run CodeVenture, navigate to the project directory and execute:

```bash
python manage.py runserver
```

After executing the above command, the application will start, and you'll typically see output indicating the server is running. You can then access the application by opening a web browser and navigating to:

```bash
http://localhost:8000/
```

Simply copy and paste the above URL into your browser's address bar to access CodeVenture.



## Testing Instructions 🧪

To thoroughly test the platform, we've created four types of user accounts, each with unique access and functionalities. Here are the details for testing:

### Admin Account
- **Username:** `admin`
- **Password:** `Codeventure2023`
- **Capabilities:** Full administrative access including user management and analytics.

### Student Account
- **Username:** `studentaccount`
- **Password:** `Codeventure2023`
- **Capabilities:** Access to learning modules, quizzes, and personal progress tracking.

### Parent Account
- **Username:** `parentaccount`
- **Password:** `Codeventure2023`
- **Capabilities:** Ability to track children's progress and access educational resources.

### Teacher Account
- **Username:** `teacheraccount`
- **Password:** `Codeventure2023`
- **Capabilities:** Access to student progress tracking, and curriculum customization.

Feel free to explore these accounts to experience the platform from different user perspectives.

## License 📝

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file in our GitHub repository.
