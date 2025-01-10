#this is the mapping for nepali-english dict 
import json

nepali_to_english_dict = {   
    "" : "treaty",
    "" : "king mahendra bir bikram shah dev",
    "" : "mahendra bir bikram shah dev",
    "" : "nepal",
    "" : "raja",
    "" : ""
    
}

english_to_nepali_dict = {v.lower(): k for k, v in nepali_to_english_dict.items()}
