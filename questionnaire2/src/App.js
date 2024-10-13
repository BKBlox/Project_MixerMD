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
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [responses, setResponses] = useState(Array(questions.length).fill(''));

    // Handle the selection of an answer
    const handleOptionChange = (event) => {
        const updatedResponses = [...responses];
        updatedResponses[currentQuestion] = event.target.value;
        setResponses(updatedResponses);
    };

    // Move to the next question
    const nextQuestion = () => {
        if (currentQuestion < questions.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
        }
    };

    // Handle form submission
    const handleSubmit = (event) => {
        event.preventDefault();
        if (currentQuestion === questions.length - 1) {
            alert("Questionnaire completed! Your responses: " + JSON.stringify(responses));
            // Reset questionnaire
            setCurrentQuestion(0);
            setResponses(Array(questions.length).fill(''));
        } else {
            nextQuestion();
        }
    };

    return (
        <section className="home">
            <div style={{padding: '20px', maxWidth: '600px', margin: 'auto'}}>
                <h1>Questionnaire</h1>
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
                    <button type="submit">{currentQuestion === questions.length - 1 ? 'Finish' : 'Next'}</button>
                </form>
            </div>
        </section>

    );
}

export default App;
