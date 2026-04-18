"""
Author: Mahtabin Tushi
Student ID: 000952184
Course: Intro to Intelligent Systems - COMP-10261
Description:
This script defines a Personal Finance Assistant Agent named FinanceBot using the OpenAI Agents SDK.
FinanceBot helps users analyze their financial data, monitor budgets, and plan savings goals by
orchestrating multiple tools. The agent demonstrates multi-step reasoning over mock datasets and
returns actionable financial insights.
"""

import json
import os
from typing import Optional
from agents import Agent, Runner, function_tool

# -------------------- API KEY PLACEHOLDER --------------------
OPENAI_API_KEY = " "
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# -------------------- DATA LOADING --------------------
def _load_json(relative_path: str) -> dict:
    """Load a JSON file from mock_data/ directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, relative_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

TRANSACTION_DATA = _load_json("mock_data/user_transactions.json")
BUDGET_DATA = _load_json("mock_data/user_budget.json")
SAVINGS_DATA = _load_json("mock_data/savings_goals.json")

# -------------------- TOOLS --------------------
@function_tool
def load_user_transactions(user_id: str) -> str:
    """
    Retrieve and summarize all transactions for a given user.

    Args:
        user_id: Unique identifier of the user (e.g., "userId123").

    Returns:
        Summary of total transactions and total spending.
    """
    transactions = TRANSACTION_DATA.get("users", {}).get(user_id, [])

    if not transactions:
        return f"No transactions found for {user_id}."

    total_spending = 0
    for t in transactions:
        total_spending += t.get("amount", 0)

    summary = (
        f"Total transactions for {user_id}: {len(transactions)} items, "
        f"Total spending: ${total_spending:.2f}"
    )

    return summary

@function_tool
def analyze_category_spending(user_id: str, category: str) -> str:
    """
    Calculate total spending in a specific category.

    Args:
        user_id: Unique identifier of the user.
        category: Spending category (e.g., "groceries", "rent").

    Returns:
        Total spending for the category.
    """
    transactions = TRANSACTION_DATA.get("users", {}).get(user_id, [])
    if not transactions:
        return f"No transaction data found for {user_id}."

    category_spending = 0
    for t in transactions:
        if t.get("category", "").lower() == category.lower():
            category_spending += t.get("amount", 0)

    return f"Total spending on {category} for {user_id}: ${category_spending:.2f}"

@function_tool
def evaluate_monthly_budget(user_id: str) -> str:
    """
    Determine if user is within monthly budget.

    Args:
        user_id: Unique identifier of the user.

    Returns:
        Budget status message.
    """
    budget_info = BUDGET_DATA.get("users", {}).get(user_id)
    if not budget_info:
        return f"No budget data found for {user_id}."

    current_spending = budget_info.get("current_month_spending", 0)
    monthly_budget = budget_info.get("monthly_budget", 0)

    if monthly_budget <= 0:
        return f"Invalid or missing monthly budget for {user_id}."

    status = "on budget" if current_spending <= monthly_budget else "over budget"

    return f"Your budget status for {user_id}: You are currently {status}."

@function_tool
def calculate_savings_timeline(
    current_savings: float,
    savings_goal: float,
    monthly_contribution: float
) -> str:
    """
    Estimate how many months are needed to reach a savings goal.

    Args:
        current_savings: Current amount saved.
        savings_goal: Target savings goal.
        monthly_contribution: Monthly savings contribution.

    Returns:
        Timeline in months or informative message.
    """
    if monthly_contribution <= 0:
        return "Monthly contribution must be greater than zero."

    remaining = savings_goal - current_savings
    if remaining <= 0:
        return "You have already reached your savings goal."

    months_needed = remaining / monthly_contribution
    return f"Months needed to reach savings goal: {months_needed:.1f} months."

# -------------------- AGENT --------------------
SYSTEM_PROMPT = """
You are FinanceBot, a Personal Finance Assistant designed to help users manage their finances.
You can summarize user transactions, analyze spending by category, evaluate budget status,
and calculate savings timelines. Always use the available tools to answer queries and
combine multiple tool outputs into coherent financial insights. Ask for missing information if needed.
"""

personal_finance_agent = Agent(
    name="FinanceBot",
    model="gpt-4o",
    instructions=SYSTEM_PROMPT,
    tools=[
        load_user_transactions,
        analyze_category_spending,
        evaluate_monthly_budget,
        calculate_savings_timeline,
    ],
)

# -------------------- DEMO QUERIES --------------------
DEMO_QUERIES = [
    {
        "title": "Demo 1 - Transactions",
        "query": "Show transactions for userId123"
    },
    {
        "title": "Demo 2 - Grocery Spending",
        "query": "How much does userId123 spend on groceries?"
    },
    {
        "title": "Demo 3 - Full Financial Analysis",
        "query": (
            "Analyze the financial situation for userId123 including transactions, "
            "grocery spending, budget status, and how long it will take to save $5000 "
            "with $200 monthly contribution and current savings of $1200."
        )
    }
]

# -------------------- MAIN --------------------
def main():
    print("Running Demo Queries...\n")
    for demo in DEMO_QUERIES:
        print(f"{demo['title']}: {demo['query']}")
        result = Runner.run_sync(personal_finance_agent, demo['query'])
        print(result.final_output)
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()