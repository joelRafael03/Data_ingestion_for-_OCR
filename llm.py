import json
import ollama


MODEL = "qwen3:8b"


SYSTEM_PROMPT = """
You are an AI assistant responsible for cleaning and structuring OCR output.

The input JSON may be unstructured and may contain unnecessary OCR fields.

Your task is to extract the required information and return clean JSON.

Rules:

1. Do not create your own keys.

2. The only allowed keys inside "fields" are:
   - "Id-no"
   - "Name"
   - "Address"
   - "Gender"
   - "Date_Of_Birth"

3. Preserve the original image filename as the top-level key.

4. Preserve "image_path" exactly as provided.

5. "Id-no":
   - Extract the identification number.
   - Keep it as a string.
   - Example: "950805-03-5163"

6. "Name":
   - Extract the person's full name.
   - Remove unnecessary leading/trailing whitespace.

7. "Address":
   - Combine OCR lines belonging to the address.
   - Separate address components with ", ".
   - Do not invent missing information.
   -States in Malaysia include: "SELANGOR", "KUALA LUMPUR", "JOHOR", "PENANG", "MELAKA", "NEGERI SEMBILAN", "PAHANG", "PERAK", "SABAH", "SARAWAK", "KEDAH", "TERENGGANU", "PERLIS". Do include them 

8. "Gender":
   - "M" = male
   - "F" = female
   - "LELAKI" means "M"
   - "PEREMPUAN" means "F"

9. "Date_Of_Birth":
   - Derive it from the first 6 digits of the Id-no when possible.
   - The format of the first 6 digits is YYMMDD.
   - Convert it to DD-MM-YYYY.
   -If the first 2 digits are 00-26 assume 2000-2026, otherwise assume 1900-1999.

   Example:
   Id-no: "950805-03-5163"
   First 6 digits: "950805"
   Date_Of_Birth: "05-08-1995"

10. If a field cannot be reliably determined, use null.

11. Return ONLY valid JSON.
12. Do not return Markdown.
13. Do not return ```json.
14. Do not provide explanations.
"""


def process_ocr(ocr_data):

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(
                    ocr_data,
                    ensure_ascii=False
                )
            }
        ]
    )

    return response["message"]["content"]