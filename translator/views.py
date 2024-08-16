from django.http import FileResponse, JsonResponse, HttpResponse
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
import io

# Morse code dictionaries
ENGLISH_TO_MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '~': '.-.-..', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '(': '-.--.',
    '/': '-..-.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', '#': '.--.--...', ' ': ' ',
    '%': '.----.-'
}

MORSE_TO_ENGLISH = {v: k for k, v in ENGLISH_TO_MORSE.items()}

ENGLISH_TO_BRAILLE = {
    "A": "⠁", "B": "⠃", "C": "⠉", "D": "⠙", "E": "⠑", "F": "⠋", "G": "⠛", "H": "⠓", "I": "⠊", "J": "⠚",
    "K": "⠅", "L": "⠇", "M": "⠍", "N": "⠝", "O": "⠕", "P": "⠏", "Q": "⠟", "R": "⠗", "S": "⠎", "T": "⠞",
    "U": "⠥", "V": "⠧", "W": "⠺", "X": "⠭", "Y": "⠽", "Z": "⠵", "1": "⠼⠁", "2": "⠼⠃", "3": "⠼⠉", 
    "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋", "7": "⠼⠛", "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚",
    ".": "⠲", ",": "⠂", ";": "⠆", ":": "⠒", "!": "⠖", "?": "⠦", "”": "⠶", "(": "⠐⠣", ")": "⠐⠜", 
    "-": "⠤", "/": "⠌", "+": "⠖", "=": "⠶", "*": "⠔", "&": "⠯", "Capital": "⠠", "Number": "⠼"
}

braille_mapping = {
    # Letters
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100', 'f': '111000',
    'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100', 'k': '100010', 'l': '101010',
    'm': '110010', 'n': '110110', 'o': '100110', 'p': '111010', 'q': '111110', 'r': '101110',
    's': '011010', 't': '011110', 'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011',
    'y': '110111', 'z': '100111',
    
    # Numbers (Note: In actual Braille, numbers require a number sign prefix)
    '0': '011100', '1': '100000', '2': '101000', '3': '110000', '4': '110100', '5': '100100',
    '6': '111000', '7': '111100', '8': '101100', '9': '011000',
    
    # Special Characters (for completeness, you might include these as well)
    '.': '010011', ',': '010000', '?': '011001', '!': '011010', '-': '001001', ':': '010010',
    ';': '011000', '(': '011011', ')': '011011', "'": '001000', '"': '001011', '#': '010111',
    '*': '001010', '@': '000001', '&': '001010', '%': '000011', '+': '011010', '=': '011110',
    '/': '001100', '\\': '100001',
}

def index(request):
    return render(request, 'translator/index.html')

def translate(request):
    user_input = request.POST.get('userInput', '').strip()
    translation_type = request.POST.get('translationType', '')

    morse_output = ''
    english_output = ''
    braille_output = ''
    
    if translation_type == 'toMorse':
        morse_output = ' '.join(ENGLISH_TO_MORSE.get(char.upper(), '') for char in user_input)
    elif translation_type == 'toEnglish':
        morse_words = user_input.strip().split('   ')  
        english_output = ' '.join(''.join(MORSE_TO_ENGLISH.get(letter, '') for letter in word.split(' ')) for word in morse_words)
    elif translation_type == 'toBraille':
        braille_output = ''.join(ENGLISH_TO_BRAILLE.get(char.upper(), '') for char in user_input)
        
        # Handle PNG download (if requested)
        if 'download' in request.POST:
            try:
                image = Image.new('RGB', (500, 100), color=(255, 255, 255))
                draw = ImageDraw.Draw(image)
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust path as needed
                try:
                    font = ImageFont.truetype(font_path, 15)
                except IOError:
                    font = ImageFont.load_default()
                draw.text((10, 10), braille_output, fill=(0, 0, 0), font=font)
                image_io = io.BytesIO()
                image.save(image_io, format='PNG')
                image_io.seek(0)
                return FileResponse(image_io, as_attachment=True, filename='braille_image.png')
            except Exception as e:
                print(f"Error generating image: {e}")
                return JsonResponse({'error': 'An error occurred while generating the image.'}, status=500)

    return JsonResponse({'morseOutput': morse_output, 'englishOutput': english_output, 'brailleOutput': braille_output})

def generate_mirror_braille(input_text):
    def flip_braille(braille_pattern):
        return braille_pattern[3] + braille_pattern[0] + braille_pattern[4] + braille_pattern[1] + braille_pattern[5] + braille_pattern[2]

    mirrored_braille = ''
    for char in input_text.lower():
        if char in braille_mapping:
            original_braille = braille_mapping[char]
            mirrored_braille += flip_braille(original_braille) + ' '
    
    return mirrored_braille.strip()

def download_mirror_result(request):
    input_text = request.GET.get('input_text', '').strip()
    if not input_text:
        return HttpResponse("No input text provided.", content_type="text/plain")

    braille_content = generate_mirror_braille(input_text)
    response = HttpResponse(braille_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="mirror_result.brf"'
    return response
