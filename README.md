Hybrid Static Analysis + Machine Learning

This project implements a hybrid security analysis framework for Ethereum smart contracts that combines:

Graph-based static analysis (reentrancy, gas-DoS)

Feature extraction from contract semantics

Machine learning–based anomaly detection (Isolation Forest)

A hybrid decision engine for final risk verdicts

The tool can be used in:

CLI mode (single contract analysis)

Batch mode (dataset generation + ML training)

GUI mode (web interface using Flask + Jinja)

1. Environment Setup
1.1 Create and activate virtual environment (recommended)
python -m venv venv


Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

1.2 Install dependencies
pip install -r requirements.txt


If requirements.txt is missing, install manually:

pip install py-solc-x pandas scikit-learn flask joblib

2. CLI Mode — Single Contract Analysis

This mode analyzes one Solidity contract and prints:

External calls

Call graph

Reentrancy findings

Gas-loop risks

Feature vector

Risk score

| Signal                     | Weight | Reason                |
| -------------------------- | ------ | --------------------- |
| Reentrancy flag            | +40    | High severity         |
| External call present      | +20    | Control transfer risk |
| Loop present               | +15    | Gas risk              |
| Loop + external call       | +30    | High gas-DoS risk     |
| Many public functions (>3) | +10    | Larger attack surface |

2.1 Run CLI scanner
python scan.py contracts/sample.sol

2.2 Example Output
External Calls Found:
Function: withdraw | Type: call

Function Call Graph:
withdraw -> _send

Reentrancy Vulnerabilities:
⚠️ Potential reentrancy in function: withdraw

Gas Limit / Loop-Based Risks:

ML Feature Vector:
num_functions: 2
num_public_functions: 1
num_external_calls: 1
num_reentrancy_flags: 1
num_loops: 0
num_loops_with_external_calls: 0


This mode is useful for:

Debugging

Understanding static analysis behavior

Viva demonstrations

3. Dataset Generation (Batch Mode)

This mode scans multiple contracts and generates a CSV dataset for ML.

3.1 Organize contracts
contracts/
├── benign/
│   ├── wallet.sol
│   └── escrow.sol
├── vulnerable/
│   ├── reentrant.sol
│   └── gas_dos.sol

3.2 Generate dataset
python dataset_builder.py

3.3 Output

A file dataset.csv will be created:

num_functions,num_public_functions,num_external_calls,...
2,1,1,1,0,0,60
1,1,1,1,1,1,105
...


Each row represents one contract.

4. Train Machine Learning Model (Isolation Forest)

This step trains an anomaly detection model on the dataset and saves it for later use.

4.1 Train model
python ml/train_iforest.py

4.2 Output artifacts
ml/
├── iforest_model.joblib
└── scaler.joblib


These files are required for GUI mode.

5. GUI Mode — Web Interface (Flask + Jinja)

The GUI allows users to:

Upload a .sol file

Run static + ML analysis

View final hybrid verdict in browser

5.1 Start the web app
python app.py

5.2 Open browser
http://127.0.0.1:5000

5.3 GUI Workflow

Upload a Solidity (.sol) file

Click Analyze

View results:

External calls

Reentrancy risks

Gas-loop risks

Feature vector

Risk score

Isolation Forest prediction

Final hybrid verdict

6. Hybrid Decision Logic (How Results Are Computed)

The final verdict combines:

Static risk score (rule-based)

Isolation Forest anomaly prediction

Decision rules:

High static risk → HIGH RISK

Medium risk + anomaly → HIGH RISK

Medium risk only → MEDIUM RISK

Anomaly only → MEDIUM RISK

Otherwise → LOW RISK

This provides:

High recall from static analysis

Reduced false positives via ML

7. Notes & Limitations (Important for Viva)

ML model is anomaly detection, not supervised classification

Dataset is curated and small (research prototype)

Reentrancy detection is conservative

GUI is for demonstration, not production hardening

All of these are intentional design choices.

8. Recommended Demo Order (Viva)

Show architecture slide

Run scan.py on a reentrant contract

Show dataset.csv

Show Isolation Forest output

Upload contract via GUI

Explain final hybrid verdict

9. Summary

This project demonstrates a hybrid smart contract security analyzer that integrates:

Graph-based static analysis

Feature engineering

Machine learning anomaly detection

Explainable hybrid decision logic

It is designed for research validation, viva defense, and future extension.