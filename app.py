import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Import for PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import base64

# Set page config
st.set_page_config(
    page_title='AI Financial Advisor — By Ayush Shukla', 
    page_icon='🤖', 
    layout='wide',
    initial_sidebar_state='auto'
)

# Super Impressive Enhanced Light Theme
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    .main .block-container {
        background-color: #ffffff;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.12);
        margin: 1rem auto;
        max-width: 1400px;
        border: 1px solid #f1f5f9;
    }
    
    /* Perfect text visibility */
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1 { font-size: 2.5rem !important; margin-bottom: 1rem !important; }
    h2 { font-size: 2rem !important; margin-bottom: 0.75rem !important; }
    h3 { font-size: 1.5rem !important; margin-bottom: 0.5rem !important; }
    
    p, div, span, label, .stMarkdown, .stText {
        color: #374151 !important;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Enhanced widget styling */
    .stNumberInput>div>div>input, .stTextInput>div>div>input {
        color: #1e293b !important;
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 12px 16px !important;
    }
    
    .stSelectbox>div>div>select {
        color: #1e293b !important;
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 12px !important;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        height: 6px !important;
        border-radius: 10px !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        margin: 8px 0;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #f1f5f9;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        margin-bottom: 0.5rem;
    }
    
    /* Enhanced custom components */
    .ml-insight {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #7dd3fc;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #0c4a6e !important;
        font-weight: 500;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(125, 211, 252, 0.15);
        border-left: 4px solid #0ea5e9;
    }
    
    .financial-sticker {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #86efac;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #166534 !important;
        font-weight: 500;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(134, 239, 172, 0.15);
        border-left: 4px solid #22c55e;
    }
    
    .ai-prediction {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 2px solid #fcd34d;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #92400e !important;
        font-weight: 500;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(252, 211, 77, 0.15);
        border-left: 4px solid #f59e0b;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
        border: 2px solid #c4b5fd;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #5b21b6 !important;
        font-weight: 500;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(196, 181, 253, 0.15);
        border-left: 4px solid #8b5cf6;
    }
    
    /* Quiz specific styling */
    .quiz-question {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px solid #7dd3fc;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(125, 211, 252, 0.2);
    }
    
    /* Personality result cards */
    .personality-conservative {
        background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%);
        border: 3px solid #3b82f6;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
    }
    
    .personality-moderate {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #f59e0b;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    }
    
    .personality-aggressive {
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
        border: 3px solid #ef4444;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
    }
    
    .personality-balanced {
        background: linear-gradient(135deg, #bbf7d0 0%, #86efac 100%);
        border: 3px solid #22c55e;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.2);
    }
    
    /* Social links */
    .social-link {
        display: inline-block;
        padding: 15px 25px;
        margin: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        text-decoration: none;
        border-radius: 12px;
        transition: all 0.3s ease;
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .social-link:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        color: white !important;
        text-decoration: none;
    }
    
    /* Tab enhancements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: #f8fafc;
        border-radius: 12px 12px 0 0;
        padding: 15px 20px;
        font-weight: 600;
        font-size: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .metric-value {
            font-size: 2rem !important;
        }
        .metric-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- PDF Report Generator ---
class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
    def create_comprehensive_pdf(self, user_data, goals, portfolio, quiz_results=None, ml_insights=None):
        """Create a comprehensive PDF report with all user details and analysis"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=72, bottomMargin=72)
        
        styles = self.styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=30,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=6
        )
        
        story = []
        
        # Title
        story.append(Paragraph("AI Financial Advisor - Comprehensive Report", title_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        total_expenses = sum(user_data.get('expenses', {}).values())
        monthly_income = user_data.get('monthly_income', 0)
        monthly_savings = monthly_income - total_expenses
        savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        story.append(Paragraph(f"Financial Health Score: {self.calculate_health_score(user_data)}/100", normal_style))
        story.append(Paragraph(f"Monthly Income: ₹{monthly_income:,.0f}", normal_style))
        story.append(Paragraph(f"Monthly Savings: ₹{monthly_savings:,.0f} ({savings_rate:.1f}%)", normal_style))
        story.append(Paragraph(f"Total Goals: {len(goals)}", normal_style))
        story.append(Spacer(1, 15))
        
        # Personal Information
        story.append(Paragraph("Personal Information", heading_style))
        personal_data = [
            ['Field', 'Value'],
            ['Age', str(user_data.get('age', 'Not specified'))],
            ['Investment Experience', f"{user_data.get('investment_experience', 0)}/5"],
            ['Monthly Income', f"₹{user_data.get('monthly_income', 0):,.0f}"],
            ['Current Savings', f"₹{user_data.get('current_savings', 0):,.0f}"],
            ['Investment Percentage', f"{user_data.get('investment_percentage', 0)}%"]
        ]
        
        personal_table = Table(personal_data, colWidths=[2.5*inch, 2.5*inch])
        personal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1'))
        ]))
        story.append(personal_table)
        story.append(Spacer(1, 15))
        
        # Expense Analysis
        if total_expenses > 0:
            story.append(Paragraph("Expense Breakdown", heading_style))
            expenses = user_data.get('expenses', {})
            expense_data = [['Category', 'Amount (₹)', 'Percentage']]
            for category, amount in expenses.items():
                if amount > 0:
                    percentage = (amount / total_expenses) * 100
                    expense_data.append([category, f"₹{amount:,.0f}", f"{percentage:.1f}%"])
            
            expense_table = Table(expense_data, colWidths=[1.8*inch, 1.5*inch, 1.2*inch])
            expense_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0'))
            ]))
            story.append(expense_table)
            story.append(Spacer(1, 15))
        
        # Goals Section
        if goals:
            story.append(Paragraph("Financial Goals", heading_style))
            goals_data = [['Goal Name', 'Target Amount', 'Timeline', 'Monthly SIP Required']]
            
            for goal in goals:
                r = goal.get('return_rate', 8)/100/12
                n = goal.get('years', 1)*12
                target = goal.get('amount', 0)
                if r > 0 and n > 0:
                    sip = target * (r / ((1+r)**n - 1)) if (1+r)**n > 1 else target / n
                else:
                    sip = target / n if n > 0 else 0
                
                goals_data.append([
                    goal.get('name', 'Unnamed'),
                    f"₹{target:,.0f}",
                    f"{goal.get('years', 0)} years",
                    f"₹{sip:,.0f}"
                ])
            
            goals_table = Table(goals_data, colWidths=[1.5*inch, 1.2*inch, 1.0*inch, 1.5*inch])
            goals_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef3c7')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fcd34d'))
            ]))
            story.append(goals_table)
            story.append(Spacer(1, 15))
        
        # Portfolio Section
        if portfolio:
            story.append(Paragraph("Investment Portfolio", heading_style))
            portfolio_data = [['Holding', 'Category', 'Amount (₹)', 'Percentage']]
            total_portfolio = sum(item.get('amount', 0) for item in portfolio)
            
            for item in portfolio:
                percentage = (item.get('amount', 0) / total_portfolio * 100) if total_portfolio > 0 else 0
                portfolio_data.append([
                    item.get('name', 'Unnamed'),
                    item.get('category', 'Other'),
                    f"₹{item.get('amount', 0):,.0f}",
                    f"{percentage:.1f}%"
                ])
            
            portfolio_table = Table(portfolio_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
            portfolio_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd6fe'))
            ]))
            story.append(portfolio_table)
            story.append(Spacer(1, 15))
        
        # Recommendations Section
        story.append(Paragraph("AI-Powered Recommendations", heading_style))
        recommendations = self.generate_recommendations(user_data, goals, portfolio)
        for i, rec in enumerate(recommendations[:10], 1):
            story.append(Paragraph(f"{i}. {rec}", normal_style))
        
        story.append(Spacer(1, 15))
        
        # Quiz Results (if available)
        if quiz_results:
            story.append(Paragraph("Behavioral Analysis", heading_style))
            story.append(Paragraph(f"Investment Personality: {quiz_results.get('personality', 'Not assessed')}", normal_style))
            story.append(Paragraph(f"Risk Level: {quiz_results.get('risk_level', 'Not assessed')}", normal_style))
            story.append(Paragraph(f"Personality Score: {quiz_results.get('score', 0)} ({quiz_results.get('score_percentage', 0):.1f}%)", normal_style))
            story.append(Spacer(1, 10))
        
        # ML Insights (if available)
        if ml_insights:
            story.append(Paragraph("Machine Learning Insights", heading_style))
            story.append(Paragraph(f"Risk Profile: {ml_insights.get('risk_profile', 'Not assessed')}", normal_style))
            story.append(Paragraph(f"Risk Score: {ml_insights.get('risk_score', 0):.1f}/10", normal_style))
            story.append(Spacer(1, 10))
        
        # Action Plan
        story.append(Paragraph("Recommended Action Plan", heading_style))
        action_items = [
            "Review and optimize your expense categories monthly",
            "Set up automatic SIPs for your financial goals",
            "Build an emergency fund covering 6 months of expenses",
            "Diversify your investment portfolio across asset classes",
            "Regularly review and rebalance your portfolio",
            "Consider tax-saving investment options",
            "Monitor your financial health score regularly"
        ]
        
        for item in action_items:
            story.append(Paragraph(f"• {item}", normal_style))
        
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
    
    def calculate_health_score(self, user_data):
        """Calculate financial health score"""
        score = 0
        monthly_income = user_data.get('monthly_income', 0)
        total_expenses = sum(user_data.get('expenses', {}).values())
        
        if monthly_income == 0:
            return 0
            
        # Savings rate (max 40 points)
        savings_rate = ((monthly_income - total_expenses) / monthly_income) * 100
        if savings_rate >= 20:
            score += 40
        elif savings_rate >= 15:
            score += 30
        elif savings_rate >= 10:
            score += 20
        elif savings_rate >= 5:
            score += 10
        
        # Emergency fund (max 30 points)
        if total_expenses > 0:
            emergency_months = user_data.get('current_savings', 0) / total_expenses
            if emergency_months >= 6:
                score += 30
            elif emergency_months >= 4:
                score += 20
            elif emergency_months >= 2:
                score += 10
        
        # Investment commitment (max 30 points)
        investment_pct = user_data.get('investment_percentage', 0)
        if investment_pct >= 20:
            score += 30
        elif investment_pct >= 15:
            score += 20
        elif investment_pct >= 10:
            score += 10
        
        return min(score, 100)
    
    def generate_recommendations(self, user_data, goals, portfolio):
        """Generate personalized recommendations"""
        recommendations = []
        monthly_income = user_data.get('monthly_income', 0)
        total_expenses = sum(user_data.get('expenses', {}).values())
        
        if monthly_income > 0:
            savings_rate = ((monthly_income - total_expenses) / monthly_income) * 100
            # Savings recommendations
            if savings_rate < 10:
                recommendations.append("Increase your savings rate to at least 15-20% for better financial growth")
            elif savings_rate < 15:
                recommendations.append("Good savings rate! Consider optimizing expenses to reach 20% savings")
            else:
                recommendations.append("Excellent savings rate! Maintain this discipline for wealth accumulation")
            
            # Emergency fund recommendations
            if total_expenses > 0:
                emergency_months = user_data.get('current_savings', 0) / total_expenses
                if emergency_months < 3:
                    recommendations.append("Build emergency fund to cover 3-6 months of essential expenses")
                elif emergency_months < 6:
                    recommendations.append("Continue building emergency fund to reach 6 months coverage")
        
        # Investment recommendations
        investment_pct = user_data.get('investment_percentage', 0)
        if investment_pct < 10:
            recommendations.append("Start with systematic investments through SIPs in diversified mutual funds")
        elif investment_pct < 20:
            recommendations.append("Consider increasing investment allocation to 20% for accelerated wealth creation")
        
        # Goal-based recommendations
        if goals:
            total_goals_value = sum(goal.get('amount', 0) for goal in goals)
            if monthly_income > 0 and total_goals_value > monthly_income * 12:
                recommendations.append("Prioritize your goals and focus on achievable timelines")
        
        # Portfolio recommendations
        if portfolio:
            total_portfolio = sum(item.get('amount', 0) for item in portfolio)
            if monthly_income > 0 and total_portfolio < monthly_income * 6:
                recommendations.append("Diversify your portfolio across different asset classes for risk management")
        
        # Age-based recommendations
        age = user_data.get('age', 30)
        if age < 35:
            recommendations.append("Focus on equity-oriented investments for long-term wealth creation")
        elif age < 50:
            recommendations.append("Maintain balanced portfolio with mix of equity and debt instruments")
        else:
            recommendations.append("Consider shifting towards debt-oriented investments for capital preservation")
        
        return recommendations

# --- Financial Behavior Quiz Class ---
class FinancialBehaviorQuiz:
    def __init__(self):
        self.questions = [
            {
                'id': 1,
                'question': '💰 How do you react when the stock market drops by 20% in a short period?',
                'options': [
                    {'text': 'Sell everything immediately to prevent further losses', 'score': 1},
                    {'text': 'Hold my investments and wait for recovery', 'score': 3},
                    {'text': 'Review my portfolio but maintain my strategy', 'score': 5},
                    {'text': 'Buy more stocks at discounted prices', 'score': 7}
                ]
            },
            {
                'id': 2,
                'question': '📈 What is your primary investment goal?',
                'options': [
                    {'text': 'Capital preservation and safety of principal', 'score': 2},
                    {'text': 'Steady growth with minimal volatility', 'score': 4},
                    {'text': 'Balanced growth with some risk for better returns', 'score': 6},
                    {'text': 'Maximum growth potential, accepting higher volatility', 'score': 8}
                ]
            },
            {
                'id': 3,
                'question': '⏰ What is your preferred investment time horizon?',
                'options': [
                    {'text': 'Short-term (1-2 years) for specific goals', 'score': 2},
                    {'text': 'Medium-term (3-5 years) for planned expenses', 'score': 4},
                    {'text': 'Long-term (5-10 years) for wealth building', 'score': 6},
                    {'text': 'Very long-term (10+ years) for retirement', 'score': 8}
                ]
            },
            {
                'id': 4,
                'question': '🎯 How much volatility can you tolerate in your portfolio?',
                'options': [
                    {'text': 'Minimal - I prefer stable, predictable returns', 'score': 1},
                    {'text': 'Low - Small fluctuations are acceptable', 'score': 3},
                    {'text': 'Moderate - I can handle typical market swings', 'score': 5},
                    {'text': 'High - I can withstand significant ups and downs', 'score': 7}
                ]
            },
            {
                'id': 5,
                'question': '📊 How experienced are you with investing?',
                'options': [
                    {'text': 'Beginner - Just starting to learn about investing', 'score': 2},
                    {'text': 'Some experience - Have made a few investments', 'score': 4},
                    {'text': 'Experienced - Regular investor with good knowledge', 'score': 6},
                    {'text': 'Expert - Extensive experience and advanced knowledge', 'score': 8}
                ]
            },
            {
                'id': 6,
                'question': '💸 What percentage of your income are you comfortable investing?',
                'options': [
                    {'text': 'Less than 10% - Prefer to keep most cash available', 'score': 2},
                    {'text': '10-20% - Regular savings with some investment', 'score': 4},
                    {'text': '20-30% - Significant portion for wealth building', 'score': 6},
                    {'text': 'Over 30% - Maximum allocation for growth', 'score': 8}
                ]
            },
            {
                'id': 7,
                'question': '🛡️ How important is having an emergency fund to you?',
                'options': [
                    {'text': 'Extremely important - 6+ months of expenses', 'score': 2},
                    {'text': 'Very important - 3-6 months of expenses', 'score': 4},
                    {'text': 'Somewhat important - 1-3 months of expenses', 'score': 6},
                    {'text': 'Minimal - Prefer to invest most available funds', 'score': 8}
                ]
            },
            {
                'id': 8,
                'question': '🎲 How do you approach financial decisions?',
                'options': [
                    {'text': 'Very cautious - Extensive research before any decision', 'score': 2},
                    {'text': 'Careful - Research and consult before deciding', 'score': 4},
                    {'text': 'Balanced - Research but willing to take calculated risks', 'score': 6},
                    {'text': 'Opportunistic - Quick to act on good opportunities', 'score': 8}
                ]
            }
        ]
    
    def calculate_personality(self, answers):
        """Calculate investment personality based on quiz answers"""
        total_score = sum(answers.values())
        max_score = len(self.questions) * 8
        
        score_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        if score_percentage <= 30:
            personality = "🛡️ Conservative Defender"
            risk_level = "Low"
            description = "You prioritize capital preservation and prefer stable, low-risk investments."
            color = "#3b82f6"
        elif score_percentage <= 50:
            personality = "📊 Cautious Planner"
            risk_level = "Low to Moderate"
            description = "You prefer steady growth with minimal risk, balancing safety with growth opportunities."
            color = "#f59e0b"
        elif score_percentage <= 70:
            personality = "⚖️ Balanced Grower"
            risk_level = "Moderate"
            description = "You seek balanced growth through diversified investments."
            color = "#22c55e"
        else:
            personality = "🚀 Aggressive Builder"
            risk_level = "High"
            description = "You're comfortable with significant risk for maximum growth potential."
            color = "#ef4444"
        
        return {
            'personality': personality,
            'risk_level': risk_level,
            'score': total_score,
            'score_percentage': score_percentage,
            'description': description,
            'color': color
        }
    
    def get_recommendations(self, personality_result):
        """Get personalized investment recommendations based on personality"""
        personality = personality_result['personality']
        
        if "Conservative" in personality:
            return {
                'asset_allocation': {
                    'Debt Funds & FDs': '60-70%',
                    'Large Cap Equity': '20-25%',
                    'Gold': '5-10%',
                    'Cash': '5%'
                },
                'recommended_funds': [
                    'ICICI Prudential Corporate Bond Fund',
                    'HDFC Short Term Debt Fund',
                    'SBI Magnum Gilt Fund',
                    'Axis Bluechip Fund'
                ],
                'strategy': 'Focus on capital preservation with stable returns.',
                'suggestions': [
                    'Build a strong emergency fund (6+ months)',
                    'Prioritize debt instruments and fixed deposits',
                    'Consider tax-saving fixed deposits',
                    'Start with small SIPs in large cap funds'
                ]
            }
        elif "Cautious" in personality:
            return {
                'asset_allocation': {
                    'Debt Funds': '50-60%',
                    'Large Cap Equity': '30-35%',
                    'Gold': '5%',
                    'Mid Cap Equity': '5-10%'
                },
                'recommended_funds': [
                    'Mirae Asset Large Cap Fund',
                    'Kotak Corporate Bond Fund',
                    'Axis Midcap Fund',
                    'SBI Gold Fund'
                ],
                'strategy': 'Balanced approach with focus on steady growth.',
                'suggestions': [
                    'Maintain 4-6 months emergency fund',
                    'Systematic Investment Plans (SIPs) in diversified funds',
                    'Consider balanced advantage funds',
                    'Regular portfolio reviews every 6 months'
                ]
            }
        elif "Balanced" in personality:
            return {
                'asset_allocation': {
                    'Equity Funds': '60-70%',
                    'Debt Funds': '20-25%',
                    'Gold': '5%',
                    'International Funds': '5-10%'
                },
                'recommended_funds': [
                    'Parag Parikh Flexi Cap Fund',
                    'ICICI Prudential Bluechip Fund',
                    'Kotak Emerging Equity Fund',
                    'Motilal Oswal NASDAQ 100 ETF'
                ],
                'strategy': 'Growth-oriented approach with diversified portfolio.',
                'suggestions': [
                    '3-4 months emergency fund sufficient',
                    'Aggressive SIPs for long-term goals',
                    'Consider sectoral funds for diversification',
                    'Regular rebalancing of portfolio annually'
                ]
            }
        else:
            return {
                'asset_allocation': {
                    'Equity Funds': '75-85%',
                    'Debt Funds': '10-15%',
                    'Small Cap Funds': '5-10%',
                    'International Funds': '5%'
                },
                'recommended_funds': [
                    'SBI Small Cap Fund',
                    'Axis Small Cap Fund',
                    'Mirae Asset Emerging Bluechip Fund',
                    'PGIM India Midcap Opportunities Fund'
                ],
                'strategy': 'Maximum growth focus with high equity exposure.',
                'suggestions': [
                    '2-3 months emergency fund adequate',
                    'Direct equity investments can be considered',
                    'Sector rotation strategies',
                    'Systematic Transfer Plans for lump sum investments'
                ]
            }

# --- ML Financial Predictor Class ---
class MLFinancialPredictor:
    def __init__(self):
        self.risk_factors = {}
        
    def predict_risk_tolerance(self, user_data):
        """Enhanced ML model to predict risk tolerance with explainable factors"""
        age = user_data.get('age', 30)
        monthly_income = user_data.get('monthly_income', 50000)
        current_savings = user_data.get('current_savings', 100000)
        expenses = user_data.get('expenses', {})
        total_expenses = sum(expenses.values())
        total_debt = sum(user_data.get('liabilities', {}).values())
        investment_experience = user_data.get('investment_experience', 2)
        financial_goals = len(user_data.get('goals', []))
        
        # Enhanced ML-based risk score with more factors
        income_factor = min((monthly_income / 10000) * 0.25, 1.0) if monthly_income > 0 else 0
        savings_factor = min((current_savings / 50000) * 0.20, 1.0) if current_savings > 0 else 0
        debt_factor = -(total_debt / max(monthly_income, 1)) * 0.15 if total_debt > 0 else 0
        experience_factor = min((investment_experience * 2) * 0.20, 1.0)
        age_factor = min((min(age, 60) / 30) * 0.10, 0.5)
        goals_factor = min((financial_goals * 0.5) * 0.10, 0.3)
        
        risk_score = max(0, min(10, income_factor + savings_factor + debt_factor + experience_factor + age_factor + goals_factor))
        
        # Store risk factors for explainability
        self.risk_factors = {
            'Income Stability': max(0, min(10, income_factor * 10)),
            'Savings Buffer': max(0, min(10, savings_factor * 10)),
            'Debt Burden': max(0, min(10, debt_factor * -10)),
            'Investment Experience': max(0, min(10, experience_factor * 10)),
            'Age Factor': max(0, min(10, age_factor * 10)),
            'Financial Goals': max(0, min(10, goals_factor * 10))
        }
        
        if risk_score < 3:
            return "🛡️ Conservative", 0.3, risk_score, "Low risk appetite suitable for stable investments"
        elif risk_score < 7:
            return "⚖️ Balanced", 0.5, risk_score, "Moderate risk with balanced growth approach"
        else:
            return "🚀 Aggressive", 0.7, risk_score, "High risk tolerance for equity-heavy portfolios"
    
    def predict_goal_success_probability(self, goal, user_finances):
        """Enhanced ML goal prediction with multiple features"""
        monthly_savings = user_finances.get('monthly_savings', 0)
        goal_amount = goal.get('amount', 0)
        timeline = goal.get('years', 1)
        expected_return = goal.get('return_rate', 8)
        user_age = user_finances.get('age', 30)
        current_savings = user_finances.get('current_savings', 0)
        
        required_monthly = goal_amount / (timeline * 12) if timeline > 0 else 0
        savings_ratio = monthly_savings / required_monthly if required_monthly > 0 else 0
        
        # Enhanced probability calculation
        base_probability = min(savings_ratio * 0.7, 0.95)
        timeline_factor = min(timeline / 10, 1.0) * 0.15
        return_factor = min(expected_return / 12, 1.0) * 0.10
        age_factor = (1 - min(user_age, 65) / 65) * 0.05
        
        # Current savings impact
        savings_support = min(current_savings / goal_amount, 1.0) * 0.10 if goal_amount > 0 else 0
        
        final_probability = min(base_probability + timeline_factor + return_factor + age_factor + savings_support, 0.98)
        
        # ML confidence intervals
        if final_probability >= 0.8:
            confidence = "🎯 High confidence - You're on track to achieve this goal!"
            color = "#10b981"
        elif final_probability >= 0.6:
            confidence = "✅ Moderate confidence - Minor adjustments may be needed"
            color = "#f59e0b"
        elif final_probability >= 0.4:
            confidence = "⚠️ Low confidence - Consider increasing savings or extending timeline"
            color = "#f97316"
        else:
            confidence = "🚨 Very low confidence - Goal may be unrealistic with current approach"
            color = "#ef4444"
            
        return final_probability, confidence, color

    def get_financial_recommendations(self, user_data, metrics):
        """Generate comprehensive financial recommendations"""
        recommendations = []
        monthly_income = user_data.get('monthly_income', 0)
        total_expenses = sum(user_data.get('expenses', {}).values())
        
        if monthly_income > 0:
            savings_rate = ((monthly_income - total_expenses) / monthly_income) * 100
            
            # Savings recommendations
            if savings_rate < 10:
                recommendations.append("🚨 **Priority**: Increase your savings rate to at least 15-20%")
            elif savings_rate < 15:
                recommendations.append("📈 **Good Progress**: Consider optimizing expenses to reach 20% savings rate")
            else:
                recommendations.append("🎉 **Excellent**: Maintain your savings discipline for wealth accumulation")
        
        # Emergency fund recommendations
        if total_expenses > 0:
            emergency_months = user_data.get('current_savings', 0) / total_expenses
            if emergency_months < 3:
                recommendations.append("🛡️ **Priority**: Build emergency fund to cover 3-6 months of expenses")
            elif emergency_months < 6:
                recommendations.append("💰 **Good Start**: Continue building emergency fund to reach 6 months coverage")
        
        # Investment recommendations
        investment_pct = user_data.get('investment_percentage', 0)
        if investment_pct < 10:
            recommendations.append("📊 **Start Investing**: Begin with systematic investments through SIPs")
        elif investment_pct < 20:
            recommendations.append("📈 **Increase Investments**: Consider increasing allocation to 20%")
        
        # Expense optimization
        expenses = user_data.get('expenses', {})
        if total_expenses > 0:
            dining_ratio = expenses.get('Dining & Entertainment', 0) / total_expenses
            if dining_ratio > 0.15:
                recommendations.append(f"🍽️ **Spending Alert**: Dining expenses are high at {dining_ratio*100:.1f}% of total")
        
        # Age-based recommendations
        age = user_data.get('age', 30)
        if age < 35:
            recommendations.append("🎯 **Strategy**: Focus on equity-oriented investments for long-term growth")
        elif age < 50:
            recommendations.append("⚖️ **Strategy**: Maintain balanced portfolio with mix of equity and debt")
        else:
            recommendations.append("🛡️ **Strategy**: Consider shifting towards debt-oriented investments")
        
        return recommendations

# --- Portfolio Integration Class ---
class PortfolioIntegrator:
    def __init__(self):
        self.supported_brokers = {
            'zerodha': {'name': 'Zerodha Kite', 'type': 'broker'},
            'angelone': {'name': 'Angel One', 'type': 'broker'},
            'icici_direct': {'name': 'ICICI Direct', 'type': 'broker'},
            'hdfc_sec': {'name': 'HDFC Securities', 'type': 'broker'}
        }
        
        self.supported_banks = {
            'hdfc_bank': {'name': 'HDFC Bank', 'type': 'bank'},
            'icici_bank': {'name': 'ICICI Bank', 'type': 'bank'},
            'sbi_bank': {'name': 'State Bank of India', 'type': 'bank'}
        }
    
    def get_integration_instructions(self, platform_type, platform_name):
        """Provide instructions for manual integration"""
        if platform_type == 'broker':
            return f"""
            ### 📊 {platform_name} Integration Instructions
            
            **🔒 Privacy-First Approach**: For maximum security, we recommend manual CSV import:
            
            1. **Login to your {platform_name} account**
            2. **Navigate to Portfolio/Holdings section**
            3. **Export as CSV/Excel file**
            4. **Upload the file here for automatic processing**
            
            **Supported Data**:
            - Stocks & Equity Holdings
            - Mutual Fund Investments  
            - ETF Holdings
            
            **Security Note**: Your data never leaves your device.
            """
        else:
            return f"""
            ### 🏦 {platform_name} Integration Instructions
            
            **🔒 Secure Manual Integration**:
            
            1. **Login to {platform_name} Net Banking**
            2. **Go to Investments/Portfolio section**
            3. **Download investment statement (CSV/PDF)**
            4. **Upload here for local processing**
            
            **Supported Investments**:
            - Fixed Deposits (FDs)
            - Recurring Deposits (RDs)  
            - Mutual Funds via bank
            
            **Privacy Guarantee**: All data processing occurs locally.
            """
    
    def process_csv_upload(self, uploaded_file):
        """Process uploaded CSV file for portfolio data"""
        try:
            df = pd.read_csv(uploaded_file)
            processed_holdings = []
            
            for _, row in df.iterrows():
                processed_holdings.append({
                    'name': str(row.iloc[0]) if len(row) > 0 else 'Unknown',
                    'amount': float(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else 0,
                    'category': 'Imported',
                    'source': 'CSV Import'
                })
            
            return processed_holdings
        except Exception as e:
            st.error(f"Error processing CSV file: {str(e)}")
            return []

# --- Tax Planning Module ---
class TaxPlanner:
    def __init__(self):
        self.tax_saving_options = {
            'ELSS': {
                'name': 'Equity Linked Savings Scheme',
                'lockin': '3 years',
                'max_deduction': 150000,
                'returns': '12-15%',
                'risk': 'High',
                'description': 'Tax-saving mutual funds with equity exposure'
            },
            'PPF': {
                'name': 'Public Provident Fund',
                'lockin': '15 years',
                'max_deduction': 150000,
                'returns': '7.1%',
                'risk': 'Low',
                'description': 'Government-backed long-term savings'
            },
            'NPS': {
                'name': 'National Pension System',
                'lockin': 'Till retirement',
                'max_deduction': 50000,
                'returns': '8-10%',
                'risk': 'Medium',
                'description': 'Retirement-focused scheme'
            }
        }
    
    def get_tax_recommendations(self, user_data, goals):
        """Generate personalized tax saving recommendations"""
        recommendations = []
        monthly_income = user_data.get('monthly_income', 0)
        annual_income = monthly_income * 12
        
        # Basic tax slab analysis
        if annual_income <= 700000:
            recommendations.append("💡 **Tax Planning**: You're below taxable income limit. Focus on wealth creation.")
        elif annual_income <= 1200000:
            recommendations.append("💡 **Tax Planning**: Consider ELSS funds for tax saving with growth potential.")
            recommendations.append("🏦 **Recommendation**: Allocate to Section 80C instruments (ELSS, PPF)")
        else:
            recommendations.append("💡 **Tax Planning**: Maximize all tax-saving avenues including NPS.")
        
        # Age-based recommendations
        age = user_data.get('age', 30)
        if age < 40:
            recommendations.append("🎯 **Strategy**: Prefer ELSS over traditional options for better returns")
        else:
            recommendations.append("🎯 **Strategy**: Balance between ELSS and PPF for moderate risk")
        
        return recommendations
    
    def calculate_tax_savings(self, investments, annual_income):
        """Calculate potential tax savings"""
        total_investment = sum(investments.values())
        max_deduction = min(total_investment, 150000)
        
        tax_saved = 0
        if annual_income <= 700000:
            tax_saved = 0
        elif annual_income <= 900000:
            tax_saved = max_deduction * 0.05
        elif annual_income <= 1200000:
            tax_saved = max_deduction * 0.20
        else:
            tax_saved = max_deduction * 0.30
        
        return tax_saved, max_deduction

# --- Educational Content Module ---
class FinancialEducator:
    def __init__(self):
        self.concepts = {
            'behavioral_finance': {
                'title': '🧠 Behavioral Finance',
                'content': """
                **Understanding Your Money Psychology**
                
                Behavioral finance studies how psychological influences affect financial decisions.
                
                **Why it matters**: Understanding these biases helps you make rational financial decisions.
                """,
                'tip': 'Regularly review decisions to identify your behavioral patterns.'
            },
            'risk_profile': {
                'title': '🎯 Risk Profile Analysis',
                'content': """
                **Finding Your Investment Comfort Zone**
                
                Your risk profile determines suitable investments based on:
                - Risk Capacity: How much risk you can afford
                - Risk Tolerance: How much risk you're comfortable with
                - Risk Requirement: How much risk you need to achieve goals
                """,
                'tip': 'Rebalance portfolio annually to maintain your target risk level.'
            },
            'sip_vs_lumpsum': {
                'title': '💰 SIP vs Lump Sum Investing',
                'content': """
                **Choosing the Right Investment Approach**
                
                **SIP (Systematic Investment Plan)**:
                - Invest fixed amount regularly
                - Benefits from rupee cost averaging
                - Ideal for salaried individuals
                
                **Lump Sum Investing**:
                - Invest large amount at once
                - Better if markets are rising
                - Suitable for bonuses/inheritance
                """,
                'tip': 'Start with SIP for discipline, add lump sum during market corrections.'
            },
            'asset_allocation': {
                'title': '📊 Asset Allocation Strategy',
                'content': """
                **The Foundation of Smart Investing**
                
                Asset allocation means dividing investments among different categories:
                - Equity: High growth, high risk
                - Debt: Stable returns, low risk
                - Gold: Inflation hedge
                
                **Golden Rule**: Your age in percentage should be in debt instruments.
                """,
                'tip': 'Diversification is the only free lunch in investing.'
            }
        }
    
    def get_tooltip(self, concept_key):
        """Get educational tooltip for financial concepts"""
        concept = self.concepts.get(concept_key, {})
        return concept.get('tip', 'Learn more in our educational section.')

# --- Data Persistence ---
DATA_DIR = '.ai_financial_data'
os.makedirs(DATA_DIR, exist_ok=True)
SNAPSHOT_FILE = os.path.join(DATA_DIR, 'user_snapshot.json')
GOALS_FILE = os.path.join(DATA_DIR, 'user_goals.json')
PORTFOLIO_FILE = os.path.join(DATA_DIR, 'user_portfolio.json')

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def format_currency(amount):
    """Format currency with Indian numbering system"""
    return f"₹{amount:,.0f}"

# --- Investment Calculators ---
def investment_projection_calculator(monthly_investment, years, expected_return):
    monthly_rate = expected_return / 100 / 12
    months = int(years * 12)
    if monthly_rate > 0:
        future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        future_value = monthly_investment * months
    total_invested = monthly_investment * months
    profit = future_value - total_invested
    return future_value, total_invested, profit

# --- Initialize Session State ---
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_json(SNAPSHOT_FILE, {})
if 'goals' not in st.session_state:
    st.session_state.goals = load_json(GOALS_FILE, [])
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = load_json(PORTFOLIO_FILE, [])
if 'current_page' not in st.session_state:
    st.session_state.current_page = "📊 Snapshot"
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'tax_investments' not in st.session_state:
    st.session_state.tax_investments = {}

# --- Mutual Fund Data ---
@st.cache_data
def get_mutual_fund_data():
    data = {
        'Category': ['Large Cap', 'Large Cap', 'Mid Cap', 'Mid Cap', 'Small Cap', 'Small Cap', 
                    'Flexi Cap', 'Flexi Cap', 'ELSS', 'ELSS', 'Debt', 'Debt'],
        'Fund Name': ['Axis Bluechip Fund', 'Mirae Asset Large Cap', 'Axis Midcap Fund', 
                     'Kotak Emerging Equity', 'Axis Small Cap Fund', 'SBI Small Cap Fund',
                     'Parag Parikh Flexi Cap', 'PGIM India Flexi Cap', 'Mirae Asset Tax Saver',
                     'Canara Robeco Equity Tax Saver', 'ICICI Prudential Corporate Bond',
                     'HDFC Short Term Debt'],
        '1Y Return': [15.2, 16.1, 25.6, 27.2, 35.8, 38.2, 22.1, 24.5, 20.3, 21.1, 7.1, 6.8],
        '3Y CAGR': [14.5, 15.2, 22.1, 23.5, 28.9, 30.1, 19.8, 21.2, 18.5, 19.2, 6.5, 6.2],
        '5Y CAGR': [16.1, 17.2, 20.5, 21.8, 25.4, 26.8, 18.9, 20.1, 17.2, 18.1, 7.5, 7.2],
        'Risk': ['Moderate', 'Moderate', 'High', 'High', 'Very High', 'Very High', 
                'High', 'High', 'High', 'High', 'Low', 'Low'],
        'Rating': [5, 5, 5, 4, 5, 4, 5, 4, 5, 4, 4, 3]
    }
    return pd.DataFrame(data)

# --- Plotly Theme ---
def apply_plotly_theme(fig):
    """Apply consistent theme to all Plotly charts"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=14, color="#1e293b"),
        title_font=dict(size=20, color="#1e293b"),
        legend=dict(bgcolor='rgba(255,255,255,0.95)', bordercolor='#e2e8f0', borderwidth=1),
        xaxis=dict(gridcolor='#e2e8f0', gridwidth=1),
        yaxis=dict(gridcolor='#e2e8f0', gridwidth=1)
    )
    return fig

# --- Main App Header ---
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='font-size: 3rem; margin-bottom: 1rem;'>🤖 AI Financial Advisor</h1>
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1rem; border-radius: 16px; 
                margin: 1rem auto; max-width: 700px;'>
        <h2 style='color: white; margin: 0; font-size: 1.5rem;'>ML-Powered Financial Planning</h2>
        <p style='color: white; margin: 0.5rem 0 0 0; opacity: 0.95;'>Smart Analytics • Personalized Insights • Data-Driven Recommendations</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Privacy Banner ---
st.markdown("""
<div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            color: white; padding: 1rem; border-radius: 12px; 
            margin: 1rem 0; text-align: center;'>
    <h3 style='color: white; margin: 0; font-size: 1.2rem;'>🔒 100% Private & Secure</h3>
    <p style='color: white; margin: 0.25rem 0 0 0; font-size: 0.9rem;'>
    All your financial data is stored locally on your device • Complete privacy guaranteed
    </p>
</div>
""", unsafe_allow_html=True)

# --- Navigation ---
nav_options = [
    "📊 Snapshot", "📈 Dashboard", "🤖 ML Insights", 
    "🧠 Behavior Quiz", "💹 Investment Center", "🎯 Goals Planner", 
    "💼 Portfolio", "🏦 Tax Planner", "📚 Learn", "📥 Export", "👨‍💻 Developer"
]

cols = st.columns(len(nav_options))
for i, option in enumerate(nav_options):
    with cols[i]:
        if st.button(option, key=f"nav_{i}", use_container_width=True):
            st.session_state.current_page = option
            st.rerun()

st.markdown("---")

# --- Snapshot Page ---
if st.session_state.current_page == "📊 Snapshot":
    st.header('📊 Financial Snapshot')
    
    if st.session_state.user_data:
        st.markdown("""
        <div class='financial-sticker'>
            <h3>✅ Your Financial Profile is Ready!</h3>
            <p>You can update your information below or explore other features.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form('snapshot_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 Income & Profile")
            monthly_income = st.number_input('Monthly Take-Home Income (₹)', min_value=0, 
                                           value=int(st.session_state.user_data.get('monthly_income', 0)), 
                                           step=1000)
            current_savings = st.number_input('Current Savings & Emergency Fund (₹)', min_value=0, 
                                            value=int(st.session_state.user_data.get('current_savings', 0)), 
                                            step=5000)
            investment_percentage = st.slider('% of Income to Invest Monthly', 0, 100, 
                                            st.session_state.user_data.get('investment_percentage', 0))
            
            age = st.number_input('Your Age', min_value=18, max_value=80, 
                                value=st.session_state.user_data.get('age', 30))
            investment_experience = st.slider('Investment Experience Level (1-5)', 1, 5, 
                                            st.session_state.user_data.get('investment_experience', 2))
            
        with col2:
            st.markdown("### 💸 Monthly Expenses")
            expenses = st.session_state.user_data.get('expenses', {})
            rent_emi = st.number_input('🏠 Rent / Home Loan EMI (₹)', 0, 
                                     value=int(expenses.get('Rent/EMI', 0)), step=1000)
            groceries = st.number_input('🛒 Groceries & Household (₹)', 0, 
                                      value=int(expenses.get('Groceries', 0)), step=500)
            utilities = st.number_input('⚡ Utilities (₹)', 0, 
                                      value=int(expenses.get('Utilities', 0)), step=200)
            transportation = st.number_input('🚗 Transportation (₹)', 0, 
                                           value=int(expenses.get('Transportation', 0)), step=500)
            dining_entertainment = st.number_input('🍽️ Dining & Entertainment (₹)', 0, 
                                                 value=int(expenses.get('Dining & Entertainment', 0)), step=500)
            miscellaneous = st.number_input('📦 Miscellaneous (₹)', 0, 
                                          value=int(expenses.get('Miscellaneous', 0)), step=200)

        # Assets & Liabilities
        st.markdown("### 🏦 Assets & Liabilities")
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### 💎 Assets")
            assets = st.session_state.user_data.get('assets', {})
            cash_balance = st.number_input('💵 Cash & Bank Balance (₹)', 0, 
                                         value=int(assets.get('Cash', 0)), step=5000)
            stocks_mf = st.number_input('📈 Stocks & Mutual Funds (₹)', 0, 
                                      value=int(assets.get('Stocks/MF', 0)), step=10000)
            property_value = st.number_input('🏠 Property Value (₹)', 0, 
                                           value=int(assets.get('Property', 0)), step=50000)
        
        with col4:
            st.markdown("#### 📄 Liabilities")
            liabilities = st.session_state.user_data.get('liabilities', {})
            home_loan = st.number_input('🏦 Home Loan Outstanding (₹)', 0, 
                                      value=int(liabilities.get('Home Loan', 0)), step=10000)
            personal_loan = st.number_input('💳 Personal Loan Outstanding (₹)', 0, 
                                          value=int(liabilities.get('Personal Loan', 0)), step=5000)
            other_debt = st.number_input('📝 Other Debt (₹)', 0, 
                                       value=int(liabilities.get('Other Debt', 0)), step=5000)

        if st.form_submit_button('💾 Save Financial Snapshot', use_container_width=True):
            user_data = {
                'monthly_income': monthly_income,
                'current_savings': current_savings,
                'investment_percentage': investment_percentage,
                'age': age,
                'investment_experience': investment_experience,
                'expenses': {
                    'Rent/EMI': rent_emi,
                    'Groceries': groceries,
                    'Utilities': utilities,
                    'Transportation': transportation,
                    'Dining & Entertainment': dining_entertainment,
                    'Miscellaneous': miscellaneous
                },
                'assets': {
                    'Cash': cash_balance,
                    'Stocks/MF': stocks_mf,
                    'Property': property_value
                },
                'liabilities': {
                    'Home Loan': home_loan,
                    'Personal Loan': personal_loan,
                    'Other Debt': other_debt
                }
            }
            st.session_state.user_data = user_data
            save_json(SNAPSHOT_FILE, user_data)
            st.success('✅ Financial Snapshot saved successfully!')
            st.balloons()
            st.rerun()

# --- Dashboard Page ---
elif st.session_state.current_page == "📈 Dashboard":
    st.header('📈 Financial Dashboard')
    
    if not st.session_state.user_data:
        st.warning("🚨 No financial snapshot found. Please create one in 'Snapshot' first!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        user_data = st.session_state.user_data
        analyzer = MLFinancialPredictor()
        total_expenses = sum(user_data.get('expenses', {}).values())
        monthly_income = user_data.get('monthly_income', 0)
        monthly_savings = monthly_income - total_expenses
        savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
        
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>💰 Monthly Income</div>
                <div class='metric-value'>{format_currency(monthly_income)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>📊 Savings Rate</div>
                <div class='metric-value'>{savings_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            risk_profile, _, risk_score, _ = analyzer.predict_risk_tolerance(user_data)
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🛡️ Risk Profile</div>
                <div class='metric-value'>{risk_profile}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            net_worth = sum(user_data.get('assets', {}).values()) - sum(user_data.get('liabilities', {}).values())
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>🏦 Net Worth</div>
                <div class='metric-value'>{format_currency(net_worth)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("### 💡 AI Recommendations")
        metrics = {'monthly_income': monthly_income, 'total_expenses': total_expenses}
        recommendations = analyzer.get_financial_recommendations(user_data, metrics)
        for rec in recommendations:
            st.markdown(f"<div class='recommendation-card'>{rec}</div>", unsafe_allow_html=True)
        
        # Expense Analysis
        st.markdown("### 💸 Expense Analysis")
        expense_data = {k: v for k, v in user_data.get('expenses', {}).items() if v > 0}
        if expense_data:
            fig = px.pie(values=list(expense_data.values()), names=list(expense_data.keys()),
                        title='Expense Distribution')
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

# --- ML Insights Page ---
elif st.session_state.current_page == "🤖 ML Insights":
    st.header('🤖 Advanced ML Insights')
    
    if not st.session_state.user_data:
        st.warning("🚨 Please create a financial snapshot first to get ML insights!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        user_data = st.session_state.user_data
        analyzer = MLFinancialPredictor()
        
        st.markdown("### 🎯 Deep Risk Analysis")
        risk_profile, risk_allocation, risk_score, risk_explanation = analyzer.predict_risk_tolerance(user_data)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🤖 ML Risk Assessment</h3>
                <div style='text-align: center;'>
                    <h1 style='color: #7c3aed;'>{risk_profile}</h1>
                    <p><strong>Risk Score:</strong> {risk_score:.1f}/10</p>
                    <p>{risk_explanation}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📊 Risk Factor Analysis")
            for factor, score in analyzer.risk_factors.items():
                st.progress(min(score/10, 1.0), text=f"{factor}: {score:.1f}/10")
        
        with col2:
            if st.session_state.goals:
                st.markdown("### 🎯 ML Goal Success Probability")
                for goal in st.session_state.goals:
                    probability, confidence, color = analyzer.predict_goal_success_probability(goal, user_data)
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h4>🎯 {goal['name']}</h4>
                        <p>Target: {format_currency(goal['amount'])} in {goal['years']} years</p>
                        <div style='background: #e2e8f0; border-radius: 10px; height: 30px; margin: 10px 0;'>
                            <div style='background: {color}; width: {probability*100}%; height: 100%; 
                                      border-radius: 10px; text-align: center; color: white; line-height: 30px;'>
                                {probability*100:.1f}%
                            </div>
                        </div>
                        <p>{confidence}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("🎯 No goals set yet. Visit Goals Planner to set your financial goals!")

# --- Behavior Quiz Page ---
elif st.session_state.current_page == "🧠 Behavior Quiz":
    st.header('🧠 Financial Behavior Quiz')
    
    if not st.session_state.user_data:
        st.warning("🚨 Please create a financial snapshot first to get personalized quiz results!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        st.markdown("""
        <div class='financial-sticker'>
            <h3>Discover Your Investment Personality</h3>
            <p>This quiz will help us understand your financial behavior.</p>
            <p><strong>Time:</strong> 5-7 minutes | <strong>Questions:</strong> 8</p>
        </div>
        """, unsafe_allow_html=True)
        
        quiz = FinancialBehaviorQuiz()
        
        if not st.session_state.quiz_completed:
            current_q = quiz.questions[st.session_state.current_question]
            
            st.markdown(f"""
            <div class='quiz-question'>
                <h3>Question {st.session_state.current_question + 1} of {len(quiz.questions)}</h3>
                <h4>{current_q['question']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for i, option in enumerate(current_q['options']):
                if st.button(f"{option['text']}", key=f"q{current_q['id']}_opt{i}", use_container_width=True):
                    st.session_state.quiz_answers[current_q['id']] = option['score']
                    if st.session_state.current_question < len(quiz.questions) - 1:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_completed = True
                        st.rerun()
            
            progress = (st.session_state.current_question + 1) / len(quiz.questions)
            st.progress(progress, text=f"Progress: {int(progress*100)}%")
        
        else:
            st.balloons()
            st.success("🎉 Quiz Completed! Here's Your Investment Personality Analysis")
            
            personality_result = quiz.calculate_personality(st.session_state.quiz_answers)
            recommendations = quiz.get_recommendations(personality_result)
            
            personality_class = ""
            if "Conservative" in personality_result['personality']:
                personality_class = "personality-conservative"
            elif "Cautious" in personality_result['personality']:
                personality_class = "personality-moderate"
            elif "Balanced" in personality_result['personality']:
                personality_class = "personality-balanced"
            else:
                personality_class = "personality-aggressive"
            
            st.markdown(f"""
            <div class='{personality_class}'>
                <h2>{personality_result['personality']}</h2>
                <h3 style='color: {personality_result["color"]};'>Risk Level: {personality_result['risk_level']}</h3>
                <p>{personality_result['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Recommended Asset Allocation")
                for asset, percentage in recommendations['asset_allocation'].items():
                    st.write(f"**{asset}:** {percentage}")
            
            with col2:
                st.markdown("#### 🏆 Recommended Funds")
                for fund in recommendations['recommended_funds']:
                    st.write(f"• {fund}")
            
            if st.button("🔄 Take Quiz Again", use_container_width=True):
                st.session_state.quiz_answers = {}
                st.session_state.current_question = 0
                st.session_state.quiz_completed = False
                st.rerun()

# --- Investment Center Page ---
elif st.session_state.current_page == "💹 Investment Center":
    st.header('💹 Investment Center')
    
    if not st.session_state.user_data:
        st.warning("🚨 Please create a financial snapshot first!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        st.markdown("""
        <div class='financial-sticker'>
            <h3>Smart Investing Made Simple</h3>
            <p>Explore mutual funds and simulate your investment growth.</p>
        </div>
        """, unsafe_allow_html=True)
        
        mf_df = get_mutual_fund_data()
        
        tab1, tab2 = st.tabs(["💰 Lump Sum Investment", "📅 SIP Calculator"])
        
        with tab1:
            st.subheader("Lump Sum Investment Simulation")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                category = st.selectbox('Fund Category', mf_df['Category'].unique())
                funds_filtered = mf_df[mf_df['Category']==category]
                fund_name = st.selectbox('Select Fund', funds_filtered['Fund Name'])
                invest_amt = st.number_input('Investment Amount (₹)', min_value=1000, value=50000, step=1000)
                years = st.slider('Investment Period (Years)', 1, 20, 5)
                
                selected_fund = mf_df[mf_df['Fund Name']==fund_name].iloc[0]
                st.write(f"**Risk Level:** {selected_fund['Risk']}")
            
            with col2:
                future_value = invest_amt * ((1 + selected_fund['5Y CAGR']/100) ** years)
                profit = future_value - invest_amt
                
                st.markdown(f"""
                <div class='metric-card'>
                    <h3>Projected Returns</h3>
                    <p><strong>Investment Amount:</strong> {format_currency(invest_amt)}</p>
                    <p><strong>Expected Returns:</strong> {selected_fund['5Y CAGR']:.1f}% p.a.</p>
                    <p><strong>Future Value:</strong> {format_currency(future_value)}</p>
                    <p><strong>Estimated Profit:</strong> {format_currency(profit)}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.subheader("SIP Calculator")
            col1, col2 = st.columns(2)
            
            with col1:
                monthly_sip = st.number_input('Monthly SIP Amount (₹)', min_value=500, value=5000, step=500)
                sip_years = st.slider('Investment Period (Years)', 1, 30, 10)
                expected_return = st.slider('Expected Annual Return (%)', 5, 25, 12)
            
            with col2:
                future_value, total_invested, profit = investment_projection_calculator(monthly_sip, sip_years, expected_return)
                st.markdown(f"""
                <div class='metric-card'>
                    <h3>SIP Projection Results</h3>
                    <p><strong>Total Invested:</strong> {format_currency(total_invested)}</p>
                    <p><strong>Future Value:</strong> {format_currency(future_value)}</p>
                    <p><strong>Estimated Profit:</strong> {format_currency(profit)}</p>
                </div>
                """, unsafe_allow_html=True)

# --- Goals Planner Page ---
elif st.session_state.current_page == "🎯 Goals Planner":
    st.header('🎯 Goals & SIP Planner')
    
    if not st.session_state.user_data:
        st.warning("🚨 Please create a financial snapshot first!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        with st.form('goal_add'):
            st.markdown("### 🎯 Add New Financial Goal")
            col1, col2, col3 = st.columns(3)
            with col1:
                g_name = st.text_input('Goal Name', placeholder='e.g., Dream House, Car, Vacation')
            with col2:
                g_amount = st.number_input('Target Amount (₹)', min_value=0, value=500000, step=1000)
            with col3:
                g_years = st.number_input('Years to Achieve', min_value=1, value=5)
            
            g_return = st.slider('Expected Annual Return (%)', 0, 20, 8)
            
            if st.form_submit_button('🚀 Add Goal', use_container_width=True) and g_name:
                st.session_state.goals.append({
                    'name': g_name, 'amount': g_amount, 'years': g_years, 'return_rate': g_return
                })
                save_json(GOALS_FILE, st.session_state.goals)
                st.success(f'🎯 Goal "{g_name}" added!')
                st.rerun()
        
        if st.session_state.goals:
            for i, goal in enumerate(st.session_state.goals):
                r = goal['return_rate']/100/12
                n = goal['years']*12
                target = goal['amount']
                sip = target * (r / ((1+r)**n - 1)) if r > 0 and (1+r)**n > 1 else target / n if n > 0 else 0
                
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown(f"**🎯 {goal['name']}**")
                    st.write(f"Target: {format_currency(target)} | Timeline: {goal['years']} years")
                with col2:
                    st.write(f"**Monthly SIP Required:** {format_currency(sip)}")
                with col3:
                    if st.button('🗑️', key=f'del_{i}'):
                        st.session_state.goals.pop(i)
                        save_json(GOALS_FILE, st.session_state.goals)
                        st.rerun()
        else:
            st.info("🎯 No goals set yet. Add your first financial goal above!")

# --- Portfolio Page ---
elif st.session_state.current_page == "💼 Portfolio":
    st.header('💼 Portfolio Manager')
    
    with st.form('portfolio_form'):
        col1, col2, col3 = st.columns(3)
        name = col1.text_input('Holding Name')
        amt = col2.number_input('Amount (₹)', min_value=0, value=0, step=1000)
        category = col3.selectbox('Category', ['Stocks', 'Mutual Funds', 'FD/RD', 'Gold', 'Other'])
        
        if st.form_submit_button('➕ Add Holding') and name and amt>0:
            st.session_state.portfolio.append({'name': name, 'amount': amt, 'category': category})
            save_json(PORTFOLIO_FILE, st.session_state.portfolio)
            st.success('✅ Holding added!')
            st.rerun()
    
    if st.session_state.portfolio:
        pfdf = pd.DataFrame(st.session_state.portfolio)
        total_portfolio = pfdf['amount'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(pfdf.style.format({'amount': '₹{:,.0f}'}), use_container_width=True)
            st.metric("Total Portfolio Value", format_currency(total_portfolio))
        
        with col2:
            fig = px.pie(pfdf, names='category', values='amount', title='Portfolio Allocation')
            fig = apply_plotly_theme(fig)
            st.plotly_chart(fig, use_container_width=True)

# --- Tax Planner Page ---
elif st.session_state.current_page == "🏦 Tax Planner":
    st.header('🏦 Tax Planning Center')
    
    if not st.session_state.user_data:
        st.warning("🚨 Please create a financial snapshot first!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        tax_planner = TaxPlanner()
        user_data = st.session_state.user_data
        
        st.markdown("### 💡 Tax Saving Options")
        for key, option in tax_planner.tax_saving_options.items():
            with st.expander(f"📈 {option['name']}"):
                st.write(f"**Lock-in:** {option['lockin']}")
                st.write(f"**Expected Returns:** {option['returns']}")
                st.write(f"**Risk:** {option['risk']}")
                st.write(f"**Description:** {option['description']}")
                
                investment = st.number_input(f"Investment in {option['name']} (₹)", 
                                           min_value=0, 
                                           max_value=option['max_deduction'],
                                           value=0,
                                           key=f"tax_{key}")
                st.session_state.tax_investments[key] = investment
        
        if st.button("Calculate Tax Savings", use_container_width=True):
            annual_income = user_data.get('monthly_income', 0) * 12
            tax_saved, max_deduction = tax_planner.calculate_tax_savings(st.session_state.tax_investments, annual_income)
            st.metric("Estimated Tax Saved", format_currency(tax_saved))
            st.progress(min(max_deduction/150000, 1.0), text=f"80C Limit Utilization: {format_currency(max_deduction)}/1,50,000")

# --- Learn Page ---
elif st.session_state.current_page == "📚 Learn":
    st.header('📚 Financial Education Center')
    
    educator = FinancialEducator()
    
    for key, concept in educator.concepts.items():
        with st.expander(f"📖 {concept['title']}"):
            st.markdown(concept['content'])
            st.info(f"💡 **Pro Tip:** {concept['tip']}")

# --- Export Page ---
elif st.session_state.current_page == "📥 Export":
    st.header('📥 Export Reports & Data')
    
    if not st.session_state.user_data:
        st.warning("🚨 Please create a financial snapshot first!")
        if st.button("📊 Go to Snapshot", use_container_width=True):
            st.session_state.current_page = "📊 Snapshot"
            st.rerun()
    else:
        if st.button('📊 Generate PDF Report', use_container_width=True):
            pdf_generator = PDFReportGenerator()
            
            analyzer = MLFinancialPredictor()
            risk_profile, _, risk_score, _ = analyzer.predict_risk_tolerance(st.session_state.user_data)
            ml_insights = {'risk_profile': risk_profile, 'risk_score': risk_score}
            
            pdf_data = pdf_generator.create_comprehensive_pdf(
                st.session_state.user_data,
                st.session_state.goals,
                st.session_state.portfolio,
                st.session_state.get('quiz_results'),
                ml_insights
            )
            
            st.download_button(
                '📥 Download PDF Report', 
                pdf_data, 
                f'financial_report_{datetime.now().strftime("%Y%m%d")}.pdf', 
                'application/pdf'
            )

# --- Developer Page ---
elif st.session_state.current_page == "👨‍💻 Developer":
    st.header('👨‍💻 About the Developer')
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; color: white; margin-bottom: 2rem;'>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🤖</div>
        <h1 style='color: white; margin-bottom: 0.5rem;'>Ayush Shukla</h1>
        <p style='font-size: 1.2rem;'>Data Scientist & ML Engineer</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📱 Connect")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[🐙 GitHub](https://github.com/asdharupur1-boop)")
    with col2:
        st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/ayush-shukla-890072337/)")
    with col3:
        st.markdown("[📧 Email](mailto:Asdharupur1@gmail.com)")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 1rem;'>
    <p>Built with ❤️ by Ayush Shukla | AI Financial Advisor</p>
    <p>🔒 100% Private - Your data stays on your device</p>
</div>
""", unsafe_allow_html=True)
