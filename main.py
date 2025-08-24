import streamlit as st
import time
import random
import json
from utils.llm_helpers import summarize, analyze_sentiment, analyze_style, estimate_tokens, calculate_cost

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Settings")

provider = st.sidebar.radio(
    "Select Provider",
    ["Groq", "Gemini", "Mistral"],
    index=0
)

model_options = {
    "Groq": ["llama3-8b-8192 (Groq)"],
    "Gemini": ["gemini-2.0-flash"],
    "Mistral": ["devstral-medium-2507"]
}

model = st.sidebar.selectbox(
    "Choose Model",
    model_options[provider]
)

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.number_input("Max Tokens", 50, 2000, 500)
safe_mode = st.sidebar.toggle("Safe Mode (disable expensive models)", value=False)


# --- Main Input ---
st.title("📝 LLM Text Tool")
text_input = st.text_area("Enter text to analyze", height=150)
analyze = st.button("🔍 Analyze")

# Check environment variables and show status
try:
    from utils.llm_helpers import validate_environment_variables
    validate_environment_variables()
    env_status = "✅ API Keys Configured"
except EnvironmentError as e:
    env_status = f"⚠️ {str(e)}"
except:
    env_status = "❓ Environment check failed"

# Session info meter with real-time updates
session_tokens = st.session_state.get('total_tokens', 0)
session_cost = st.session_state.get('total_cost', 0.0)

st.caption(
    f"{env_status} | "
    f"🔑 Session Tokens: {session_tokens} | "
    f"Est. Cost: ${round(session_cost, 6)}"
)


# --- Results Section ---
if analyze and text_input.strip():
    st.subheader("📊 Results")

    # --- Summarization First ---
    st.markdown("## ✨ Summarization Tool")
    
    total_tokens_used = 0
    total_cost = 0.0
    
    st.markdown(f"**{provider} ({model})**")
    
    # Get actual model name without display text
    actual_model = model.split(" (")[0] if " (" in model else model
    
    # Call actual summarization API
    with st.spinner(f"Generating summary with {provider}..."):
        summary_text, prompt_tokens, completion_tokens, latency, error = summarize(
            text_input, 
            provider.lower(), 
            model=actual_model,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    if error:
        st.error(f"Error with {provider}: {error}")
    else:
        try:
            # Parse JSON response if available
            if summary_text.strip().startswith('{'):
                summary_data = json.loads(summary_text)
                summary_content = summary_data.get("summary", summary_text)
            else:
                summary_content = summary_text
            
            # Calculate actual cost
            actual_cost = calculate_cost(provider.lower(), prompt_tokens, completion_tokens)
            total_tokens_used += (prompt_tokens + completion_tokens)
            total_cost += actual_cost
            
            st.write(f"**Summary:** {summary_content}")
            st.write(f"- **Latency:** {round(latency, 2)}s")
            st.write(f"- **Tokens:** {prompt_tokens} (prompt) + {completion_tokens} (completion)")
            st.write(f"- **Est. Cost:** ${round(actual_cost, 6)}")
            
        except json.JSONDecodeError:
            st.write(f"**Raw Response:** {summary_text}")
            st.write(f"- **Latency:** {round(latency, 2)}s")
            st.write(f"- **Tokens:** {prompt_tokens} (prompt) + {completion_tokens} (completion)")
    
    st.divider()

    # Update session state with total usage
    st.session_state.total_tokens = st.session_state.get('total_tokens', 0) + total_tokens_used
    st.session_state.total_cost = st.session_state.get('total_cost', 0.0) + total_cost

    # --- Other Analysis ---
    st.markdown("## 🔍 Detailed Analysis")

    with st.expander("Tokenizer Breakdown"):
        actual_tokens = estimate_tokens(text_input)
        st.write({
            "tokens": actual_tokens,
            "words": len(text_input.split()),
            "preview": text_input.split()[:10] if len(text_input.split()) > 10 else text_input.split()
        })

    with st.expander("Top Words"):
        # Simple word frequency analysis (could be enhanced)
        words = [word.lower().strip('.,!?;:"') for word in text_input.split() if len(word) > 3]
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        st.write([word for word, freq in top_words])

    with st.expander("Readability Scores"):
        # Placeholder for readability analysis - could integrate actual library
        st.write({
            "Flesch": round(random.uniform(50, 90), 1),
            "Grade Level": round(random.uniform(5, 15), 1),
            "Note": "Using placeholder values - integrate readability library for real analysis"
        })

    with st.expander("Sentiment & Style Analysis"):
        # Use actual sentiment analysis from LLM
        with st.spinner("Analyzing sentiment and style..."):
            sentiment_result, s_prompt_tokens, s_completion_tokens, s_latency, s_error = analyze_sentiment(
                text_input, provider.lower()
            )
            style_result, st_prompt_tokens, st_completion_tokens, st_latency, st_error = analyze_style(
                text_input, provider.lower()
            )
        
        if s_error:
            st.error(f"Sentiment analysis error: {s_error}")
        else:
            try:
                sentiment_data = json.loads(sentiment_result) if sentiment_result.strip().startswith('{') else {"label": "Unknown", "reason": sentiment_result}
                st.write(f"**Sentiment:** {sentiment_data.get('label', 'Unknown')}")
                st.write(f"**Reason:** {sentiment_data.get('reason', 'No reason provided')}")
            except:
                st.write(f"**Sentiment Raw:** {sentiment_result}")
        
        if st_error:
            st.error(f"Style analysis error: {st_error}")
        else:
            try:
                style_data = json.loads(style_result) if style_result.strip().startswith('{') else {"style": "Unknown", "complexity": "Unknown", "examples": []}
                st.write(f"**Style:** {style_data.get('style', 'Unknown')}")
                st.write(f"**Complexity:** {style_data.get('complexity', 'Unknown')}")
                st.write("**Examples:**")
                for example in style_data.get('examples', [])[:2]:
                    st.write(f"- {example}")
            except:
                st.write(f"**Style Raw:** {style_result}")

    # --- Bottom: Export Section ---
    st.markdown("## 📂 Export & Saved Files")
    
    # Prepare data for export
    analysis_data = {
        "input_text": text_input,
        "provider": provider,
        "model": model,
        "summary": summary_content if 'summary_content' in locals() else "",
        "sentiment": sentiment_data if 'sentiment_data' in locals() else {},
        "style": style_data if 'style_data' in locals() else {},
        "token_count": actual_tokens,
        "word_count": len(text_input.split()),
        "cost": total_cost,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Export as CSV"):
            # Create CSV content
            import csv
            import io
            
            # Create a CSV string
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(["Field", "Value"])
            
            # Write data
            for key, value in analysis_data.items():
                if isinstance(value, (dict, list)):
                    writer.writerow([key, json.dumps(value)])
                else:
                    writer.writerow([key, str(value)])
            
            # Create download button
            st.download_button(
                label="Download CSV",
                data=output.getvalue(),
                file_name="analysis_export.csv",
                mime="text/csv"
            )
        
        if st.button("📑 Export as JSON"):
            # Create JSON download button
            st.download_button(
                label="Download JSON",
                data=json.dumps(analysis_data, indent=2),
                file_name="analysis_export.json",
                mime="application/json"
            )
