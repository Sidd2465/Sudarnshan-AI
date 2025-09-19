import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import re
import json
from typing import List, Dict, Tuple
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Configure page
st.set_page_config(
    page_title="LegalAI Demystifier",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .analysis-box {
        background: #f8f9ff;
        border: 2px solid #e1e8ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 2px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d1f2eb;
        border: 2px solid #00b894;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Mock AI/LLM Functions (In production, replace with actual LLM API calls)
class LegalAI:
    def __init__(self):
        self.legal_terms_db = {
            "consideration": "Something of value exchanged between parties in a contract",
            "tort": "A civil wrong that causes harm to another person",
            "liability": "Legal responsibility for one's actions or debts",
            "indemnification": "Protection from legal responsibility or compensation for losses",
            "jurisdiction": "The authority of a court to hear and decide cases",
            "force majeure": "Unforeseeable circumstances that prevent fulfilling a contract",
            "arbitration": "Resolving disputes outside of court with a neutral third party",
            "liquidated damages": "Pre-agreed amount of compensation for contract breach",
            "severability": "If one part of contract is invalid, the rest remains enforceable",
            "governing law": "Which state or country's laws apply to the contract"
        }
        
    def extract_key_terms(self, text: str) -> List[Dict]:
        """Extract and explain legal terms from text"""
        terms_found = []
        text_lower = text.lower()
        
        for term, definition in self.legal_terms_db.items():
            if term in text_lower:
                # Find context around the term
                pattern = rf'.{{0,50}}{re.escape(term)}.{{0,50}}'
                matches = re.findall(pattern, text, re.IGNORECASE)
                context = matches[0] if matches else ""
                
                terms_found.append({
                    'term': term.title(),
                    'definition': definition,
                    'context': context,
                    'importance': 'High' if term in ['liability', 'governing law', 'arbitration'] else 'Medium'
                })
        
        return terms_found
    
    def simplify_legal_text(self, text: str) -> str:
        """Simulate LLM simplification of legal text"""
        # In production, this would call an actual LLM API
        time.sleep(1)  # Simulate API call delay
        
        simplified_patterns = [
            (r'\bwhereas\b', 'Since'),
            (r'\bheretofore\b', 'before this'),
            (r'\bhereinafter\b', 'from now on'),
            (r'\bnotwithstanding\b', 'despite'),
            (r'\bpursuant to\b', 'according to'),
            (r'\bshall\b', 'must'),
            (r'\bmay\b', 'can'),
            (r'\bparty of the first part\b', 'first party'),
            (r'\bparty of the second part\b', 'second party'),
        ]
        
        simplified = text
        for pattern, replacement in simplified_patterns:
            simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
        
        return simplified
    
    def analyze_document_structure(self, text: str) -> Dict:
        """Analyze document structure and provide insights"""
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        # Mock complexity analysis
        complexity_score = min(100, word_count / 10 + sentence_count / 5)
        readability = 100 - complexity_score
        
        sections = []
        if 'whereas' in text.lower():
            sections.append('Recitals/Background')
        if 'agree' in text.lower():
            sections.append('Agreement Terms')
        if 'terminate' in text.lower():
            sections.append('Termination Clauses')
        if 'govern' in text.lower():
            sections.append('Governing Law')
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'complexity_score': round(complexity_score, 1),
            'readability_score': round(readability, 1),
            'estimated_read_time': max(1, word_count // 200),
            'sections_identified': sections
        }
    
    def identify_risks_and_obligations(self, text: str) -> Dict:
        """Identify potential risks and obligations"""
        risk_keywords = ['liable', 'penalty', 'breach', 'default', 'terminate', 'forfeit', 'damages']
        obligation_keywords = ['must', 'shall', 'required', 'obligated', 'responsible', 'duty']
        
        risks = []
        obligations = []
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            if any(keyword in sentence_lower for keyword in risk_keywords):
                risks.append({
                    'text': sentence,
                    'severity': 'High' if any(word in sentence_lower for word in ['penalty', 'damages', 'forfeit']) else 'Medium'
                })
            
            if any(keyword in sentence_lower for keyword in obligation_keywords):
                obligations.append({
                    'text': sentence,
                    'type': 'Legal Obligation'
                })
        
        return {
            'risks': risks[:5],  # Top 5 risks
            'obligations': obligations[:5]  # Top 5 obligations
        }

# Initialize AI
legal_ai = LegalAI()

# Header
st.markdown("""
<div class="main-header">
    <h1>⚖️ LegalAI Document Demystifier</h1>
    <p>Transform Complex Legal Documents into Clear, Actionable Insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    
    page = st.selectbox(
        "Choose Your Tool",
        ["🏠 Home", "📄 Document Analyzer", "🔍 Smart Search", "📊 Analytics Dashboard", "❓ Legal Q&A"]
    )
    
    st.markdown("---")
    
    st.markdown("### 📋 Quick Actions")
    if st.button("📤 Upload Document"):
        st.info("Click on Document Analyzer tab")
    
    if st.button("🤖 AI Chat"):
        st.info("Click on Legal Q&A tab")
    
    st.markdown("---")
    
    # Sample documents
    st.markdown("### 📚 Sample Documents")
    sample_docs = {
        "Employment Contract": "This Employment Agreement is entered into between Company ABC and Employee. The Employee agrees to perform duties as Software Engineer. Salary shall be $75,000 annually. Either party may terminate this agreement with 30 days notice. Employee shall maintain confidentiality of proprietary information. Governing law shall be the state of California.",
        
        "Terms of Service": "By using our service, you agree to these terms. We may modify these terms at any time. Users are responsible for maintaining account security. We are not liable for any damages arising from service use. Disputes shall be resolved through binding arbitration. This agreement is governed by Delaware law.",
        
        "Lease Agreement": "Landlord leases to Tenant the premises at 123 Main St. Monthly rent is $2,000 due on the 1st. Lease term is 12 months. Tenant shall maintain premises in good condition. Late payment penalty is $50. Either party may terminate for material breach with 30 days notice."
    }
    
    selected_sample = st.selectbox("Try a sample:", ["Select sample..."] + list(sample_docs.keys()))

# Main content based on page selection
if page == "🏠 Home":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 What We Do</h3>
            <p>Our AI-powered platform transforms complex legal jargon into plain English, helping you understand contracts, agreements, and legal documents without needing a law degree.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key features
        features = [
            ("🔍 Smart Analysis", "AI-powered document parsing and term extraction"),
            ("📝 Plain English Translation", "Convert legal jargon to understandable language"),
            ("⚠️ Risk Assessment", "Identify potential risks and obligations"),
            ("📊 Visual Insights", "Charts and analytics for document complexity"),
            ("💬 Interactive Q&A", "Ask questions about your documents"),
            ("🔒 Secure Processing", "Your documents are processed securely")
        ]
        
        for title, desc in features:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Platform Stats")
        
        # Mock statistics
        stats = [
            ("Documents Analyzed", "10,247"),
            ("Terms Simplified", "25,891"),
            ("Users Helped", "3,456"),
            ("Success Rate", "94.2%")
        ]
        
        for stat_name, stat_value in stats:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{stat_value}</h3>
                <p>{stat_name}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Get Started")
        st.info("👈 Use the sidebar to navigate to different tools or upload a document to begin analysis!")

elif page == "📄 Document Analyzer":
    st.markdown("## 📄 Document Analysis & Simplification")
    
    # Document input
    doc_input_method = st.radio("How would you like to input your document?", 
                               ["📝 Paste Text", "📁 Upload File"])
    
    document_text = ""
    
    if doc_input_method == "📝 Paste Text":
        if selected_sample != "Select sample...":
            document_text = sample_docs[selected_sample]
            st.success(f"Loaded sample: {selected_sample}")
        
        document_text = st.text_area(
            "Paste your legal document here:",
            value=document_text,
            height=200,
            help="Paste the text of your legal document for AI-powered analysis"
        )
    
    else:
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=['txt', 'pdf', 'doc', 'docx'],
            help="Upload your legal document (PDF, DOC, DOCX, or TXT)"
        )
        
        if uploaded_file is not None:
            # Mock file processing
            if uploaded_file.type == "text/plain":
                document_text = str(uploaded_file.read(), "utf-8")
            else:
                st.info("File uploaded successfully! In production, this would extract text from PDF/DOC files.")
                document_text = sample_docs["Employment Contract"]  # Mock extracted text
    
    if document_text and st.button("🔍 Analyze Document", type="primary"):
        with st.spinner("🤖 AI is analyzing your document..."):
            # Document structure analysis
            structure_analysis = legal_ai.analyze_document_structure(document_text)
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Overview", "📝 Simplified Version", "⚖️ Legal Terms", 
                "⚠️ Risks & Obligations", "📈 Analytics"
            ])
            
            with tab1:
                st.markdown("### 📋 Document Overview")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Word Count", structure_analysis['word_count'])
                
                with col2:
                    st.metric("Readability Score", f"{structure_analysis['readability_score']}%")
                
                with col3:
                    st.metric("Complexity", f"{structure_analysis['complexity_score']}/100")
                
                with col4:
                    st.metric("Read Time", f"{structure_analysis['estimated_read_time']} min")
                
                # Sections identified
                if structure_analysis['sections_identified']:
                    st.markdown("### 🗂️ Document Sections Identified")
                    for section in structure_analysis['sections_identified']:
                        st.markdown(f"- {section}")
                
                # Readability assessment
                readability = structure_analysis['readability_score']
                if readability >= 70:
                    st.markdown("""
                    <div class="success-box">
                        <strong>✅ Good Readability:</strong> This document is relatively easy to understand.
                    </div>
                    """, unsafe_allow_html=True)
                elif readability >= 40:
                    st.markdown("""
                    <div class="warning-box">
                        <strong>⚠️ Moderate Complexity:</strong> This document contains some complex legal language.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                        <strong>🔴 High Complexity:</strong> This document is quite complex and may benefit from legal consultation.
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown("### 📝 Simplified Version")
                
                with st.spinner("🤖 Translating to plain English..."):
                    simplified_text = legal_ai.simplify_legal_text(document_text)
                
                st.markdown("#### Original Text:")
                st.markdown(f"""
                <div class="analysis-box">
                    {document_text}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### Simplified Version:")
                st.markdown(f"""
                <div class="success-box">
                    <strong>📝 Plain English Translation:</strong><br>
                    {simplified_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Download button for simplified version
                st.download_button(
                    label="📥 Download Simplified Version",
                    data=simplified_text,
                    file_name="simplified_document.txt",
                    mime="text/plain"
                )
            
            with tab3:
                st.markdown("### ⚖️ Legal Terms Explained")
                
                key_terms = legal_ai.extract_key_terms(document_text)
                
                if key_terms:
                    for term in key_terms:
                        with st.expander(f"📖 {term['term']} - {term['importance']} Importance"):
                            st.markdown(f"**Definition:** {term['definition']}")
                            if term['context']:
                                st.markdown(f"**Context in document:** \"{term['context']}\"")
                            
                            # Importance indicator
                            if term['importance'] == 'High':
                                st.error("🔴 High importance - Pay special attention to this term")
                            else:
                                st.warning("🟡 Medium importance - Good to understand")
                else:
                    st.info("No complex legal terms detected in this document.")
            
            with tab4:
                st.markdown("### ⚠️ Risks & Obligations Analysis")
                
                risk_analysis = legal_ai.identify_risks_and_obligations(document_text)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🚨 Potential Risks")
                    if risk_analysis['risks']:
                        for i, risk in enumerate(risk_analysis['risks'], 1):
                            severity_color = "🔴" if risk['severity'] == 'High' else "🟡"
                            st.markdown(f"""
                            <div class="analysis-box">
                                <strong>{severity_color} Risk {i} ({risk['severity']} Severity):</strong><br>
                                {risk['text']}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("✅ No significant risks identified")
                
                with col2:
                    st.markdown("#### 📋 Your Obligations")
                    if risk_analysis['obligations']:
                        for i, obligation in enumerate(risk_analysis['obligations'], 1):
                            st.markdown(f"""
                            <div class="analysis-box">
                                <strong>📝 Obligation {i}:</strong><br>
                                {obligation['text']}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No specific obligations identified")
            
            with tab5:
                st.markdown("### 📈 Document Analytics")
                
                # Complexity visualization
                fig_complexity = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = structure_analysis['complexity_score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Document Complexity"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                st.plotly_chart(fig_complexity, use_container_width=True)
                
                # Word frequency (mock data)
                st.markdown("#### 📊 Key Word Frequency")
                word_freq_data = pd.DataFrame({
                    'Word': ['Agreement', 'Party', 'Terms', 'Shall', 'Rights', 'Obligations'],
                    'Frequency': [15, 12, 10, 8, 7, 6]
                })
                
                fig_bar = px.bar(
                    word_freq_data, 
                    x='Word', 
                    y='Frequency',
                    title="Most Common Legal Terms",
                    color='Frequency',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_bar, use_container_width=True)

elif page == "🔍 Smart Search":
    st.markdown("## 🔍 Smart Document Search")
    
    st.info("Upload multiple documents and search across them using AI-powered semantic search!")
    
    # Mock search interface
    search_query = st.text_input("🔍 Search your documents:", placeholder="e.g., 'termination clauses' or 'payment terms'")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📚 Document Library")
        
        # Mock document library
        documents_df = pd.DataFrame({
            'Document': ['Employment Contract - John Doe', 'Software License Agreement', 'Terms of Service v2.1'],
            'Type': ['Employment', 'License', 'Terms'],
            'Pages': [5, 12, 8],
            'Last Modified': ['2024-01-15', '2024-01-10', '2024-01-05'],
            'Status': ['✅ Processed', '✅ Processed', '⏳ Processing']
        })
        
        st.dataframe(documents_df, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Search Stats")
        st.metric("Documents", "3")
        st.metric("Total Pages", "25")
        st.metric("Avg. Processing Time", "2.3 min")
    
    if search_query and st.button("🔍 Search"):
        with st.spinner("🤖 Searching across documents..."):
            time.sleep(1)
            
            st.markdown("### 🎯 Search Results")
            
            # Mock search results
            results = [
                {
                    'document': 'Employment Contract - John Doe',
                    'excerpt': '...Either party may terminate this agreement with 30 days notice...',
                    'relevance': 95,
                    'page': 3
                },
                {
                    'document': 'Software License Agreement',
                    'excerpt': '...License may be terminated immediately upon breach of terms...',
                    'relevance': 87,
                    'page': 7
                }
            ]
            
            for i, result in enumerate(results, 1):
                st.markdown(f"""
                <div class="analysis-box">
                    <h4>📄 {result['document']} (Page {result['page']})</h4>
                    <p><strong>Relevance:</strong> {result['relevance']}%</p>
                    <p><em>"{result['excerpt']}"</em></p>
                </div>
                """, unsafe_allow_html=True)

elif page == "📊 Analytics Dashboard":
    st.markdown("## 📊 Analytics Dashboard")
    
    # Mock analytics data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents Processed", "127", "+12")
    
    with col2:
        st.metric("Avg. Complexity Score", "64.2", "-5.3")
    
    with col3:
        st.metric("Terms Explained", "1,234", "+89")
    
    with col4:
        st.metric("User Satisfaction", "94%", "+2%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Document Types Processed")
        doc_types = pd.DataFrame({
            'Type': ['Employment', 'Lease', 'Terms of Service', 'License', 'Other'],
            'Count': [45, 32, 28, 15, 7]
        })
        
        fig_pie = px.pie(doc_types, values='Count', names='Type', title="Document Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Complexity Trends")
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        complexity_data = pd.DataFrame({
            'Date': dates,
            'Avg_Complexity': np.random.normal(60, 10, 30)
        })
        
        fig_line = px.line(complexity_data, x='Date', y='Avg_Complexity', 
                          title="Average Document Complexity Over Time")
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Recent activity
    st.markdown("### 🔄 Recent Activity")
    recent_activity = pd.DataFrame({
        'Time': ['2 mins ago', '15 mins ago', '1 hour ago', '3 hours ago'],
        'Action': ['Document analyzed', 'Terms explained', 'Risk assessment completed', 'New user registered'],
        'Document': ['Employment Contract', 'Lease Agreement', 'Terms of Service', 'N/A'],
        'Status': ['✅ Complete', '✅ Complete', '✅ Complete', '✅ Complete']
    })
    
    st.dataframe(recent_activity, use_container_width=True)

elif page == "❓ Legal Q&A":
    st.markdown("## ❓ Legal Q&A Chat Assistant")
    
    st.info("💬 Ask questions about legal concepts, your documents, or get general legal guidance!")
    
    # Chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Legal AI Assistant. I can help explain legal terms, analyze contracts, and answer questions about legal documents. What would you like to know?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your legal question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                time.sleep(1)  # Simulate processing time
                
                # Mock AI responses based on question type
                if any(word in prompt.lower() for word in ['contract', 'agreement']):
                    response = "A contract is a legally binding agreement between two or more parties. Key elements include offer, acceptance, consideration, and mutual intent. Would you like me to analyze a specific contract for you?"
                elif any(word in prompt.lower() for word in ['liability', 'responsible']):
                    response = "Liability refers to legal responsibility for one's actions or debts. It can be limited or unlimited depending on the context. In contracts, liability clauses often specify what each party is responsible for if something goes wrong."
                elif any(word in prompt.lower() for word in ['terminate', 'end', 'cancel']):
                    response = "Contract termination can happen in several ways: mutual agreement, completion of terms, breach by one party, or specific termination clauses. Always check your contract for notice periods and termination procedures."
                else:
                    response = f"That's a great question about '{prompt}'. Legal matters can be complex, and I'd recommend reviewing the specific terms in your documents or consulting with a qualified attorney for personalized advice. Is there a particular document you'd like me to analyze?"
                
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Suggested questions
    st.markdown("### 💡 Suggested Questions")
    suggestions = [
        "What is a force majeure clause?",
        "How do I know if a contract is legally binding?",
        "What are my rights if the other party breaches the contract?",
        "Can you explain what 'governing law' means?",
        "What should I look for in termination clauses?"
    ]
    
    for suggestion in suggestions:
        if st.button(f"💭 {suggestion}", key=suggestion):
            # Simulate clicking on suggestion
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>⚖️ <strong>LegalAI Demystifier</strong> | Empowering informed legal decisions through AI</p>
    <p><em>Disclaimer: This tool provides general information only and should not replace professional legal advice.</em></p>
</div>
""", unsafe_allow_html=True)
