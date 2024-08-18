from pathlib import Path
import shutil
import traceback

import utils


def main() -> None:
    try:
        copy_static_to_public("static", "public")
        parse_content("content/", "template.html", "public/")
    except Exception as err:
        print(f"❌ ERROR:")
        tb = traceback.extract_tb(err.__traceback__)
        file_name = tb[0].filename
        err_line = tb[0].lineno
        print(f"File: {file_name}")
        print(f"Line: {err_line}")
        quit()


def copy_static_to_public(src_path: str, dest_path: str) -> None:
    dest_dir_path = Path(dest_path)
    if dest_dir_path.exists():
        shutil.rmtree(dest_path)

    shutil.copytree(src_path, dest_path)
    print()
    print(f"📂 Files are successfully copied from '{
          src_path}/' to '{dest_path}/'")
    print("--------------------------------------------------------------------------")


def generate_page(src_path: str, template_path: str, dest_path: str):
    print(f"⏳ Generating page from '{src_path}' to '{
          dest_path}' using '{template_path}'...")
    print("--------------------------------------------------------------------------")

    with open(src_path, "r") as src_md, open(dest_path, "x") as dest_html, open(template_path, "r") as template:
        get_markdown = src_md.read()
        heading = utils.extract_title(get_markdown)
        md_to_html = utils.markdown_to_html(get_markdown)
        template = template.read()
        template = template.replace("{{ Title }}", heading).replace(
            "{{ Content }}", md_to_html.to_html())
        dest_html.write(template)
        print("✅ The page is successfully generated!")
        print(
            "--------------------------------------------------------------------------")


def parse_content(src_dir_path: str, template_path: str, dest_dir_path: str):
    src_path = Path(src_dir_path)
    for p in src_path.glob("*"):
        updated_dest_path = p.as_posix().split(
            "content/")[1].replace(".md", ".html")
        if p.is_dir():
            if not Path(f"public/{p.as_posix().split("content/")[1]}").exists():
                Path(f"public/{p.as_posix().split("content/")[1]}").mkdir()
            parse_content(p.as_posix(), template_path, dest_dir_path)
        else:
            generate_page(p.as_posix(), template_path, f"public/{updated_dest_path}")


if __name__ == "__main__":
    main()
