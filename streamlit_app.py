import streamlit as st
import asyncio
import json
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
import arxiv
import pandas as pd
from typing import List, Dict

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🔬 Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'papers_data' not in st.session_state:
    st.session_state.papers_data = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'anthropic_client' not in st.session_state:
    st.session_state.anthropic_client = None

# Constants
PAPER_DIR = "papers"
os.makedirs(PAPER_DIR, exist_ok=True)

class StreamlitResearchAssistant:
    def __init__(self):
        self.anthropic = None
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.anthropic = Anthropic()
            except Exception as e:
                st.error(f"Failed to initialize Anthropic client: {e}")
    
    def search_papers(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Search for papers on arXiv and return structured data"""
        try:
            # Use arxiv to find papers
            client = arxiv.Client()
            search = arxiv.Search(
                query=topic,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = client.results(search)
            
            # Process papers
            papers_data = []
            for paper in papers:
                paper_info = {
                    'id': paper.get_short_id(),
                    'title': paper.title,
                    'authors': [author.name for author in paper.authors],
                    'authors_str': ', '.join([author.name for author in paper.authors]),
                    'summary': paper.summary,
                    'pdf_url': paper.pdf_url,
                    'published': str(paper.published.date()),
                    'categories': paper.categories,
                    'primary_category': paper.primary_category
                }
                papers_data.append(paper_info)
            
            # Save to local storage
            self.save_papers_to_file(topic, papers_data)
            
            return papers_data
            
        except Exception as e:
            st.error(f"Error searching papers: {str(e)}")
            return []
    
    def save_papers_to_file(self, topic: str, papers_data: List[Dict]):
        """Save papers data to local JSON file"""
        try:
            topic_dir = topic.lower().replace(" ", "_")
            path = os.path.join(PAPER_DIR, topic_dir)
            os.makedirs(path, exist_ok=True)
            
            file_path = os.path.join(path, "papers_info.json")
            
            # Convert to the format expected by the original code
            papers_info = {}
            for paper in papers_data:
                papers_info[paper['id']] = {
                    'title': paper['title'],
                    'authors': paper['authors'],
                    'summary': paper['summary'],
                    'pdf_url': paper['pdf_url'],
                    'published': paper['published']
                }
            
            with open(file_path, "w") as json_file:
                json.dump(papers_info, json_file, indent=2)
                
        except Exception as e:
            st.error(f"Error saving papers: {str(e)}")
    
    def get_paper_info(self, paper_id: str) -> Dict:
        """Extract paper information from local storage"""
        try:
            for item in os.listdir(PAPER_DIR):
                item_path = os.path.join(PAPER_DIR, item)
                if os.path.isdir(item_path):
                    file_path = os.path.join(item_path, "papers_info.json")
                    if os.path.isfile(file_path):
                        with open(file_path, "r") as json_file:
                            papers_info = json.load(json_file)
                            if paper_id in papers_info:
                                return papers_info[paper_id]
            return None
        except Exception as e:
            st.error(f"Error retrieving paper info: {str(e)}")
            return None
    
    def chat_with_claude(self, message: str, context: str = "") -> str:
        """Chat with Claude using the Anthropic API"""
        if not self.anthropic:
            return "❌ Anthropic API not configured. Please set ANTHROPIC_API_KEY in your .env file."
        
        try:
            full_message = f"{context}\n\n{message}" if context else message
            
            response = self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": full_message}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"❌ Error calling Claude: {str(e)}"

# Initialize the research assistant
@st.cache_resource
def get_research_assistant():
    return StreamlitResearchAssistant()

assistant = get_research_assistant()

# Main App UI
st.title("🔬 Research Assistant")
st.markdown("*Powered by arXiv API and Claude AI*")

# Sidebar
with st.sidebar:
    st.header("🛠️ Tools")
    
    # API Key Status
    if os.getenv("ANTHROPIC_API_KEY"):
        st.success("✅ Anthropic API Key loaded")
    else:
        st.error("❌ Anthropic API Key not found")
        st.info("Add ANTHROPIC_API_KEY to your .env file")
    
    st.divider()
    
    # Search Parameters
    st.subheader("🔍 Search Settings")
    max_results = st.slider("Max Results", 1, 20, 5)
    
    # Saved Topics
    st.subheader("📁 Saved Topics")
    if os.path.exists(PAPER_DIR):
        topics = [d for d in os.listdir(PAPER_DIR) if os.path.isdir(os.path.join(PAPER_DIR, d))]
        if topics:
            for topic in topics:
                if st.button(f"📚 {topic.replace('_', ' ').title()}", key=f"topic_{topic}"):
                    st.session_state.selected_topic = topic
        else:
            st.info("No saved topics yet")

# Main content area
tab1, tab2, tab3 = st.tabs(["🔍 Search Papers", "💬 Chat with Claude", "📊 Paper Analysis"])

with tab1:
    st.header("Search Academic Papers")
    
    # Search form
    with st.form("search_form"):
        search_topic = st.text_input("Enter research topic:", placeholder="e.g., machine learning, quantum computing, climate change")
        search_button = st.form_submit_button("🔍 Search Papers", use_container_width=True)
    
    if search_button and search_topic:
        with st.spinner(f"Searching for papers on '{search_topic}'..."):
            papers = assistant.search_papers(search_topic, max_results)
            
            if papers:
                st.session_state.papers_data = papers
                st.success(f"Found {len(papers)} papers!")
                
                # Display papers
                for i, paper in enumerate(papers):
                    with st.expander(f"📄 {paper['title']}", expanded=i < 3):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Authors:** {paper['authors_str']}")
                            st.write(f"**Published:** {paper['published']}")
                            st.write(f"**Categories:** {', '.join(paper['categories'])}")
                            st.write(f"**Paper ID:** {paper['id']}")
                            
                        with col2:
                            st.link_button("📄 View PDF", paper['pdf_url'])
                        
                        st.write("**Summary:**")
                        st.write(paper['summary'])
            else:
                st.warning("No papers found. Try a different search term.")

with tab2:
    st.header("Chat with Claude")
    
    # Chat interface
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about research papers or any topic..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Prepare context from current papers
        context = ""
        if st.session_state.papers_data:
            context = "Here are some recent papers I found:\n\n"
            for paper in st.session_state.papers_data[:3]:  # Use top 3 papers for context
                context += f"- {paper['title']} by {paper['authors_str']}\n"
                context += f"  Summary: {paper['summary'][:200]}...\n\n"
        
        # Get Claude's response
        with st.spinner("Claude is thinking..."):
            response = assistant.chat_with_claude(prompt, context)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Rerun to display new messages
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

with tab3:
    st.header("Paper Analysis")
    
    if st.session_state.papers_data:
        papers_df = pd.DataFrame(st.session_state.papers_data)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Papers", len(papers_df))
        with col2:
            avg_authors = papers_df['authors'].apply(len).mean()
            st.metric("Avg Authors", f"{avg_authors:.1f}")
        with col3:
            years = papers_df['published'].apply(lambda x: x.split('-')[0]).value_counts()
            st.metric("Most Common Year", years.index[0] if len(years) > 0 else "N/A")
        
        # Publication timeline
        st.subheader("📅 Publication Timeline")
        years_df = papers_df['published'].apply(lambda x: x.split('-')[0]).value_counts().sort_index()
        st.bar_chart(years_df)
        
        # Authors analysis
        st.subheader("👥 Top Authors")
        all_authors = []
        for authors_list in papers_df['authors']:
            all_authors.extend(authors_list)
        
        if all_authors:
            author_counts = pd.Series(all_authors).value_counts().head(10)
            st.bar_chart(author_counts)
        
        # Categories
        st.subheader("🏷️ Research Categories")
        all_categories = []
        for categories_list in papers_df['categories']:
            all_categories.extend(categories_list)
        
        if all_categories:
            category_counts = pd.Series(all_categories).value_counts().head(10)
            st.bar_chart(category_counts)
        
        # Download data
        st.subheader("💾 Download Data")
        csv = papers_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"research_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("Search for papers first to see analysis.")

# Footer
st.divider()
st.markdown("Made with ❤️ using Streamlit • arXiv API • Claude AI")
