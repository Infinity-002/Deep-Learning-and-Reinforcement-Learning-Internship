import streamlit as st
from transformers import MBartForConditionalGeneration, MBart50Tokenizer

st.set_page_config(page_title="Translation App", page_icon=":globe_with_meridians:", layout="wide")

@st.cache_resource
def load_model():
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    tokenizer = MBart50Tokenizer.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

lang_map = {
    "English": "en_XX",
    "Hindi": "hi_IN",
    "Telugu": "te_IN",
    "Tamil": "ta_IN",
    "Marathi": "mr_IN",
    "Bengali": "bn_IN",
    "Gujarati": "gu_IN",
    "Punjabi": "pa_IN",
    "German": "de_DE",
    "Spanish": "es_XX",
    "Chinese": "zh_CN",
    "Japanese": "ja_XX",
    "Korean": "ko_KR"
}

st.title("Multilingual Translation App")
st.markdown("Translate text")

src_lang = st.selectbox("Select source language", list(lang_map), index =  0)
tgt_lang = st.selectbox("Select target language", list(lang_map), index =  1)

text = st.text_area("Enter text to translate")


if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter text to translate")

    else:
        tokenizer.src_lang = lang_map[src_lang]
        encoded = tokenizer(text, return_tensors = "pt")
        generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id[lang_map[tgt_lang]]
    )
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens = True)[0]
        st.markdown(f"**Translated Text:**\n{translated_text}")