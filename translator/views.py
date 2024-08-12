

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse

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



def index(request):
    return render(request, 'translator/index.html')

# Assuming you already have ENGLISH_TO_MORSE and MORSE_TO_ENGLISH dictionaries defined





def translate(request):
    user_input = request.POST.get('userInput', '').strip()
    translation_type = request.POST.get('translationType', '')

    morse_output = ''
    english_output = ''

    if translation_type == 'toMorse':
        # Translate English to Morse
        morse_output = ' '.join(ENGLISH_TO_MORSE.get(char.upper(), '') for char in user_input)
    elif translation_type == 'toEnglish':
        # Translate Morse to English
        morse_words = user_input.strip().split('   ')  # Morse words separated by 3 spaces
        english_output = ' '.join(''.join(MORSE_TO_ENGLISH.get(letter, '') for letter in word.split(' ')) for word in morse_words)

    return JsonResponse({'morseOutput': morse_output, 'englishOutput': english_output})




