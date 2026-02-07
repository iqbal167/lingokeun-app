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
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{spinner[idx]} {message}...")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner)
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
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
    typer.secho("=" * 40, fg=typer.colors.BLUE)
    typer.secho("🚀 LINGOKEUN: Daily Task Generator", fg=typer.colors.BLUE, bold=True)
    typer.secho(f"📅 Tanggal: {today}", fg=typer.colors.WHITE)
    typer.secho("=" * 40, fg=typer.colors.BLUE)

    try:
        # 2. Proses AI
        typer.secho("\n🤖 Menghubungi Gemini...", fg=typer.colors.YELLOW)

        service = AIService()

        # Start spinner
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(
            target=show_spinner, args=(stop_spinner, "Generating task")
        )
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
    task_number: int = typer.Option(
        1, "--task", "-t", help="Task number to review (1, 2, 3, or 4)"
    ),
):
    """
    Review completed task and append results to task file.
    Opens editor for input.

    Usage:
    - uv run lingokeun review 2026-01-29 --task 1
    - uv run lingokeun review 2026-01-29 -t 2
    - uv run lingokeun review 2026-01-29 -t 3
    - uv run lingokeun review 2026-01-29 -t 4
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

    typer.secho("=" * 40, fg=typer.colors.BLUE)
    typer.secho("📝 LINGOKEUN: Task Review", fg=typer.colors.BLUE, bold=True)
    typer.secho(f"📅 Date: {task_date} | Task: {task_number}", fg=typer.colors.WHITE)
    typer.secho("=" * 40, fg=typer.colors.BLUE)

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
            typer.secho(
                "\n🤖 Reviewing Word Transformation Challenge...",
                fg=typer.colors.YELLOW,
            )
            spinner_thread = threading.Thread(
                target=show_spinner, args=(stop_spinner, "Reviewing Task 1")
            )
            spinner_thread.start()
            review_result = service.review_task1(user_input)
            stop_spinner.set()
            spinner_thread.join()

            # Extract vocabulary mastery from review
            service.extract_vocabulary_mastery_from_review(review_result, task_date)

        elif task_number == 2:
            typer.secho(
                "\n🤖 Reviewing Translation Challenge...", fg=typer.colors.YELLOW
            )
            task_content = task_file.read_text(encoding="utf-8")
            spinner_thread = threading.Thread(
                target=show_spinner, args=(stop_spinner, "Reviewing Task 2")
            )
            spinner_thread.start()
            review_result = service.review_task2(task_content, user_input)
            stop_spinner.set()
            spinner_thread.join()
        elif task_number == 3:
            typer.secho(
                "\n🤖 Reviewing Conversation Transliteration Challenge...",
                fg=typer.colors.YELLOW,
            )
            task_content = task_file.read_text(encoding="utf-8")
            spinner_thread = threading.Thread(
                target=show_spinner, args=(stop_spinner, "Reviewing Task 3")
            )
            spinner_thread.start()
            review_result = service.review_task3(task_content, user_input)
            stop_spinner.set()
            spinner_thread.join()
        elif task_number == 4:
            typer.secho(
                "\n🤖 Reviewing Tense Construction Challenge...", fg=typer.colors.YELLOW
            )
            spinner_thread = threading.Thread(
                target=show_spinner, args=(stop_spinner, "Reviewing Task 4")
            )
            spinner_thread.start()
            review_result = service.review_task4(user_input)
            stop_spinner.set()
            spinner_thread.join()
        else:
            typer.secho(
                "❌ Invalid task number. Use 1, 2, 3, or 4", fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

        # Append review to task file
        with open(task_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n\n# Review - Task {task_number}\n")
            f.write(
                f"**Reviewed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write(review_result)

        # Update user profile with weaknesses
        service.update_user_profile_after_review(
            review_result, f"task_{task_number}", task_date
        )

        typer.secho(
            f"\n✅ Review completed and appended to {task_file}",
            fg=typer.colors.GREEN,
            bold=True,
        )

        # Show weakness summary
        _show_weakness_summary(service)

    except Exception as e:
        typer.secho(f"\n💥 Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("profile")
def show_profile():
    """
    Show your learning profile and weaknesses summary.

    Usage: uv run lingokeun profile
    """
    from .ai_service import AIService

    service = AIService()
    profile = service.profile_manager.load_profile()

    typer.secho("=" * 50, fg=typer.colors.BLUE)
    typer.secho("📊 YOUR LEARNING PROFILE", fg=typer.colors.BLUE, bold=True)
    typer.secho("=" * 50, fg=typer.colors.BLUE)

    typer.secho(
        f"\n📈 Total Reviews: {profile['total_reviews']}", fg=typer.colors.WHITE
    )

    # Focus Areas
    if profile["focus_areas"]["urgent"]:
        typer.secho(
            "\n🔴 URGENT - Need immediate attention:", fg=typer.colors.RED, bold=True
        )
        for area in profile["focus_areas"]["urgent"]:
            typer.echo(f"   • {area}")

    if profile["focus_areas"]["practice"]:
        typer.secho(
            "\n🟡 PRACTICE - Keep working on:", fg=typer.colors.YELLOW, bold=True
        )
        for area in profile["focus_areas"]["practice"]:
            typer.echo(f"   • {area}")

    if profile["focus_areas"]["maintain"]:
        typer.secho("\n🟢 MAINTAIN - Doing well:", fg=typer.colors.GREEN, bold=True)
        for area in profile["focus_areas"]["maintain"]:
            typer.echo(f"   • {area}")

    # Patterns
    if profile["patterns"]["persistent_issues"]:
        typer.secho("\n⚠️  Persistent Issues (3+ mistakes):", fg=typer.colors.MAGENTA)
        for issue in profile["patterns"]["persistent_issues"]:
            typer.echo(f"   • {issue}")

    if profile["patterns"]["improving_areas"]:
        typer.secho("\n✨ Improving Areas:", fg=typer.colors.CYAN)
        for area in profile["patterns"]["improving_areas"]:
            typer.echo(f"   • {area}")

    # Vocabulary Gaps
    if profile["vocabulary_gaps"]:
        typer.secho("\n📚 Vocabulary Gaps:", fg=typer.colors.YELLOW)
        for vocab in profile["vocabulary_gaps"][:5]:
            typer.echo(f"   • {vocab['word']} (missed {vocab['missed_count']}x)")

    typer.echo()


def _show_weakness_summary(service):
    """Show brief weakness summary after review."""
    profile = service.profile_manager.load_profile()

    if profile["focus_areas"]["urgent"]:
        typer.secho(
            "\n⚠️  Focus on: " + ", ".join(profile["focus_areas"]["urgent"][:2]),
            fg=typer.colors.YELLOW,
        )

    if profile["patterns"]["new_issues"]:
        typer.secho(
            f"🆕 New issues detected: {', '.join(profile['patterns']['new_issues'][:2])}",
            fg=typer.colors.CYAN,
        )


@app.command("material")
def generate_material(
    topic: str = typer.Option(
        None, "--topic", "-t", help="Specific topic to generate material for"
    ),
    list_suggestions: bool = typer.Option(
        False, "--list", "-l", help="List suggested topics based on your weaknesses"
    ),
):
    """
    Generate B1 level learning material on specific topics.
    Materials are saved in material/ folder.

    Usage:
    - uv run lingokeun material --list (show suggestions)
    - uv run lingokeun material --topic "Phrasal Verbs"
    """
    from .ai_service import AIService
    import re

    service = AIService()
    material_dir = Path("material")
    material_dir.mkdir(exist_ok=True)

    # List existing materials
    existing_materials = [f.stem for f in material_dir.glob("*.md")]

    # Show suggestions
    if list_suggestions or not topic:
        typer.secho("=" * 50, fg=typer.colors.BLUE)
        typer.secho("📚 SUGGESTED LEARNING MATERIALS", fg=typer.colors.BLUE, bold=True)
        typer.secho("=" * 50, fg=typer.colors.BLUE)

        suggestions = service.suggest_material_topics()

        if suggestions:
            typer.secho("\n💡 Based on your weaknesses:", fg=typer.colors.YELLOW)
            for i, suggested_topic in enumerate(suggestions, 1):
                # Check if already exists
                filename = (
                    re.sub(r"[^\w\s-]", "", suggested_topic)
                    .strip()
                    .replace(" ", "_")
                    .lower()
                )
                status = (
                    "✓ Generated" if filename in existing_materials else "○ Not yet"
                )
                typer.echo(f"   {i}. {suggested_topic} [{status}]")
        else:
            typer.secho("\n💡 No weaknesses detected yet.", fg=typer.colors.GREEN)
            typer.echo(
                "   Complete some reviews first to get personalized material suggestions!"
            )

        if existing_materials:
            typer.secho(
                f"\n📖 Existing materials ({len(existing_materials)}):",
                fg=typer.colors.GREEN,
            )
            for mat in existing_materials[:10]:
                typer.echo(f"   • {mat.replace('_', ' ').title()}")

        if not topic:
            typer.echo('\nUse: uv run lingokeun material --topic "Topic Name"')
            return

    # Generate material
    typer.secho("=" * 50, fg=typer.colors.BLUE)
    typer.secho("📝 GENERATING MATERIAL", fg=typer.colors.BLUE, bold=True)
    typer.secho(f"Topic: {topic}", fg=typer.colors.WHITE)
    typer.secho("=" * 50, fg=typer.colors.BLUE)

    # Create filename
    filename = re.sub(r"[^\w\s-]", "", topic).strip().replace(" ", "_").lower()
    filepath = material_dir / f"{filename}.md"

    # Check if already exists
    if filepath.exists():
        overwrite = typer.confirm(f"\n⚠️  Material '{topic}' already exists. Overwrite?")
        if not overwrite:
            typer.secho("❌ Cancelled", fg=typer.colors.RED)
            raise typer.Exit(code=0)

    try:
        typer.secho("\n🤖 Generating material with AI...", fg=typer.colors.YELLOW)

        # Start spinner
        stop_spinner = threading.Event()
        spinner_thread = threading.Thread(
            target=show_spinner, args=(stop_spinner, "Generating material")
        )
        spinner_thread.start()

        material_content = service.generate_learning_material(topic)

        # Stop spinner
        stop_spinner.set()
        spinner_thread.join()

        if material_content.startswith("Error"):
            typer.secho(f"\n💥 Failed: {material_content}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        # Save material
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(material_content)

        typer.secho(
            f"\n✅ Material saved: {filepath}", fg=typer.colors.GREEN, bold=True
        )
        typer.echo("   Open and study this material to improve your B1 level skills!")

    except Exception as e:
        typer.secho(f"\n💥 Error: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command("vocab")
def manage_vocabulary(
    add: str = typer.Option(None, "--add", "-a", help="Add new vocabulary word"),
    word_type: str = typer.Option(None, "--type", "-y", help="Word type (n/v/adj/adv)"),
    meaning: str = typer.Option(None, "--meaning", "-m", help="Meaning of the word"),
    stats: bool = typer.Option(
        False, "--stats", "-s", help="Show vocabulary statistics"
    ),
    word: str = typer.Option(
        None, "--word", "-w", help="Show details of specific word"
    ),
    update_form: str = typer.Option(
        None,
        "--update-form",
        "-u",
        help="Update word form: word:form_type:value (e.g., facilitate:noun:facilitation)",
    ),
):
    """
    Manage vocabulary database.

    Usage:
    - uv run lingokeun vocab --add prominently --type adv --meaning "secara menonjol"
    - uv run lingokeun vocab --stats
    - uv run lingokeun vocab --word facilitate
    - uv run lingokeun vocab --update-form "facilitate:noun:facilitation"
    """
    from .ai_service import AIService

    service = AIService()
    vocab_db = service.profile_manager.vocab_db

    # Update word form
    if update_form:
        parts = update_form.split(":")
        if len(parts) != 3:
            typer.secho(
                "❌ Format: word:form_type:value (e.g., facilitate:noun:facilitation)",
                fg=typer.colors.RED,
            )
            return

        word_name, form_type, form_value = parts
        valid_forms = ["verb", "noun", "adjective", "adverb", "opposite"]

        if form_type.lower() not in valid_forms:
            typer.secho(
                f"❌ Invalid form type. Use: {', '.join(valid_forms)}",
                fg=typer.colors.RED,
            )
            return

        success = vocab_db.update_word_form(word_name, form_type, form_value)

        if success:
            typer.secho(f"\n✅ Updated {word_name}", fg=typer.colors.GREEN, bold=True)
            typer.echo(f"   {form_type.title()}: {form_value}")
        else:
            typer.secho(f"❌ Word '{word_name}' not found", fg=typer.colors.RED)
        return

    # Add new vocabulary
    if add:
        vocab_db.add_vocabulary(
            word=add, word_type=word_type, meaning=meaning, source="manual"
        )
        typer.secho(f"\n✅ Added vocabulary: {add}", fg=typer.colors.GREEN, bold=True)
        if word_type:
            typer.echo(f"   Type: {word_type}")
        if meaning:
            typer.echo(f"   Meaning: {meaning}")
        typer.echo("   This word will be included in future tasks!")
        return

    # Show statistics
    if stats:
        stats_data = vocab_db.get_vocabulary_stats()

        typer.secho("=" * 50, fg=typer.colors.BLUE)
        typer.secho("📊 VOCABULARY STATISTICS", fg=typer.colors.BLUE, bold=True)
        typer.secho("=" * 50, fg=typer.colors.BLUE)

        typer.echo(f"\n📚 Total Vocabulary: {stats_data['total']}")
        typer.secho(
            f"✅ Mastered (80%+): {stats_data['mastered']}", fg=typer.colors.GREEN
        )
        typer.secho(f"⚠️  Weak (<80%): {stats_data['weak']}", fg=typer.colors.YELLOW)
        typer.secho(f"🆕 Unreviewed: {stats_data['unreviewed']}", fg=typer.colors.CYAN)

        # Show progress
        if stats_data["total"] > 0:
            mastery_rate = int((stats_data["mastered"] / stats_data["total"]) * 100)
            typer.echo(f"\n📈 Mastery Rate: {mastery_rate}%")
            typer.echo(f"🎯 Target: 5000 vocabulary ({stats_data['total']}/5000)")

        typer.echo()
        return

    # Show word details
    if word:
        details = vocab_db.get_word_details(word)

        if not details:
            typer.secho(f"❌ Word '{word}' not found in database", fg=typer.colors.RED)
            return

        typer.secho("=" * 50, fg=typer.colors.BLUE)
        typer.secho(f"📖 {details['word'].upper()}", fg=typer.colors.BLUE, bold=True)
        typer.secho("=" * 50, fg=typer.colors.BLUE)

        if details["word_type"]:
            typer.echo(f"\n🏷️  Type: {details['word_type']}")

        if details["meaning"]:
            typer.echo(f"💡 Meaning: {details['meaning']}")

        typer.echo(f"\n📊 Reviews: {details['total_reviews']}")
        typer.echo(f"🎯 Accuracy: {details['accuracy_score']}%")

        if details["last_reviewed"]:
            typer.echo(f"📅 Last Reviewed: {details['last_reviewed']}")

        typer.echo(f"📌 Source: {details['source']}")

        # Show forms with values and meanings
        if details["forms"]:
            typer.echo("\n📝 Word Forms:")
            for form, data in details["forms"].items():
                status = "✅" if data["is_mastered"] else "❌"
                value = data["value"] if data["value"] else "-"
                meaning = data["meaning"] if data["meaning"] else "-"
                typer.echo(f"   {status} {form.title()}: {value} ({meaning})")

        if details["history"]:
            typer.echo("\n📈 Review History:")
            for h in details["history"][:5]:
                typer.echo(f"   {h['date']}: {h['accuracy']}%")

        typer.echo()
        return

    # No options provided, show help
    typer.echo("Use --help to see available options")


@app.command("tokens")
def show_token_usage():
    """Show AI token usage statistics."""
    from .token_monitor import TokenMonitor
    
    monitor = TokenMonitor()
    stats = monitor.get_stats()
    
    typer.secho("=" * 50, fg=typer.colors.BLUE)
    typer.secho("🤖 AI TOKEN USAGE STATISTICS", fg=typer.colors.BLUE, bold=True)
    typer.secho("=" * 50, fg=typer.colors.BLUE)
    
    typer.echo("\n📊 Total Usage:")
    typer.echo(f"   Input Tokens:  {stats['total_input']:,}")
    typer.echo(f"   Output Tokens: {stats['total_output']:,}")
    typer.secho(f"   Total Tokens:  {stats['total']:,}", fg=typer.colors.CYAN, bold=True)
    
    typer.echo(f"\n📈 API Calls: {stats['total_calls']}")
    
    if stats['recent']:
        typer.echo("\n🕐 Recent Operations (last 10):")
        for entry in stats['recent']:
            timestamp = entry['timestamp'][:19].replace('T', ' ')
            operation = entry['operation']
            total = entry['total_tokens']
            typer.echo(f"   {timestamp} | {operation:25s} | {total:,} tokens")
    
    typer.echo()


if __name__ == "__main__":
    app()
