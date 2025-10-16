import tkinter as tk
from tkinter import messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
import random
import ssl # Para lidar com a segurança SSL/TLS

# --- Frases de Sabedoria (você pode adicionar mais!) ---
FRASES_SABEDORIA = [
    "A sabedoria começa na reflexão.",
    "O único verdadeiro conhecimento é saber que você não sabe nada.",
    "A persistência realiza o impossível.",
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "A maior glória em viver não reside em nunca cair, mas em levantar-se cada vez que caímos.",
    "O futuro pertence àqueles que acreditam na beleza de seus sonhos.",
    "Se você quer algo que nunca teve, precisa fazer algo que nunca fez.",
    "A vida é 10% do que acontece com você e 90% de como você reage a isso.",
    "A mente é tudo. O que você pensa, você se torna.",
    "Não espere por condições perfeitas; comece onde você está."
]

class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sabedoria Diária por E-mail 📧")
        self.root.geometry("600x800") # Tamanho da janela
        self.root.resizable(False, False) # Impede redimensionamento

        self.create_widgets()

    def create_widgets(self):
        # Frame principal para organização
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Configurações do Remetente ---
        tk.Label(main_frame, text="Seu Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sender_email_entry = tk.Entry(main_frame, width=50)
        self.sender_email_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(main_frame, text="Sua Senha do Email (ou Senha de App):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sender_password_entry = tk.Entry(main_frame, width=50, show="*") # show="*" esconde a senha
        self.sender_password_entry.grid(row=1, column=1, pady=5, padx=5)

        # --- Configurações do Destinatário ---
        tk.Label(main_frame, text="Email do Destinatário:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.receiver_email_entry = tk.Entry(main_frame, width=50)
        self.receiver_email_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(main_frame, text="Assunto:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.subject_entry = tk.Entry(main_frame, width=50)
        self.subject_entry.insert(0, "Uma Dose Diária de Sabedoria ✨") # Assunto padrão
        self.subject_entry.grid(row=3, column=1, pady=5, padx=5)

        # --- Botão Enviar ---
        send_button = tk.Button(main_frame, text="Enviar Sabedoria por E-mail", command=self.send_email, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        send_button.grid(row=4, column=0, columnspan=2, pady=20)

        # --- Cópia da Mensagem Enviada ---
        tk.Label(main_frame, text="Corpo da Mensagem Enviada:").grid(row=5, column=0, sticky=tk.W, pady=10)
        self.message_display = scrolledtext.ScrolledText(main_frame, width=60, height=15, wrap=tk.WORD, state=tk.DISABLED, bg="#f0f0f0")
        self.message_display.grid(row=6, column=0, columnspan=2, pady=5)

    def send_email(self):
        sender_email = self.sender_email_entry.get()
        sender_password = self.sender_password_entry.get()
        receiver_email = self.receiver_email_entry.get()
        subject = self.subject_entry.get()

        # Validação básica dos campos
        if not sender_email or not sender_password or not receiver_email or not subject:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de enviar.")
            return

        # Escolhe uma frase aleatória
        wisdom_quote = random.choice(FRASES_SABEDORIA)
        body = f"Olá!\n\nAqui está sua dose diária de sabedoria:\n\n\" {wisdom_quote} \"\n\nTenha um ótimo dia!"

        # Cria o objeto MIMEText
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Exibe o corpo da mensagem na tela
        self.message_display.config(state=tk.NORMAL) # Habilita para escrita
        self.message_display.delete(1.0, tk.END) # Limpa conteúdo anterior
        self.message_display.insert(tk.END, body)
        self.message_display.config(state=tk.DISABLED) # Desabilita novamente

        try:
            # Configurações do servidor SMTP - Exemplo para Gmail
            # Para outros provedores, você precisará encontrar o servidor SMTP e a porta
            # Ex: Outlook/Hotmail: smtp-mail.outlook.com (porta 587)
            # Ex: Yahoo Mail: smtp.mail.yahoo.com (porta 587)
            smtp_server = "mail.gmx.com"
            smtp_port = 587 # Porta TLS/STARTTLS

            # Cria um contexto SSL seguro
            context = ssl.create_default_context()

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls(context=context) # Inicia a criptografia TLS
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            
            messagebox.showinfo("Sucesso", "E-mail de sabedoria enviado com sucesso! 🎉")

        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Erro de Autenticação", 
                                 "Falha ao autenticar. Verifique seu email e senha.\n"
                                 "Para Gmail, talvez precise usar uma 'Senha de App' se a Verificação em Duas Etapas estiver ativada, ou permitir 'Acesso a apps menos seguros' (não recomendado).\n"
                                 "")
        except smtplib.SMTPConnectError:
            messagebox.showerror("Erro de Conexão", 
                                 "Não foi possível conectar ao servidor SMTP. Verifique sua conexão com a internet ou o endereço do servidor/porta.")
        except Exception as e:
            messagebox.showerror("Erro de Envio", f"Ocorreu um erro ao enviar o e-mail: {e}")

# --- Executa a Aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EmailSenderApp(root)
    root.mainloop()