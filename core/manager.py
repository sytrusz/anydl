import subprocess
import threading
import queue

class DownloadManager:
    def __init__(self):
        self.output_queue = queue.Queue()
        self.process = None

    def start_download(self, command, cwd=None):
        """Starts the download process in a separate thread."""
        self.output_queue.put(("STATUS", f"Starting command: {' '.join(command)}"))
        if cwd:
            self.output_queue.put(("STATUS", f"Output directory: {cwd}"))
        thread = threading.Thread(target=self._run_process, args=(command, cwd), daemon=True)
        thread.start()

    def _run_process(self, command, cwd):
        """Runs the subprocess and captures stdout and stderr."""
        try:
            self.process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Start threads to read stdout and stderr continuously
            stdout_thread = threading.Thread(target=self._read_stream, args=(self.process.stdout, "STDOUT"), daemon=True)
            stderr_thread = threading.Thread(target=self._read_stream, args=(self.process.stderr, "STDERR"), daemon=True)
            
            stdout_thread.start()
            stderr_thread.start()
            
            self.process.wait()
            
            stdout_thread.join()
            stderr_thread.join()
            
            self.output_queue.put(("STATUS", f"Process finished with exit code {self.process.returncode}"))
            
        except Exception as e:
            self.output_queue.put(("ERROR", str(e)))

    def _read_stream(self, stream, stream_type):
        """Reads from a stream and puts lines into the queue, handling carriage returns."""
        buffer = ""
        while True:
            char = stream.read(1)
            if not char:
                if buffer:
                    self.output_queue.put((stream_type, buffer.strip()))
                break
            if char in ['\r', '\n']:
                if buffer:
                    self.output_queue.put((stream_type, buffer.strip()))
                    buffer = ""
            else:
                buffer += char
        stream.close()

    def get_messages(self):
        """Returns all available messages from the queue without blocking."""
        messages = []
        while not self.output_queue.empty():
            try:
                messages.append(self.output_queue.get_nowait())
            except queue.Empty:
                break
        return messages
