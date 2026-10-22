import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        existing_file_path = os.path.isfile(target_file_path)

        if not existing_file_path:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        completedProcess = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""

        if completedProcess.returncode:
            output += f"Process exited with code {completedProcess.returncode} "

        if not completedProcess.stdout and not completedProcess.stderr:
            output += "No output produced "
        else:
            if completedProcess.stdout:
                output += f"STDOUT: {completedProcess.stdout} "
            if completedProcess.stderr:
                output += f"STDERR: {completedProcess.stderr} "

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
