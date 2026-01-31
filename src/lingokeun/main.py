import typer
from datetime import date, datetime
from pathlib import Path
import threading
import time
import sys
from .ai_service import AIService

# Inisialisasi aplikasi Typer
app = typer.Typer()

def show_spinner(stop_event, message="Processing"):
    """Display a spinner animation while processing."""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r{spinner[idx]} {message}...')
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner)
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
    sys.stdout.flush()

@app.command("generate")
def generate():
    """
    Generate materi latihan harian.
    
    Biarkan AI yang memilihkan 5 kata terbaik untukmu hari ini.
    Usage: uv run lingokeun generate
    """
    
    # 1. Setup Tanggal
    today = date.today().strftime("%Y-%m-%d")
    
    # Header Tampilan
    typer.secho("="*40, fg=typer.colors.BLUE)
    typer.secho("🚀 LINGOKEUN: Daily Task Generator", fg=typer.colors.BLUE, bold=True)
    typer.secho(f"📅 Tanggal: {today}", fg=typer.colors.WHITE)
    typer.secho("="*40, fg=typer.colors.BLUE)

    try:
        # 2. Proses AI
        typer.secho("\n🤖 Menghubungi Gemini...", fg=typer.colors.YELLOW)
        
        service = AIService()
        
        # Start spinner
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner, "Generating task"))
        spinner_thread.start()
        
        # Panggil fungsi tanpa argumen
        markdown_content = service.generate_daily_task()
        
        # Stop spinner
        stop_spinner.set()
        spinner_thread.join()

        # 3. Cek Error dari Service
        if markdown_content.startswith("Error"):
            typer.secho(f"\n💥 Gagal: {markdown_content}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        # 4. Simpan ke File
        tasks_dir = Path("tasks")
        tasks_dir.mkdir(exist_ok=True)
        filename = tasks_dir / f"task_{today}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        # 5. Sukses
        typer.secho("\n✅ BERHASIL!", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"   Materi telah disimpan di file: {filename}")
        typer.echo("   Selamat belajar! Jangan lupa 'commit' ilmu hari ini. 😉")

    except Exception as e:
        typer.secho(f"\n💥 Terjadi kesalahan sistem: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command("review")
def review(
    task_date: str = typer.Argument(..., help="Task date in YYYY-MM-DD format"),
    task_number: int = typer.Option(1, "--task", "-t", help="Task number to review (1, 2, or 3)")
):
    """
    Review completed task and append results to task file.
    Opens editor for input.
    
    Usage: 
    - uv run lingokeun review 2026-01-29 --task 1
    - uv run lingokeun review 2026-01-29 -t 2
    - uv run lingokeun review 2026-01-29 -t 3
    """
    
    # Validate date format
    try:
        datetime.strptime(task_date, "%Y-%m-%d")
    except ValueError:
        typer.secho("❌ Invalid date format. Use YYYY-MM-DD", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    # Check task file exists
    task_file = Path("tasks") / f"task_{task_date}.md"
    if not task_file.exists():
        typer.secho(f"❌ Task file not found: {task_file}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    typer.secho("="*40, fg=typer.colors.BLUE)
    typer.secho("📝 LINGOKEUN: Task Review", fg=typer.colors.BLUE, bold=True)
    typer.secho(f"📅 Date: {task_date} | Task: {task_number}", fg=typer.colors.WHITE)
    typer.secho("="*40, fg=typer.colors.BLUE)
    
    # Open editor for user input
    typer.secho("\n✏️  Opening editor for your answers...", fg=typer.colors.YELLOW)
    typer.echo("   Paste your completed task answers, save and close the editor.\n")
    
    user_input = typer.edit("")
    
    if not user_input or user_input.strip() == "":
        typer.secho("❌ No input provided. Review cancelled.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    try:
        service = AIService()
        
        # Start spinner
        stop_spinner = threading.Event()
        
        if task_number == 1:
            typer.secho("\n🤖 Reviewing Word Transformation Challenge...", fg=typer.colors.YELLOW)
            spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner, "Reviewing Task 1"))
            spinner_thread.start()
            review_result = service.review_task1(user_input)
            stop_spinner.set()
            spinner_thread.join()
        elif task_number == 2:
            typer.secho("\n🤖 Reviewing Translation Challenge...", fg=typer.colors.YELLOW)
            task_content = task_file.read_text(encoding="utf-8")
            spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner, "Reviewing Task 2"))
            spinner_thread.start()
            review_result = service.review_task2(task_content, user_input)
            stop_spinner.set()
            spinner_thread.join()
        elif task_number == 3:
            typer.secho("\n🤖 Reviewing Conversation Transliteration Challenge...", fg=typer.colors.YELLOW)
            task_content = task_file.read_text(encoding="utf-8")
            spinner_thread = threading.Thread(target=show_spinner, args=(stop_spinner, "Reviewing Task 3"))
            spinner_thread.start()
            review_result = service.review_task3(task_content, user_input)
            stop_spinner.set()
            spinner_thread.join()
        else:
            typer.secho("❌ Invalid task number. Use 1, 2, or 3", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        
        # Append review to task file
        with open(task_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n# Review - Task {task_number}\n")
            f.write(f"**Reviewed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(review_result)
        
        typer.secho(f"\n✅ Review completed and appended to {task_file}", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"\n💥 Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()