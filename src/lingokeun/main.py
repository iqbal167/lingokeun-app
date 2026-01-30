import typer
from datetime import date, datetime
from pathlib import Path
from .ai_service import AIService

# Inisialisasi aplikasi Typer
app = typer.Typer()

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
        typer.echo("   Meminta AI memilih 5 kata teknis & membuat soal level B1...")
        
        service = AIService()
        
        # Panggil fungsi tanpa argumen
        markdown_content = service.generate_daily_task()

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
    task_number: int = typer.Option(1, "--task", "-t", help="Task number to review (1 or 2)")
):
    """
    Review completed task and append results to task file.
    Opens editor for input.
    
    Usage: 
    - uv run lingokeun review 2026-01-29 --task 1
    - uv run lingokeun review 2026-01-29 -t 2
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
        
        if task_number == 1:
            typer.secho("\n🤖 Reviewing Word Transformation Challenge...", fg=typer.colors.YELLOW)
            review_result = service.review_task1(user_input)
        elif task_number == 2:
            typer.secho("\n🤖 Reviewing Translation Challenge...", fg=typer.colors.YELLOW)
            task_content = task_file.read_text(encoding="utf-8")
            review_result = service.review_task2(task_content, user_input)
        else:
            typer.secho("❌ Invalid task number. Use 1 or 2", fg=typer.colors.RED)
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