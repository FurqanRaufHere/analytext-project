# LLM Text Analysis Tool

A **Text Analysis Tool** built for the Buildables AI Fellowship Week 1 assignment.  
This project demonstrates understanding of **LLM basics, tokenization, multi-model comparison, and text analysis** using free tokenizers and APIs.

---

## Features

**Core Features**
- Text Summarization using **GROQ**, **Mistral**, and **Gemini**.
- Tokenization analysis using Hugging Face tokenizers (GPT-2, BERT, RoBERTa).
- Multi-model comparison for summarization outputs.
- Token usage tracking and cost estimation.

**Advanced Features**
- Sentiment Analysis using LLM.
- Writing Style Analysis (formal/informal, complexity).
- Text Statistics (readability scores, word frequency).
- Export results in JSON or CSV format.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/llm-text-analysis.git
   cd llm-text-analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file and add your API keys:
     ```bash
     # Get your API keys from:
     # Groq: https://console.groq.com/
     # Gemini: https://aistudio.google.com/
     # Mistral: https://console.mistral.ai/
     
     GROQ_API_KEY=your_actual_groq_api_key_here
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     MISTRAL_API_KEY=your_actual_mistral_api_key_here
     ```

4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

---

## Usage

1. **Select LLM Providers**: Choose which providers to use from the sidebar (Groq, Gemini, Mistral).
2. **Enter Text**: Paste your text in the input area or upload files for batch processing.
3. **Configure Settings**: Adjust temperature and enable/disable features as needed.
4. **Analyze**: Click "Analyze Single Text" or "Analyze Batch" to process your text.
5. **Review Results**: View multi-model comparisons, tokenization details, and text statistics.
6. **Export**: Download results in JSON or CSV format if enabled.

---

## Environment Variables

The application requires the following environment variables to be set in your `.env` file:

- `GROQ_API_KEY`: Your Groq API key
- `GEMINI_API_KEY`: Your Google Gemini API key  
- `MISTRAL_API_KEY`: Your Mistral AI API key

If any API keys are missing, the application will display a clear error message with instructions.

---

## Troubleshooting

**Common Issues:**
- **Missing API Keys**: Ensure all required API keys are set in your `.env` file
- **Invalid API Keys**: Verify your API keys are correct and have sufficient credits
- **Network Issues**: Check your internet connection if API calls fail

**Error Messages:**
- "Configuration Error: Missing environment variables: GROQ_API_KEY, GEMINI_API_KEY" - This means your `.env` file is missing required API keys
- "401 Unauthorized" - Your API key may be invalid or expired
- "429 Too Many Requests" - You've exceeded your API rate limits

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
