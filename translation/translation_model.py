import torch
import warnings
import re
from translation.mapping_dictionary import nepali_to_english_dict, english_to_nepali_dict
import ctranslate2
import transformers
import os
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore")
translation_model_path = os.getenv("translation_model_path")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


translation_tokenizer = transformers.AutoTokenizer.from_pretrained(translation_model_path)
translation_model = ctranslate2.Translator(translation_model_path)


# Function to handle quoted text
def handle_quoted_text(text, src_lang, tgt_lang):
    quoted_pattern = r'\"(.*?)\"'
    quoted_texts = re.findall(quoted_pattern, text)
    translated_quotes = {}

    for quoted_text in quoted_texts:
        translated = translation(quoted_text, src_lang=src_lang, tgt_lang=tgt_lang)
        translated_quotes[quoted_text] = translated

    for original, translated in translated_quotes.items():
        text = text.replace(f"\"{original}\"", f"\"{translated}\"")
    return text


# Function to split large text into manageable chunks
def split_text(text, max_length=1024):
    sentences = re.split(r'(\n+|[.?!])', text.strip())
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Function to replace dictionary mappings with placeholders
def dictionary_replace_and_translate(text, src_lang, tgt_lang):
    preprocessed_text = text.lower()
    print("Preprocessing: Original text:", preprocessed_text)
    entity_mapping = {}
    placeholder_counter = 1

    # Determine which dictionary to use
    translation_dict = nepali_to_english_dict if src_lang == "npi_Deva" else english_to_nepali_dict

    # Regex to ignore website and email address
    url_pattern = r'(www\.[^\s]+|http[^\s]+)'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    excluded_matches = {}
    for match in re.finditer(f'{url_pattern}|{email_pattern}', preprocessed_text):
        placeholder = f"EXCLUDE{placeholder_counter}"
        excluded_matches[placeholder] = match.group(0)
        preprocessed_text = preprocessed_text.replace(match.group(0), placeholder, 1)
        placeholder_counter += 1

    # Sort dictionary keys by length (multi-word phrases first)
    sorted_dict_keys = sorted(translation_dict.keys(), key=lambda x: len(x), reverse=True)

    for key in sorted_dict_keys:
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, preprocessed_text):
            placeholder = f"x{placeholder_counter}"
            entity_mapping[placeholder] = translation_dict[key]
            preprocessed_text = re.sub(pattern, placeholder, preprocessed_text, count=1)
            placeholder_counter += 1

    for placeholder, original_value in excluded_matches.items():
        preprocessed_text = preprocessed_text.replace(placeholder, original_value)

    print("Entity Mapping:", entity_mapping)
    print("Text after replacing dictionary words with placeholders:", preprocessed_text)
    return preprocessed_text, entity_mapping


# Function to translate text using the translation model
def translation(text, src_lang='npi_Deva', tgt_lang='eng_Latn', max_input_length=1024, num_beams=4, **kwargs):
    translation_tokenizer.src_lang = src_lang
    translation_tokenizer.tgt_lang = tgt_lang

    print(f"Text before translation: {text}")
    inputs = translation_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_input_length).to(device)
    
    source_tokens = translation_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    target_prefix = [tgt_lang]
    results = translation_model.translate_batch([source_tokens], target_prefix=[target_prefix], beam_size=num_beams, **kwargs)
    translated_tokens = results[0].hypotheses[0][1:]
    translated_text = translation_tokenizer.decode(translation_tokenizer.convert_tokens_to_ids(translated_tokens), skip_special_tokens=True)
    print(f"Translation of the text: {translated_text}")
    return translated_text


def translate_by_sentence(text, src_lang, tgt_lang):
    text = text.replace("\\n", "\n")  
    chunks = split_text(text)
    translated_chunks = []

    for chunk in chunks:
        print(f"Processing chunk: {chunk}")
        chunk_with_quotes = handle_quoted_text(chunk, src_lang, tgt_lang)
        text_with_placeholders, entity_mapping = dictionary_replace_and_translate(chunk_with_quotes, src_lang, tgt_lang)
        translated_text = translation(text_with_placeholders, src_lang, tgt_lang)

        for placeholder, mapped_word in entity_mapping.items():
            translated_text = re.sub(rf'\b{placeholder}\b', mapped_word, translated_text)

        translated_text = translated_text.replace("\n", "\\n").replace("\n", "\\n")
        translated_chunks.append(translated_text)

    print("All translated chunks:", translated_chunks)  
    return '\n\n'.join(translated_chunks)



# Input text
input_text = ("\"To apply for a home loan with Global IME Bank, you can follow these steps:\\n\\n1. **Determine Your Requirement**\\n - Figure out why you need a home loan and how much you need. For example, you may need a loan to purchase a new home or to renovate your existing one.\\n\\n2. **Check Loan Eligibility**\\n - Once you know how much you need, you should check whether you are eligible. You can visit the Global IME Bank Eligibility Calculator online to find out how much you can borrow and calculate your monthly installments.\\n\\n3. **Approach the Bank**\\n - You can apply for a home loan with Global IME Bank in a variety of ways: Via online application or by visiting the nearest branch.\\n\\n4. **Submit Documents**\\n - Next, find out what documents are required for a home loan. Usually, you will need income proof, address proof, ID proof, and collateral documents. Hand over copies of your home loan documents at the bank. Once your application and documents are approved, the loan amount will be disbursed to your account.\\n\\nWould you like more detailed information on any of these steps?\"")
src_lang = "eng_Latn"
tgt_lang = "npi_Deva"
translated_text = translate_by_sentence(input_text, src_lang, tgt_lang)

output = {
    "output_text": input_text,
    "translated_text": translated_text
}

print(output)