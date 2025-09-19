from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def genereaza_factura_proforma(nume_client, cont_client, descriere, valoare, numar_factura="PRO-001"):
    pdf_file = f"Factura_{numar_factura}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    # Titlu
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "FACTURA")

    # Informații factură
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Nr. {numar_factura} / 04.08.2025")

    # Furnizor
    c.drawString(50, height - 110, "Furnizor:")
    c.drawString(70, height - 125, "SC Nu e teapa SRL")
    c.drawString(70, height - 140, "CUI: IACUI")
    c.drawString(70, height - 155, "Nr. Reg. Com.: J00/0000/2025")
    c.drawString(70, height - 170, "Adresa: Str. Iasi, Nr. 1, Iasi")
    c.drawString(70, height - 185, "IBAN: RO82REVO0000165156337655")
    c.drawString(70, height - 200, "Banca: Revolut Bank")

    # Client
    c.drawString(300, height - 110, "Client:")
    c.drawString(320, height - 125, f"{nume_client}")
    #c.drawString(320, height - 140, f"Cont client: {cont_client}")

    # Tabel produse
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 230, "Nr. crt.")
    c.drawString(100, height - 230, "Descriere")
    c.drawString(300, height - 230, "Cant.")
    c.drawString(350, height - 230, "UM")
    c.drawString(400, height - 230, "Pret unitar")
    c.drawString(480, height - 230, "Valoare")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 245, "1")
    c.drawString(100, height - 245, descriere)
    c.drawString(300, height - 245, "1")
    c.drawString(350, height - 245, "buc")
    c.drawString(400, height - 245, f"{valoare:.2f} lei")
    c.drawString(480, height - 245, f"{valoare:.2f} lei")

    # Total
    c.setFont("Helvetica-Bold", 10)
    c.drawString(400, height - 280, "Total de plata:")
    c.drawString(480, height - 280, f"{valoare:.2f} lei")

    # Alte mențiuni
    c.setFont("Helvetica", 9)
    c.drawString(50, height - 310, "Scadenta: 5 zile lucratoare de la data emiterii")
    c.drawString(50, height - 325, "Modalitate de plata: Transfer bancar")
    #c.drawString(50, height - 350, "*Aceasta este o factura proforma. Nu ține loc de document fiscal.*")

    # Semnătură
    # c.drawString(50, height - 390, "Semnătură și ștampilă:")
    # c.line(180, height - 392, 350, height - 392)

    c.save()
    print(f"Factura '{pdf_file}' a fost generată cu succes.")

# Exemplu de utilizare
genereaza_factura_proforma(
    nume_client="Pitica Sebastian Razvan",
    cont_client="RO82REVO0000165156337655",
    descriere="Raft + montare + livrare",
    valoare=500.00
)
