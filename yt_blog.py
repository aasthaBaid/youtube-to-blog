# YouTube to Blog Post Generator using LangChain and LangGraph

import os
from typing import TypedDict, List
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        youtube_url: The URL of the YouTube video to process.
        transcript: The fetched transcript of the video.
        title: The generated blog post title.
        blog_post: The final generated blog content.
        error: A field to store any error messages that occur.
    """
    youtube_url: str
    transcript: str
    title: str
    blog_post: str
    error: str

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)


def get_transcript(state: GraphState) -> GraphState:
    """
    Fetches the transcript for a given YouTube URL.

    Args:
        state: The current state of the graph.

    Returns:
        An updated state with the transcript or an error message.
    """
    print("--- 1. FETCHING TRANSCRIPT ---")
    try:
        url = state.get("youtube_url", "").strip()
        if not url:
            raise ValueError("YouTube URL is missing.")
            
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
        documents = loader.load()
        
        if not documents:
            return {"error": "Could not retrieve transcript. The video may not have one available."}

        transcript_text = " ".join([doc.page_content for doc in documents]).strip()
        
        print(f"Transcript fetched successfully. Length: {len(transcript_text)} characters.")
        return {"transcript": transcript_text, "error": None}

    except Exception as e:
        print(f"ERROR fetching transcript: {e}")
        return {"error": f"Failed to fetch transcript: {e}"}


def generate_title(state: GraphState) -> GraphState:
    """
    Generates a catchy, SEO-friendly title based on the transcript.

    Args:
        state: The current state of the graph.

    Returns:
        An updated state with the generated title or an error.
    """
    print("--- 2. GENERATING BLOG TITLE ---")
    if state.get("error"): 
        return {}
        
    transcript = state.get("transcript", "")
    
   
    prompt = ChatPromptTemplate.from_template(
        """Based on the following video transcript, please generate a concise, engaging, and SEO-friendly title for a blog post.

        Transcript:
        "{transcript}"

        Title:"""
    )
    
    title_chain = prompt | llm | StrOutputParser()
    
    try:
        title = title_chain.invoke({"transcript": transcript})
        print(f"Generated Title: {title}")
        return {"title": title, "error": None}
    except Exception as e:
        print(f"ERROR generating title: {e}")
        return {"error": f"Failed to generate title: {e}"}


def generate_blog_post(state: GraphState) -> GraphState:
    """
    Generates the full blog post content using the title and transcript.

    Args:
        state: The current state of the graph.

    Returns:
        An updated state with the final blog post or an error.
    """
    print("--- 3. GENERATING BLOG POST ---")
    if state.get("error"):
        return {}
        
    title = state.get("title", "")
    transcript = state.get("transcript", "")
    
    # Prompt template for the final blog post
    prompt = ChatPromptTemplate.from_template(
        """You are an expert blog post writer. Your task is to write a comprehensive, well-structured blog post using the provided title and video transcript.

        **Blog Post Title:** {title}

        **Video Transcript:**
        {transcript}

        ---
        Instructions:
        - Start with an engaging introduction that hooks the reader.
        - Structure the content logically with clear headings and subheadings (using Markdown for formatting).
        - Convert the key points from the transcript into well-written paragraphs.
        - Maintain a consistent and informative tone.
        - Conclude with a summary and a call to action if appropriate.
        - Ensure the final output is only the blog post content itself.

        **Final Blog Post:**
        """
    )
    
    # Create the generation chain
    blog_post_chain = prompt | llm | StrOutputParser()
    
    try:
        blog_post = blog_post_chain.invoke({"title": title, "transcript": transcript})
        print("--- BLOG POST GENERATED ---")
        return {"blog_post": blog_post, "error": None}
    except Exception as e:
        print(f"ERROR generating blog post: {e}")
        return {"error": f"Failed to generate blog post: {e}"}

def handle_error(state: GraphState) -> str:
    """
    A conditional edge function. It decides the next step based on
    whether an error has occurred in the graph's state.
    """
    if state.get("error"):
        print("--- An error occurred. Ending execution. ---")
        return "end" 
    return "continue" 


workflow = StateGraph(GraphState)

# Add nodes to the graph
workflow.add_node("get_transcript", get_transcript)
workflow.add_node("generate_title", generate_title)
workflow.add_node("generate_blog_post", generate_blog_post)

# Define the edges and control flow
workflow.set_entry_point("get_transcript")

# Conditional edge from get_transcript
workflow.add_conditional_edges(
    "get_transcript",
    handle_error,
    {
        "continue": "generate_title",
        "end": END,
    },
)

# Conditional edge from generate_title
workflow.add_conditional_edges(
    "generate_title",
    handle_error,
    {
        "continue": "generate_blog_post",
        "end": END,
    },
)

# The final step before ending the graph
workflow.add_edge("generate_blog_post", END)

# Compile the graph into a runnable application
app = workflow.compile()



if __name__ == "__main__":
    print("--- YouTube to Blog Post Generator ---")
    
    # Example URL. Replace this with any YouTube video URL that has transcripts.
    # url = "https://www.youtube.com/watch?v=k_B7e5b_4wA" # Example: A video about LangGraph
    url = input("Please enter the YouTube video URL: ").strip()

    if not url:
        print("No URL provided. Exiting.")
    else:
        # The initial state to kick off the graph
        initial_state = {"youtube_url": url}
        
        # Invoke the graph with the initial state
        final_state = app.invoke(initial_state)
        
        # Print the final output
        print("\n" + "="*50)
        if final_state.get("error"):
            print("Process finished with an error:")
            print(final_state["error"])
        else:
            print("Final Blog Post:")
            print("-" * 50)
            print("# " + final_state.get("title", "No Title Generated"))
            print(final_state.get("blog_post", "No content generated."))
        print("="*50)
