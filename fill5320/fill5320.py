#!/usr/bin/env python3
import argparse
import csv
import os
from pdfforms.pdfforms import (
    read_data,
    load_field_defs,
    make_path,
    generate_fdf,
    fill_form,
)

import tempfile
import PyPDF2
from datetime import datetime
from reportlab.pdfgen import canvas

DATE_FIELD = "37"


def _get_tmp_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name


def sign_pdf(out_file, in_pdf, sig_img, coords):
    page_num, x1, y1, width, height = [int(a) for a in coords.split("x")]
    page_num -= 1

    output_filename = out_file or "{}_signed{}".format(*os.path.splitext(in_pdf))

    pdf_fh = open(in_pdf, "rb")
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None

    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:
            # Create PDF for signature
            sig_tmp_filename = _get_tmp_filename()
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            c.drawImage(sig_img, x1, y1, width, height, mask="auto")
            c.showPage()
            c.save()

            # Merge PDF in to original page
            sig_tmp_fh = open(sig_tmp_filename, "rb")
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)

        writer.addPage(page)
    with open(output_filename, "wb") as fh:
        writer.write(fh)

    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)


def fill_forms(path_func, field_defs, data, flatten=True):
    for filepath, formdata in data.items():
        if not formdata:
            continue
        yield filepath
        output_path = path_func(filepath)
        original_fp_parts = filepath.split("_")
        original_fp_ext = original_fp_parts[-1].split(".")
        orginal_path = "_".join(original_fp_parts[:-1])
        orginal_path = "{}.{}".format(orginal_path, original_fp_ext[-1])
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fdf_str = generate_fdf(field_defs[orginal_path], formdata)
        fill_form(orginal_path, fdf_str, output_path, flatten)


def read_dest_data(instream):
    form_data = {}
    row_num = 0
    for row in csv.reader(instream):
        if row_num > 0:
            form_data[row_num] = {}
            form_data[row_num]["postfix"] = str(row[3])
            form_data[row_num]["address"] = str(row[2])
            form_data[row_num]["id"] = str(row[0])
        row_num += 1
    return form_data


def main(argv=None):
    with open("static_data.csv", "r", encoding="utf-8") as df:
        form_static_data = read_data(df)

    with open("destinations_data.csv", "r", encoding="utf-8") as df:
        form_dest_data = read_dest_data(df)

    field_defs = load_field_defs("fields.json")

    for fd, fd_val in form_static_data.items():
        for di, dest in form_dest_data.items():
            fileparts = fd.split(".")
            fd_val[dest["id"]] = dest["address"]
            fd_val[DATE_FIELD] = datetime.now().strftime("%x")
            filename = "{}_{}.{}".format(fileparts[0], dest["postfix"], fileparts[1])
            out_val = {filename: fd_val}
            fg = fill_forms(make_path("filled/"), field_defs, out_val, True)

            for filepath in fg:
                print(filepath)
            # sign it
            os.makedirs(os.path.dirname("signed/"), exist_ok=True)
            sign_pdf(
                os.path.join("signed", filename),
                os.path.join("filled", filename),
                "signature.png",
                "1x70x195x200x12",
            )


if __name__ == "__main__":
    main()
