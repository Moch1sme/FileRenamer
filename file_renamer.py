import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File & Folder Renamer")
        self.root.geometry("950x620")
        self.root.configure(bg="#F5F5F3")
        self.root.resizable(True, True)

        self.items = []  # list of dict: {path, name, base, ext, is_folder, new_name}
        self.drag_src_idx = None
        self.current_mode = tk.StringVar(value="sequence")

        self._build_ui()
        self._update_preview()

    def _build_ui(self):
        # Main container
        main = tk.Frame(self.root, bg="#F5F5F3")
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Left panel
        left = tk.Frame(main, bg="#FFFFFF", relief="flat", bd=0,
                        highlightthickness=1, highlightbackground="#DEDDD8")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left.pack_propagate(False)
        left.config(width=300)

        tk.Label(left, text="PENGATURAN RENAME", bg="#F5F5F3", fg="#888780",
                 font=("Helvetica", 10, "bold"), pady=8).pack(fill=tk.X, padx=12)

        sep = tk.Frame(left, bg="#DEDDD8", height=1)
        sep.pack(fill=tk.X)

        ctrl_frame = tk.Frame(left, bg="#FFFFFF")
        ctrl_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        # Mode tabs
        tk.Label(ctrl_frame, text="Mode rename", bg="#FFFFFF", fg="#5F5E5A",
                 font=("Helvetica", 10)).pack(anchor="w", pady=(0, 4))
        mode_frame = tk.Frame(ctrl_frame, bg="#FFFFFF")
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.mode_btns = {}
        modes = [("Urutan angka", "sequence"), ("Ganti teks", "replace"), ("Custom", "custom")]
        for label, val in modes:
            btn = tk.Button(mode_frame, text=label, command=lambda v=val: self._set_mode(v),
                            font=("Helvetica", 9), relief="flat", bd=0, cursor="hand2",
                            padx=6, pady=4)
            btn.pack(side=tk.LEFT, padx=2)
            self.mode_btns[val] = btn
        self._update_mode_btns("sequence")

        # -- Sequence frame --
        self.seq_frame = tk.Frame(ctrl_frame, bg="#FFFFFF")
        self._make_label(self.seq_frame, "Prefix (awal nama)")
        self.prefix_var = tk.StringVar()
        self._make_entry(self.seq_frame, self.prefix_var, "contoh: foto_")

        self._make_label(self.seq_frame, "Suffix (akhir nama)")
        self.suffix_var = tk.StringVar()
        self._make_entry(self.seq_frame, self.suffix_var, "contoh: _edit")

        row2 = tk.Frame(self.seq_frame, bg="#FFFFFF")
        row2.pack(fill=tk.X, pady=(4, 0))
        left2 = tk.Frame(row2, bg="#FFFFFF")
        left2.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        right2 = tk.Frame(row2, bg="#FFFFFF")
        right2.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self._make_label(left2, "Mulai dari")
        self.start_var = tk.IntVar(value=1)
        tk.Spinbox(left2, from_=0, to=9999, textvariable=self.start_var, width=8,
                   command=self._update_preview, font=("Helvetica", 10)).pack(fill=tk.X)

        self._make_label(right2, "Step")
        self.step_var = tk.IntVar(value=1)
        tk.Spinbox(right2, from_=1, to=100, textvariable=self.step_var, width=8,
                   command=self._update_preview, font=("Helvetica", 10)).pack(fill=tk.X)

        row3 = tk.Frame(self.seq_frame, bg="#FFFFFF")
        row3.pack(fill=tk.X, pady=(6, 0))
        left3 = tk.Frame(row3, bg="#FFFFFF")
        left3.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        right3 = tk.Frame(row3, bg="#FFFFFF")
        right3.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self._make_label(left3, "Padding (digit)")
        self.padding_var = tk.IntVar(value=2)
        tk.Spinbox(left3, from_=1, to=6, textvariable=self.padding_var, width=8,
                   command=self._update_preview, font=("Helvetica", 10)).pack(fill=tk.X)

        self._make_label(right3, "Urutan")
        self.sort_var = tk.StringVar(value="original")
        sort_cb = ttk.Combobox(right3, textvariable=self.sort_var, width=10, font=("Helvetica", 9),
                               values=["original", "a-z", "z-a"], state="readonly")
        sort_cb.pack(fill=tk.X)
        sort_cb.bind("<<ComboboxSelected>>", lambda e: self._update_preview())

        self.seq_frame.pack(fill=tk.X)

        # -- Replace frame --
        self.rep_frame = tk.Frame(ctrl_frame, bg="#FFFFFF")
        self._make_label(self.rep_frame, "Cari teks")
        self.find_var = tk.StringVar()
        self._make_entry(self.rep_frame, self.find_var, "teks yang dicari")

        self._make_label(self.rep_frame, "Ganti dengan")
        self.replace_var = tk.StringVar()
        self._make_entry(self.rep_frame, self.replace_var, "teks pengganti")

        # -- Custom frame --
        self.cust_frame = tk.Frame(ctrl_frame, bg="#FFFFFF")
        self._make_label(self.cust_frame, "Template nama")
        self.template_var = tk.StringVar(value="{n}_{name}")
        self._make_entry(self.cust_frame, self.template_var, "{n}_{name}")
        tk.Label(self.cust_frame, text="Variabel: {n}=nomor, {name}=nama asli, {ext}=ekstensi",
                 bg="#FFFFFF", fg="#888780", font=("Helvetica", 8), wraplength=250, justify="left"
                 ).pack(anchor="w", pady=(2, 6))

        self._make_label(self.cust_frame, "Prefix")
        self.cust_prefix_var = tk.StringVar()
        self._make_entry(self.cust_frame, self.cust_prefix_var, "opsional")

        self._make_label(self.cust_frame, "Suffix")
        self.cust_suffix_var = tk.StringVar()
        self._make_entry(self.cust_frame, self.cust_suffix_var, "opsional")

        # Apply to
        sep2 = tk.Frame(ctrl_frame, bg="#DEDDD8", height=1)
        sep2.pack(fill=tk.X, pady=8)

        self._make_label(ctrl_frame, "Terapkan pada")
        self.apply_to_var = tk.StringVar(value="all")
        apply_cb = ttk.Combobox(ctrl_frame, textvariable=self.apply_to_var, font=("Helvetica", 10),
                                values=["all", "files", "folders"], state="readonly")
        apply_cb.pack(fill=tk.X, pady=(0, 6))
        apply_cb.bind("<<ComboboxSelected>>", lambda e: self._update_preview())

        # Trace vars
        for var in [self.prefix_var, self.suffix_var, self.find_var, self.replace_var,
                    self.template_var, self.cust_prefix_var, self.cust_suffix_var]:
            var.trace_add("write", lambda *a: self._update_preview())
        self.start_var.trace_add("write", lambda *a: self._update_preview())
        self.step_var.trace_add("write", lambda *a: self._update_preview())
        self.padding_var.trace_add("write", lambda *a: self._update_preview())

        # Action buttons
        btn_sep = tk.Frame(left, bg="#DEDDD8", height=1)
        btn_sep.pack(fill=tk.X)
        btn_frame = tk.Frame(left, bg="#F5F5F3", pady=8)
        btn_frame.pack(fill=tk.X, padx=12)

        tk.Button(btn_frame, text="✓ Terapkan", command=self._apply_rename,
                  bg="#378ADD", fg="white", relief="flat", font=("Helvetica", 10, "bold"),
                  padx=10, pady=6, cursor="hand2").pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_frame, text="↺ Reset", command=self._reset_all,
                  bg="#D3D1C7", fg="#2C2C2A", relief="flat", font=("Helvetica", 10),
                  padx=10, pady=6, cursor="hand2").pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_frame, text="🗑 Hapus", command=self._clear_all,
                  bg="#E24B4A", fg="white", relief="flat", font=("Helvetica", 10),
                  padx=10, pady=6, cursor="hand2").pack(side=tk.LEFT)

        # Right panel
        right = tk.Frame(main, bg="#FFFFFF", highlightthickness=1, highlightbackground="#DEDDD8")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Drag drop zone
        self.drop_frame = tk.Frame(right, bg="#F5F5F3", relief="flat",
                                   highlightthickness=2, highlightbackground="#B4B2A9")
        self.drop_frame.pack(fill=tk.X, padx=12, pady=12)
        self.drop_label = tk.Label(self.drop_frame,
                                   text="📂  Drag & drop file atau folder ke sini\n"
                                        "atau klik untuk pilih file/folder",
                                   bg="#F5F5F3", fg="#888780", font=("Helvetica", 11),
                                   pady=18, cursor="hand2")
        self.drop_label.pack(fill=tk.X)
        self.drop_frame.bind("<Button-1>", lambda e: self._pick_files())
        self.drop_label.bind("<Button-1>", lambda e: self._pick_files())

        # Enable drag and drop via tkinterdnd2 if available, else skip
        try:
            self.root.drop_target_register('DND_Files')
            self.root.dnd_bind('<<Drop>>', self._on_dnd_drop)
        except Exception:
            pass

        # File list header
        hdr = tk.Frame(right, bg="#F5F5F3")
        hdr.pack(fill=tk.X, padx=12)
        tk.Label(hdr, text="", bg="#F5F5F3", width=3).pack(side=tk.LEFT)
        tk.Label(hdr, text="Nama saat ini", bg="#F5F5F3", fg="#5F5E5A",
                 font=("Helvetica", 9, "bold"), anchor="w").pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Label(hdr, text="Nama baru", bg="#F5F5F3", fg="#378ADD",
                 font=("Helvetica", 9, "bold"), anchor="w").pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Label(hdr, text="Hapus", bg="#F5F5F3", fg="#5F5E5A",
                 font=("Helvetica", 9, "bold"), width=7).pack(side=tk.LEFT)

        sep_h = tk.Frame(right, bg="#DEDDD8", height=1)
        sep_h.pack(fill=tk.X, padx=12)

        # Scrollable list
        list_frame = tk.Frame(right, bg="#FFFFFF")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 0))

        self.canvas = tk.Canvas(list_frame, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scroll_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Status bar
        status_sep = tk.Frame(right, bg="#DEDDD8", height=1)
        status_sep.pack(fill=tk.X, padx=0)
        status_bar = tk.Frame(right, bg="#F5F5F3", pady=6)
        status_bar.pack(fill=tk.X, padx=12)
        self.status_label = tk.Label(status_bar, text="Belum ada item", bg="#F5F5F3",
                                     fg="#888780", font=("Helvetica", 10))
        self.status_label.pack(side=tk.LEFT)

        # Add file/folder buttons
        btn_add_frame = tk.Frame(right, bg="#FFFFFF", pady=6)
        btn_add_frame.pack(fill=tk.X, padx=12)
        tk.Button(btn_add_frame, text="+ Tambah File", command=self._pick_files,
                  bg="#E6F1FB", fg="#185FA5", relief="flat", font=("Helvetica", 10),
                  padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_add_frame, text="+ Tambah Folder", command=self._pick_folder,
                  bg="#FAEEDA", fg="#854F0B", relief="flat", font=("Helvetica", 10),
                  padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT)

    def _make_label(self, parent, text):
        tk.Label(parent, text=text, bg="#FFFFFF", fg="#5F5E5A",
                 font=("Helvetica", 9)).pack(anchor="w", pady=(6, 2))

    def _make_entry(self, parent, var, placeholder=""):
        entry = tk.Entry(parent, textvariable=var, font=("Helvetica", 10),
                         relief="flat", bd=1, highlightthickness=1,
                         highlightbackground="#DEDDD8", highlightcolor="#378ADD")
        entry.pack(fill=tk.X, ipady=4)
        return entry

    def _set_mode(self, mode):
        self.current_mode.set(mode)
        self._update_mode_btns(mode)
        self.seq_frame.pack_forget()
        self.rep_frame.pack_forget()
        self.cust_frame.pack_forget()
        if mode == "sequence":
            self.seq_frame.pack(fill=tk.X)
        elif mode == "replace":
            self.rep_frame.pack(fill=tk.X)
        else:
            self.cust_frame.pack(fill=tk.X)
        self._update_preview()

    def _update_mode_btns(self, active):
        colors = {"sequence": ("#378ADD", "white"), "replace": ("#378ADD", "white"),
                  "custom": ("#378ADD", "white")}
        for k, btn in self.mode_btns.items():
            if k == active:
                btn.config(bg="#378ADD", fg="white")
            else:
                btn.config(bg="#E8E7E2", fg="#444441")

    def _pick_files(self):
        paths = filedialog.askopenfilenames(title="Pilih file")
        for path in paths:
            self._add_path(path)
        self._update_preview()

    def _pick_folder(self):
        path = filedialog.askdirectory(title="Pilih folder")
        if path:
            self._add_path(path)
            self._update_preview()

    def _on_dnd_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        for path in paths:
            self._add_path(path)
        self._update_preview()

    def _add_path(self, path):
        path = os.path.normpath(path)
        is_folder = os.path.isdir(path)
        name = os.path.basename(path)
        if is_folder:
            ext = ""
            base = name
        else:
            ext = os.path.splitext(name)[1]
            base = os.path.splitext(name)[0]
        self.items.append({
            "path": path,
            "dir": os.path.dirname(path),
            "name": name,
            "base": base,
            "ext": ext,
            "is_folder": is_folder,
            "new_name": name,
        })

    def _compute_new_name(self, item, seq_idx):
        apply_to = self.apply_to_var.get()
        if apply_to == "files" and item["is_folder"]:
            return item["name"]
        if apply_to == "folders" and not item["is_folder"]:
            return item["name"]

        mode = self.current_mode.get()
        if mode == "sequence":
            prefix = self.prefix_var.get()
            suffix = self.suffix_var.get()
            try:
                start = int(self.start_var.get())
            except Exception:
                start = 1
            try:
                step = int(self.step_var.get())
            except Exception:
                step = 1
            try:
                padding = int(self.padding_var.get())
            except Exception:
                padding = 2
            num = start + seq_idx * step
            return f"{prefix}{str(num).zfill(padding)}{suffix}{item['ext']}"
        elif mode == "replace":
            find = self.find_var.get()
            rep = self.replace_var.get()
            if not find:
                return item["name"]
            return item["name"].replace(find, rep)
        else:
            template = self.template_var.get()
            cp = self.cust_prefix_var.get()
            cs = self.cust_suffix_var.get()
            if not template:
                return f"{cp}{item['base']}{cs}{item['ext']}"
            result = template.replace("{n}", str(seq_idx + 1).zfill(2))
            result = result.replace("{name}", item["base"])
            result = result.replace("{ext}", item["ext"].lstrip("."))
            result = result.replace("{prefix}", cp)
            result = result.replace("{suffix}", cs)
            return result

    def _get_sorted_items(self):
        sort = self.sort_var.get()
        indexed = list(enumerate(self.items))
        if sort == "a-z":
            indexed.sort(key=lambda x: x[1]["name"].lower())
        elif sort == "z-a":
            indexed.sort(key=lambda x: x[1]["name"].lower(), reverse=True)
        return indexed

    def _update_preview(self):
        apply_to = self.apply_to_var.get()
        sorted_items = self._get_sorted_items()
        seq_idx = 0
        for orig_idx, item in sorted_items:
            applies = (apply_to == "all" or
                       (apply_to == "files" and not item["is_folder"]) or
                       (apply_to == "folders" and item["is_folder"]))
            new_name = self._compute_new_name(item, seq_idx if applies else seq_idx)
            if applies:
                seq_idx += 1
            self.items[orig_idx]["new_name"] = new_name
        self._render_list()

    def _render_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not self.items:
            tk.Label(self.scroll_frame, text="Belum ada item\nTambahkan file atau folder di atas",
                     bg="#FFFFFF", fg="#B4B2A9", font=("Helvetica", 11), pady=30
                     ).pack(fill=tk.X)
            self.status_label.config(text="Belum ada item")
            return

        for idx, item in enumerate(self.items):
            self._make_row(idx, item)

        files = sum(1 for i in self.items if not i["is_folder"])
        folders = sum(1 for i in self.items if i["is_folder"])
        self.status_label.config(text=f"{len(self.items)} item  |  {files} file  |  {folders} folder")

    def _make_row(self, idx, item):
        row = tk.Frame(self.scroll_frame, bg="#FFFFFF",
                       highlightthickness=1, highlightbackground="#F1EFE8")
        row.pack(fill=tk.X)

        icon = "📁" if item["is_folder"] else "📄"
        tk.Label(row, text=icon, bg="#FFFFFF", font=("Helvetica", 12), width=3).pack(side=tk.LEFT)

        changed = item["new_name"] != item["name"]
        tk.Label(row, text=item["name"], bg="#FFFFFF", fg="#5F5E5A",
                 font=("Helvetica", 10), anchor="w", wraplength=220).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        color = "#185FA5" if changed else "#5F5E5A"
        tk.Label(row, text=item["new_name"], bg="#FFFFFF", fg=color,
                 font=("Helvetica", 10, "bold" if changed else "normal"),
                 anchor="w", wraplength=220).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)
        tk.Button(row, text="✕", command=lambda i=idx: self._remove_item(i),
                  bg="#FFFFFF", fg="#E24B4A", relief="flat", font=("Helvetica", 11),
                  cursor="hand2", width=4).pack(side=tk.LEFT)

        # Drag reorder bindings
        row.bind("<ButtonPress-1>", lambda e, i=idx: self._drag_start(i))
        row.bind("<B1-Motion>", self._drag_motion)
        row.bind("<ButtonRelease-1>", lambda e, i=idx: self._drag_end(i))

    def _drag_start(self, idx):
        self.drag_src_idx = idx

    def _drag_motion(self, event):
        pass

    def _drag_end(self, idx):
        if self.drag_src_idx is not None and self.drag_src_idx != idx:
            item = self.items.pop(self.drag_src_idx)
            self.items.insert(idx, item)
            self._update_preview()
        self.drag_src_idx = None

    def _remove_item(self, idx):
        self.items.pop(idx)
        self._update_preview()

    def _apply_rename(self):
        if not self.items:
            messagebox.showwarning("Kosong", "Tidak ada item yang akan di-rename.")
            return

        errors = []
        success = 0
        for item in self.items:
            if item["new_name"] == item["name"]:
                continue
            old_path = item["path"]
            new_path = os.path.join(item["dir"], item["new_name"])
            try:
                os.rename(old_path, new_path)
                item["path"] = new_path
                item["name"] = item["new_name"]
                item["base"] = os.path.splitext(item["new_name"])[0]
                success += 1
            except Exception as e:
                errors.append(f"{item['name']}: {e}")

        if errors:
            messagebox.showerror("Gagal", f"{len(errors)} rename gagal:\n" + "\n".join(errors))
        else:
            messagebox.showinfo("Berhasil", f"✓ {success} item berhasil di-rename!")
        self._update_preview()

    def _reset_all(self):
        for item in self.items:
            item["new_name"] = item["name"]
        self._render_list()

    def _clear_all(self):
        self.items.clear()
        self._render_list()


def main():
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        root = tk.Tk()

    app = FileRenamerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
