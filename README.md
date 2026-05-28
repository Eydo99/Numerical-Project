# 🔢 Numerical Methods Solver

<div align="center">

![Numerical Methods Solver](https://img.shields.io/badge/Numerical-Methods_Solver-6366f1?style=for-the-badge&logo=python&logoColor=white)
![Angular](https://img.shields.io/badge/Angular-18-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)

**An interactive, full-stack numerical methods solver with step-by-step simulation, function plotting, and real-time visualization.**

[Features](#-features) · [Architecture](#-architecture) · [Getting Started](#-getting-started) · [Methods](#-supported-methods) · [API Reference](#-api-reference)

</div>

---

## ✨ Features

- **Two solver phases** — Linear Algebra (Phase 1) and Root Finding (Phase 2)
- **Step-by-step simulation** — Watch each iteration animate in real time
- **Function plotter** — Visualize f(x), g(x), or both on the same graph with configurable axes
- **Custom function input** — A full-featured math keyboard with trig, hyperbolic, power, log, roots, and constant buttons
- **Error analysis** — Relative error, correct significant figures, and convergence status for every solve
- **Scaling & pivoting** — Optional scaled partial pivoting for Gaussian and LU methods
- **Dark-themed UI** — A sleek navy/indigo interface built for extended sessions

---

## 🏗️ Architecture

```
📦 NumericalSolver
├── 🐍 Backend (Python / Flask)
│   ├── app.py                      # Flask entry point
│   ├── routes/
│   │   ├── lse.py                  # Linear system endpoints
│   │   └── rootfinding.py          # Root finding endpoints
│   ├── LSE/                        # Linear System of Equations solvers
│   │   ├── GaussEliminationStandard/
│   │   │   ├── gauss_solver.py
│   │   │   └── gauss_jordan.py
│   │   ├── LUStandard/
│   │   │   ├── dolittle_solver.py
│   │   │   ├── crout_solver.py
│   │   │   └── cholesky_solver.py
│   │   ├── Iterative/
│   │   │   ├── jacobi_solver.py
│   │   │   └── gauss_seidel_solver.py
│   │   └── utils/
│   └── RootFinding/                # Root finding solvers
│       ├── BracketingMethods/
│       │   ├── bisection_method.py
│       │   └── false_position.py
│       ├── OpenMethods/
│       │   ├── fixedPoint_method.py
│       │   ├── original_newtonRaphson_method.py
│       │   ├── modified_newtonRaphson.py
│       │   └── secant_method.py
│       ├── plotter.py
│       └── utils/
└── 🅰️ Frontend (Angular 18)
    └── src/app/
        ├── home/                   # Landing page
        ├── phase1/                 # Linear algebra solver
        ├── phase2/                 # Root finding solver
        ├── components/
        │   ├── topbar/             # Method selection bar
        │   ├── input/              # Math keyboard & settings
        │   ├── output/             # Results & step viewer
        │   └── simulator/          # Step-by-step playback
        └── services/
            ├── rootfinding.service.ts
            └── solve-service.ts
```

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.9+ |
| Node.js | 18+ |
| npm | 9+ |

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/numerical-solver.git
cd numerical-solver

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install flask flask-cors sympy numpy matplotlib scipy

# Start the backend server
python app.py
# Server runs on http://127.0.0.1:8080
```

### Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install

# Start the development server
ng serve
# App runs on http://localhost:4200
```

---

## 📐 Supported Methods

### Phase 1 — Linear Algebra Solver

Solves systems of linear equations **Ax = b** with matrix sizes from 2×2 up to 8×8.

| Method | Description | Features |
|--------|-------------|----------|
| **Gaussian Elimination** | Forward elimination + back substitution | Scaled partial pivoting, step simulation |
| **Gauss-Jordan** | Full elimination to reduced row echelon form | Scaled partial pivoting, step simulation |
| **LU Decomposition (Doolittle)** | Decomposes A into L·U with unit upper diagonal | Scaled partial pivoting, L/U matrix simulation |
| **LU Decomposition (Crout)** | Decomposes A into L·U with unit lower diagonal | Step-by-step L/U visualization |
| **LU Decomposition (Cholesky)** | For symmetric positive-definite matrices | Symmetry and PD validation |
| **Jacobi Method** | Iterative diagonal update | Diagonal dominance check, convergence tracking |
| **Gauss-Seidel** | Iterative in-place update | Diagonal dominance permutation, convergence tracking |

**Special flags reported:**
- ✅ Diagonally dominant (convergence guaranteed)
- ⚠️ Not diagonally dominant (may or may not converge)
- ❌ Singular, asymmetric, or non-positive-definite matrix

---

### Phase 2 — Root Finding Solver

Finds roots of nonlinear equations f(x) = 0.

| Method | Type | Required Inputs |
|--------|------|----------------|
| **Bisection** | Bracketing | Interval [a, b] |
| **False Position (Regula Falsi)** | Bracketing | Interval [a, b] |
| **Fixed Point Iteration** | Open | Initial guess x₀, g(x) |
| **Newton-Raphson (Original)** | Open | Initial guess x₀ |
| **Newton-Raphson (Modified 1)** | Open | Initial guess x₀, multiplicity m |
| **Newton-Raphson (Modified 2)** | Open | Initial guess x₀ |
| **Secant Method** | Open | Two initial guesses x₀, x₁ |

**Results include:**
- Approximate root x ≈
- Number of iterations
- Execution time (ms)
- Relative error percentage
- Correct significant figures
- Convergence status (Converged / Diverged)

---

## 🎹 Math Keyboard

The function input panel provides a full on-screen keyboard:

| Category | Functions |
|----------|-----------|
| **Trig** | sin, cos, tan, sec, csc, cot and their inverses |
| **Hyperbolic** | sinh, cosh, tanh, sech, csch, coth and their inverses |
| **Powers** | x², x³, xⁿ, nˣ, n!, eˣ |
| **Log** | ln, log₁₀, logₙ |
| **Roots** | √, ∛, ⁿ√ |
| **Constants** | π, e |

A blinking cursor tracks your position and supports click-to-position, left/right navigation, and backspace deletion.

---

## 📊 Function Plotter

Configure the plot before running a method:

```
X Start / X End   →   Horizontal axis range
Y Start / Y End   →   Vertical axis range (clip tall spikes)
```

**Plot modes:**
- **Standard** — Plot f(x) alone
- **f(x) & g(x)** — Overlay both functions (Fixed Point mode)
- **x & g(x)** — Check convergence visually (Fixed Point mode)

---

## 🌐 API Reference

All endpoints accept and return JSON. Base URL: `http://127.0.0.1:8080`

### Linear Algebra Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/solve/gausselim` | POST | Gaussian Elimination |
| `/solve/gaussjordan` | POST | Gauss-Jordan |
| `/solve/dolittle` | POST | LU Doolittle |
| `/solve/crout` | POST | LU Crout |
| `/solve/cholesky` | POST | LU Cholesky |
| `/solve/jacobi` | POST | Jacobi iteration |
| `/solve/gauss_seidel` | POST | Gauss-Seidel iteration |

**Request body (linear):**
```json
{
  "dim": 3,
  "coeff": [[3, -0.1, -0.2], [0.1, 7, -0.3], [0.3, -0.2, 10]],
  "answers": [7.85, -19.3, 71.4],
  "sig_figs": 4,
  "max_itrs": 100,
  "tol": 0.0001,
  "initial": [0, 0, 0],
  "scaling": true,
  "single_step": true
}
```

**Response:**
```json
{
  "result": [3.0, -2.5, 7.0],
  "steps": [...],
  "exec_time": 0.000123,
  "itr_cnt": 5,
  "flags": { "dd": true, "conv": 1 }
}
```

---

### Root Finding Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bisection` | POST | Bisection method |
| `/false_position` | POST | False position |
| `/fixed_point` | POST | Fixed point iteration |
| `/classic_newton` | POST | Newton-Raphson original |
| `/modified_newton` | POST | Newton-Raphson modified |
| `/secant` | POST | Secant method |
| `/plot` | POST | Function plotting → PNG blob |

**Request body (root finding):**
```json
{
  "func": "x**3 - 6*x**2 + 11*x - 6",
  "first": 1.5,
  "second": 2.5,
  "tol": 0.00001,
  "max_itrs": 50,
  "sig_figs": 6,
  "single_step": true
}
```

**Response:**
```json
{
  "sol": 2.0,
  "itrs": 14,
  "steps": [...],
  "status": 1,
  "exec_time": 0.000089,
  "rel_err": 4.2e-6,
  "corr_sig_figs": 5
}
```

---

## ⚙️ Configuration

### Solver Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| Max Iterations | 50 | Upper bound on iteration count |
| Tolerance (ε) | 0.00001 | Stopping criterion |
| Significant Figures | 6 | Rounding precision throughout |

### Plot Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| X Start | -10 | Left bound of plot |
| X End | 10 | Right bound of plot |
| Y Start | -10 | Bottom bound of plot |
| Y End | 10 | Top bound of plot |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend framework | Angular 18 (standalone components) |
| Styling | Custom CSS + Tailwind CSS |
| HTTP client | Angular HttpClient |
| Backend framework | Flask (Python) |
| Symbolic math | SymPy |
| Numerical arrays | NumPy |
| Plotting | Matplotlib |
| CORS | Flask-CORS |

---

## 📁 Key Design Patterns

- **Step Recorder pattern** — Every solver optionally records each iteration into a typed step list, enabling the frontend simulator without coupling solve logic to display logic.
- **LinearSystem model** — Deep-copies input data on construction so solvers never mutate caller data.
- **FunctionParser utility** — Translates the user's math-keyboard input (e.g. `sin(x^2)`) into Python/SymPy-compatible syntax (`sin(x**2)`) before sending to the backend.
- **Blueprint routing** — Flask routes are split into `lse` and `rootfinding` blueprints for clean separation.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

---
