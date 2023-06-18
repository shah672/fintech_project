import streamlit as st


beginner_questions = [
    {
        "question": "What does ROI stand for?",
        "options": ["Return on Investment", "Rate of Interest", "Risk of Inflation"],
        "answer": "Return on Investment"
    },
    {
        "question": "What is diversification?",
        "options": ["Investing in a single asset", "Spreading investments across different assets", "Investing in foreign currencies"],
        "answer": "Spreading investments across different assets"
    },
    {
        "question": "What is a stock?",
        "options": ["A type of bond", "A partial ownership of a company", "A loan provided by a bank"],
        "answer": "A partial ownership of a company"
    },
    {
        "question": "What is the stock market?",
        "options": ["A place to buy and sell groceries", "A market for buying and selling stocks", "A market for buying and selling real estate"],
        "answer": "A market for buying and selling stocks"
    },
    {
        "question": "What is a dividend?",
        "options": ["A tax on investments", "A type of bond", "A payment made by a company to its shareholders"],
        "answer": "A payment made by a company to its shareholders"
    }
]

intermediate_questions = [
    {
        "question": "What is a mutual fund?",
        "options": ["A type of stock", "An investment vehicle that pools money from multiple investors", "A loan provided by a bank"],
        "answer": "An investment vehicle that pools money from multiple investors"
    },
    {
        "question": "What is an ETF?",
        "options": ["An Exchange-Traded Fund", "A type of mutual fund", "A tax on investments"],
        "answer": "An Exchange-Traded Fund"
    },
    {
        "question": "What is the concept of 'buy low, sell high'?",
        "options": ["Purchasing assets when prices are high and selling when prices are low", "Purchasing assets when prices are low and selling when prices are high", "Holding onto assets without selling"],
        "answer": "Purchasing assets when prices are low and selling when prices are high"
    },
    {
        "question": "What is an options contract?",
        "options": ["A contract to buy or sell a stock at a specified price before a specific date", "A contract to lend money to a company", "A contract for buying real estate"],
        "answer": "A contract to buy or sell a stock at a specified price before a specific date"
    },
    {
        "question": "What is market volatility?",
        "options": ["The ease of buying and selling stocks", "The rate of return on an investment", "The degree of variation in stock prices"],
        "answer": "The degree of variation in stock prices"
    }
]

advanced_questions = [
    {
        "question": "What is technical analysis?",
        "options": ["Analysis of a company's financial statements", "Analysis of a company's market share", "Analysis of stock price patterns and trends"],
        "answer": "Analysis of stock price patterns and trends"
    },
    {
        "question": "What is fundamental analysis?",
        "options": ["Analysis of stock price patterns and trends", "Analysis of a company's financial statements", "Analysis of market sentiment"],
        "answer": "Analysis of a company's financial statements"
    },
    {
        "question": "What is a margin call?",
        "options": ["A request for more funds from a broker to cover potential losses", "A loan provided by a bank", "A request to sell securities"],
        "answer": "A request for more funds from a broker to cover potential losses"
    },
    {
        "question": "What is a limit order?",
        "options": ["An order to buy or sell a stock at the best available price", "An order to buy or sell a stock at a specific price or better", "An order to hold onto assets without selling"],
        "answer": "An order to buy or sell a stock at a specific price or better"
    },
    {
        "question": "What is short selling?",
        "options": ["Borrowing and selling a stock with the expectation of buying it back at a lower price", "Selling stocks to buy real estate", "Investing in foreign currencies"],
        "answer": "Borrowing and selling a stock with the expectation of buying it back at a lower price"
    }
]


def main():
    st.title("Investment and Trading Quiz")
    

    level = st.selectbox("Select Level", ["Beginner", "Intermediate", "Advanced"])
 
    if level == "Beginner":
        display_questions(beginner_questions)
    elif level == "Intermediate":
        display_questions(intermediate_questions)
    elif level == "Advanced":
        display_questions(advanced_questions)
    
# Display questions
def display_questions(questions):
    st.header("Quiz Questions")
    for i, question in enumerate(questions):
        st.subheader(f"Question {i+1}:")
        st.write(question["question"])
        selected_option = st.radio(f"Select an option", question["options"], key=f"question_{i}")
        submitted = st.button(f"Submit Answer {i}")
        if submitted:
            if selected_option == "":
                st.warning("Please select an option")
            elif selected_option == question["answer"]:
                st.success("Correct!")
            else:
                st.error("Wrong. The correct answer is: " + question["answer"])
        st.write("---")

if __name__ == "__main__":
    main()
