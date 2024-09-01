#!/usr/bin/env python3

import panflute as pf


def prepare(doc):
    doc.sidenotes = {}
    doc.current_sidenote_index = 1


def finalize(doc):
    if hasattr(doc, "sidenotes"):
        for sidenote in doc.sidenotes.values():
            doc.content.append(sidenote)


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
        return ref
    elif isinstance(elem, pf.Div) and "footnotes" in elem.classes:
        # Remove the footnotes div as we're handling footnotes as sidenotes
        return []
    elif isinstance(elem, pf.Para):
        new_content = []
        for child in elem.content:
            if (
                isinstance(child, pf.Superscript)
                and len(child.content) == 1
                and isinstance(child.content[0], pf.Str)
            ):
                text = child.content[0].text
                if text.startswith("[") and text.endswith("]"):
                    try:
                        index = int(text[1:-1])
                        if index in doc.sidenotes:
                            new_content.append(child)
                            if elem.parent:
                                elem.parent.content.insert(
                                    elem.parent.content.index(elem) + 1,
                                    doc.sidenotes[index],
                                )
                            del doc.sidenotes[index]
                            continue
                    except ValueError:
                        pass
            new_content.append(child)
        elem.content = pf.ListContainer(*new_content)
    return elem


if __name__ == "__main__":
    pf.run_filter(sidenote, prepare=prepare, finalize=finalize)
