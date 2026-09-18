from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import add_pet, get_pet
import random

#!!! TROQUE AQUI PELO SEU TOKEN DO BOTFATHER!!!
TOKEN = "SEU_TOKEN_AQUI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐾 Bem-vindo a Bichometria!\n\n"
        "Comandos:\n"
        "/cadastrar - Cadastra um pet perdido (teste)\n"
        "/buscar BICH-1234 - Busca um pet pelo código\n"
        "/meuid - Mostra seu ID"
    )

async def meuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Seu ID é: {chat_id}\nGuarde ele!")

async def cadastrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    nome_user = update.effective_user.first_name

    # Gera um código aleatório
    codigo = f"BICH-{random.randint(1000, 9999)}"

    # Cadastra um pet de exemplo com SEU ID
    add_pet(codigo, "Rex", "Cachorro", nome_user, str(chat_id))

    await update.message.reply_text(
        f"✅ CADASTRADO COM SUCESSO!\n\n"
        f"Código: {codigo}\n"
        f"Nome: Rex\n"
        f"Tutor: {nome_user}\n\n"
        f"Agora teste: /buscar {codigo}"
    )

async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use assim: /buscar BICH-1234")
        return

    codigo = context.args[0].upper()
    pet = get_pet(codigo)

    if not pet:
        await update.message.reply_text(f"❌ Código {codigo} não encontrado.")
        return

    # pet = (codigo, nome, tipo, tutor_nome, tutor_chat_id)
    await update.message.reply_text(
        f"✅ ENCONTRADO!\n\n"
        f"Código: {pet[0]}\n"
        f"Nome: {pet[1]}\n"
        f"Tipo: {pet[2]}\n"
        f"Tutor: {pet[3]}"
    )

    # Notifica o tutor
    try:
        if str(pet[4])!= str(update.effective_chat.id):
            await context.bot.send_message(
                chat_id=pet[4],
                text=f"🔔 ALERTA! Alguém buscou pelo código do seu pet {pet[1]} ({pet[0]}). Seu pet pode ter sido encontrado!"
            )
    except:
        pass

print("Iniciando o bot...")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("meuid", meuid))
app.add_handler(CommandHandler("cadastrar", cadastrar))
app.add_handler(CommandHandler("buscar", buscar))

app.run_polling()