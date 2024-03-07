from summarizer import summarize_from_pdf, ollama_summarize

if __name__=="__main__":
    summary = summarize_from_pdf("./tmp/sample.pdf")
    summary = ollama_summarize("""
        Hello,
        We received your request to have your account reinstated. 
        Please respond to this email with the reason you believe your account suspension was in error and/or the reason you are requesting an appeal.
        Once we receive your response, we will review and provide a follow up response with the outcome of our review. If this request is for an account reinstatement under our new criteria, please allow 3-5 days for us to review and respond. In some instances, it may take us longer to get back to you. 
        Thanks,
        X  
    """)

    print(summary.response)
