import typer
from datetime import date
from pathlib import Path
from .ai_service import AIService

# Inisialisasi aplikasi Typer
app = typer.Typer()

@app.command()
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
    typer.secho(f"🚀 LINGOKEUN: Daily Task Generator", fg=typer.colors.BLUE, bold=True)
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
        typer.secho(f"\n✅ BERHASIL!", fg=typer.colors.GREEN, bold=True)
        typer.echo(f"   Materi telah disimpan di file: {filename}")
        typer.echo("   Selamat belajar! Jangan lupa 'commit' ilmu hari ini. 😉")

    except Exception as e:
        typer.secho(f"\n💥 Terjadi kesalahan sistem: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()