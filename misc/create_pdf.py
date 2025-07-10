from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "CONTRACT DE ANGAJAMENT", ln=True, align='C')
        self.ln(10)
#TODO download #https://www.fontsquirrel.com/fonts/download/dejavu-sans, unzip it and put the DejaVuSans.ttf in the same folder as this script
# Folosim un font care suportă caractere UTF-8
pdf = PDF()
pdf.add_page()
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Asigură-te că fișierul este în același folder
pdf.set_font("DejaVu", size=10)

# Textul contractului
contract_text = """
Încheiat astăzi, 26.06.2025

Între:
X, denumit în continuare STATUS1 și
Y, denumit în continuare STATUS2

Obiectul contractului:
Prezentul contract are ca scop stabilirea unui angajament ferm din partea STATUS1 ..., în condițiile specificate mai jos.

Clauze:
1. Dacă STATUS1 susține prezentarea programată în data de ...,
2. Atunci STATUS2 se obligă să ...
3. Neîndeplinirea acestei obligații atrage pierderea ...

Dispoziții finale:
- Acest contract este asumat de bună credință și are valoare morală în cadrul participantilor.
- Părțile pot modifica acest acord doar cu consimțământul ambelor părți.
- Contractul intră în vigoare la data semnării sale.

_____________________                                          _____________________
X                    STATUS1                                   Y                    STATUS2
"""

# Adaugă textul
pdf.multi_cell(0, 10, contract_text.strip())

# Salvează PDF-ul
pdf.output("Contract_Angajament_X_Y.pdf")
