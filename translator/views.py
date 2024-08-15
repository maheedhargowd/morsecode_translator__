from django.http import FileResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
import io 
from django.shortcuts import render 
# Morse code dictionaries
ENGLISH_TO_MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '~':'.-.-..', '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '(': '-.--.',
    '/': '-..-.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.', '#':'.--.--...', ' ': ' ',
    '%':'.----.-'
}

MORSE_TO_ENGLISH = {v: k for k, v in ENGLISH_TO_MORSE.items()}

ENGLISH_TO_BRAILLE = {
    "A": "⠁",
    "B": "⠃",
    "C": "⠉",
    "D": "⠙",
    "E": "⠑",
    "F": "⠋",
    "G": "⠛",
    "H": "⠓",
    "I": "⠊",
    "J": "⠚",
    "K": "⠅",
    "L": "⠇",
    "M": "⠍",
    "N": "⠝",
    "O": "⠕",
    "P": "⠏",
    "Q": "⠟",
    "R": "⠗",
    "S": "⠎",
    "T": "⠞",
    "U": "⠥",
    "V": "⠧",
    "W": "⠺",
    "X": "⠭",
    "Y": "⠽",
    "Z": "⠵",
    "1": "⠼⠁",
    "2": "⠼⠃",
    "3": "⠼⠉",
    "4": "⠼⠙",
    "5": "⠼⠑",
    "6": "⠼⠋",
    "7": "⠼⠛",
    "8": "⠼⠓",
    "9": "⠼⠊",
    "0": "⠼⠚",
    ".": "⠲",
    ",": "⠂",
    ";": "⠆",
    ":": "⠒",
    "!": "⠖",
    "?": "⠦",
    "”": "⠶",
    "(": "⠐⠣",
    ")": "⠐⠜",
    "-": "⠤",
    "/": "⠌",
    "+": "⠖",
    "=": "⠶",
    "*": "⠔",
    "&": "⠯",
    "Capital": "⠠",
    "Number": "⠼"
}

def index(request) :
    return render(request,'index.html')
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
        
        # Create a PNG file for download
        if 'download' in request.POST:
            try:
                # Create an image with white background
                image = Image.new('RGB', (500, 100), color=(255, 255, 255))
                draw = ImageDraw.Draw(image)
                
                # Define the font and size
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust the path for the font on your server
                try:
                    font = ImageFont.truetype(font_path, 15)
                except IOError:
                    font = ImageFont.load_default()

                # Add Braille text to the image
                draw.text((10, 10), braille_output, fill=(0, 0, 0), font=font)
                
                # Save the image to a BytesIO object
                image_io = io.BytesIO()
                image.save(image_io, format='PNG')
                image_io.seek(0)

                # Create a FileResponse to download the image
                response = FileResponse(image_io, as_attachment=True, filename='mirror_result.png')
                return response

            except Exception as e:
                # Log the error for debugging
                print(f"Error generating image: {e}")

                # Return an error response
                return JsonResponse({'error': 'An error occurred while generating the image.'}, status=500)

    return JsonResponse({'morseOutput': morse_output, 'englishOutput': english_output, 'brailleOutput': braille_output})
