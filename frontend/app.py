<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>AI Interview Simulator | Practice Like a Pro</title>
    <!-- Google Fonts & Simple Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #f8fafc;
            font-family: 'Inter', sans-serif;
            color: #0f172a;
            line-height: 1.5;
        }

        .app-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.5rem 2rem 3rem;
        }

        /* Navbar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: white;
            border-radius: 24px;
            padding: 0.75rem 1.8rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 2px 6px rgba(0,0,0,0.03);
            border: 1px solid #e9eef3;
        }
        .logo {
            font-weight: 700;
            font-size: 1.5rem;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #2563eb, #4f46e5);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .logo span {
            font-weight: 500;
            color: #334155;
            background: none;
        }
        .nav-right {
            display: flex;
            align-items: center;
            gap: 1rem;
            font-size: 0.8rem;
            color: #475569;
            background: #f1f5f9;
            padding: 0.4rem 1rem;
            border-radius: 40px;
        }
        .badge-round {
            background: #eef2ff;
            color: #2563eb;
            border-radius: 100px;
            padding: 0.25rem 0.9rem;
            font-size: 0.7rem;
            font-weight: 600;
        }

        /* Progress Tracker */
        .progress-track {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: white;
            border-radius: 60px;
            padding: 0.5rem 1rem;
            margin-bottom: 2rem;
            border: 1px solid #eef2ff;
        }
        .step {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex: 1;
        }
        .step-node {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #f8fafc;
            padding: 0.4rem 1rem;
            border-radius: 40px;
            font-weight: 500;
            font-size: 0.8rem;
        }
        .step-node.active {
            background: #eef2ff;
            color: #2563eb;
            border: 1px solid #cbdffc;
        }
        .step-node.completed {
            background: #e6f7ec;
            color: #15803d;
        }
        .step-line {
            height: 2px;
            background: #e2e8f0;
            flex: 1;
            margin: 0 0.5rem;
        }
        .step-line.done {
            background: #4f46e5;
        }

        /* Interview Grid */
        .interview-grid {
            display: flex;
            gap: 1.8rem;
            flex-wrap: wrap;
        }
        .interviewer-card {
            flex: 1.2;
            background: white;
            border-radius: 28px;
            border: 1px solid #eef2ff;
            overflow: hidden;
        }
        .chat-panel {
            flex: 1.8;
            background: white;
            border-radius: 28px;
            border: 1px solid #eef2ff;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
        }

        .interviewer-header {
            background: #fefefe;
            padding: 1.5rem 1.5rem 0.5rem;
            border-bottom: 1px solid #f0f4f9;
            text-align: center;
        }
        .avatar-ring {
            width: 100px;
            height: 100px;
            background: linear-gradient(145deg, #f1f5ff, #ffffff);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 0.8rem;
            font-size: 3rem;
            box-shadow: 0 6px 12px -8px rgba(0,0,0,0.1);
            border: 2px solid #e2e8f0;
        }
        .interviewer-name {
            font-size: 1.2rem;
            font-weight: 700;
        }
        .interviewer-title {
            font-size: 0.75rem;
            color: #4b5563;
        }
        .company-badge {
            background: #f1f5f9;
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.7rem;
            margin-top: 0.5rem;
        }
        .round-tag {
            background: #eef2ff;
            color: #1e40af;
            padding: 0.25rem 1rem;
            border-radius: 30px;
            font-weight: 600;
            font-size: 0.7rem;
            display: inline-block;
            margin: 0.5rem 0;
        }
        .question-bubble {
            background: #f8fafc;
            margin: 1rem 1.2rem;
            padding: 1.2rem;
            border-radius: 20px;
            border-left: 4px solid #3b82f6;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            line-height: 1.55;
            color: #1e293b;
        }
        .question-meta {
            display: flex;
            justify-content: space-between;
            padding: 0 1.2rem 1rem;
            font-size: 0.7rem;
            color: #64748b;
        }
        .dot-progress {
            display: flex;
            gap: 6px;
        }
        .dot {
            width: 24px;
            height: 4px;
            background: #e2e8f0;
            border-radius: 4px;
        }
        .dot.active {
            background: #3b82f6;
        }
        .dot.done {
            background: #22c55e;
        }

        /* Chat */
        .chat-history {
            flex: 1;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding-right: 0.5rem;
        }
        .message {
            display: flex;
            gap: 12px;
            margin-bottom: 1rem;
            animation: fadeUp 0.2s ease;
        }
        .message.user {
            flex-direction: row-reverse;
        }
        .message-avatar {
            width: 32px;
            height: 32px;
            background: #f1f5f9;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
        }
        .message-bubble {
            max-width: 80%;
            padding: 0.7rem 1rem;
            border-radius: 18px;
            font-size: 0.85rem;
            line-height: 1.45;
        }
        .message.ai .message-bubble {
            background: #f1f5f9;
            color: #0f172a;
            border-top-left-radius: 4px;
        }
        .message.user .message-bubble {
            background: #eef2ff;
            color: #1e293b;
            border-top-right-radius: 4px;
        }
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(8px);}
            to { opacity: 1; transform: translateY(0);}
        }

        .eval-card {
            background: #fefce8;
            border-left: 4px solid #eab308;
            padding: 0.8rem 1rem;
            margin: 1rem 1.2rem;
            border-radius: 16px;
        }
        .score-badge {
            font-size: 1.5rem;
            font-weight: 800;
            font-family: monospace;
        }

        textarea {
            width: 100%;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 0.9rem 1rem;
            font-family: 'Inter', monospace;
            font-size: 0.85rem;
            resize: vertical;
            background: #ffffff;
        }
        textarea:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
        }
        .btn-primary {
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 40px;
            padding: 0.7rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85rem;
            width: 100%;
            transition: all 0.2s;
        }
        .btn-primary:hover {
            background: #1d4ed8;
            transform: translateY(-1px);
        }
        .btn-secondary {
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 40px;
            padding: 0.7rem;
            font-weight: 500;
            cursor: pointer;
        }

        /* Landing */
        .hero {
            text-align: center;
            padding: 2rem 1rem 2rem;
        }
        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #0f172a, #2563eb);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .feature-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
        }
        .feature {
            background: white;
            border-radius: 24px;
            padding: 1rem 1.5rem;
            flex: 1 1 180px;
            border: 1px solid #eef2ff;
            text-align: center;
        }
        .upload-area {
            background: white;
            border: 2px dashed #cbd5e1;
            border-radius: 28px;
            padding: 2rem;
            text-align: center;
            margin-top: 1rem;
        }

        /* Resume preview */
        .resume-preview {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        .resume-card {
            background: white;
            border-radius: 24px;
            padding: 1.2rem;
            border: 1px solid #eef2ff;
            flex: 1;
        }
        .skill-chip {
            background: #eef2ff;
            padding: 0.2rem 0.7rem;
            border-radius: 30px;
            font-size: 0.7rem;
            display: inline-block;
            margin: 0.2rem;
        }
        .score-circle {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: conic-gradient(#2563eb 0% 75%, #e2e8f0 75% 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.8rem;
            margin: 0 auto;
        }
        .score-inner {
            background: white;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
        }

        .results-banner {
            background: white;
            border-radius: 32px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid #eef2ff;
        }
        hr {
            margin: 1rem 0;
            border-color: #eef2ff;
        }
        @media (max-width: 780px) {
            .interview-grid { flex-direction: column; }
            .app-container { padding: 1rem; }
        }
    </style>
</head>
<body>
<div id="root" class="app-container"></div>

<script>
    (function() {
        // ---------- DATA ----------
        const ROUNDS = ["HR", "APTITUDE", "TECHNICAL", "DSA"];
        const ROUND_META = {
            "HR": { label: "HR Round", icon: "👤", color: "#3b82f6" },
            "APTITUDE": { label: "Aptitude", icon: "🧮", color: "#f59e0b" },
            "TECHNICAL": { label: "Technical", icon: "💻", color: "#10b981" },
            "DSA": { label: "DSA Round", icon: "🔢", color: "#ef4444" }
        };
        const INTERVIEWER_DATA = {
            "HR": { emoji: "👩‍💼", name: "Sarah Chen", title: "HR Business Partner", company: "TechCorp" },
            "APTITUDE": { emoji: "🧑‍🏫", name: "Prof. Arjun", title: "Assessment Lead", company: "EvalPro" },
            "TECHNICAL": { emoji: "👨‍💻", name: "Alex Rivera", title: "Principal Engineer", company: "Silicon Labs" },
            "DSA": { emoji: "🤖", name: "ARIA-9", title: "Algorithms Expert", company: "DeepCode AI" }
        };
        
        const QUESTION_BANK = {
            "HR": [
                "Tell me about yourself and why you're interested in this role?",
                "Describe a time you faced a conflict at work and how you resolved it.",
                "Where do you see yourself in 5 years and how does this role align?"
            ],
            "APTITUDE": [
                "If a car travels 60 km in 1.5 hours, what is its average speed in km/h? Explain logic.",
                "A man buys a shirt for $40 and sells it at a 25% profit. What is the selling price?",
                "Complete the series: 2, 6, 12, 20, ? Explain pattern."
            ],
            "TECHNICAL": [
                "Explain the difference between REST and GraphQL APIs. When would you use each?",
                "What is your favorite programming language and what project have you built with it?",
                "Describe a challenging bug you solved and your debugging process."
            ],
            "DSA": [
                "Write the algorithm to reverse a linked list and analyze its complexity.",
                "Explain how a hashmap works internally and how you handle collisions.",
                "Given an array of integers, find two numbers that sum to a target. Optimal approach?"
            ]
        };
        
        // ---------- STATE ----------
        let appState = {
            page: "landing",
            sessionToken: "demo_" + Math.random().toString(36).substr(2, 8),
            resumeData: null,
            resumeScore: null,
            currentRound: "HR",
            currentQuestion: "",
            questionNumber: 1,
            chatHistory: [],
            roundsCompleted: [],
            lastEval: null,
            finalReport: null,
            totalQuestionsPerRound: 3
        };
        
        // Helper: update & re-render
        function updateState(updates) {
            Object.assign(appState, updates);
            renderApp();
        }
        
        // Mock resume upload
        function mockResumeUpload() {
            return new Promise((resolve) => {
                setTimeout(() => {
                    resolve({
                        session_token: appState.sessionToken,
                        resume_data: {
                            name: "Alex Johnson",
                            technical_skills: ["JavaScript", "React", "Python", "Node.js", "SQL", "Docker"],
                            projects: [
                                { name: "AI Mock Interview Platform", description: "Full-stack app using OpenAI and React", technologies: ["React", "FastAPI"] },
                                { name: "Ecommerce Dashboard", description: "Analytics dashboard with realtime updates", technologies: ["Vue", "D3"] }
                            ],
                            experience: [
                                { role: "Software Engineer", company: "TechStart Inc", duration: "2022-Present" },
                                { role: "Intern", company: "CodeWorks", duration: "2021-2022" }
                            ]
                        },
                        resume_score: {
                            percentage: 82,
                            grade: "A-",
                            breakdown: { skills: 18, projects: 22, experience: 20, education: 14, contact: 8 },
                            feedback: ["Strong technical stack", "Add more metrics to projects", "Good experience section"]
                        }
                    });
                }, 500);
            });
        }
        
        // Start round
        async function startRound(round) {
            const questions = QUESTION_BANK[round] || QUESTION_BANK["HR"];
            const firstQ = questions[0];
            updateState({
                currentQuestion: firstQ,
                questionNumber: 1,
                chatHistory: [...appState.chatHistory, { role: "assistant", content: firstQ, round: round }],
                lastEval: null
            });
        }
        
        // Submit answer & handle flow
        async function submitAnswer(answerText, isSkip = false) {
            const finalAnswer = isSkip ? "(skipped)" : (answerText.trim() || "(no answer)");
            const round = appState.currentRound;
            const qNum = appState.questionNumber;
            const total = appState.totalQuestionsPerRound;
            
            // Add user message
            const updatedHistory = [...appState.chatHistory, { role: "user", content: finalAnswer, round: round }];
            updateState({ chatHistory: updatedHistory, lastEval: null });
            
            // Mock evaluation
            let score = 5;
            let feedbackText = "Your answer was concise. Try to add more details and structure.";
            let strengths = [];
            let improvements = [];
            if (finalAnswer.length > 40 && !isSkip) { 
                score = 7; 
                feedbackText = "Good answer with relevant points. You can deepen technical depth."; 
                strengths = ["Clear structure"]; 
                improvements = ["Add examples"]; 
            }
            if (finalAnswer.length > 100) { 
                score = 8.5; 
                feedbackText = "Excellent detailed answer! Demonstrates strong knowledge."; 
                strengths = ["Thorough explanation", "Good examples"]; 
                improvements = ["Slightly more concise"]; 
            }
            if (isSkip) { 
                score = 3; 
                feedbackText = "You skipped the question. Practice articulating under pressure."; 
                improvements = ["Attempt all questions"]; 
            }
            
            const evaluation = {
                score: score,
                feedback: feedbackText,
                strengths: strengths,
                improvements: improvements,
                sample_answer_hint: "Consider using the STAR method for behavioral questions."
            };
            
            updateState({ lastEval: evaluation });
            
            const isRoundComplete = qNum >= total;
            if (isRoundComplete) {
                const newCompleted = [...appState.roundsCompleted, round];
                const currentIdx = ROUNDS.indexOf(round);
                const nextRound = currentIdx + 1 < ROUNDS.length ? ROUNDS[currentIdx + 1] : null;
                
                if (!nextRound) {
                    // All rounds done
                    const roundScores = {};
                    ROUNDS.forEach(r => { 
                        roundScores[r] = (r === round) ? score : (Math.floor(Math.random() * 25) / 5 + 5); 
                    });
                    const overall = (Object.values(roundScores).reduce((a,b)=>a+b,0)/ROUNDS.length).toFixed(1);
                    const finalReportMock = {
                        overall_score: parseFloat(overall),
                        round_scores: roundScores,
                        final_feedback: {
                            grade: overall > 7 ? "B+" : (overall > 5 ? "C+" : "D"),
                            verdict: overall > 7 ? "✅ Strong Candidate" : (overall > 5 ? "📌 Potential" : "⚠️ Needs Improvement"),
                            executive_summary: "You showed solid potential but need more depth in technical rounds.",
                            top_strengths: ["Communication", "Honesty"],
                            key_improvements: ["Technical precision", "DSA practice"],
                            next_steps: ["Review data structures", "Mock more HR questions"]
                        }
                    };
                    updateState({ finalReport: finalReportMock, page: "results", roundsCompleted: newCompleted });
                    renderApp();
                    return;
                } else {
                    // Move to next round
                    updateState({
                        currentRound: nextRound,
                        roundsCompleted: newCompleted,
                        currentQuestion: "",
                        questionNumber: 0,
                        lastEval: null,
                        chatHistory: [...appState.chatHistory, { role: "assistant", content: `🎉 Round ${ROUND_META[round].label} completed! Moving to ${ROUND_META[nextRound].label}.`, round: nextRound }]
                    });
                    setTimeout(() => {
                        startRound(nextRound);
                    }, 300);
                    return;
                }
            } else {
                // Next question in same round
                const questionsArr = QUESTION_BANK[round];
                const nextQuestion = questionsArr[qNum]; // because qNum is current (1-indexed) so next index = qNum
                const newHistory = [...appState.chatHistory, { role: "assistant", content: nextQuestion, round: round }];
                updateState({
                    currentQuestion: nextQuestion,
                    questionNumber: qNum + 1,
                    chatHistory: newHistory,
                    lastEval: evaluation
                });
                renderApp();
            }
        }
        
        function resetInterview() {
            appState = {
                page: "landing",
                sessionToken: "demo_" + Math.random().toString(36).substr(2, 8),
                resumeData: null,
                resumeScore: null,
                currentRound: "HR",
                currentQuestion: "",
                questionNumber: 1,
                chatHistory: [],
                roundsCompleted: [],
                lastEval: null,
                finalReport: null,
                totalQuestionsPerRound: 3
            };
            renderApp();
        }
        
        // ---------- RENDERERS ----------
        function renderNavbar(showRound = false) {
            let roundInfo = "";
            if (showRound && appState.currentRound) {
                const meta = ROUND_META[appState.currentRound];
                roundInfo = `<div class="badge-round"><i class="fas fa-microphone-alt"></i> ${meta.icon} ${meta.label}</div>`;
            }
            return `
                <div class="navbar">
                    <div class="logo">INTERVIEW<span>AI</span></div>
                    <div class="nav-right">
                        <i class="fas fa-bolt"></i> <span>Powered by Groq</span> <span style="margin:0 0.3rem">|</span> <span>llama-3.3-70b</span>
                        ${roundInfo}
                    </div>
                </div>
            `;
        }
        
        function renderProgress() {
            let stepsHtml = '';
            for (let i=0; i<ROUNDS.length; i++) {
                const r = ROUNDS[i];
                const isDone = appState.roundsCompleted.includes(r);
                const isActive = (appState.currentRound === r && !isDone && appState.page === "interview");
                let statusClass = "";
                if (isActive) statusClass = "active";
                if (isDone) statusClass = "completed";
                stepsHtml += `
                    <div class="step">
                        <div class="step-node ${statusClass}">
                            <i class="fas ${isDone ? 'fa-check-circle' : (isActive ? 'fa-circle-play' : 'fa-circle')}"></i>
                            <span>${ROUND_META[r].label}</span>
                        </div>
                        ${i < ROUNDS.length-1 ? `<div class="step-line ${isDone ? 'done' : ''}"></div>` : ''}
                    </div>
                `;
            }
            return `<div class="progress-track">${stepsHtml}</div>`;
        }
        
        function renderInterviewerPanel() {
            const round = appState.currentRound;
            const meta = ROUND_META[round];
            const interviewer = INTERVIEWER_DATA[round];
            const qNum = appState.questionNumber;
            const total = appState.totalQuestionsPerRound;
            let dots = "";
            for (let i=1; i<=total; i++) {
                let cls = "dot";
                if (i < qNum) cls += " done";
                if (i === qNum) cls += " active";
                dots += `<div class="${cls}"></div>`;
            }
            return `
                <div class="interviewer-card">
                    <div class="interviewer-header">
                        <div class="avatar-ring">${interviewer.emoji}</div>
                        <div class="interviewer-name">${interviewer.name}</div>
                        <div class="interviewer-title">${interviewer.title}</div>
                        <div class="company-badge"><i class="fas fa-building"></i> ${interviewer.company}</div>
                        <div><span class="round-tag">${meta.icon} ${meta.label}</span></div>
                    </div>
                    <div class="question-bubble">
                        ${appState.currentQuestion || "Loading your first question..."}
                    </div>
                    <div class="question-meta">
                        <span>Question ${qNum} of ${total}</span>
                        <div class="dot-progress">${dots}</div>
                    </div>
                    ${appState.lastEval ? `
                    <div class="eval-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="score-badge" style="color:${appState.lastEval.score>=7?'#10b981':'#eab308'}">${appState.lastEval.score}/10</span>
                            <span style="font-size:0.7rem;">Answer Score</span>
                        </div>
                        <p style="font-size:0.75rem; margin-top:6px;">${appState.lastEval.feedback}</p>
                        <div style="margin-top:8px;"><small>💡 ${appState.lastEval.sample_answer_hint}</small></div>
                    </div>
                    ` : ''}
                </div>
            `;
        }
        
        function renderChat() {
            const roundFilter = appState.currentRound;
            const filtered = appState.chatHistory.filter(m => m.round === roundFilter || !m.round);
            let messagesHtml = "";
            filtered.slice(-8).forEach(msg => {
                const isUser = msg.role === "user";
                messagesHtml += `
                    <div class="message ${isUser ? 'user' : 'ai'}">
                        <div class="message-avatar">${isUser ? '👤' : '🤖'}</div>
                        <div class="message-bubble">${escapeHtml(msg.content)}</div>
                    </div>
                `;
            });
            if (!messagesHtml) messagesHtml = '<div style="color:#94a3b8;text-align:center;">Start the conversation by answering the question</div>';
            return `<div class="chat-history">${messagesHtml}</div>`;
        }
        
        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            }).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, function(c) {
                return c;
            });
        }
        
        function renderInterview() {
            return `
                ${renderNavbar(true)}
                ${renderProgress()}
                <div class="interview-grid">
                    ${renderInterviewerPanel()}
                    <div class="chat-panel">
                        <div style="display:flex; gap:8px; align-items:center; margin-bottom:12px;">
                            <i class="fas fa-comments" style="color:#2563eb;"></i>
                            <span style="font-weight:600; font-size:0.8rem;">Conversation Log</span>
                        </div>
                        ${renderChat()}
                        <hr />
                        <label style="font-size:0.7rem; font-weight:500;">Your Answer</label>
                        <textarea id="userAnswer" rows="3" placeholder="Type your answer here... Be specific, use examples."></textarea>
                        <div style="display:flex; gap:1rem; margin-top:0.8rem;">
                            <button id="submitBtn" class="btn-primary">Submit Answer →</button>
                            <button id="skipBtn" class="btn-secondary">Skip</button>
                        </div>
                    </div>
                </div>
            `;
        }
        
        function renderLanding() {
            return `
                ${renderNavbar(false)}
                <div class="hero">
                    <h1>Practice Interviews<br>Like a Pro.</h1>
                    <p style="color:#475569; max-width:600px; margin:1rem auto;">Face AI interviewers across 4 real rounds — HR, Aptitude, Technical & DSA. Get instant personalised feedback based on your resume.</p>
                    <div class="feature-grid">
                        <div class="feature">👤 HR Round<br><small>Behavioral & cultural fit</small></div>
                        <div class="feature">🧮 Aptitude<br><small>Quant & logical reasoning</small></div>
                        <div class="feature">💻 Technical<br><small>Domain & project deep-dive</small></div>
                        <div class="feature">🔢 DSA Round<br><small>Algorithms & data structures</small></div>
                    </div>
                    <div class="upload-area">
                        <i class="fas fa-file-pdf" style="font-size:2rem; color:#2563eb;"></i>
                        <p style="margin-top:8px;"><strong>Upload your resume (PDF/DOCX)</strong> to start AI-driven interview</p>
                        <input type="file" id="resumeFileInput" accept=".pdf,.docx" style="margin-top:12px;" />
                        <button id="uploadStartBtn" class="btn-primary" style="margin-top:16px; width:auto; padding:0.5rem 1.8rem;">🚀 Parse & Begin</button>
                    </div>
                </div>
            `;
        }
        
        function renderResumePreview() {
            const rd = appState.resumeData || { name: "Candidate", technical_skills: [] };
            const rs = appState.resumeScore || { percentage: 78, grade: "B+", feedback: [] };
            const skills = rd.technical_skills || [];
            return `
                ${renderNavbar(false)}
                <div style="text-align:center; margin-bottom:1.5rem;">
                    <h2>Welcome, ${escapeHtml(rd.name)} 👋</h2>
                    <p>Review your profile before entering the interview arena</p>
                </div>
                <div class="resume-preview">
                    <div class="resume-card">
                        <h4><i class="fas fa-code"></i> Technical Skills</h4>
                        <div>${skills.map(s => `<span class="skill-chip">${escapeHtml(s)}</span>`).join('') || '—'}</div>
                        <hr>
                        <h4>Projects</h4>
                        ${(rd.projects || []).map(p => `<div><strong>📁 ${escapeHtml(p.name)}</strong><br><small>${escapeHtml(p.description)}</small><div>${(p.technologies || []).map(t => `<span class="skill-chip">${escapeHtml(t)}</span>`).join('')}</div></div>`).join('') || '<p>—</p>'}
                    </div>
                    <div class="resume-card" style="text-align:center;">
                        <div class="score-circle">
                            <div class="score-inner">${rs.percentage}%</div>
                        </div>
                        <h3>Resume Score: ${rs.grade}</h3>
                        <div style="text-align:left; margin-top:1rem;">
                            <strong>Feedback:</strong><br>
                            ${(rs.feedback || []).map(f => `✓ ${escapeHtml(f)}`).join('<br>')}
                        </div>
                        <button id="enterInterviewBtn" class="btn-primary" style="margin-top:1.5rem;">🎤 Enter Interview Arena</button>
                    </div>
                </div>
            `;
        }
        
        function renderResults() {
            const report = appState.finalReport;
            if (!report) return "<div>Loading report...</div>";
            const overall = report.overall_score || 0;
            const verdictText = report.final_feedback?.verdict || (overall >= 7 ? "✅ Strong Candidate" : (overall >= 5 ? "📌 Potential" : "⚠️ Needs Improvement"));
            return `
                ${renderNavbar(false)}
                <div class="results-banner">
                    <div class="verdict" style="color:${overall>=7?'#15803d':'#b45309'}">${verdictText}</div>
                    <div style="font-size:3rem; font-weight:800;">${overall}<span style="font-size:1rem;">/10</span></div>
                    <p>${report.final_feedback?.executive_summary || "Great effort across all rounds!"}</p>
                    <button id="resetBtn" class="btn-primary" style="margin-top:1rem;">🔄 Start New Interview</button>
                </div>
                <div class="resume-preview">
                    <div class="resume-card"><h4>Round Scores</h4>${Object.entries(report.round_scores || {}).map(([r,s]) => `<div>${ROUND_META[r]?.icon || r} ${ROUND_META[r]?.label || r}: <strong>${s.toFixed(1)}/10</strong></div>`).join('')}</div>
                    <div class="resume-card"><h4>Top Strengths</h4>${(report.final_feedback?.top_strengths || []).map(s => `✓ ${escapeHtml(s)}`).join('<br>') || '—'}</div>
                </div>
            `;
        }
        
        // Attach events after each render
        function attachEventListeners() {
            const uploadBtn = document.getElementById("uploadStartBtn");
            if (uploadBtn) {
                uploadBtn.onclick = async () => {
                    const fileInput = document.getElementById("resumeFileInput");
                    if (!fileInput || !fileInput.files.length) {
                        alert("Please upload a resume file (PDF/DOCX)");
                        return;
                    }
                    const mock = await mockResumeUpload();
                    updateState({
                        page: "resume_preview",
                        resumeData: mock.resume_data,
                        resumeScore: mock.resume_score,
                        chatHistory: []
                    });
                };
            }
            const enterInterview = document.getElementById("enterInterviewBtn");
            if (enterInterview) {
                enterInterview.onclick = () => {
                    updateState({ page: "interview", currentRound: "HR", roundsCompleted: [], lastEval: null, chatHistory: [] });
                    startRound("HR");
                };
            }
            const submitBtn = document.getElementById("submitBtn");
            if (submitBtn) {
                submitBtn.onclick = () => {
                    const answerArea = document.getElementById("userAnswer");
                    const ans = answerArea ? answerArea.value : "";
                    submitAnswer(ans, false);
                    if (answerArea) answerArea.value = "";
                };
            }
            const skipBtn = document.getElementById("skipBtn");
            if (skipBtn) {
                skipBtn.onclick = () => {
                    submitAnswer("", true);
                    const area = document.getElementById("userAnswer");
                    if (area) area.value = "";
                };
            }
            const resetBtn = document.getElementById("resetBtn");
            if (resetBtn) resetBtn.onclick = () => resetInterview();
        }
        
        function renderApp() {
            let html = "";
            if (appState.page === "landing") html = renderLanding();
            else if (appState.page === "resume_preview") html = renderResumePreview();
            else if (appState.page === "interview") html = renderInterview();
            else if (appState.page === "results") html = renderResults();
            else html = renderLanding();
            document.getElementById("root").innerHTML = html;
            attachEventListeners();
        }
        
        renderApp();
    })();
</script>
</body>
</html>