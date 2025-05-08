"""This module handles the translation pipeline, including preprocessing, translation, and postprocessing."""
import re
import logging
from translation.translator import TranslatorModel
from translation.file_ops import save_to_csv, check_existing_translation, save_debug_json


logger = logging.getLogger(__name__)
model = TranslatorModel()


def _preprocess_text(text: str) -> dict:
    """Preprocess the input text: replace URLs, split lines, and strip symbols."""
    # this will replace urls
    sentence_with_placeholders, placeholder_map = model.mask_urls_with_placeholders(text)
    split_newlines = model.split_preserving_newlines(sentence_with_placeholders)
    logger.info("This is split new lines: %s", split_newlines)
    split_with_symbols = model.split_on_punctuation(split_newlines)
    logger.info("This is split with symbols: %s", split_with_symbols)
    # this will remove symbols
    text_only = model.remove_punctuation_tokens(split_with_symbols)
    logger.info("This is text only before translation: %s", text_only)

    return {
        "sentence_with_placeholders": sentence_with_placeholders,
        "placeholder_map": placeholder_map,
        "split_newlines": split_newlines,
        "split_with_symbols": split_with_symbols,
        "text_only": text_only
    }



def _translate_sentences(sentences: list[str], src_lang: str, tgt_lang: str) -> list[str]:
    """Translate a list of cleaned text parts."""
    return [
        model.translate_single_sentence(sentence, src_lang, tgt_lang)
        for sentence in sentences
    ]


def _postprocess_text(processed: dict, translated: list[str], tgt_lang: str) -> str:
    """Reassemble the translated output with symbols and formatting."""
    translated_with_symbols = model.reinsert_punctuation_tokens(processed["split_with_symbols"], translated)
    logger.info("This is translated with symbols: %s", translated_with_symbols)
    # Convert \n to \\n
    translated_with_symbols = [
        item.replace('\n', '\\n') if isinstance(item, str) else item
        for item in translated_with_symbols
    ]
    final_text = model.assemble_final_text(translated_with_symbols)
    translated_text = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'**\1**', final_text)

    if tgt_lang == 'npi_Deva':
        translated_text = model.replace_dot(translated_text)

    return model.unmask_urls_from_placeholders(translated_text, processed["placeholder_map"])


def run_translation_pipeline(text: str, src_lang: str, tgt_lang: str) -> str:
    """
    Executes the full translation pipeline:
    1. Checks if result exists
    2. Preprocesses text
    3. Translates
    4. Postprocesses
    5. Saves to CSV + JSON
    """
    try:
        logger.info("Starting translation for: %s", text)
        cached = check_existing_translation(tgt_lang, text)
        if cached:
            logger.info("Using cached result.")
            return cached

        processed = _preprocess_text(text)
        translated = _translate_sentences(processed["text_only"], src_lang, tgt_lang)
        final_response = _postprocess_text(processed, translated, tgt_lang)

        # Save output
        save_to_csv(tgt_lang, text, final_response)
        save_debug_json({
            "original_sentence": text,
            **processed,
            "translated_sentence": translated,
            "final_text_with_urls": final_response,
        })

        logger.info("Translation completed.")
        return final_response

    except Exception as e:
        logger.error("Translation pipeline failed: %s", str(e))
        raise RuntimeError("Translation pipeline failed.") from e



