#!/usr/bin/env python3

import panflute as pf
import logging

logging.basicConfig(level=logging.DEBUG, filename="sidenote_filter.log", filemode="a")


def prepare(doc):
    logging.info(f"Processing document: {doc.get_metadata('title', 'Untitled')}")
    doc.sidenotes = {}
    doc.current_sidenote_index = 1
    doc.processed_superscripts = set()
    doc.missing_references = set()


def finalize(doc):
    if hasattr(doc, "sidenotes"):
        for index in doc.missing_references:
            if index in doc.sidenotes:
                logging.warning(
                    f"Sidenote {index} was created but its reference was not found in the text. Adding to end of document."
                )
                doc.content.append(doc.sidenotes[index])


def create_sidenote_ref(index):
    return pf.Superscript(pf.Str(f"[{index}]"))


def create_sidenote(index, content):
    sidenote = pf.Div(classes=["sidenote"])
    sidenote_content = pf.ListContainer(pf.Para(pf.Str(f"[{index}] ")))
    sidenote_content.extend(content)
    sidenote.content = sidenote_content
    return sidenote


def sidenote(elem, doc):
    if isinstance(elem, pf.Note):
        index = doc.current_sidenote_index
        doc.current_sidenote_index += 1
        ref = create_sidenote_ref(index)
        note = create_sidenote(index, elem.content)
        doc.sidenotes[index] = note
        doc.missing_references.add(index)  # Assume missing until found
        # logging.debug(f"Created sidenote with index {index}")
        return ref
    elif isinstance(elem, pf.Div) and "footnotes" in elem.classes:
        # logging.debug("Removed footnotes div")
        return []
    elif isinstance(elem, pf.Para):
        return process_paragraph(elem, doc)
    return elem


def process_paragraph(elem, doc):
    new_content = []
    sidenotes_to_insert = []
    # logging.debug(f"Processing paragraph: {pf.stringify(elem)}")
    for child in elem.content:
        # logging.debug(f"Checking element: {type(child).__name__}")
        # if isinstance(child, pf.Link):
        # logging.debug(f"Found link: {pf.stringify(child)}")
        if is_sidenote_reference(child):
            processed = process_sidenote_reference(child, doc)
            new_content.append(processed[0])  # Add the reference
            if len(processed) > 1:
                sidenotes_to_insert.append(
                    processed[1]
                )  # Store the sidenote for later insertion
        else:
            new_content.append(child)

    elem.content = pf.ListContainer(*new_content)

    if sidenotes_to_insert:
        # Insert sidenotes after the paragraph
        return [elem] + sidenotes_to_insert
    return elem


def process_sidenote_reference(elem, doc):
    text = elem.content[0].text
    # logging.debug(f"Processing superscript: {text}")
    try:
        index = int(text[1:-1])
        if index in doc.sidenotes:
            doc.processed_superscripts.add(index)
            doc.missing_references.discard(
                index
            )  # Reference found, remove from missing set
            # logging.debug(f"Found reference for sidenote {index}")
            return [elem, doc.sidenotes[index]]
        else:
            logging.warning(f"Sidenote {index} not found in doc.sidenotes")
    except ValueError:
        logging.warning(f"Invalid sidenote index: {text}")
    return [elem]


def is_sidenote_reference(elem):
    is_ref = (
        isinstance(elem, pf.Superscript)
        and len(elem.content) == 1
        and isinstance(elem.content[0], pf.Str)
        and elem.content[0].text.startswith("[")
        and elem.content[0].text.endswith("]")
    )
    # if is_ref:
    # logging.debug(f"Found sidenote reference: {pf.stringify(elem)}")
    return is_ref


if __name__ == "__main__":
    pf.run_filter(sidenote, prepare=prepare, finalize=finalize)
