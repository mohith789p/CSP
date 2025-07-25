import streamlit as st

def create_advanced_legal_prompt(query, category="General"):
    return f"""You are an expert Indian legal consultant specializing in {category} with comprehensive knowledge of:

LEGAL FRAMEWORK:
- Indian Constitution (Articles, Fundamental Rights & Duties)
- Indian Penal Code (IPC) & Bharatiya Nyaya Sanhita (BNS) 2023
- Criminal Procedure Code (CrPC) & Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023
- Civil Procedure Code (CPC) & Evidence Act
- Family laws: Hindu Marriage Act, Special Marriage Act, Muslim Personal Law
- Property laws: Transfer of Property Act, Registration Act
- Consumer Protection Act 2019 & Labor Laws
- Recent Supreme Court & High Court judgments

RESPONSE REQUIREMENTS:
1. ✅ Provide accurate, practical legal guidance
2. 📋 Include relevant legal sections/acts when applicable
3. 🔄 Give step-by-step procedural guidance
4. ⏰ Mention approximate timelines and costs
5. 📄 List required documents and forms
6. ⚖️ Reference landmark judgments if relevant
7. 🏛️ Suggest appropriate courts/forums
8. ⚠️ Always recommend consulting qualified lawyers for specific cases

CATEGORY: {category}
QUERY: {query}

Provide comprehensive legal guidance in clear, professional English:"""


def generate_legal_response(model_pipeline, query, model_type, category="General"):
    try:
        legal_prompt = create_advanced_legal_prompt(query, category)

        generation_params = {
            "temperature": 0.7,
            "do_sample": True,
            "repetition_penalty": 1.2,
            "length_penalty": 1.0,
            "no_repeat_ngram_size": 3
        }

        if "flan-t5" in model_type.lower():
            response = model_pipeline(
                legal_prompt,
                max_length=600,
                min_length=100,
                **generation_params
            )
            generated_text = response[0]['generated_text']
        else:
            response = model_pipeline(
                legal_prompt,
                max_new_tokens=500,
                min_length=len(legal_prompt) + 50,
                pad_token_id=model_pipeline.tokenizer.eos_token_id,
                eos_token_id=model_pipeline.tokenizer.eos_token_id,
                return_full_text=False,
                **generation_params
            )
            generated_text = response[0]['generated_text']

        generated_text = generated_text.strip()

        if "consult" not in generated_text.lower() and "lawyer" not in generated_text.lower():
            generated_text += "\n\n⚠️ IMPORTANT: This is general information only. Please consult a qualified lawyer for advice specific to your situation."

        return generated_text

    except Exception as e:
        error_msg = f"Response generation error: {str(e)}. Please try again or rephrase your question."
        st.error(error_msg)
        return error_msg
