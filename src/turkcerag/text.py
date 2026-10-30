def tr_lower(s:str)->str:
  translation_table = str.maketrans({
      "I": "ı", 
      "İ": "i"
  })
  clean_text = s.translate(translation_table)
  return clean_text.lower()

assert tr_lower("İSTANBUL") == "istanbul"
assert tr_lower("ISPARTA") == "ısparta"