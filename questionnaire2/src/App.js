import React, { useState } from 'react';
import './App.css';

// List of questions
const questions = [
    {
        question: "How do you prefer to spend your free time?",
        options: [
            "A) Socializing with friends",
            "B) Engaging in solo hobbies (reading, gaming, etc.)",
            "C) Exploring outdoors and nature",
            "D) Learning or trying new skills",
        ],
    },
    {
        question: "How do you handle challenges or problems?",
        options: [
            "A) I rely on others for advice and support",
            "B) I analyze the situation and try to solve it myself",
            "C) I take it one step at a time without overthinking",
            "D) I avoid the problem and hope it resolves itself",
        ],
    },
    {
        question: "Which type of social setting do you feel most comfortable in?",
        options: [
            "A) Large gatherings with many people",
            "B) Small groups of close friends",
            "C) One-on-one conversations",
            "D) I prefer being alone or with very few people",
        ],
    },
    {
        question: "What drives your decision-making?",
        options: [
            "A) Logic and reason",
            "B) Emotion and intuition",
            "C) A mix of both",
            "D) I prefer to follow others' lead",
        ],
    },
    {
        question: "How do you prefer to communicate?",
        options: [
            "A) Direct and straightforward",
            "B) Thoughtful and empathetic",
            "C) Brief and to the point",
            "D) Playful and humorous",
        ],
    },
    {
        question: "Which of the following best describes your approach to teamwork?",
        options: [
            "A) I enjoy taking the lead and organizing tasks",
            "B) I like contributing in a supportive role",
            "C) I prefer working independently within the group",
            "D) I enjoy brainstorming and offering ideas, but dislike structured roles",
        ],
    },
    {
        question: "What kind of activities do you enjoy the most?",
        options: [
            "A) Physical activities like sports or dancing",
            "B) Creative tasks like writing or painting",
            "C) Mental challenges like puzzles or strategy games",
            "D) Social games like board games or trivia",
        ],
    },
    {
        question: "How would your friends describe your energy levels?",
        options: [
            "A) Very energetic and always on the go",
            "B) Calm and relaxed most of the time",
            "C) Somewhere in the middle—balanced energy",
            "D) Quiet and reserved, but engaged",
        ],
    },
    {
        question: "How do you prefer to spend time during social events?",
        options: [
            "A) Meeting as many people as possible",
            "B) Sticking with familiar faces and having meaningful conversations",
            "C) Observing or staying in the background",
            "D) Engaging in group activities or games",
        ],
    },
    {
        question: "What is your preferred method of resolving conflicts?",
        options: [
            "A) Discussing it openly and directly",
            "B) Avoiding confrontation and letting things cool off",
            "C) Finding a compromise that works for everyone",
            "D) Seeking mediation from a third party",
        ],
    },
];

function App() {
    // State to track current question and user responses
    const [currentQuestion, setCurrentQuestion] = useState(1);
    const [responses, setResponses] = useState(Array(questions.length + 1).fill(''));
    const [username, setUsername] = useState('');        // State to store the username
    const [hasStarted, setHasStarted] = useState(false); // State to track if the questionnaire has started
    const [isWaiting, setIsWaiting] = useState(false);   // State to track if the user is on the waiting screen
    const [userShort, setUserShort] = useState('');
    const [selectedOption, setSelectedOption] = useState(''); // Track selected option for the current question

    // Handle the change of username input
    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    // Handle the selection of an answer
    const handleOptionChange = (event) => {
        const updatedResponses = [...responses];
        updatedResponses[currentQuestion] = event.target.value;
        setResponses(updatedResponses);
        setSelectedOption(event.target.value); // Update selected option
    };

    // Handle starting the questionnaire
    const startQuestionnaire = (event) => {
        event.preventDefault();
        if (username.trim() !== '') {
            const updatedResponses = [...responses];
            updatedResponses[0] = username;
            setResponses(updatedResponses);
            setHasStarted(true);  // Move to the questionnaire screen
            setUserShort(username.trim().charAt(0) + ".");
        } else {
            alert('Please enter a username to start');
        }
    };

    // Move to the next question
    const nextQuestion = () => {
        if (currentQuestion < questions.length - 1 && selectedOption.length) {
            setSelectedOption('')
            setCurrentQuestion(currentQuestion + 1);
        }
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (currentQuestion === questions.length - 1) {
            setIsWaiting(true);
            // Send data to the server
            fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(responses),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to submit data');
                }
                return response.json();  // Parse JSON from the response
            })
            .then(jsonResponse => {
                if (jsonResponse.status === 'success') {
                    document.cookie = `userId=${jsonResponse.uuid};path=/;max-age=86400`;  // 1 day expiration
                    const userId = getCookie('userId');
                    window.location.href="/emojifeeling.html";
                } else {
                    console.error('Submission failed:', jsonResponse.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Optionally handle errors, such as displaying a notification to the user
            });
        } else {
            nextQuestion();
        }
    };

    return (
        <div className="home">
            <div style={{padding: '20px', maxWidth: '600px', margin: 'auto', color: 'white'}}>
                {!hasStarted ? (
                    // Render username input screen
                    <form onSubmit={startQuestionnaire}>
                        <h1>Personality Test</h1>
                        <div className="userscreen">
                            <label htmlFor="username">Enter your name to begin:</label>
                            <input
                                type="text"
                                id="username"
                                value={username}
                                onChange={handleUsernameChange}
                                required
                                style={{padding: '10px', fontSize: '16px', margin: '10px 0', width: '100%'}}
                            />
                        </div>
                        <button type="submit" style={{padding: '10px 20px', fontSize: '16px'}}>
                            Start
                        </button>
                    </form>
                    ) : isWaiting ? (
                    // Render waiting screen
                    <div>
                        <h1>Congrats, {username}!</h1>
                        <h2>You've been matched!</h2>
                        <h4>Wait here until the next game starts....</h4>
                    </div>
                ) : (
                    // Render questionnaire screen
                    <form onSubmit={handleSubmit}>
                        <h2>{questions[currentQuestion].question}</h2>
                        {questions[currentQuestion].options.map((option, index) => (
                            <div className="radio-container" key={index}>
                                <input
                                    type="radio"
                                    id={`option-${index}`}
                                    value={option}
                                    checked={responses[currentQuestion] === option}
                                    onChange={handleOptionChange}
                                    required
                                />
                                <label htmlFor={`option-${index}`}>{option}</label>
                            </div>
                        ))}
                        <button type="submit" disabled={!selectedOption}>
                            {currentQuestion === questions.length - 1 ? 'Finish' : 'Next'}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export default App;
