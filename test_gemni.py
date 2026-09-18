from app.ai.gemini import ask_gemini


prompt = "Explain what a resume is in one simple sentence."

response = ask_gemini(prompt)

print("\nGemini Response:")
print(response)