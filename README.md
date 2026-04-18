
# Personal Finance Assistant Agent - FinanceBot

## Table of Contents

* [Project Description](#project-description)
* [Agent Design](#agent-design)

 * [Tools](#tools)
* [Setup & Installation](#setup--installation)
* [How to Run](#how-to-run)
* [Demo Queries](#demo-queries)
* [Mock Data Examples](#mock-data-examples)
* [Assumptions & Limitations](#assumptions--limitations)

---

## Project Description

**FinanceBot** is a Personal Finance Assistant Agent built using the OpenAI Agents SDK.
It helps users analyze their financial data, monitor budgets, and plan savings goals.
FinanceBot can answer complex financial questions by orchestrating multiple tools, providing insights such as transaction summaries, category-specific spending, budget evaluation, and savings projections.

---

## Agent Design

### Tools

1. **load_user_transactions**

   * **Purpose:** Retrieve and summarize all transactions for a user.
   * **Input Parameters:** `user_id` (str) — unique identifier for the user.
   * **Returns:** Total number of transactions and total spending as a formatted string.
   * **Data Source:** Mock data (`mock_data/user_transactions.json`).

2. **analyze_category_spending**

   * **Purpose:** Calculate total spending in a specific category.
   * **Input Parameters:**

     * `user_id` (str) — unique identifier for the user
     * `category` (str) — spending category (e.g., "groceries").
   * **Returns:** Total spending for the category as a formatted string.
   * **Data Source:** Mock data (`mock_data/user_transactions.json`).

3. **evaluate_monthly_budget**

   * **Purpose:** Determine if the user is within their monthly budget.
   * **Input Parameters:** `user_id` (str) — unique identifier for the user.
   * **Returns:** Budget status message.
   * **Data Source:** Mock data (`mock_data/user_budget.json`).

4. **calculate_savings_timeline**

   * **Purpose:** Estimate the number of months needed to reach a savings goal.
   * **Input Parameters:**

     * `current_savings` (float) — current saved amount
     * `savings_goal` (float) — target savings goal
     * `monthly_contribution` (float) — monthly savings amount
   * **Returns:** Timeline in months or informative message.
   * **Data Source:** Pure computation (no API needed).

---

## Setup & Installation

1. Clone or download this project.
2. Ensure you have Python 3.10+ installed.
3. Install required dependencies:

```bash
pip install openai-agents
```

4. Place all mock JSON files inside the `mock_data/` folder:

* `user_transactions.json`
* `user_budget.json`
* `savings_goals.json`

5. Set your OpenAI API key in `agent.py`:

```python
OPENAI_API_KEY = "sk-your-api-key-here"
```

---

## How to Run

Run the agent and demo queries with:

```bash
python agent.py
```

The agent will execute demo queries and print structured outputs.

---

## Demo Queries

1. **Transactions**
   **Query:** `"Show transactions for userId123"`
   **Tools Called:** `load_user_transactions`

2. **Grocery Spending**
   **Query:** `"How much does userId123 spend on groceries?"`
   **Tools Called:** `analyze_category_spending`

3. **Full Financial Analysis**
   **Query:** `"Analyze the financial situation for userId123 including transactions, grocery spending, budget status, and how long it will take to save $5000 with $200 monthly contribution and current savings of $1200."`
   **Tools Called:** All four tools

---

## Mock Data Examples

**user_transactions.json**

```json
{
  "users": {
    "userId123": [
      {
        "date": "2023-06-01",
        "category": "groceries",
        "amount": 50.00
      },
      {
        "date": "2023-06-02",
        "category": "entertainment",
        "amount": 30.00
      },
      {
        "date": "2023-06-05",
        "category": "utilities",
        "amount": 100.00
      }
    ]
}
```

**user_budget.json**

```json
{
  "users": {
    "userId123": {
      "monthly_budget": 1000.00,
      "current_month_spending": 700.00,
      "remaining_budget": 300.00,
      "spending_percentage": 70
    }
}
```

**savings_goals.json**

```json
{
   "users": {
    "userId123": {
      "goal_name": "Emergency Fund",
      "target_amount": 5000.00,
      "current_savings": 1200.00,
      "deadline": "2024-12-31",
      "progress_percentage": 24
    }
}
```

---

## Assumptions & Limitations

* Data is **mocked**, not connected to real financial accounts.
* Users are assumed to have **unique IDs**.
* Savings timeline assumes **fixed monthly contributions** with no interest.
* Category names are **case-insensitive**, but must match exactly in mock JSON.
* Agent does **not perform live API calls**, only uses mock data and pure computation.

---

