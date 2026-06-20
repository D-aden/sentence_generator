import tkinter as tk
from tkinter import ttk, filedialog
from main import clean_articles 
from main import read_articles
from main import markov_model
from main import text_generation


def generate_text():
    """
    - used in the 'Generate Text' button 
    - opens file dialog, allows user to pick one or more csv files
    - file is read and cleaned, a markov model is built, and tex is generated 
        using the sentence length and count. 
    - output is written in ouput text widget 
    """
    files = filedialog.askopenfilenames(title='Select Articles', filetypes=[('CSV Files', '*.csv')])

    if not files:
        return

    texts = [read_articles(f) for f in files]
    all_text = ' '.join(texts)

    tokens = clean_articles(all_text)

    model = markov_model(tokens, int(order.get()))

    final_text = text_generation(model, tokens, int(order.get()), int(length.get()), int(num_sentences.get()))

    output.delete('1.0', tk.END)
    output.insert(tk.END, final_text)



window = tk.Tk()
window.title('Markov Text Generator')
window.configure(background='#1e1e2e')
window.geometry('900x600')
window.minsize(800, 500)

style=ttk.Style()
style.theme_use('clam')
style.configure('Title.TLabel', font=('Segoe UI', 22, 'bold'), background='#282a36', foreground='white')
style.configure('Card.TFrame', background='#282a36')
style.configure('TLabel', background='#282a36', foreground='white', font=('Segoe UI', 10))
style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), padding=8)

# widgets are placed in the padded card so that the dark window is visible as a border 
card = ttk.Frame(window, style='Card.TFrame', padding=25)
card.pack(fill='both', expand=True, padx=25, pady=25)
title= ttk.Label(card, text='Markov Text Generator', style='Title.TLabel')
title.grid(row=0, column=0, columnspan=2, pady=(0,25))


#entry widget created to enter preferred n-gram order 
ttk.Label(card, text='N-gram Order').grid(row=1, column=0, sticky='w', pady=5)
order = tk.StringVar(value='2')
ttk.Entry(card, textvariable=order, width=20).grid(row=1, column=1, sticky='ew', pady=5)

#entry widget created to enter preferred sentence length  
ttk.Label(card, text='Sentence Length').grid(row=2, column=0, sticky='w', pady=5)
length = tk.StringVar(value='15')
ttk.Entry(card, textvariable=length, width=20).grid(row=2, column=1, sticky='ew', pady=5)

#entry widget created to enter preferred number of sentences 
ttk.Label(card, text='Number of Sentences').grid(row=3, column=0, sticky='w', pady=5)
num_sentences = tk.StringVar(value='5')
ttk.Entry(card, textvariable=num_sentences, width=20).grid(row=3, column=1, sticky='ew', pady=5)

#button created to lead to file dialogue and to initiate text generation 
ttk.Button(card, text='Generate Text', command=generate_text, style='Accent.TButton').grid(row=4, column=0, sticky='ew', pady=(20,20))

#scrollable text box created to display the generated text. 
output = tk.Text(card, wrap='word', font=('Consolas', 11), background='#1e1e2e',
foreground='white', insertbackground='white', relief='flat', padx=12, pady=12)
output.grid(row=5, column=0, columnspan=2, sticky='nsew')


card.columnconfigure(1, weight=1)
card.rowconfigure(5, weight=1)

window.mainloop()
