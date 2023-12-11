import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
import tkinter.ttk as ttk

from rcon.console import Console
from rcon.util import remove_formatting_codes

def main():
    root = tk.Tk()
    root.title('RCON GUI')

    # log in

    frame = ttk.Frame(root, padding=5)
    frame.pack(padx=20)

    ttk.Label(frame, text='Host:').grid(row=0, column=0, pady=5)
    entry_host = ttk.Entry(frame)
    entry_host.grid(row=0, column=1)
    entry_host.focus_set()

    ttk.Label(frame, text='Password:').grid(row=1, column=0, pady=5)
    entry_password = ttk.Entry(frame, show='*')
    entry_password.grid(row=1, column=1)

    def run_console(*_):
        host = entry_host.get()
        password = entry_password.get()
        # clear password
        entry_password.delete(0, tk.END)

        try:
            if ":" in host:
                host_splitted = host.split(':')
                host = host_splitted[0]
                port = int(host_splitted[1])
            else:
                port = 25575

            console = Console(host, password, port)
        except Exception as e:
            mb.showerror(message=f'Connection failed: {e}')
            return

        root.withdraw()
        console_window = tk.Toplevel(root)

        def close_console():
            console.close()
            console_window.destroy()
            root.deiconify()

        console_window.protocol('WM_DELETE_WINDOW', close_console)

        # Scroll bar

        frame = ttk.Frame(console_window)
        frame.pack(fill=tk.BOTH, expand=tk.YES, padx=(10, 0), pady=(10, 0))

        scroll = st.ScrolledText(frame)
        scroll.configure(state=tk.DISABLED)
        scroll.pack(fill=tk.BOTH, expand=tk.YES)

        # Command input form

        frame = ttk.Frame(console_window, padding=10)
        frame.pack(fill=tk.X)
        frame.columnconfigure(0, weight=1)

        entry = ttk.Entry(frame)
        entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        entry.focus_force()

        def update(*_):
            command_text = entry.get()
            entry.delete(0, tk.END)

            # Remove leading slash
            if command_text.startswith('/'):
                command_text = command_text[1:]

            res_body = console.command(command_text)

            # Remove all formatting codes
            res_body = remove_formatting_codes(res_body)

            # If the response does not end with a newline, add a newline
            if not res_body.endswith('\n'):
                res_body += '\n'

            scroll.configure(state=tk.NORMAL)
            scroll.insert(tk.END, f'[{host}:{port}] > {command_text}\n')
            scroll.insert(tk.END, res_body)
            scroll.configure(state=tk.DISABLED)
            scroll.yview_moveto(1)

        def clear(*_):
            scroll.configure(state=tk.NORMAL)
            scroll.delete('1.0', tk.END)
            scroll.configure(state=tk.DISABLED)

        entry.bind('<Return>', update)
        ttk.Button(frame, text='Submit', command=update).grid(
            row=0, column=1, padx=(0, 5))
        ttk.Button(frame, text='Clear', command=clear).grid(row=0, column=2)

    frame = ttk.Frame(root, padding=10)
    frame.pack()

    entry_password.bind('<Return>', run_console)
    ttk.Button(frame, text='Exit', command=root.quit).grid(
        row=0, column=0, padx=(0, 5))
    ttk.Button(frame, text='Login',
               command=run_console).grid(row=0, column=1)

    root.mainloop()


if __name__ == '__main__':
    main()
