import flet
import subprocess


def main(page: flet.Page):
    page.title = "OllamaLlink"
    page.window_width = 640
    page.window_height = 400
    page.window_resizable = True

    def theme_change(e):
        page.theme_mode = (
            flet.ThemeMode.LIGHT
            if page.theme_mode == flet.ThemeMode.DARK
            else flet.ThemeMode.DARK
        )
        color_switch.label = "🌙" if page.theme_mode == flet.ThemeMode.DARK else "☀️"
        page.update()

    page.theme_mode = flet.ThemeMode.DARK
    color_switch = flet.Switch(label="🌙", on_change=theme_change)

    t = flet.Text()
    tb1 = flet.TextField(label="Enter LLM name")

    def llm_name(e):
        t.value = f"{tb1.value}"
        page.update()

        return t.value

    def pick_files_result(e: flet.FilePickerResultEvent):
        selected_file_path = (
            ", ".join(map(lambda f: f.path, e.files))
            if e.files
            else "No *.GGUF file was selected!"
        )
        selected_file.value = selected_file_path

        page.update()

        with open("Modelfile", "w") as f:
            f.write(f"FROM {selected_file_path}\n")

    pick_files_dialog = flet.FilePicker(on_result=pick_files_result)
    page.add(pick_files_dialog)

    selected_file = flet.Text()
    page.add(selected_file)

    def add_llm_to_ollama(e):
        print(tb1.value)
        command = rf"ollama create {tb1.value} -f Modelfile"
        try:
            result = subprocess.run(command, shell=True)
            if result.returncode == 0:
                fine = flet.AlertDialog(
                    title=flet.Text("LLM Added succesfully"),
                )
                page.dialog = fine
                fine.open = True
                page.update()
            else:
                wrong = flet.AlertDialog(
                    title=flet.Text("Something went wrong"),
                )
                page.dialog = wrong
                wrong.open = True
                page.update()
        except Exception as e:
            fail = flet.AlertDialog(
                title=flet.Text("An error has ocurred"),
                content=flet.Text(
                    "Please check the command promp to see what the error is"
                ),
            )
            page.dialog = fail
            fail.open = True
            page.update()

    page.add(
        flet.Row(
            [
                color_switch,
            ],
            alignment=flet.MainAxisAlignment.END,
        ),
        flet.Row(
            controls=[
                flet.CupertinoFilledButton(
                    content=flet.Text(
                        "Select LLM GGUF Model",
                        width=180,
                    ),
                    opacity_on_click=0.3,
                    on_click=lambda e: (
                        pick_files_dialog.pick_files(allowed_extensions=["*gguf"])
                    ),
                ),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        ),
        flet.Row(
            [
                tb1,
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        ),
        flet.Row(
            controls=[],
            alignment=flet.MainAxisAlignment.CENTER,
        ),
        flet.Row(
            controls=[
                flet.CupertinoFilledButton(
                    content=flet.Text(
                        "Add LLM to Ollama",
                        width=180,
                    ),
                    opacity_on_click=0.3,
                    on_click=add_llm_to_ollama,
                ),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        ),
    )
    page.update()


flet.app(target=main)
