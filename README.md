# Ezzzit - Interactive Code Execution & Visualization Platform

<div align="center">

**A powerful educational platform for visualizing code execution with AI-powered insights**

[Live Demo](https://systemnotfound.xyz) • [Report Bug](https://github.com/sumit-bhagat-2004/ezzzit/issues) • [Request Feature](https://github.com/sumit-bhagat-2004/ezzzit/issues)

</div>

---

## 🚀 Overview

Ezzzit is an advanced code execution and visualization platform designed for computer science education. It provides real-time code tracing, intelligent data structure visualizations, AI-powered explanations, and voice-enabled learning experiences. Built with modern technologies and deployed on Digital Ocean, Ezzzit makes understanding complex algorithms and data structures easier than ever.

### ✨ Key Features

- 🔄 **Real-Time Code Tracing** - Step-by-step execution visualization with adjustable playback speed
- 🎨 **Smart Data Structure Visualizations** - Dynamic visualizations for Arrays, Stacks, Queues, Graphs, Sets, Maps, and Matrices
- 🤖 **AI-Powered Analysis** - Intelligent code analysis and insights using Google Gemini
- 📚 **RAG-Based Explanations** - Context-aware explanations powered by Snowflake vector database
- 🎙️ **Voice Explanations** - Audio explanations using ElevenLabs text-to-speech
- 🎯 **Multi-Level Learning** - Beginner, Medium, and Advanced explanation levels
- ⚡ **Secure Code Execution** - Sandboxed execution environment via Judge0
- 🔐 **Authentication** - Secure user authentication with Auth0

---

## 🛠️ Technology Stack

### Frontend

- **[Next.js 16](https://nextjs.org/)** - React framework with App Router
- **[React 19](https://react.dev/)** - UI library
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **[Monaco Editor](https://microsoft.github.io/monaco-editor/)** - VS Code-powered code editor
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Framer Motion](https://www.framer.com/motion/)** - Animation library
- **[Auth0](https://auth0.com/)** - Authentication and authorization
- **[ElevenLabs React SDK](https://elevenlabs.io/)** - AI voice generation
- **[XYFlow React](https://reactflow.dev/)** - Interactive graph visualization
- **[Lucide React](https://lucide.dev/)** - Icon library
- **[ShadcN UI](https://ui.shadcn.com/)** - Component library

### Backend Services

#### Main API Server (`/server`)

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI web server
- **[Judge0](https://judge0.com/)** - Code execution engine
- **[Google Gemini API](https://ai.google.dev/)** - AI-powered code analysis
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation

#### RAG Service (`/rag_service`)

- **[FastAPI](https://fastapi.tiangolo.com/)** - API framework
- **[Snowflake](https://www.snowflake.com/)** - Cloud data platform & vector database
- **[Snowflake Arctic Embed](https://www.snowflake.com/en/data-cloud/arctic/)** - Embedding model
- **[HTTPX](https://www.python-httpx.org/)** - Async HTTP client

### Infrastructure & Hosting

- **[Digital Ocean](https://www.digitalocean.com/)** - Cloud hosting platform
- **[Judge0 CE](https://github.com/judge0/judge0)** - Self-hosted code execution
- **[Snowflake Cortex](https://www.snowflake.com/en/data-cloud/cortex/)** - Vector search & embeddings

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│                  https://systemnotfound.xyz                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Monaco Editor │ Visualizers │ Timeline Controls     │  │
│  │  AI Analysis Panel │ Voice Controls │ Variable Table │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬─────────────────────────┬──────────────────────┘
             │                         │
    ┌────────▼────────┐       ┌────────▼─────────┐
    │  Main API       │       │  RAG Service     │
    │  (FastAPI)      │       │  (FastAPI)       │
    │  Port 8000      │       │  Port 8001       │
    │                 │       │                  │
    │  ┌───────────┐  │       │  ┌────────────┐ │
    │  │  Judge0   │  │       │  │ Snowflake  │ │
    │  │  Executor │  │       │  │ Vector DB  │ │
    │  └───────────┘  │       │  └────────────┘ │
    │  ┌───────────┐  │       │  ┌────────────┐ │
    │  │  Gemini   │  │       │  │  Concept   │ │
    │  │  AI API   │  │       │  │ Extractor  │ │
    │  └───────────┘  │       │  └────────────┘ │
    └─────────────────┘       └──────────────────┘
             │                         │
    ┌────────▼─────────────────────────▼────────┐
    │         Digital Ocean Cloud                │
    │  (Ubuntu Droplets + Load Balancer)         │
    └────────────────────────────────────────────┘
```

---

## 📦 Project Structure

```
ezzzit/
├── ezzzit-client/          # Next.js frontend application
│   ├── app/                # Next.js app router
│   │   ├── api/            # API routes
│   │   └── editor/         # Code editor page
│   ├── components/         # React components
│   │   ├── visualizers/    # Data structure visualizers
│   │   ├── Editor.tsx      # Main code editor
│   │   ├── TimelineControls.tsx  # Playback controls
│   │   ├── AIAnalysisPanel.tsx   # AI insights panel
│   │   └── VoiceExplainControls.tsx  # Voice controls
│   └── lib/                # Utility libraries
│       ├── TracePlayer.ts  # Execution trace player
│       └── dataTypeDetector.ts  # Type detection
│
├── server/                 # Main FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── services/           # Business logic
│   │   ├── judge0_client.py      # Judge0 integration
│   │   ├── gemini_service.py     # Gemini AI service
│   │   └── injector.py           # Code tracer injector
│   ├── models/             # Pydantic models
│   └── tracer/             # Python tracer templates
│
└── rag_service/            # RAG explanation service
    ├── app.py              # FastAPI application
    ├── config.py           # Snowflake configuration
    ├── docs/               # Programming concept documentation
    ├── execution/          # Concept extraction
    ├── explainer/          # Step-by-step explanations
    ├── retrieval/          # Vector search
    └── trace_analysis/     # Trace processing
```

---

## 🚦 Getting Started

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.10+
- **Judge0** instance (self-hosted or cloud)
- **Snowflake** account
- **API Keys**:
  - Auth0 credentials
  - Google Gemini API key
  - ElevenLabs API key
  - Snowflake credentials

### Environment Variables

#### Frontend (`.env.local`)

```env
AUTH0_SECRET=your_auth0_secret
AUTH0_BASE_URL=http://localhost:3000
AUTH0_ISSUER_BASE_URL=https://your-domain.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_RAG_API_URL=http://localhost:8001
```

#### Backend Server (`.env`)

```env
JUDGE0_URL=https://systemnotfound.xyz
GEMINI_API_KEY=your_gemini_api_key
```

#### RAG Service (`.env`)

```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
EXECUTION_API_URL=http://localhost:8000
```

### Installation

#### 1. Frontend Setup

```bash
cd ezzzit-client
npm install
npm run dev
```

Access at: http://localhost:3000

#### 2. Backend Server Setup

```bash
cd server
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API available at: http://localhost:8000

#### 3. RAG Service Setup

```bash
cd rag_service
pip install -r requirements.txt
uvicorn app:app --reload --port 8001
```

API available at: http://localhost:8001

---

## 🎯 Core Features Explained

### 1. Code Execution & Tracing

- Submit code in Python, JavaScript, or Java
- Secure execution via Judge0 sandbox
- Step-by-step variable tracking
- Call stack visualization
- Adjustable playback speed (0.25x - 2x)

### 2. Data Structure Visualizations

**Automatic Detection & Visualization:**

- **Arrays**: Indexed element display with highlighting
- **Matrices**: 2D grid visualization
- **Stacks**: LIFO structure with push/pop animation
- **Queues**: FIFO structure with enqueue/dequeue
- **Sets**: Unique element collections
- **Maps/Dictionaries**: Key-value pair visualization
- **Graphs**: Interactive node-edge diagrams with XYFlow

### 3. AI-Powered Analysis

**Powered by Google Gemini:**

- Automatic data structure detection
- Algorithm pattern recognition
- Complexity analysis
- Code quality insights
- Operation summaries

### 4. RAG-Based Explanations

**Snowflake Vector Search:**

- Context-aware concept retrieval
- Step-by-step explanations
- Three difficulty levels
- Programming concept documentation
- Relevant code examples

### 5. Voice Explanations

**ElevenLabs Integration:**

- Text-to-speech for all explanations
- Natural, human-like narration
- Play/pause controls
- synchronized with code execution

---

## 🔧 API Endpoints

### Main Server (Port 8000)

```
POST /execute
  - Execute code and return trace
  - Body: { code, language, stdin }
  - Response: { output, trace, steps, ai_analysis }

POST /analyze
  - Get AI analysis of code
  - Body: { code, language, trace_data, output }
  - Response: { structures, summary, trace_enrichment }
```

### RAG Service (Port 8001)

```
POST /rag/explain_trace
  - Get RAG-enhanced explanations
  - Body: { code, language, stdin, level }
  - Response: { trace, concepts, explanations }

GET /rag/health
  - Health check endpoint
```

---

## 📊 Performance & Limits

- **Execution Time**: 3s CPU time limit, 5s wall time limit
- **Memory**: 128MB per execution
- **Trace Steps**: Optimized for up to 1000 steps
- **Concurrent Users**: Scalable on Digital Ocean infrastructure

---

## 🔐 Security Features

- Sandboxed code execution via Judge0
- Auth0 user authentication
- Environment variable protection
- Rate limiting on API endpoints
- Input validation with Pydantic
- CORS configuration

---

## 🎓 Use Cases

- **Computer Science Education**: Learn algorithms and data structures
- **Interview Preparation**: Practice coding problems with visualizations
- **Debugging**: Understand code execution flow
- **Teaching**: Demonstrate concepts to students
- **Self-Learning**: Explore programming concepts at your own pace

---

## 🚀 Deployment

### Digital Ocean Deployment

The application is deployed on Digital Ocean with the following setup:

1. **Frontend**: Next.js app on Ubuntu droplet with Nginx
2. **Backend Services**: Python APIs on separate droplets
3. **Judge0**: Self-hosted Judge0 CE instance
4. **Database**: Snowflake cloud data platform
5. **Load Balancer**: Digital Ocean load balancer for high availability

**Production URL**: [https://systemnotfound.xyz](https://systemnotfound.xyz)

### Build Commands

```bash
# Frontend production build
cd ezzzit-client
npm run build
npm run start

# Backend services (run with process manager like PM2 or systemd)
uvicorn main:app --host 0.0.0.0 --port 8000
uvicorn app:app --host 0.0.0.0 --port 8001
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Judge0** - For the powerful code execution engine
- **Google Gemini** - For AI-powered code analysis
- **Snowflake** - For vector database and embeddings
- **ElevenLabs** - For natural voice synthesis
- **Digital Ocean** - For reliable cloud hosting
- **Monaco Editor** - For VS Code-quality code editing
- **Next.js Team** - For the amazing React framework

---

## 📧 Contact

Project Link: [https://github.com/yourusername/ezzzit](https://github.com/yourusername/ezzzit)

Website: [https://systemnotfound.xyz](https://systemnotfound.xyz)

---

<div align="center">

**Made with ❤️ for Computer Science Education**

⭐ Star us on GitHub — it motivates us a lot!

</div>
