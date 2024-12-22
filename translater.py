# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
device


tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M").to(device)

# Now you can use the model for translation or inference
def translate(
    text, src_lang='eng_Latn', tgt_lang='npi_Deva',
    a=32, b=3, max_input_length=1024, num_beams=4, **kwargs
):
    """Turn a text or a list of texts into a list of translations"""
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = tgt_lang
    inputs = tokenizer(
        text, return_tensors='pt', padding=True, truncation=True,
        max_length=max_input_length
    )
    model.eval()
    # Generate translated text
    result = model.generate(
        **inputs.to(model.device),
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_new_tokens=int(a + b * inputs.input_ids.shape[1]),
        num_beams=num_beams, **kwargs
    )
    # Decode the result and return the translated text
    return tokenizer.batch_decode(result, skip_special_tokens=True)

# Test translation
t = "The quick brown fox jumps over the lazy dog."
translated_text = translate(t, src_lang='eng_Latn', tgt_lang='npi_Deva')
print(translated_text)