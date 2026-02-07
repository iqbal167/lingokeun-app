import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class TokenMonitor:
    def __init__(self):
        self.log_dir = Path("profile")
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "token_usage.json"
        self._ensure_log_file()

    def _ensure_log_file(self):
        """Create log file if it doesn't exist."""
        if not self.log_file.exists():
            self.log_file.write_text(json.dumps({"total": {"input": 0, "output": 0}, "history": []}, indent=2))

    def log_usage(
        self,
        operation: str,
        input_tokens: int,
        output_tokens: int,
        model: str = "gemini-3-flash-preview",
        metadata: Optional[dict] = None,
    ):
        """Log token usage for an API call."""
        data = json.loads(self.log_file.read_text())

        # Update totals
        data["total"]["input"] += input_tokens
        data["total"]["output"] += output_tokens

        # Add to history
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }

        if metadata:
            entry["metadata"] = metadata

        data["history"].append(entry)

        # Save
        self.log_file.write_text(json.dumps(data, indent=2))

    def get_stats(self) -> dict:
        """Get token usage statistics."""
        data = json.loads(self.log_file.read_text())
        
        total_input = data["total"]["input"]
        total_output = data["total"]["output"]
        total = total_input + total_output
        
        return {
            "total_input": total_input,
            "total_output": total_output,
            "total": total,
            "total_calls": len(data["history"]),
            "recent": data["history"][-10:] if data["history"] else [],
        }
