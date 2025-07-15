import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

def analyze_keywords_with_gemini(keywords):
    if not keywords:
        return {}

    prompt = f"""
    Analyze these keywords for SEO strength, competitiveness, and grouping:
    {', '.join(keywords)}.
    Provide suggestions to improve keyword targeting.
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return {"insights": response.text}
